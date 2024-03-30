import pytest
import json
from common.evopay.conf_init import evopay_conf, db_tyo_evopay,db_sgp_evopay
from common.evopay.reponse_check import Checkresponse
from common.evopay.read_data import EvopayTestCase
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from base.read_config import Conf
from base.http_request import HttpRequest
from common.evopay.replace_data import multi_replace,case
from base.db import MongoDB
from base.encrypt import Encrypt
from common.evopay.read_csv import ReadCSV
from common.evopay.mongo_data_check import Checkmongo
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.cpm.cpm_token import CPM_Token_Message
from common.evopay.common_functions.cpm.cpm_payment import CPM_Payment_Message
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.common_functions.mpm.mpmpaymentauthentication import MPMpaymentauthentication
from common.evopay.common_functions.mpm.mpmnotify import MPMnotify
from common.evopay.common_functions.refund.refund import Refund
from common.evopay.common_functions.inqy.inqy import Inquiry
from common.evopay.common_functions.cancel.cancel import Cancel
from common.evopay.Initialization import initialization
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification
from case.interface.evopay.QR_single_node_mode.test_refund import Testrefund
from case.interface.evopay.QR_single_node_mode.test_cancellation import Testcancellation

data_file=ReadFile().read_data_file("evopay_evonet_paymentinquiry","QR_single_node_mode","evopay")
paymentinquiry_testdata=ReadCSV(data_file).read_data()

