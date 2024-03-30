import csv
import pandas as pd
class ReadCSV(object):
    def __init__(self,filename):
        '''

        :param filename: 文件名

        '''
        self.filename=filename

    #打开CSV文件
    def open(self):
        with open(self.filename,'r') as file:
            self.data=pd.read_csv(file)

    def read_data(self):
        with open(self.filename, 'r',encoding='UTF-8') as file:
            data = pd.read_csv(file,encoding='UTF-8',sep='|',keep_default_na=False)

            #数据转化成列表
            wb=data.T.reset_index().T.values.tolist()
            print(wb)
            #获取title
            title=wb[0]

            #遍历第二行开始的数据
            cases=[]
            for row in wb[1:]:
                data=[]
                #再次遍历每一个数据
                for r in row:

                    data.append(r)
                case=dict(zip(title,data))

                cases.append(case)

            return cases
    #读取功能测试的数据
    def read_data_function(self):
        read_data_all=self.read_data()
        data_function_list=[]
        for item in read_data_all:
            if 'function'in item['module'] :
                data_function_list.append(item)
        return data_function_list
    # #读取冒烟测试的数据
    def read_data_smoke(self):
        read_data_all = self.read_data()
        data_smoke_list = []
        for item in read_data_all:
            if 'function' in item['module']:
                data_smoke_list.append(item)
        return data_smoke_list


