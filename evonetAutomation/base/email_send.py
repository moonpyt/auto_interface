# !/usr/bin/python3
import time
import os
import shutil
import random
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import CryptoLibrary
from encrypt import Encrypt

class SendMail(object):
    def __init__(self,username,passwd,recv,title,content,
                 file=None,
                 email_host='smtp.qiye.163.com',port=465):
        self.username = username
        self.passwd = passwd
        self.recv = recv
        self.title = title
        self.content = content
        self.file = file
        self.email_host = email_host
        self.port = port
    def send_mail(self):
        msg = MIMEMultipart()

        #发送内容的对象
        if self.file:#处理附件的
            att = MIMEText(open(self.file,encoding='utf-8').read())
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"'%self.file
            msg.attach(att)
        msg.attach(MIMEText(self.content))#邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = self.recv  # 接收者账号列表
        self.smtp = smtplib.SMTP_SSL(self.email_host,port=self.port)
        #发送邮件服务器的对象
        try:
            # self.smtp.ehlo()
            # self.smtp.starttls()
            self.smtp.login(self.username,self.passwd)
            self.smtp.sendmail(self.username,self.recv,msg.as_string())
        except Exception as e:
            print('send is wrong',e)
if __name__ == '__main__':
    time.sleep(2)
    os.chdir("../report/")
    file_path=os.getcwd()
    for i in os.listdir(file_path):
        if i.startswith("report"):
            report_name=i
            recv_list=["zealot.jiang@cardinfolink.com","jolly.cheng@cardinfolink.com","strong.si@cardinfolink.com","walker.zhang@cardinfolink.com"]
            # recv_list = recv_list = ["walker.zhang@cardinfolink.com", "1401660184@qq.com"]  # test后面会用到
            for receive_name in recv_list:
                passwd_encrypt='Q1qqP3KZnlwA5GuwAbxFP/qAgxjKdD3BaWZVLddkWXir40vstSBJ5n4/BioTlJSFJoOzwN7rAsTp4VImzVsaGw=='
                passwd=Encrypt().decrypt(passwd_encrypt)
                m = SendMail(
                        username='evonet.itsupport@cardinfolink.com',passwd=passwd,recv=receive_name,
                        title='EVONET report'+str(random.randint(1000000000,9000000000)),content=' the report of evonet. Please download it and open it with browser',file=report_name
                    )
                m.send_mail()
            #备份发送文件
            shutil.move(report_name, "../../../../report/" + report_name)