class Testpaymentinquiry():
    def __init__(self,envirs):
        self.envirs=envirs

    def common_params_init(self,test_info,node='single'):
        if test_info["interface"] == 'MPM QR Verification':
            common_params = MPMqrverify()
            if node=='single':
                common_params_Conf = common_params.MPMqrverify_Conf
                common_params_body = common_params.MPMqrverify_Body
            else:
                common_params_Conf = common_params.MPMqrverify_Conf_double
                common_params_body = common_params.MPMqrverify_Body_double

        elif test_info["interface"] == 'MPM Payment Authentication':
            common_params = MPMpaymentauthentication()
            if node == 'single':
                common_params_Conf = common_params.MPMpaymentauthentication_Conf
                common_params_body = common_params.MPMpaymentauthentication_Body
            else:
                common_params_Conf = common_params.MPMpaymentauthentication_Conf_double
                common_params_body = common_params.MPMpaymentauthentication_Body_double

        elif test_info["interface"] == 'CPM Token':
            common_params = CPM_Token_Message()
            if node == 'single':
                common_params_Conf = common_params.CPM_Token_Conf
                common_params_body = common_params.CPM_Token_Body
            else:
                common_params_Conf = common_params.CPM_Token_Conf_double
                common_params_body = common_params.CPM_Token_Body_double

        elif test_info["interface"] == 'CPM Payment':
            common_params = CPM_Payment_Message()
            if node == 'single':
                common_params_Conf = common_params.CPM_Payment_Conf
                common_params_body = common_params.CPM_Payment_Body
            else:
                common_params_Conf = common_params.CPM_Payment_Conf_double
                common_params_body = common_params.CPM_Payment_Body_double
        elif test_info["interface"] == 'Payment Notification':
            common_params = MPMnotify()
            if node == 'single':
                common_params_Conf = common_params.notify_Conf
                common_params_body = common_params.notify_Body
            else:
                common_params_Conf = common_params.notify_Conf_double
                common_params_body = common_params.notify_Body_double
        elif test_info["interface"] == 'Refund':
            common_params = Refund()
            if node == 'single':
                common_params_Conf = common_params.Refund_Conf
                common_params_body = common_params.Refund_Body
            else:
                common_params_Conf = common_params.Refund_Conf_double
                common_params_body = common_params.Refund_Body_double

        elif test_info["interface"] == 'Cancellation':
            common_params = Cancel()
            if node == 'single':
                common_params_Conf = common_params.Cancel_Conf
                common_params_body = common_params.Cancel_Body
            else:
                common_params_Conf = common_params.Cancel_Conf_double
                common_params_body = common_params.Cancel_Body_double

        else:
            common_params = Inquiry()
            if node == 'single':
                common_params_Conf = common_params.Inquiry_Conf_Common
                common_params_body = common_params.Inquiry_Body_Common
            else:
                common_params_Conf = common_params.Inquiry_Conf_Common_double
                common_params_body = common_params.Inquiry_Body_Common_double
        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        # 兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info.get("url"):
            head_params["url"] = test_info["url"]
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] =test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] =test_info["mopParticipantID"]
        return body_params,head_params

    @pytest.mark.parametrize('test_info',paymentinquiry_testdata)
    def test_paymentinquiry(self,test_info):
        if test_info["interface"]=='MPM QR Verification':
            body_params,head_params = self.common_params_init(test_info)
            res = Testmpmqrverification(self.envirs).post_mpmqrverification(test_info, head_params, body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result,test_info,traceID)
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)
            return result,traceID,body_params,head_params


        #MPM_Payment_Authentication接口
        elif test_info["interface"] == 'MPM Payment Authentication':
            body_params,head_params = self.common_params_init(test_info)
            res,config_currency = Testmpmpaymentauthentication(self.envirs).post_mpmauthentication(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            # 获取接口返回的evonetReference
            self.responce_check_inqiury(result, test_info,traceID)
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
            # mongo_result = db_tyo_evopay.get_one(table='trans', query_params={"evonetOrderNumber": getattr(case, 'evonetOrderNumber')})
            # mopOrderNumber=mongo_result['mopOrderNumber']
            # setattr(case, 'originalMopOrderNumber', mopOrderNumber)
            return result,traceID,body_params,head_params

        #notify接口
        elif test_info["interface"] == 'Payment Notification':
            body_params,head_params = self.common_params_init(test_info)
            billing_key = {}
            if test_info['data']:
                billing_csv = json.loads(test_info['data'])
                if 'billingAmount' in  billing_csv:
                    body_params['billingAmount'] = billing_csv['billingAmount']
                if 'billingFXRate' in  billing_csv:
                    body_params['billingFXRate'] = billing_csv['billingFXRate']
                if 'settleAmount' in  billing_csv:
                    body_params['settleAmount'] = billing_csv['settleAmount']
                if 'settleFXRate' in  billing_csv:
                    body_params['settleFXRate'] = billing_csv['settleFXRate']
            res = Testpaymentnotification(self.envirs).post_mpmnotify(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result, test_info,traceID)
            return result,traceID,body_params,head_params

            # CPM_token接口
        elif test_info["interface"] == 'CPM Token':
            # 获取URL
            body_params, head_params = self.common_params_init(test_info)
            res = Testcpmtoken(self.envirs).post_cpmtoken(test_info, head_params, body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result, test_info,traceID)
            mopToken = result['mopToken']
            for item in mopToken:
                if item['type'] == 'Barcode':
                    mopToken_barcode_value = item['value']
                    setattr(case, 'mopToken', mopToken_barcode_value)
                else:
                    mopToken_quickResponseCode_value = item['value']
                    setattr(case, 'mopToken', mopToken_quickResponseCode_value)
            return result, traceID, body_params, head_params

        # CPM_payment接口
        elif test_info["interface"] == 'CPM Payment':
            body_params, head_params = self.common_params_init(test_info)
            res,config_currency = Testcpmpayment(self.envirs).post_cpmpayment(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result,test_info,traceID)
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            mopOrderNumber = result['mopOrderNumber']
            setattr(case, 'originalMopOrderNumber', mopOrderNumber)
            if test_info['update_mongo']:

                mongo_query =multi_replace(str(test_info["check_mongo"]))
                db_tyo_evopay.update_one(table='trans',query_params=eval(mongo_query),updata_params=eval(test_info["update_mongo"]))
            return result,traceID,body_params,head_params


        #取消接口
        elif test_info["interface"] == 'Cancellation':
            body_params, head_params = self.common_params_init(test_info)
            res = Testcancellation(self.envirs).post_cancel(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result, test_info,traceID)
            return result,traceID,body_params,head_params

        #退款接口
        elif test_info["interface"] == 'Refund':
            body_params, head_params = self.common_params_init(test_info)
            res = Testrefund(self.envirs).post_refund(test_info, head_params, body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result, test_info,traceID)
            return result,traceID,body_params,head_params


        #payment Inquirey查询接口
        else:
            body_params, head_params = self.common_params_init(test_info)
            res = Testpaymentinquiry(self.envirs).post_inquiry(test_info, head_params, body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_inqiury(result, test_info,traceID)
            return result,traceID,body_params,head_params

    def post_inquiry(self,test_info,head_params,body_params,node='single'):
        # 查询URL中是否有替换的数据,获取url
        check_sign_url = multi_replace(str(test_info['url']))
        if node == 'double':
            base_url = evopay_conf.base_url_mop
        else:
            base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']
        # 判断data是否有数据进行替换,用来查数据库
        body_params = multi_replace(str(body_params))

        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()

        participantID = head_params['mopParticipantID']
        if test_info['pre-query mongo'] and "#" in test_info['pre-query mongo'] :
            test_info['pre-query mongo'] = multi_replace(str(test_info['pre-query mongo']))
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
        result = res.json()
        headers = res.headers
        traceID = headers['Traceid']
        if test_info['pre-update table']:
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).update_data_reset(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            else:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data_reset(
                    table=test_info['pre-update table'])
        return res

    def responce_check_inqiury(self,result,test_info,traceID,node='single'):
        # 断言
        # 获取测试案例中的期望
        expected = test_info["expected"]
        # 获取interface
        interface = test_info["interface"]
        result_evonetOrderNumber = ''
        # 断言response的数据

        try:
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"] == 'S0000' and result["result"]["message"] == 'Success.':
                if interface == 'MPM QR Verification':
                    Checkresponse().check_MPMQRVerification_res(interface, result)
                elif interface == 'MPM Payment Authentication':
                    Checkresponse().check_MPMPaymentAuthentication_res(interface, result)
                elif interface == 'Payment Inquiry':
                    Checkresponse().check_PaymentInquiry_res(interface, result)

            # 断言数据库
            try:
                # 判断是否有数据库校验语句
                if test_info['check_mongo']:
                    # 判断接口是Payment Inquiry
                    if interface == 'Payment Inquiry':
                        if "mopOrderNumber" in test_info["check_mongo"]:

                            result_mopOrderNumber = result['mopOrderNumber']
                            mongo_query = str(test_info["check_mongo"]).replace("#mopOrderNumber#",
                                                                                result_mopOrderNumber)
                        else:
                            result_evonetOrderNumber = result['evonetOrderNumber']
                            mongo_query = str(test_info["check_mongo"]).replace("#evonetOrderNumber#",
                                                                                result_evonetOrderNumber)
                        if node=='single':

                            mongo_result = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))
                            print(mongo_result)
                            # 获取数据库的数据
                            mongo_status = mongo_result['status']
                            mongo_wopStatus = mongo_result['wopStatus']
                            mongo_mopStatus = mongo_result['mopStatus']
                            # 获取测试数据数据库的断言
                            mongo_expected = test_info["check_mongo_expected"]
                            # 断言数据库里的字段
                            assert eval(mongo_expected)["status"] == mongo_status
                            assert eval(mongo_expected)["wopStatus"] == mongo_wopStatus
                            assert eval(mongo_expected)["mopStatus"] == mongo_mopStatus
                        else:
                            mongo_result_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query))
                            # 获取sgp数据库的数据
                            mongo_status_sgp = mongo_result_sgp['status']
                            mongo_wopStatus_sgp = mongo_result_sgp['wopStatus']
                            mongo_mopStatus_sgp = mongo_result_sgp['mopStatus']
                            mongo_expected = test_info["check_mongo_expected"]
                            assert eval(mongo_expected)["status"] == mongo_status_sgp
                            assert eval(mongo_expected)["wopStatus"] == mongo_wopStatus_sgp
                            assert eval(mongo_expected)["mopStatus"] == mongo_mopStatus_sgp


                else:
                    print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"], traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"], traceID))

        except AssertionError as e:
            if test_info["interface"] == 'MPM QR Verification':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'MPM Payment Authentication':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'Payment Notification':
                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'CPM Token':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'CPM Payment':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'Cancellation':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'Refund':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            else:

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))

            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"], traceID))










