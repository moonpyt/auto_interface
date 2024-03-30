import pytest
import json
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evoconfig, db_tyo_evologs,db_sgp_evopay
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
from common.evopay.mongo_data_check import Checkmongo
from common.evopay.read_csv import ReadCSV
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.common_functions.cpm.cpm_token import CPM_Token_Message
from common.evopay.common_functions.cpm.cpm_payment import CPM_Payment_Message
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.common_functions.mpm.mpmpaymentauthentication import MPMpaymentauthentication
from common.evopay.common_functions.mpm.mpmnotify import MPMnotify
from common.evopay.common_functions.refund.refund import Refund
from common.evopay.common_functions.inqy.inqy import Inquiry
from common.evopay.Initialization import initialization
from common.evopay.exception_operation_yapi import Exception_Yapi
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification
data_file=ReadFile().read_data_file("evopay_evonet_refund","QR_single_node_mode","evopay")
refund_testdata=ReadCSV(data_file).read_data()
class Testrefund():
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
        elif test_info["interface"] == 'Payment Inquiry':
            common_params = Inquiry()
            if node == 'single':
                common_params_Conf = common_params.Inquiry_Conf
                common_params_body = common_params.Inquiry_Body
            else:
                common_params_Conf = common_params.Inquiry_Conf_double
                common_params_body = common_params.Inquiry_Body_double
        else:
            common_params = Refund()
            if node == 'single':
                common_params_Conf = common_params.Refund_Conf
                common_params_body = common_params.Refund_Body
            else:
                common_params_Conf = common_params.Refund_Conf_double
                common_params_body = common_params.Refund_Body_double

        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        # 兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params




    @pytest.mark.parametrize('test_info',refund_testdata)
    def test_refund(self,test_info):
        #判断接口是MPM_QR_Verification
        if test_info["interface"]=='MPM QR Verification':
            body_params,head_params = self.common_params_init(test_info)
            res = Testmpmqrverification(self.envirs).post_mpmqrverification(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_refund(result,test_info,head_params,body_params,traceID)
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)



        #MPM_Payment_Authentication接口
        elif test_info["interface"] == 'MPM Payment Authentication':
            body_params,head_params = self.common_params_init(test_info)
            res,config_currency = Testmpmpaymentauthentication(self.envirs).post_mpmauthentication(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_refund(result, test_info,head_params,body_params,traceID)
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            setattr(case, 'MPMevonetOrderNumber', evonetOrderNumber)
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
            res = Testpaymentnotification(self.envirs).post_mpmnotify(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_refund(result,test_info,head_params,body_params,traceID)



            # CPM_token接口
        elif test_info["interface"] == 'CPM Token':
            # 获取URL
            body_params,head_params = self.common_params_init(test_info)
            res = Testcpmtoken(self.envirs).post_cpmtoken(test_info,head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_refund(result,test_info,head_params,body_params,traceID)
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
            self.responce_check_refund(result, test_info,head_params,body_params,traceID)
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)



        #查询接口
        elif test_info["interface"] == 'Payment Inquiry':
            # 查询URL中是否有替换的数据,获取url
            body_params,head_params = self.common_params_init(test_info)
            check_sign_url = multi_replace(str(head_params['url']))
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = head_params['method']
            # 判断data是否有数据进行替换,用来查数据库
            data = multi_replace(str(body_params))

            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()

            participantID = head_params['mopParticipantID']
            if test_info['pre-update table']:
                if test_info['pre-update mongo']:
                    Update_Mongo_Data(node='single',database=test_info['pre-update database']).updata_data(table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']), update_params=eval(test_info['pre-update mongo']))
                else:

                    Update_Mongo_Data(node='single',database=test_info['pre-update database']).delete_data(table=test_info['pre-update table'],query_params=eval(test_info['pre-query mongo']))

            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_get(method=header_method, url=check_sign_url, participantID=participantID,
                                                msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey)
            # 发送请求
            res = HttpRequest().send(url=url, method=method, headers=header)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_refund(result,test_info,head_params,body_params,traceID)
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node='single', database=test_info['pre-update database']).update_data_reset(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            else:
                Update_Mongo_Data(node='single', database=test_info['pre-update database']).delete_data_reset(
                    table=test_info['pre-update table'])
        else:
            body_params,head_params = self.common_params_init(test_info)
            res = self.post_refund(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.responce_check_refund(result,test_info,head_params,body_params,traceID)



    def post_refund(self,test_info,head_params,body_params,node='single'):
        yapi_operation = Exception_Yapi()
        update_yapi = yapi_operation.is_update_yapi(test_info)

        check_sign_url = head_params['url']
        if node == 'double':
            base_url = evopay_conf.base_url_mop
        else:
            base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']
        # 判断是否有数据进行替换
        data = multi_replace(str(body_params))


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
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)
        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
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
        #是否需要恢复yapi正常数据
        if update_yapi:
            yapi_operation.reset_yapi()
        return res

    def responce_check_refund(self,result,test_info,head_params,body_params,traceID,node='single'):
        #断言
        #获取测试案例中的期望
        expected=test_info['expected']
        #获取interface
        interface=test_info["interface"]
        result_evonetOrderNumber=''
        try:

            #断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"]=='S0000' and result["result"]["message"]=='Success.':
                if interface == 'MPM QR Verification':
                    Checkresponse().check_MPMQRVerification_res(interface, result)
                elif interface=='MPM Payment Authentication':
                    Checkresponse().check_MPMPaymentAuthentication_res(interface,result)
                elif interface=='CPM Token':
                    Checkresponse().check_CPMToken_res(interface,result)
                elif interface=='CPM Payment':
                    Checkresponse().check_CPMPayment_res(interface, result)
                elif interface=='Refund':
                    Checkresponse().check_refund_res(interface, result)
            #断言数据库
            try:
                #判断是否有数据库校验语句
                if test_info['check_mongo']:
                    #判断接口是refund
                    if interface=='Refund':
                        # 获取测试数据数据库的断言，替换数据
                        mongo_expected = multi_replace(str(test_info['check_mongo_expected']))
                        # 查询退款的交易
                        # refund交易需要替换的数据
                        result_evonetOrderNumber = result['evonetOrderNumber']
                        mongo_query_refund = str(eval(test_info["check_mongo"])["refund"]).replace(
                            "#evonetOrderNumber#", result_evonetOrderNumber)
                        # 检查数据库必填值得存入
                        # mongo_result_refund = db.get_one(table='trans', query_params=eval(mongo_query_refund))


                        mongo_result = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_refund))
                        mongo_result_refund_sgp = db_sgp_evopay.get_one(table='trans',query_params=eval(mongo_query_refund))
                        # 数据库查询出的traceID
                        traceID = mongo_result['traceID']
                        # 校验发送给parnter的数据
                        Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_refund(
                            mongo_query={"traceID": traceID}, participantID=head_params['wopParticipantID'], body=body_params)

                        Checkmongo().check_trans_mongo(test_data_interface="Refund", db_data=mongo_result)

                        mongo_result_refund = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_refund))

                        if 'failed' not in test_info['check_mongo_expected']:
                            # 校验tyo数据库成功的数据的某些字段
                            Checkmongo().check_trans_success(test_data_interface="Refund", db_data=mongo_result)
                            # 校验sgp数据库成功的数据的某些字段
                            if node=='double':
                                Checkmongo().check_trans_success(test_data_interface="Refund",
                                                                 db_data=mongo_result_refund_sgp)

                        else:
                            print('失败的交易不执行成功数据的检验')


                        if 'status' in mongo_expected:
                            # 校验数据库原交易的数据

                            # payment交易需要替换的数据
                            if 'payment_wop' not in mongo_expected:
                                mongo_query_payment = str(eval(test_info["check_mongo"])["payment"]).replace(
                                    "#originalEvonetOrderNumber#", getattr(case, 'originalEvonetOrderNumber'))
                                print(mongo_query_payment)
                                # 查询tyo数据库原交易payment的交易
                                mongo_result_payment_tyo = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_payment))
                                # 获取数据库数据
                                mongo_status_payment_tyo = mongo_result_payment_tyo['status']
                                mongo_wopStatus_payment_tyo = mongo_result_payment_tyo['wopStatus']
                                mongo_mopStatus_payment_tyo = mongo_result_payment_tyo['mopStatus']


                                # 获取测试数据（payment）数据库的断言
                                mongo_expected_payment = eval(test_info["check_mongo_expected"])["payment"]
                                print(mongo_expected_payment)

                                # 断言tyo数据库里payment的字段
                                assert mongo_expected_payment["status"] == mongo_status_payment_tyo
                                assert mongo_expected_payment["wopStatus"] == mongo_wopStatus_payment_tyo
                                assert mongo_expected_payment["mopStatus"] == mongo_mopStatus_payment_tyo

                                if node =='double':
                                    # 查询sgp数据库原交易payment的交易
                                    mongo_result_payment_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(
                                        mongo_query_payment))
                                    # 获取数据库数据
                                    mongo_status_payment_sgp = mongo_result_payment_sgp['status']
                                    mongo_wopStatus_payment_sgp = mongo_result_payment_sgp['wopStatus']
                                    mongo_mopStatus_payment_sgp = mongo_result_payment_sgp['mopStatus']
                                    # 断言sgp数据库里payment的字段
                                    assert mongo_expected_payment["status"] == mongo_status_payment_sgp
                                    assert mongo_expected_payment["wopStatus"] == mongo_wopStatus_payment_sgp
                                    assert mongo_expected_payment["mopStatus"] == mongo_mopStatus_payment_sgp

                            else:
                                mongo_query_payment = str(eval(test_info["check_mongo"])["payment"]).replace(
                                    "#originalEvonetOrderNumber#", getattr(case, 'originalEvonetOrderNumber'))
                                print(mongo_query_payment)
                                # 查询tyo数据库原交易payment的交易
                                mongo_result_payment_tyo = db_tyo_evopay.get_one(table='trans',
                                                                          query_params=eval(mongo_query_payment))
                                # 获取数据库数据
                                mongo_status_payment_tyo = mongo_result_payment_tyo['status']
                                mongo_wopStatus_payment_tyo = mongo_result_payment_tyo['wopStatus']
                                mongo_mopStatus_payment_tyo = mongo_result_payment_tyo['mopStatus']


                                # 获取测试数据（payment）wop数据库的断言
                                mongo_expected_payment_wop = eval(test_info["check_mongo_expected"])["payment_wop"]
                                print(mongo_expected_payment_wop)
                                # 获取测试数据（payment）mop数据库的断言
                                mongo_expected_payment_mop = eval(test_info["check_mongo_expected"])["payment_mop"]
                                print(mongo_expected_payment_mop)

                                # 断言tyo数据库里payment的字段
                                assert mongo_expected_payment_wop["status"] == mongo_status_payment_tyo
                                assert mongo_expected_payment_wop["wopStatus"] == mongo_wopStatus_payment_tyo
                                assert mongo_expected_payment_wop["mopStatus"] == mongo_mopStatus_payment_tyo

                                if node == 'double':
                                    # 查询sgp数据库原交易payment的交易
                                    mongo_result_payment_sgp = db_sgp_evopay.get_one(table='trans',
                                                                                     query_params=eval(
                                                                                         mongo_query_payment))
                                    # 获取数据库数据
                                    mongo_status_payment_sgp = mongo_result_payment_sgp['status']
                                    mongo_wopStatus_payment_sgp = mongo_result_payment_sgp['wopStatus']
                                    mongo_mopStatus_payment_sgp = mongo_result_payment_sgp['mopStatus']

                                    # 断言sgp数据库里payment的字段
                                    assert mongo_expected_payment_mop["status"] == mongo_status_payment_sgp
                                    assert mongo_expected_payment_mop["wopStatus"] == mongo_wopStatus_payment_sgp
                                    assert mongo_expected_payment_mop["mopStatus"] == mongo_mopStatus_payment_sgp

                            # 获取tyo数据库的数据
                            mongo_status_refund_tyo = mongo_result['status']
                            mongo_wopStatus_refund_tyo = mongo_result['wopStatus']
                            mongo_mopStatus_refund_tyo = mongo_result['mopStatus']
                            mongo_expected_refund = eval(test_info["check_mongo_expected"])["refund"]
                            # 断言tyo数据库里payment的字段
                            if mongo_expected_refund["wopStatus"] == 'succeeded':
                                if mongo_wopStatus_refund_tyo == 'processing':
                                    assert mongo_wopStatus_refund_tyo == 'processing'
                                else:
                                    assert mongo_wopStatus_refund_tyo == mongo_expected_refund['wopStatus']

                            else:
                                assert mongo_wopStatus_refund_tyo == mongo_expected_refund['wopStatus']
                            # 断言tyo数据库里refund的字段
                            assert mongo_expected_refund["status"] == mongo_status_refund_tyo
                            assert mongo_expected_refund['mopStatus'] == mongo_mopStatus_refund_tyo

                            if node == 'double':
                                # 获取sgp数据库的数据
                                mongo_status_refund_sgp = mongo_result_refund_sgp['status']
                                mongo_wopStatus_refund_sgp = mongo_result_refund_sgp['wopStatus']
                                mongo_mopStatus_refund_sgp = mongo_result_refund_sgp['mopStatus']
                                if mongo_expected_refund["wopStatus"] == 'succeeded':
                                    if mongo_wopStatus_refund_sgp == 'processing':
                                        assert mongo_wopStatus_refund_sgp == 'processing'
                                    else:
                                        assert mongo_wopStatus_refund_sgp == mongo_expected_refund[
                                            'wopStatus']

                                else:
                                    assert mongo_wopStatus_refund_sgp == mongo_expected_refund['wopStatus']
                                    # 获取测试数据数据库的断言
                                # 断言sgp数据库里refund的字段
                                assert mongo_expected_refund["status"] == mongo_status_refund_sgp
                                assert mongo_expected_refund['mopStatus'] == mongo_mopStatus_refund_sgp


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
                            mongo_result_mopsettledate = mongo_result_refund['mopSettleDate']
                            mongo_result_wopsettledate = mongo_result_refund['wopSettleDate']

                            # 断言清算日期
                            assert mongo_expected_mopsettledate == mongo_result_mopsettledate
                            assert mongo_expected_wopsettledate == mongo_result_wopsettledate
                            ###################################################
                            #连接tyo数据库
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
                            # 获取tyo数据库中的清算日期
                            mongo_result_mopsettledate_tyo = mongo_result['mopSettleDate']
                            mongo_result_wopsettledate_tyo = mongo_result['wopSettleDate']
                            # 断言tyo数据库清算日期
                            assert mongo_expected_mopsettledate == mongo_result_mopsettledate_tyo
                            assert mongo_expected_wopsettledate == mongo_result_wopsettledate_tyo

                            if node =='double':
                                # 获取sgp数据库中的清算日期
                                mongo_result_mopsettledate_sgp = mongo_result_refund_sgp['mopSettleDate']
                                mongo_result_wopsettledate_sgp = mongo_result_refund_sgp['wopSettleDate']
                                # 断言sgp数据库清算日期
                                assert mongo_expected_mopsettledate == mongo_result_mopsettledate_sgp
                                assert mongo_expected_wopsettledate == mongo_result_wopsettledate_sgp

                        elif 'mopSettleAmount' and 'wopSettleAmount' and 'billingAmount' in mongo_expected:
                            # 校验原交易
                            mongo_query_payment = str(eval(test_info["check_mongo"])["payment"]).replace(
                                "#originalEvonetOrderNumber#", getattr(case, 'originalEvonetOrderNumber'))
                            print(mongo_query_payment)
                            # 查询tyo数据库原交易payment的交易
                            mongo_result_payment_tyo = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_payment))
                            # 获取数据库数据
                            mongo_totalRefundTransAmount_payment_tyo = mongo_result_payment_tyo['totalRefundTransAmount']
                            mongo_totalRefundMOPAmount_payment_tyo = mongo_result_payment_tyo['totalRefundMOPAmount']
                            mongo_totalRefundWOPAmount_payment_tyo = mongo_result_payment_tyo['totalRefundWOPAmount']
                            # 获取测试数据（payment）数据库的断言
                            mongo_expected_payment = eval(test_info["check_mongo_expected"])["payment"]
                            print(mongo_expected_payment)

                            # 断言tyo数据库里payment的字段
                            assert mongo_expected_payment["totalRefundTransAmount"] == mongo_totalRefundTransAmount_payment_tyo
                            assert mongo_expected_payment["totalRefundMOPAmount"] == mongo_totalRefundMOPAmount_payment_tyo
                            assert mongo_expected_payment["totalRefundWOPAmount"] == mongo_totalRefundWOPAmount_payment_tyo

                            # 获取tyo数据库退款的数据
                            mongo_mopSettleCurrency_refund_tyo = mongo_result['mopSettleCurrency']
                            mongo_mopBaseSettleFXRate_refund_tyo = mongo_result['mopBaseSettleFXRate']
                            mongo_mopSettleFXRate_refund_tyo = mongo_result['mopSettleFXRate']
                            mongo_mopSettleSourceCurrency_refund_tyo = mongo_result['mopSettleSourceCurrency']
                            mongo_mopSettleDestinationCurrency_refund_tyo = mongo_result['mopSettleDestinationCurrency']
                            mongo_mccr_refund_tyo = mongo_result['mccr']
                            mongo_wopSettleAmount_refund_tyo = mongo_result['wopSettleAmount']
                            mongo_wopSettleCurrency_refund_tyo = mongo_result['wopSettleCurrency']
                            mongo_wopBaseSettleFXRate_refund_tyo = mongo_result['wopBaseSettleFXRate']
                            mongo_wopSettleFXRate_refund_tyo = mongo_result['wopSettleFXRate']
                            mongo_wopSettleSourceCurrency_refund_tyo = mongo_result['wopSettleSourceCurrency']
                            mongo_wopSettleDestinationCurrency_refund_tyo = mongo_result['wopSettleDestinationCurrency']
                            mongo_wccr_refund_tyo = mongo_result['wccr']
                            mongo_billingAmount_refund_tyo = mongo_result['billingAmount']
                            mongo_billingCurrency_refund_tyo = mongo_result['billingCurrency']
                            mongo_billingBaseFXRate_refund_tyo = mongo_result['billingBaseFXRate']
                            mongo_billingFXRate_refund_tyo = mongo_result['billingFXRate']
                            mongo_billingSourceCurrency_refund_tyo = mongo_result['billingSourceCurrency']
                            mongo_billingDestinationCurrency_refund_tyo = mongo_result['billingDestinationCurrency']
                            mongo_cccr_refund_tyo = mongo_result['cccr']
                            mongo_expected_refund = eval(test_info["check_mongo_expected"])["refund"]
                            if mongo_billingAmount_refund_tyo!= 0:
                                mongo_totalRefundBillingAmount_payment_tyo = mongo_result_payment_tyo['totalRefundBillingAmount']
                                assert mongo_expected_payment[
                                           "totalRefundBillingAmount"] == mongo_totalRefundBillingAmount_payment_tyo

                            # 断言tyo数据库里refund的字段
                            assert mongo_expected_refund["mopSettleCurrency"] == mongo_mopSettleCurrency_refund_tyo
                            assert mongo_expected_refund[
                                       'mopBaseSettleFXRate'] == mongo_mopBaseSettleFXRate_refund_tyo
                            assert mongo_expected_refund['mopSettleFXRate'] == mongo_mopSettleFXRate_refund_tyo
                            assert mongo_expected_refund[
                                       'mopSettleSourceCurrency'] == mongo_mopSettleSourceCurrency_refund_tyo
                            assert mongo_expected_refund[
                                       'mopSettleDestinationCurrency'] == mongo_mopSettleDestinationCurrency_refund_tyo
                            assert mongo_expected_refund['mccr'] == mongo_mccr_refund_tyo
                            assert mongo_expected_refund['wopSettleAmount'] == mongo_wopSettleAmount_refund_tyo
                            assert mongo_expected_refund['wopSettleCurrency'] == mongo_wopSettleCurrency_refund_tyo
                            assert mongo_expected_refund[
                                       'wopBaseSettleFXRate'] == mongo_wopBaseSettleFXRate_refund_tyo
                            assert mongo_expected_refund['wopSettleFXRate'] == mongo_wopSettleFXRate_refund_tyo
                            assert mongo_expected_refund[
                                       'wopSettleSourceCurrency'] == mongo_wopSettleSourceCurrency_refund_tyo
                            assert mongo_expected_refund[
                                       'wopSettleDestinationCurrency'] == mongo_wopSettleDestinationCurrency_refund_tyo
                            assert mongo_expected_refund['wccr'] == mongo_wccr_refund_tyo
                            assert mongo_expected_refund['billingAmount'] == mongo_billingAmount_refund_tyo
                            assert mongo_expected_refund['billingCurrency'] == mongo_billingCurrency_refund_tyo
                            assert mongo_expected_refund['billingBaseFXRate'] == mongo_billingBaseFXRate_refund_tyo
                            assert mongo_expected_refund['billingFXRate'] == mongo_billingFXRate_refund_tyo
                            assert mongo_expected_refund[
                                       'billingSourceCurrency'] == mongo_billingSourceCurrency_refund_tyo
                            assert mongo_expected_refund[
                                       'billingDestinationCurrency'] == mongo_billingDestinationCurrency_refund_tyo
                            assert mongo_expected_refund['cccr'] == mongo_cccr_refund_tyo
                            if node=='double':
                                # 查询sgp数据库原交易payment的交易
                                mongo_result_payment_sgp = db_sgp_evopay.get_one(table='trans',
                                                                                 query_params=eval(mongo_query_payment))
                                # 获取数据库数据
                                mongo_totalRefundTransAmount_payment_sgp = mongo_result_payment_sgp[
                                    'totalRefundTransAmount']
                                mongo_totalRefundMOPAmount_payment_sgp = mongo_result_payment_sgp[
                                    'totalRefundMOPAmount']
                                mongo_totalRefundWOPAmount_payment_sgp = mongo_result_payment_sgp[
                                    'totalRefundWOPAmount']
                                # 断言sgp数据库里payment的字段
                                assert mongo_expected_payment[
                                           "totalRefundTransAmount"] == mongo_totalRefundTransAmount_payment_sgp
                                assert mongo_expected_payment[
                                           "totalRefundMOPAmount"] == mongo_totalRefundMOPAmount_payment_sgp
                                assert mongo_expected_payment[
                                           "totalRefundWOPAmount"] == mongo_totalRefundWOPAmount_payment_sgp

                                # 获取sgp数据库退款的数据
                                mongo_mopSettleCurrency_refund_sgp = mongo_result_refund_sgp['mopSettleCurrency']
                                mongo_mopBaseSettleFXRate_refund_sgp = mongo_result_refund_sgp['mopBaseSettleFXRate']
                                mongo_mopSettleFXRate_refund_sgp = mongo_result_refund_sgp['mopSettleFXRate']
                                mongo_mopSettleSourceCurrency_refund_sgp = mongo_result_refund_sgp[
                                    'mopSettleSourceCurrency']
                                mongo_mopSettleDestinationCurrency_refund_sgp = mongo_result_refund_sgp[
                                    'mopSettleDestinationCurrency']
                                mongo_mccr_refund_sgp = mongo_result_refund_sgp['mccr']
                                mongo_wopSettleAmount_refund_sgp = mongo_result_refund_sgp['wopSettleAmount']
                                mongo_wopSettleCurrency_refund_sgp = mongo_result_refund_sgp['wopSettleCurrency']
                                mongo_wopBaseSettleFXRate_refund_sgp = mongo_result_refund_sgp['wopBaseSettleFXRate']
                                mongo_wopSettleFXRate_refund_sgp = mongo_result_refund_sgp['wopSettleFXRate']
                                mongo_wopSettleSourceCurrency_refund_sgp = mongo_result_refund_sgp[
                                    'wopSettleSourceCurrency']
                                mongo_wopSettleDestinationCurrency_refund_sgp = mongo_result_refund_sgp[
                                    'wopSettleDestinationCurrency']
                                mongo_wccr_refund_sgp = mongo_result_refund_sgp['wccr']
                                mongo_billingAmount_refund_sgp = mongo_result_refund_sgp['billingAmount']
                                mongo_billingCurrency_refund_sgp = mongo_result_refund_sgp['billingCurrency']
                                mongo_billingBaseFXRate_refund_sgp = mongo_result_refund_sgp['billingBaseFXRate']
                                mongo_billingFXRate_refund_sgp = mongo_result_refund_sgp['billingFXRate']
                                mongo_billingSourceCurrency_refund_sgp = mongo_result_refund_sgp[
                                    'billingSourceCurrency']
                                mongo_billingDestinationCurrency_refund_sgp = mongo_result_refund_sgp[
                                    'billingDestinationCurrency']
                                mongo_cccr_refund_sgp = mongo_result_refund_sgp['cccr']
                                if mongo_billingAmount_refund_sgp != 0:
                                    mongo_totalRefundBillingAmount_payment_sgp = mongo_result_payment_sgp['totalRefundBillingAmount']
                                    assert mongo_expected_payment["totalRefundBillingAmount"] == mongo_totalRefundBillingAmount_payment_sgp
                                    # 断言sgp数据库里refund的字段
                                assert mongo_expected_refund["mopSettleCurrency"] == mongo_mopSettleCurrency_refund_sgp
                                assert mongo_expected_refund[
                                           'mopBaseSettleFXRate'] == mongo_mopBaseSettleFXRate_refund_sgp
                                assert mongo_expected_refund['mopSettleFXRate'] == mongo_mopSettleFXRate_refund_sgp
                                assert mongo_expected_refund[
                                           'mopSettleSourceCurrency'] == mongo_mopSettleSourceCurrency_refund_sgp
                                assert mongo_expected_refund[
                                           'mopSettleDestinationCurrency'] == mongo_mopSettleDestinationCurrency_refund_sgp
                                assert mongo_expected_refund['mccr'] == mongo_mccr_refund_sgp
                                assert mongo_expected_refund['wopSettleAmount'] == mongo_wopSettleAmount_refund_sgp
                                assert mongo_expected_refund['wopSettleCurrency'] == mongo_wopSettleCurrency_refund_sgp
                                assert mongo_expected_refund[
                                           'wopBaseSettleFXRate'] == mongo_wopBaseSettleFXRate_refund_sgp
                                assert mongo_expected_refund['wopSettleFXRate'] == mongo_wopSettleFXRate_refund_sgp
                                assert mongo_expected_refund[
                                           'wopSettleSourceCurrency'] == mongo_wopSettleSourceCurrency_refund_sgp
                                assert mongo_expected_refund[
                                           'wopSettleDestinationCurrency'] == mongo_wopSettleDestinationCurrency_refund_sgp
                                assert mongo_expected_refund['wccr'] == mongo_wccr_refund_sgp
                                assert mongo_expected_refund['billingAmount'] == mongo_billingAmount_refund_sgp
                                assert mongo_expected_refund['billingCurrency'] == mongo_billingCurrency_refund_sgp
                                assert mongo_expected_refund['billingBaseFXRate'] == mongo_billingBaseFXRate_refund_sgp
                                assert mongo_expected_refund['billingFXRate'] == mongo_billingFXRate_refund_sgp
                                assert mongo_expected_refund[
                                           'billingSourceCurrency'] == mongo_billingSourceCurrency_refund_sgp
                                assert mongo_expected_refund[
                                           'billingDestinationCurrency'] == mongo_billingDestinationCurrency_refund_sgp
                                assert mongo_expected_refund['cccr'] == mongo_cccr_refund_sgp

                else:
                    print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"], traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"],traceID))

        except AssertionError as e:
            if test_info["interface"]=='MPM QR Verification':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'MPM Payment Authentication':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'Payment Notification':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif  test_info["interface"] == 'CPM Token':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            elif test_info["interface"] == 'CPM Payment':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))
            else:

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"],
                                                       traceID))

            raise e

        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"],traceID))

