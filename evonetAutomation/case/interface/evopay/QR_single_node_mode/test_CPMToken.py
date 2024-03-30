import pytest
import json
# from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evologs
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_sgp_evopay, db_sgp_evologs,db_tyo_evologs
from common.evopay.reponse_check import Checkresponse
from common.evopay.read_data import EvopayTestCase
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from base.read_config import Conf
from base.http_request import HttpRequest
from base.encrypt import Encrypt
from base.db import MongoDB
from common.evopay.read_csv import ReadCSV
from common.evopay.replace_data import multi_replace,case
from common.evopay.mongo_data_check import Checkmongo
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.cpm.cpm_token import CPM_Token_Message
from common.evopay.Initialization import initialization
from common.evopay.exception_operation_yapi import Exception_Yapi
from loguru import logger as log



data_file=ReadFile().read_data_file("evopay_evonet_cpmtoken","QR_single_node_mode","evopay")
cpmtoken_testdata=ReadCSV(data_file).read_data()


class Testcpmtoken():
    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',cpmtoken_testdata)
    def test_cpmtoken(self,test_info):
        body_params,head_params = self.common_params_init(test_info)

        res = self.post_cpmtoken(test_info,head_params,body_params)
        headers = res.headers
        traceID = headers['Traceid']
        result = res.json()
            
        self.response_check(result,test_info,head_params,body_params,traceID,)


    def common_params_init(self,test_info,node='single'):
        common_params = CPM_Token_Message()
        if node=='single':
            init = initialization(common_params.CPM_Token_Conf, common_params.CPM_Token_Body)
        else:
            init = initialization(common_params.CPM_Token_Conf_double, common_params.CPM_Token_Body_double)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        #兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params


    def post_cpmtoken(self,test_info,head_params,body_params,node='single'):
        #是否存在需要操作yapi
        yapi_operation = Exception_Yapi()
        update_yapi = yapi_operation.is_update_yapi(test_info)
        
        check_sign_url = head_params['url']

        base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']
        # 判断是否有数据进行替换,获取body
        data = multi_replace(str(body_params))

        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()
        # 获取participantID
        participantID = head_params['wopParticipantID']
        if test_info['pre-update table']:
            if test_info['pre-update mongo']:
                if '&' in test_info['pre-update table']:
                    pre_update_table = test_info['pre-update table'].split('&')
                    pre_query_mongo = test_info['pre-query mongo'].split('&')
                    pre_update_mongo = test_info['pre-update mongo'].split('&')
                    length = len(pre_update_table)
                else:
                    length = 1
                    pre_update_table = test_info['pre-update table'].split('$')
                    pre_query_mongo = test_info['pre-query mongo'].split('$')
                    pre_update_mongo = test_info['pre-update mongo'].split('$')

                for i in range(length):
                    Update_Mongo_Data(node=node, database=test_info['pre-update database']).updata_data(
                        table=pre_update_table[i],
                        query_params=eval(pre_query_mongo[i]),
                        update_params=eval(pre_update_mongo[i]))

            else:

                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']))

        # self,method,url,participantID,msgID,datetime,signkey,data
        header = CheckSign().check_sign_post(
            method=header_method,
            url=check_sign_url,
            participantID=participantID,
            msgID=msgID,
            datetime=datetime,
            signkey=evopay_conf.signkey,
            data=data)

        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
        result = res.json()
        headers = res.headers
        traceID = headers['Traceid']
        test_info['pre-update database'] = 'tyo'
        if test_info['pre-update mongo']:
            if '&' in test_info['pre-update table']:
                pre_update_table = test_info['pre-update table'].split('&')
                pre_query_mongo = test_info['pre-query mongo'].split('&')
                pre_update_mongo = test_info['pre-update mongo'].split('&')
                length = len(pre_update_table)
            else:
                length = 1
                pre_update_table = test_info['pre-update table'].split('$')
                pre_query_mongo = test_info['pre-query mongo'].split('$')
                pre_update_mongo = test_info['pre-update mongo'].split('$')
            for i in range(length):
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).update_data_reset(
                    table=pre_update_table[i],
                    query_params=eval(pre_query_mongo[i]),
                    update_params=eval(pre_update_mongo[i]))
        else:
            Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data_reset(
                table=test_info['pre-update table'])

        if test_info['update_mongo']:
            mongo_query = multi_replace(str(test_info["check_mongo"]))
            db_sgp_evopay.update_one(table='tokenVault', query_params=eval(mongo_query),
                                     updata_params=eval(test_info["update_mongo"]))
            
        #是否需要恢复yapi正常数据
        if update_yapi:
            yapi_operation.reset_yapi()
        return res


    def response_check(self,result,test_info,head_params,body_params,traceID,node='single'):
        expected = test_info['expected']
        interface = test_info["interface"]

        try:
            mopToken_value = ''
            #断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"]=='S0000' and  result["result"]["message"]=='Success.':
                # 获取mopToken.value
                mopToken_value = result['mopToken'][0]['value']
                setattr(case, 'mopToken_value', mopToken_value)
                #断言返回值
                Checkresponse().check_CPMToken_res(interface,result)

            try:
                #判断是否有数据库校验语句
                if test_info['check_mongo']:

                    if interface=='CPM Token':

                        #判断是否有数据进行替换
                        mongo_query =  eval(multi_replace(str(test_info['check_mongo'])))
                        # 校验发送给parnter的数据
                        Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_CPMToken_useWOPToken(mongo_query={ "payload.mopToken.0.value": mopToken_value }, participantID=head_params['wopParticipantID'])
                        # 检查数据库必填值得存入

                        mongo_result = db_tyo_evopay.get_one(table='tokenVault', query_params=mongo_query)
                        Checkmongo().check_CPMToken_mongo(test_data_interface="CPM Token", db_data=mongo_result)
                        mongo_wop=mongo_result['wopID']
                        mongo_mop = mongo_result['mopID']
                        if node=='double':
                            mongo_result_sgp = db_sgp_evopay.get_one(table='tokenVault', query_params=(mongo_query))
                            Checkmongo().check_CPMToken_mongo(test_data_interface="CPM Token", db_data=mongo_result_sgp)
                            mongo_wop_sgp=mongo_result_sgp['wopID']
                            mongo_mop_sgp = mongo_result_sgp['mopID']
                        #
                        # 获取测试数据数据库的断言
                        mongo_expected = multi_replace(str(test_info['check_mongo_expected']))

                        # 断言数据库里的字段

                        assert eval(mongo_expected)["wopID"] == mongo_wop
                        assert eval(mongo_expected)["mopID"] == mongo_mop
                        if node == 'double':
                            assert eval(mongo_expected)["wopID"] == mongo_wop_sgp
                            assert eval(mongo_expected)["mopID"] == mongo_mop_sgp


                else:
                    print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过".format(test_info["title"]),{ "qrList.0.value": mopToken_value })
                log.debug(f"请求的参数为{body_params}")
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"],traceID))
        except AssertionError as e:
            print("用例：{}--执行未通过,traceID为{}".format(test_info["title"], traceID))
            log.debug(f"请求的参数为{body_params}")
            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"], traceID))



