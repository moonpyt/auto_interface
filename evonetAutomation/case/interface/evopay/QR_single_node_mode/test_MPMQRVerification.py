import pytest

from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_sgp_evopay, db_sgp_evologs, db_tyo_evologs
from common.evopay.reponse_check import Checkresponse
from common.evopay.read_data import EvopayTestCase
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from base.read_config import Conf
from base.http_request import HttpRequest
from common.evopay.replace_data import multi_replace
from base.db import MongoDB
from common.evopay.read_csv import ReadCSV
from base.encrypt import Encrypt
from common.evopay.reponse_check import Checkresponse
from common.evopay.mongo_data_check import Checkmongo
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.replace_data import case
from common.evopay.Initialization import initialization
data_file=ReadFile().read_data_file("evopay_evonet_mpmqrverification","QR_single_node_mode","evopay")
mpmqrverification_testdata=ReadCSV(data_file).read_data()
class Testmpmqrverification():
    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize('test_info',mpmqrverification_testdata)
    def test_mpmqrverification(self,test_info):
        body_params,head_params = self.common_params_init(test_info)
        res = self.post_mpmqrverification(test_info,head_params,body_params)
        headers = res.headers
        traceID = headers['Traceid']
        result = res.json()
        self.check_response_mpmqrverify(result,test_info,head_params,body_params,traceID)

    def common_params_init(self,test_info,node='single'):
        common_params = MPMqrverify()
        if node == 'single':
            init = initialization(common_params.MPMqrverify_Conf, common_params.MPMqrverify_Body)
        else :
            init = initialization(common_params.MPMqrverify_Conf_double, common_params.MPMqrverify_Body_double)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        #兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params


    def post_mpmqrverification(self,test_info,head_params,body_params,node='single'):
        # 获取URL
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
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).updata_data(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            else:

                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']))
        # self,method,url,participantID,msgID,datetime,signkey,data
        header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)

        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
        result = res.json()
        headers = res.headers
        if test_info['pre-update table']:
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).update_data_reset(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            else:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data_reset(
                    table=test_info['pre-update table'])
        # 获取接口返回的evonetReference
        evonetReference = result['evonetReference']
        setattr(case, 'evonetReference', evonetReference)

        result_evonetReference = ''
        return res

    def check_response_mpmqrverify(self,result,test_info,head_params,body_params,traceID,node='single'):
        result_evonetReference = ''
        expected = test_info['expected']
        interface = test_info["interface"]
        try:
            #断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"]=='S0000' and  result["result"]["message"]=='Success.':
                Checkresponse().check_CPMToken_res(interface,result)
            #断言数据库的数据
            try:
                if test_info['check_mongo']:
                    result_evonetReference = result["evonetReference"]
                    mongo_query = str(test_info["check_mongo"]).replace("#evonetReference#", result_evonetReference)

                    # # 校验发送给parnter的数据
                    Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_MPMQRVerification(
                        mongo_query={"traceID": traceID}, participantID=head_params['wopParticipantID'], body=body_params)

                    # 检查tyo数据库必填值得存入
                    mongo_result_tyo = db_tyo_evopay.get_one(table='transReference', query_params=eval(mongo_query))
                    Checkmongo().check_transReference_mongo(test_data_interface="MPM QR Verification",
                                                            db_data=mongo_result_tyo)
                    # 检查sgp数据库必填值得存入
                    if node=='double':
                        mongo_result_sgp = db_sgp_evopay.get_one(table='transReference', query_params=eval(mongo_query))
                        Checkmongo().check_transReference_mongo(test_data_interface="MPM QR Verification",
                                                                db_data=mongo_result_sgp)
                        mongo_wopID_sgp = mongo_result_sgp['wopID']
                        mongo_mopID_sgp = mongo_result_sgp['mopID']

                    #获取tyo数据库的数据
                    mongo_wopID_tyo = mongo_result_tyo['wopID']
                    mongo_mopID_tyo = mongo_result_tyo['mopID']

                    # 获取测试数据数据库的断言,替换数据
                    mongo_expected = multi_replace(str(test_info['check_mongo_expected']))
                    # 断言tyo数据库里的字段

                    assert eval(mongo_expected)["wopID"] == mongo_wopID_tyo
                    assert eval(mongo_expected)["mopID"] == mongo_mopID_tyo
                    # 断言sgp数据库里的字段
                    if node == 'double':
                        assert eval(mongo_expected)["wopID"] == mongo_wopID_sgp
                        assert eval(mongo_expected)["mopID"] == mongo_mopID_sgp

                else:
                   print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"],traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"],traceID))
        except AssertionError as e:

            print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"],traceID))







