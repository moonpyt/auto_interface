from configparser import ConfigParser
import os
from base.read_file_path import ReadFile
class EvopayTestCase(ConfigParser):
    def __init__(self,filename,encoding="utf8"):
        #调用父类原来的__init__方法,因为原来有文件解析器
        super().__init__()
        self.filename = filename
        self.encoding = encoding
        #把文件里的数据放到文件解析器里
        self.read(filename, encoding)
    def write_data(self,section,option,value):
        self.set(section,option,value)
        self.write(open(self.filename,"w",encoding=self.encoding))
    def read_data(self,conf_file,section):
        """

        :param conf_file: 存放数据的文件
        :param section: 数据文件的模块
        :return:
        """
        conf = EvopayTestCase(conf_file)
        #获取section下的options
        options=self.options(section)
        data=[]
        #获取options下的data
        for item in options:
            testdata=eval(conf.get(section,item))
            datas=data.append(testdata)
        return data


