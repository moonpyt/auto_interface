# coding=utf-8
# -*- coding: utf-8 -*-
import uuid
import datetime
import hashlib
import json
from base.http_request import Http
from base.read_config import  *
from base.read_file_path import ReadFile
from base.db import MongoDB
class Evonet(Http):
    '''
           pytest测试
    '''

    def __init__(self,envirs, path=None, title=None, ):
        super(Evonet, self).__init__()
        if path == None:
            self.path = abspath(__file__, '../../../config/evopay/evopay_'+envirs+'.ini')
        if title == None:
            self.title = 'trans_data'
        self.evopay_config=ConfigIni(self.path,self.title)
        self.envirs=envirs


    def evopay_get_config(self,title):
        return  ConfigIni(self.path,title)

    Datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "+0800"
    key = "f08aacf22bb1faf7bd250999d1620afc"  # staging
    # MsgID: 建议使用 UUID 或者 GUID，现在用的uuid
    msgid = str("".join(str(uuid.uuid4()).split("-")))

    req_data={"returnUrl": "https://www.baidu.com/return","webhook": "https://www.baidu.com/","transAmount": {"value": "99.99","currency": "CNY"},"cardToken": "9733614916390019","card": {"number": "4000000000001000","expiryMonth": "12","expiryYear": "26",
    # "holderName":"持卡人姓名",# "cvc":"300",# "startMonth":"12",# "startYear":"20"
    }}
    data=json.dumps(req_data)

    # bb=aa.read_ini_file()
    def string_sign(self):
        # 返回header中Auhorization的值
        if self.evopay_config.get_ini("http_method")== "POST":
            string_sign = self.evopay_config.get_ini("http_method")+ "\n" + self.evopay_config.get_ini("url_string") + "\n" + self.Datetime + "\n" + self.key + "\n" + self.msgid + "\n" + self.data.rstrip()
        if self.evopay_config.get_ini("http_method")== "GET":
            string_sign = self.evopay_config.get_ini("http_method")+ "\n" + self.evopay_config.get_ini("url_string") + "\n" + self.Datetime + "\n" + self.key + "\n" + self.msgid + "\n"
        sha = hashlib.sha256()
        sha.update(string_sign.encode("utf-8"))

        return sha.hexdigest()

    def auth_sk(self, hight, age):
        self.header = {
            'Authorization': self.string_sign(),
            'Content-type': 'application/json',
            'MsgID': str(self.msgid),
            'DateTime': self.Datetime ,
            "SignType": "SHA256"}
        print(self.evopay_config.get_ini("data_1"))

        res_date = self.http_post(self.evopay_config.get_ini("http_url"), self.evopay_config.get_ini("url_string"), headers=self.header, json=json.loads(self.data))
        assert "SUCCESS" in res_date.text








