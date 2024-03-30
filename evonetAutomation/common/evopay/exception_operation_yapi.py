from base.read_file_path import ReadFile
from common.evopay.conf_init import db_yapi
from common.evopay.read_csv import ReadCSV
from loguru import logger as log
import bson

class Exception_Yapi():
    def __init__(self,node='single'):
        if node=='single':
            data_file=ReadFile().read_data_file("evopay_evonet_exception_yapi","QR_single_node_mode","evopay")
            self.yapi_testdata=ReadCSV(data_file).read_data()
            log.debug(f"csv文件中的数据为{self.yapi_testdata}")
        else:
            data_file = ReadFile().read_data_file("evopay_evonet_exception_yapi", "QR_double_node_mode", "evopay")
            self.yapi_testdata = ReadCSV(data_file).read_data()
            log.debug(f"csv文件中的数据为{self.yapi_testdata}")


    def is_update_yapi(self,test_info):
        a = test_info['test_id']
        log.debug(f"test_info文件中的数据为{test_info}")
        result_list_object = filter(lambda yapi_testdata:yapi_testdata["test_id"]==a,self.yapi_testdata)
        result_list = list(result_list_object)
        log.debug(f"test_info文件中的数据为{result_list}")
        if result_list:
            result = list(result_list)
            self.update_yapi(result[0])
        return result_list

    def update_yapi(self,yapi_value):
        self.pre_update_mongo = eval(yapi_value['pre-update mongo'])
        self.pre_query_mongo =eval(yapi_value['pre-query mongo'])
        if '连接超时' in yapi_value.values():
            self.pre_update_mongo['delay'] = bson.int64.Int64(self.pre_update_mongo['delay'])
        self.db = db_yapi
        self.db.update_one(table='adv_mock_case', query_params=self.pre_query_mongo, updata_params=self.pre_update_mongo)
        log.debug(f'更新yapi数据库成功')
    
    def reset_yapi(self):
        if 'delay' in self.pre_update_mongo:
            reset_table_mongo = {'delay':bson.int64.Int64(0)}
            self.db.update_one(table='adv_mock_case', query_params=self.pre_query_mongo,
                          updata_params=reset_table_mongo)
        
            
            

# 
# if __name__ == '__main__':
#     test_info = {'test_id': 'Y001', 'interface': 'CPMToken', 'title': 'CPMToken-brandID为空', 'conf': '', 'pre-update database': '', 'pre-update table': '', 'pre-query mongo': '', 'pre-update mongo': '', 'wopParticipantID': '', 'wopSignkey': '', 'mopParticipantID': '', 'mopSignkey': '', 'data': '{"brandID":"Auto_GrabPay_B1","userData":{"wopUserReference":"#autotest_data#","wopToken":"#autotest_data#","evonetUserReference":"#autotest_data#"}}', 'expected': '{"code":"V0001","message":"Field {brandID} absent or empty."}', 'check_mongo': '', 'check_mongo_expected': '', 'update database': '', 'update_mongo': '', 'test_scenario': 'all'}
#     AA = Exception_Yapi(test_info)










