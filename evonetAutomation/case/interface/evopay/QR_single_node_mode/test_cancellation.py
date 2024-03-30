import pytest
import json
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evologs,db_sgp_evopay
from common.evopay.reponse_check import Checkresponse
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from base.read_config import Conf
from base.http_request import HttpRequest
from common.evopay.replace_data import multi_replace,case
from base.db import MongoDB
from base.encrypt import Encrypt
from common.evopay.read_csv import ReadCSV
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.cpm.cpm_token import CPM_Token_Message
from common.evopay.common_functions.cpm.cpm_payment import CPM_Payment_Message
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.common_functions.mpm.mpmpaymentauthentication import MPMpaymentauthentication
from common.evopay.common_functions.mpm.mpmnotify import MPMnotify
from common.evopay.common_functions.cancel.cancel import Cancel
from common.evopay.common_functions.refund.refund import Refund
from common.evopay.Initialization import initialization
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification
from case.interface.evopay.QR_single_node_mode.test_refund import Testrefund


data_file=ReadFile().read_data_file("evopay_evonet_cancellation","QR_single_node_mode","evopay")
cancellation_testdata=ReadCSV(data_file).read_data()

class Testcancellation():
    def __init__(self,envirs):
        self.envirs=envirs

    def common_params_init(self,test_info,node='single'):
        if test_info["interface"] == 'MPM QR Verification':
            common_params = MPMqrverify()
            common_params_Conf = common_params.MPMqrverify_Conf
            common_params_body = common_params.MPMqrverify_Body
            if node=='double':
                common_params_Conf = common_params.MPMqrverify_Conf_double
                common_params_body = common_params.MPMqrverify_Body_double

        elif test_info["interface"] == 'MPM Payment Authentication':
            common_params = MPMpaymentauthentication()
            common_params_Conf = common_params.MPMpaymentauthentication_Conf
            common_params_body = common_params.MPMpaymentauthentication_Body
            if node=='double':
                common_params_Conf = common_params.MPMpaymentauthentication_Conf_double
                common_params_body = common_params.MPMpaymentauthentication_Body_double
        elif test_info["interface"] == 'CPM Token':
            common_params = CPM_Token_Message()
            common_params_Conf = common_params.CPM_Token_Conf
            common_params_body = common_params.CPM_Token_Body
            if node == 'double':
                common_params_Conf = common_params.CPM_Token_Conf_double
                common_params_body = common_params.CPM_Token_Body_double
        elif test_info["interface"] == 'CPM Payment':
            common_params = CPM_Payment_Message()
            common_params_Conf = common_params.CPM_Payment_Conf
            common_params_body = common_params.CPM_Payment_Body
            if node == 'double':
                common_params_Conf = common_params.CPM_Payment_Conf_double
                common_params_body = common_params.CPM_Payment_Body_double
        elif test_info["interface"] == 'Payment Notification':
            common_params = MPMnotify()
            common_params_Conf = common_params.notify_Conf
            common_params_body = common_params.notify_Body
            if node == 'double':
                common_params_Conf = common_params.notify_Conf_double
                common_params_body = common_params.notify_Body_double
        elif test_info["interface"] == 'Refund':
            common_params = Refund()
            common_params_Conf = common_params.Refund_Conf
            common_params_body = common_params.Refund_Body
            if node == 'double':
                common_params_Conf = common_params.Refund_Conf_double
                common_params_body = common_params.Refund_Body_double
        else:
            common_params = Cancel()
            common_params_Conf = common_params.Cancel_Conf
            common_params_body = common_params.Cancel_Body
            if node == 'double':
                common_params_Conf = common_params.Cancel_Conf_double
                common_params_body = common_params.Cancel_Body_double

        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        # 兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params

    @pytest.mark.parametrize('test_info',cancellation_testdata)
    def test_cancellation(self,test_info):

        #判断接口是MPM_QR_Verification
        if test_info["interface"]=='MPM QR Verification':
            body_params,head_params = self.common_params_init(test_info)
            res = Testmpmqrverification(self.envirs).post_mpmqrverification(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_cancel(result,test_info,body_params,traceID)
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)

        #MPM_Payment_Authentication接口
        elif test_info["interface"] == 'MPM Payment Authentication':
            body_params,head_params = self.common_params_init(test_info)
            res,config_currency  = Testmpmpaymentauthentication(self.envirs).post_mpmauthentication(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_cancel(result, test_info,body_params,traceID)
            # 获取接口返回的evonetReference
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            #获取evonetOrderNumber，用于反向交易传参
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)

        elif test_info["interface"] == 'Payment Notification':
            body_params,head_params = self.common_params_init(test_info)
            billing_key = {}
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
            self.responce_check_cancel(result,test_info,body_params,traceID)


            # CPM_token接口
        elif test_info["interface"] == 'CPM Token':
            # 获取URL
            body_params,head_params = self.common_params_init(test_info)
            res = Testcpmtoken(self.envirs).post_cpmtoken(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_cancel(result, test_info,body_params,traceID)
            mopToken=result['mopToken']
            for item in mopToken:
                if item['type']=='Barcode':
                    mopToken_barcode_value=item['value']
                    setattr(case,'mopToken',mopToken_barcode_value)
                else:
                    mopToken_quickResponseCode_value=item['value']
                    setattr(case, 'mopToken', mopToken_quickResponseCode_value)

        # CPM_payment接口
        elif test_info["interface"] == 'CPM Payment':
            body_params,head_params = self.common_params_init(test_info)
            res,config_currency = Testcpmpayment(self.envirs).post_cpmpayment(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_cancel(result,test_info,body_params,traceID)
            # 获取evonetOrderNumber，用于反向交易传参
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            mopOrderNumber=result['mopOrderNumber']
            setattr(case, 'originalMopOrderNumber', mopOrderNumber)
            if test_info['update_mongo']:
                mongo_query = multi_replace(str(test_info["check_mongo"]))
                db_tyo_evopay.update_one(table='trans', query_params=eval(mongo_query),
                              updata_params=eval(test_info["update_mongo"]))

        elif test_info["interface"] == 'Refund':
            body_params,head_params = self.common_params_init(test_info)
            res = Testrefund(self.envirs).post_refund(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_cancel(result, test_info,body_params,traceID)

        else:
            body_params,head_params = self.common_params_init(test_info)
            res = self.post_cancel(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_cancel(result,test_info,body_params,traceID)

    def post_cancel(self,test_info,head_params,body_params,node='single'):
        check_sign_url = head_params['url']
        if node == 'double':
            base_url = evopay_conf.base_url_mop
        else:
            base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']
        # 判断是否有数据进行替换
        self.data = multi_replace(str(body_params))

        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()

        participantID = head_params['mopParticipantID']
        if test_info['pre-update table']:
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node=node,database=test_info['pre-update database']).updata_data(table=test_info['pre-update table'],
                                                query_params=eval(test_info['pre-query mongo']),
                                                update_params=eval(test_info['pre-update mongo']))
            else:

                Update_Mongo_Data(node=node,database=test_info['pre-update database']).delete_data(table=test_info['pre-update table'],
                                                query_params=eval(test_info['pre-query mongo']))

        # self,method,url,participantID,msgID,datetime,signkey,data
        header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=self.data)
        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(self.data))
        # result = res.json()
        # headers = res.headers
        # traceID = headers['Traceid']
        if test_info['pre-update mongo']:
            Update_Mongo_Data(node=node,database=test_info['pre-update database']).update_data_reset(table=test_info['pre-update table'],
                                                  query_params=eval(test_info['pre-query mongo']),
                                                  update_params=eval(test_info['pre-update mongo']))
        else:
            Update_Mongo_Data(node=node,database=test_info['pre-update database']).delete_data_reset(table=test_info['pre-update table'])
        return res

    def responce_check_cancel(self,result,test_info,body_params,traceID,node='single'):

        #断言
        #获取测试案例中的期望
        expected=test_info['expected']
        #获取interface
        interface=test_info["interface"]

        try:

            #断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"]=='S0000' and result["result"]["message"]=='Success.':
                if interface == 'MPM QR Verification':
                    Checkresponse().check_MPMQRVerification_res(interface, result)
                elif interface=='MPM Payment Authentication':
                    Checkresponse().check_MPMPaymentAuthentication_res(interface,result)
                elif interface == 'CPM Token':
                    Checkresponse().check_CPMToken_res(interface, result)
                elif interface == 'CPM Payment':
                    Checkresponse().check_CPMPayment_res(interface, result)
                elif interface == 'Cancellation':
                    Checkresponse().check_cancellation_res(interface, result)


            #断言数据库
            try:
                #判断是否有数据库校验语句
                if test_info['check_mongo']:
                    #判断接口是Cancellation
                    if interface=='Cancellation':


                        #payment交易需要替换的数据
                        mongo_query_payment=test_info["check_mongo"].replace("#evonetOrderNumber#",getattr(case,'evonetOrderNumber'))
                        # 查询原交易payment的交易
                        mongo_result_payment = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_payment))
                        #获取数据库数据
                        # 查询原交易payment的交易(sgp数据库)
                        if node=='double':
                            mongo_result_payment_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query_payment))
                            # 获取sgp数据库数据
                            mongo_status_payment_sgp  = mongo_result_payment_sgp['status']
                            mongo_wopStatus_payment_sgp  = mongo_result_payment_sgp['wopStatus']
                            mongo_mopStatus_payment_sgp  = mongo_result_payment_sgp['mopStatus']

                        mongo_status_payment = mongo_result_payment['status']
                        mongo_wopStatus_payment = mongo_result_payment['wopStatus']
                        mongo_mopStatus_payment = mongo_result_payment['mopStatus']
                        # 数据库查询出的traceID
                        traceID = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_payment))['traceID']
                        # 校验发送给parnter的数据
                        Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_cancellation(
                            mongo_query={"traceID": traceID}, body=body_params)
                        # 获取测试数据（payment）数据库的断言
                        mongo_expected_payment = test_info["check_mongo_expected"]
                        # 断言数据库里payment的字段
                        if 'payment_wop' not in mongo_expected_payment:
                            # 断言数据库里payment的字段（tyo数据库）
                            assert eval(mongo_expected_payment)["status"] == mongo_status_payment
                            assert eval(mongo_expected_payment)["wopStatus"] == mongo_wopStatus_payment
                            assert eval(mongo_expected_payment)["mopStatus"] == mongo_mopStatus_payment
                            if node=='double':
                                # 断言数据库里payment的字段（sgp数据库）
                                assert eval(mongo_expected_payment)["status"] == mongo_status_payment_sgp
                                assert eval(mongo_expected_payment)["wopStatus"] == mongo_wopStatus_payment_sgp
                                assert eval(mongo_expected_payment)["mopStatus"] == mongo_mopStatus_payment_sgp
                        else:
                            # 获取测试数据（payment）wop数据库的断言
                            mongo_expected_payment_wop = eval(test_info["check_mongo_expected"])["payment_wop"]
                            print(mongo_expected_payment_wop)
                            # 获取测试数据（payment）mop数据库的断言
                            mongo_expected_payment_mop = eval(test_info["check_mongo_expected"])["payment_mop"]
                            print(mongo_expected_payment_mop)
                            # 断言数据库里payment的字段（tyo数据库）
                            assert mongo_expected_payment_wop["status"] == mongo_status_payment
                            assert mongo_expected_payment_wop["wopStatus"] == mongo_wopStatus_payment
                            assert mongo_expected_payment_wop["mopStatus"] == mongo_mopStatus_payment
                            if node == 'double':
                                # 断言数据库里payment的字段（sgp数据库）
                                assert mongo_expected_payment_mop["status"] == mongo_status_payment_sgp
                                assert mongo_expected_payment_mop["wopStatus"] == mongo_wopStatus_payment_sgp
                                assert mongo_expected_payment_mop["mopStatus"] == mongo_mopStatus_payment_sgp
                else:
                    print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过,traceID为".format(test_info["title"],traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为".format(test_info["title"],traceID))

        except AssertionError as e:
            if test_info["interface"] == 'MPM QR Verification':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))

            elif test_info["interface"] == 'MPM Payment Authentication':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            elif test_info["interface"] == 'Payment Notification':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            elif test_info["interface"] == 'CPM Token':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            elif test_info["interface"] == 'CPM Payment':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            elif test_info["interface"] == 'Cancellation':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))

            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"],traceID))









