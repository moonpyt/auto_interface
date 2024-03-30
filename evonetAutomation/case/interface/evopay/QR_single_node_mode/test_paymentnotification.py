import pytest
import json
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evoconfig, db_tyo_evologs,db_sgp_evopay,db_sgp_evologs
from common.evopay.reponse_check import Checkresponse
from common.evopay.read_data import EvopayTestCase
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from loguru import logger as log
from base.read_config import Conf
from base.http_request import HttpRequest
from common.evopay.replace_data import multi_replace,case
from base.db import MongoDB
from common.evopay.read_csv import ReadCSV
from base.encrypt import Encrypt
from common.evopay.mongo_data_check import Checkmongo
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.common_functions.mpm.mpmpaymentauthentication import MPMpaymentauthentication
from common.evopay.common_functions.mpm.mpmnotify import MPMnotify
from common.evopay.common_functions.cpm.cpm_token import CPM_Token_Message
from common.evopay.common_functions.cpm.cpm_payment import CPM_Payment_Message
from common.evopay.Initialization import initialization
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment
data_file=ReadFile().read_data_file("evopay_evonet_paymentnotification","QR_single_node_mode","evopay")
paymentnotification_testdata=ReadCSV(data_file).read_data()
class Testpaymentnotification():
    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',paymentnotification_testdata)
    def test_paymentnotification(self,test_info):
        #判断接口是MPM_QR_Verification
        if test_info["interface"]=='MPM QR Verification':
            body_params,head_params = self.common_params_init(test_info)
            res = Testmpmqrverification(self.envirs).post_mpmqrverification(test_info, head_params,body_params)
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)

        #MPM_Payment_Authentication接口
        elif test_info["interface"]=='MPM Payment Authentication':
            body_params,head_params=self.common_params_init(test_info)
            res,config_currency = Testmpmpaymentauthentication(self.envirs).post_mpmauthentication(test_info, head_params,body_params)
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)

        elif test_info["interface"] == 'CPM Token':
            body_params,head_params=self.common_params_init(test_info)
            res = Testcpmtoken(self.envirs).post_cpmtoken(test_info,head_params,body_params)
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] ==result["result"]["message"]

            mopToken=result['mopToken']
            for item in mopToken:
                if item['type']=='Barcode':
                    mopToken_barcode_value=item['value']
                    setattr(case,'mopToken',mopToken_barcode_value)
                else:
                    mopToken_quickResponseCode_value=item['value']
                    setattr(case, 'mopToken', mopToken_quickResponseCode_value)
        elif test_info["interface"] == 'CPM Payment':
            body_params,head_params = self.common_params_init(test_info)
            res,config_currency = Testcpmpayment(self.envirs).post_cpmpayment(test_info,head_params,body_params)
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] ==result["result"]["message"]
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)

        else:
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
            res = self.post_mpmnotify(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.check_resopnse_mpmnotify(result,test_info,head_params,body_params,traceID)


    def post_mpmnotify(self,test_info,head_params,body_params,node='single'):
        check_sign_url = head_params['url']
        base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']
        # 判断是否有数据进行替换
        data = multi_replace(str(body_params))
        body_params = eval(data)
        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()


        participantID = head_params['wopParticipantID']

        if test_info['pre-update table']:
            if '#evonetOrderNumber#' in test_info['pre-query mongo']:
                test_info['pre-query mongo'] = multi_replace(test_info['pre-query mongo'])
            if test_info['pre-update table']=='trans':
                Update_Mongo_Data(node=node,database=test_info['pre-update database'],database_name='evopay').updata_data(table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']), update_params=eval(test_info['pre-update mongo']))
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node=node,database=test_info['pre-update database']).updata_data(table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']), update_params=eval(test_info['pre-update mongo']))
            else:
                Update_Mongo_Data(node=node,database=test_info['pre-update database']).delete_data(table=test_info['pre-update table'],query_params=eval(test_info['pre-query mongo']))
        # self,method,url,participantID,msgID,datetime,signkey,data
        header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=str(data))
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
        result_evonetOrderNumber=''
        return res

    def check_resopnse_mpmnotify(self,result, test_info,head_params,body_params,traceID,node='single'):
        expected = test_info['expected']
        interface =test_info['interface']
        try:
            # 断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"] == 'S0000' and result["result"]["message"] == 'Success.':
                if interface == 'MPM QR Verification':
                    Checkresponse().check_MPMQRVerification_res(interface, result)
                elif interface == 'MPM Payment Authentication':
                    Checkresponse().check_MPMPaymentAuthentication_res(interface, result)
                elif interface == 'CPM Token':
                    Checkresponse().check_CPMToken_res(interface, result)
                elif interface == 'CPM Payment':
                    Checkresponse().check_CPMPayment_res(interface, result)

            # 断言数据库
            try:
                # 判断是否有数据库校验语句
                if test_info['check_mongo']:
                    # 判断接口是Payment Notification
                    if interface == 'Payment Notification':

                        mongo_query = multi_replace(str(test_info['check_mongo']))
                        # 检查数据库必填值得存入
                        mongo_result = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))

                        Checkmongo().check_trans_mongo(test_data_interface="Payment Notification",db_data=mongo_result)

                        # 数据库查询出的traceID
                        traceID = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))['traceID']

                        # 校验成功的数据的某些字段
                        Checkmongo().check_trans_success(test_data_interface="Payment Notification",
                                                         db_data=mongo_result)
                        if node=='single':
                            # 校验发送给parnter的数据
                            Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_MPMPaymentNotification(
                                mongo_query={"traceID": traceID}, body=body_params)

                        if node=='double':
                            # 检查sgp数据库必填值得存入
                            mongo_result_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query))
                            log.debug(f"查询语句是{mongo_result_sgp}")

                            Checkmongo().check_trans_mongo(test_data_interface="Payment Notification",
                                                           db_data=mongo_result_sgp)
                            # 校验发送给parnter的数据
                            Check_evonet_to_partner(db_sgp_evologs).check_evonet_to_partner_MPMPaymentNotification(
                                mongo_query={"traceID": traceID}, body=body_params)

                            # 校验sgp数据库成功的数据的某些字段
                            Checkmongo().check_trans_success(test_data_interface="Payment Notification",
                                                             db_data=mongo_result_sgp)
                        # 获取测试数据数据库的断言，替换数据
                        mongo_expected = multi_replace(str(test_info['check_mongo_expected']))
                        if 'wopID' in mongo_expected:
                            mongo_wop = mongo_result['wopID']
                            mongo_mop = mongo_result['mopID']
                            assert eval(mongo_expected)["wopID"] == mongo_wop
                            assert eval(mongo_expected)["mopID"] == mongo_mop
                            if node=='double':
                                mongo_wop_sgp = mongo_result_sgp['wopID']
                                mongo_mop_sgp = mongo_result_sgp['mopID']
                                assert eval(mongo_expected)["wopID"] == mongo_wop_sgp
                                assert eval(mongo_expected)["mopID"] == mongo_mop_sgp

                        elif 'status' in mongo_expected:
                            mongo_status = mongo_result['status']
                            mongo_wopStatus = mongo_result['wopStatus']
                            mongo_mopStatus = mongo_result['mopStatus']
                            assert eval(mongo_expected)["status"] == mongo_status
                            assert eval(mongo_expected)["wopStatus"] == mongo_wopStatus
                            assert eval(mongo_expected)["mopStatus"] == mongo_mopStatus
                            if node == 'double':
                                mongo_status_sgp = mongo_result_sgp['status']
                                mongo_wopStatus_sgp = mongo_result_sgp['wopStatus']
                                mongo_mopStatus_sgp = mongo_result_sgp['mopStatus']
                                assert eval(mongo_expected)["status"] == mongo_status_sgp
                                assert eval(mongo_expected)["wopStatus"] == mongo_wopStatus_sgp
                                assert eval(mongo_expected)["mopStatus"] == mongo_mopStatus_sgp

                        elif 'SettleDate' in mongo_expected:

                            mongo_result_wop = db_tyo_evoconfig.get_one(table='wop', query_params={
                                'baseInfo.wopID': test_info['wopParticipantID']})
                            cutofftime = (mongo_result_wop['settleInfo']['cutoffTime'])[0:5]
                            cutofftime = cutofftime[0:2] + cutofftime[3:5]

                            if int(cutofftime) > int(1200):
                                mongo_expected_settdate = eval(multi_replace(str(test_info['check_mongo_expected'])))[
                                    "cutofftime_over_UTC_12:00"]

                            else:
                                mongo_expected_settdate = eval(multi_replace(str(test_info['check_mongo_expected'])))[
                                    "cutofftime_less_UTC_12:00"]
                            # 获取测试案例中的清算日期
                            mongo_expected_mopsettledate = mongo_expected_settdate['mopSettleDate']
                            mongo_expected_wopsettledate = mongo_expected_settdate['mopSettleDate']
                            # 获取数据库中的清算日期
                            mongo_result_mopsettledate = mongo_result['mopSettleDate']
                            mongo_result_wopsettledate = mongo_result['wopSettleDate']

                            # 断言清算日期
                            assert mongo_expected_mopsettledate == mongo_result_mopsettledate
                            assert mongo_expected_wopsettledate == mongo_result_wopsettledate
                            if node == 'double':
                                # 获取sgp数据库中的清算日期
                                mongo_result_mopsettledate_sgp = mongo_result_sgp['mopSettleDate']
                                mongo_result_wopsettledate_sgp = mongo_result_sgp['wopSettleDate']

                                # 断言sgp清算日期
                                assert mongo_expected_mopsettledate == mongo_result_mopsettledate_sgp
                                assert mongo_expected_wopsettledate == mongo_result_wopsettledate_sgp
                else:
                    print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"], traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验".format(test_info["title"]))

        except AssertionError as e:
            if test_info["interface"] == 'MPM QR Verification':
                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            if test_info["interface"] == 'MPM Payment Authentication':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))
            else:
                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],traceID))

            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"], traceID))

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
        else:
            if node == 'single':
                common_params = MPMnotify()
                common_params_Conf = common_params.notify_Conf
                common_params_body = common_params.notify_Body
            else:
                common_params = MPMnotify()
                common_params_Conf = common_params.notify_Conf_double
                common_params_body = common_params.notify_Body_double
        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        # 兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params



