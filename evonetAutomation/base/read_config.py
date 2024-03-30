# -*- coding: utf-8 -*-
import base64
import math
from robot.api import logger
import configparser
import os
import sys
from configparser import ConfigParser


class ConfigIni():
    def __init__(self, path, title):
        self.path = path
        self.title = title
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path, encoding='utf-8')

    def get_ini(self, value):
        return self.cf.get(self.title, value)

    def set_ini(self, title, value, text):
        self.cf.set(title, value, text)
        return self.cf.write(open(self.path, "wb"))

    def add_ini(self, title):
        self.cf.add_section(title)
        return self.cf.write(open(self.path))

    def get_options(self, data):
        # 获取所有的section
        options = self.cf.options(data)
        return options


def abspath(py_file, conf_dir=None):
    if conf_dir == None: conf_dir = ""
    return os.path.normpath(
        os.path.join(os.path.normpath(
            os.path.dirname(os.path.realpath(py_file))), conf_dir))


class Conf(ConfigParser):
    def __init__(self, filename, encoding="utf8"):
        # 调用父类原来的__init__方法,因为原来有文件解析器
        super().__init__()
        self.filename = filename
        self.encoding = encoding
        # 把文件里的数据放到文件解析器里
        self.read(filename, encoding)

    def write_data(self, section, option, value):
        # 写入数据
        self.set(section, option, value)
        self.write(open(self.filename, "w", encoding=self.encoding))


class Coding():
    def base64_file_encode(self, file):
        f = open(r'%s' % file, 'rb')  # 二进制方式打开文件
        ls_f = base64.b64encode(f.read())  # 读取文件内容转换为base64编码
        f.close()
        return ls_f


class StringUtil2():
    def StringContain(self, str, substring):
        if substring in str:
            return True
        else:
            return False
