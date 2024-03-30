import pytest

from common.evopay.conf_init import evopay_conf
from common.evopay.reponse_check import Checkresponse
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from base.http_request import HttpRequest
from common.evopay.read_csv import ReadCSV
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.mopchecking.mopchecking import Mop_Checking
from common.evopay.Initialization import initialization
data_file=ReadFile().read_data_file("evopay_evonet_mopchecking","QR_single_node_mode","evopay")
mopchecking_testdata=ReadCSV(data_file).read_data()
class Testmopchecking():
    def __init__(self,envirs):
        self.envirs=envirs


    def common_params_init(self,test_info,node='single'):
        common_params = Mop_Checking()
        if node == 'single':
            common_params_Conf = common_params.Mop_checking_Conf
            common_params_body = common_params.Mop_checking_Body
        else:
            common_params_Conf = common_params.Mop_checking_Conf_double
            common_params_body = common_params.Mop_checking_Body_double


        init = initialization( common_params_Conf,common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])


        #兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["url"]:
            head_params["url"] = test_info["url"]
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params

    @pytest.mark.parametrize('test_info',mopchecking_testdata)
    def test_mopchecking(self,test_info):
        body_params,head_params = self.common_params_init(test_info)
        res = self.post_mopchecking(test_info,head_params,body_params)
        headers = res.headers
        traceID = headers['Traceid']
        result = res.json()
        self.response_check_mopchecking(result,test_info,traceID)


    def post_mopchecking(self,test_info,head_params,body_params,node='single'):
        check_sign_url = head_params['url']
        base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']

        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()

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
        header = CheckSign().check_sign_get(method=header_method, url=check_sign_url, participantID=participantID,
                                            msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey)
        # 发送请求
        res = HttpRequest().send(url=url, method=method, headers=header)
        headers = res.headers
        if test_info['pre-update mongo']:
            Update_Mongo_Data(node=node, database=test_info['pre-update database']).update_data_reset(
                table=test_info['pre-update table'],
                query_params=eval(test_info['pre-query mongo']),
                update_params=eval(test_info['pre-update mongo']))
        else:
            Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data_reset(
                table=test_info['pre-update table'])
        return res

    def response_check_mopchecking(self, result,test_info,traceID):
        #获取URL
         #断言
        #获取测试案例中的期望
        expected=test_info['expected']
        #获取interface
        interface=test_info["interface"]
        try:
            #断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"]=='S0000' and  result["result"]["message"]=='Success.':
                Checkresponse().check_MOPChecking_res(interface,result)
        except AssertionError as e:
            print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"],traceID))






