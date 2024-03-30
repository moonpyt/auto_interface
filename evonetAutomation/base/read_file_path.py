# -*- coding: utf-8 -*-
import os


class ReadFile(object):
    '''
    读取ini和测试数据文件
    '''

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(self.base_dir)

    def read_ini_file(self, envirs, project):
        """

        :param project: 配置文件对应的上层文件夹名字
        :return:
        """
        # 读取配置文件

        config_dir = os.path.normpath("%s/%s" % (self.base_dir, r"config/{0}".format(project)))
        ini_file = project + '_' + envirs + ".ini"
        conf_file = os.path.join(config_dir, ini_file)
        return conf_file

    def read_data_file(self, file, node, project):
        """

        :param file: 测试案例数据文件的文件夹
        :param project: 测试案例数据文件对应的上层文件夹
        :return:
        """
        # 读取测试数据文件

        data_dir = os.path.normpath("%s/%s" % (self.base_dir, "data"))

        data_file = os.path.normpath("%s/%s" % (data_dir, r"{0}_file/{1}/{2}.csv".format(project, node, file)))
        return data_file
