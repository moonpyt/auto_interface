import pytest

from base.amount_check import amount_check, get_config_currency
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_sgp_evopay, db_sgp_evologs,db_tyo_evologs
from common.evopay.mongo_restore_billing_settle_rate import mongo_restore_billing_settle_rate
from common.evopay.reponse_check import Checkresponse
from loguru import logger as log
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
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from common.evopay.common_functions.mpm.mpmpaymentauthentication import MPMpaymentauthentication
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.Initialization import initialization

data_file=ReadFile().read_data_file("evopay_evonet_mpmpaymentauthentication","QR_single_node_mode","evopay")
mpmpaymentauthentication_testdata=ReadCSV(data_file).read_data()


class Testmpmpayment():

    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize('test_info',mpmpaymentauthentication_testdata)
    def test_mpmpayment(self,test_info):
        #判断接口是否是MPM Payment Authentication，不是MPM Payment Authentication
        if test_info["interface"]!='MPM Payment':
            body_params,head_params=self.common_params_init(test_info)
            res = Testmpmqrverification(self.envirs).post_mpmqrverification(test_info,head_params,body_params)
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] ==result["result"]["message"]
            #获取接口返回的evonetReference
            evonetReference=result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)

        #MPM_Payment_Authentication接口
        else:
            body_params,head_params=self.common_params_init(test_info)
            res,config_currency = self.post_mpmpayment(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.check_resopnse_mpmpayment(result,test_info,head_params,body_params,traceID,config_currency)


    def common_params_init(self,test_info,node='single'):
        if test_info["interface"]!='MPM Payment':
            common_params = MPMqrverify()
            if node=='single':
                common_params_Conf = common_params.MPMqrverify_Conf
                common_params_body = common_params.MPMqrverify_Body
            else:
                common_params_Conf = common_params.MPMqrverify_Conf_double
                common_params_body = common_params.MPMqrverify_Body_double

        else:
            common_params = MPMpaymentauthentication()
            if node == 'single':
                common_params_Conf = common_params.MPMpayment_Conf
                common_params_body = common_params.MPMpayment_Body
            else:
                common_params_Conf = common_params.MPMpayment_Conf_double
                common_params_body = common_params.MPMpayment_Body_double

        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        #兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params

    def post_mpmpayment(self,test_info,conf_params,body_params,node='single'):
        check_sign_url = conf_params['url']
        base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = conf_params['method']
        # 判断是否有数据进行替换,获取body
        data = multi_replace(str(body_params))

        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()
        # 获取participantID，替换数据
        participantID = conf_params['wopParticipantID']
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
        header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)

        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
        result = res.json()
        headers = res.headers
        if "billingCurrency" in test_info["check_mongo_expected"]:
            config_currency = get_config_currency(conf_params)
            config_currency = config_currency.get()
        else:
            config_currency = None
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

        return res,config_currency

    def check_resopnse_mpmpayment(self,result,test_info,head_params,body_params,traceID,config_currency,node='single'):
        # 断言
        # 获取测试案例中的期望
        expected = test_info['expected']
        # 获取interface
        interface = test_info["interface"]
        result_evonetOrderNumber = ''
        try:
            # 断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"] == 'S0000' and result["result"]["message"] == 'Success.':
                if interface == 'MPM QR Verification':
                    Checkresponse().check_MPMQRVerification_res(interface, result)
                elif interface == 'MPM Payment Authentication':
                    Checkresponse().check_MPMPayment_res(interface, result)

            # 断言数据库
            try:
                # 判断是否有数据库校验语句
                if test_info['check_mongo']:
                    # 判断接口是MPM Payment Authentication
                    if interface == 'MPM Payment':
                        result_evonetOrderNumber = result["evonetOrderNumber"]
                        mongo_expected = multi_replace(str(test_info['check_mongo_expected']))
                        mongo_query = str(test_info["check_mongo"]).replace("#evonetOrderNumber#",
                                                                            result_evonetOrderNumber)
                        # 数据库查询出的traceID
                        traceID = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))['traceID']
                        # 校验发送给parnter的数据
                        Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_MPMPaymentAuthentication(
                            mongo_query={"traceID": traceID}, participantID=head_params['wopParticipantID'], body=body_params)


                        #检查tyo数据库必填值得存入
                        mongo_result_tyo = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))
                        Checkmongo().check_trans_mongo(test_data_interface="MPM Payment", db_data=mongo_result_tyo)
                        # 校验成功的数据的某些字段
                        Checkmongo().check_trans_success(test_data_interface="MPM Payment", db_data=mongo_result_tyo)

                        if ('mopSettleCurrency' in test_info['check_mongo_expected']) and (
                                'wopSettleCurrency' in test_info['check_mongo_expected']):
                            amountcheck = amount_check()
                            amountcheck.get(eval(test_info['check_mongo_expected']), head_params,
                                         config_currency)
                            amount = amountcheck.case_caculate()
                            amount.update(eval(test_info['check_mongo_expected']))
                            test_info['check_mongo_expected'] = str(amount)
                        single = mongo_restore_billing_settle_rate()
                        single.billing_settle_rate(mongo_result_tyo, test_info, head_params, body_params, traceID,
                                                   node='single')
                        if node == 'double':
                            mongo_result_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query))
                            Checkmongo().check_trans_mongo(test_data_interface="MPM Payment",
                                                           db_data=mongo_result_sgp)
                            # 检查tyo数据库必填值得存入
                            Checkmongo().check_trans_mongo(test_data_interface="MPM Payment", db_data=mongo_result_sgp)
                            # 校验成功的数据的某些字段
                            Checkmongo().check_trans_success(test_data_interface="MPM Payment",
                                                             db_data=mongo_result_sgp)

                            # 校验发送给parnter的数据
                            Check_evonet_to_partner(db_sgp_evologs).check_evonet_to_partner_MPMPaymentAuthentication(
                                mongo_query={"traceID": traceID}, participantID=head_params['wopParticipantID'],
                                body=body_params)

                            # 校验测试用例的预期，比如billingAount,settleAmount,mccr,cccr,status,wopID,settDate等值
                            if ('mopSettleCurrency' in test_info['check_mongo_expected']) and (
                                    'wopSettleCurrency' in test_info['check_mongo_expected']):
                                amountcheck = amount_check()
                                amountcheck.get(eval(test_info['check_mongo_expected']), head_params,
                                                           config_currency)
                                amount = amountcheck.case_caculate()
                                amount.update(eval(test_info['check_mongo_expected']))
                                test_info['check_mongo_expected'] = str(amount)
                            double = mongo_restore_billing_settle_rate()
                            double.billing_settle_rate(mongo_result_sgp, test_info, head_params, body_params, traceID,
                                                       node='double')


                        # #检查sgp数据库
                        # # 检查sgp数据库必填值得存入
                        # if node=='double':
                        #     mongo_result_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query))
                        #     Checkmongo().check_trans_mongo(test_data_interface="MPM Payment",
                        #                                    db_data=mongo_result_sgp)
                        # if 'wopID' in mongo_expected:
                        #     if node == 'double':
                        #         mongo_wop_sgp = mongo_result_sgp['wopID']
                        #         mongo_mop_sgp = mongo_result_sgp['mopID']
                        #         assert eval(mongo_expected)["wopID"] == mongo_wop_sgp
                        #         assert eval(mongo_expected)["mopID"] == mongo_mop_sgp
                        #
                        #     mongo_wop_tyo = mongo_result_tyo['wopID']
                        #     mongo_mop_tyo = mongo_result_tyo['mopID']
                        #     assert eval(mongo_expected)["wopID"] == mongo_wop_tyo
                        #     assert eval(mongo_expected)["mopID"] == mongo_mop_tyo
                        #
                        # elif 'status' in mongo_expected:
                        #     if node == 'double':
                        #         mongo_status_sgp = mongo_result_sgp['status']
                        #         assert eval(mongo_expected)["status"] == mongo_status_sgp
                        #     mongo_status_tyo = mongo_result_tyo['status']
                        #     assert eval(mongo_expected)["status"] == mongo_status_tyo
                        #
                        #
                        # elif 'mopConverterCurrencyFlag' in mongo_expected:
                        #     if node == 'double':
                        #         mongo_mopConverterCurrencyFlag_sgp = mongo_result_sgp['mopConverterCurrencyFlag']
                        #         assert eval(mongo_expected)[
                        #                    'mopConverterCurrencyFlag'] == mongo_mopConverterCurrencyFlag_sgp
                        #     mongo_mopConverterCurrencyFlag_tyo = mongo_result_tyo['mopConverterCurrencyFlag']
                        #     mongo_wopConverterCurrencyFlag_tyo = mongo_result_tyo['wopConverterCurrencyFlag']
                        #     assert eval(mongo_expected)[
                        #                'mopConverterCurrencyFlag'] == mongo_mopConverterCurrencyFlag_tyo
                        #     assert eval(mongo_expected)[
                        #                'wopConverterCurrencyFlag'] == mongo_wopConverterCurrencyFlag_tyo
                        #
                        #
                        #
                        # elif 'mopSettleAmount' and 'wopSettleAmount' and 'billingAmount' in mongo_expected:
                        #     mopSettleAmount_tyo = mongo_result_tyo['mopSettleAmount']
                        #     mopSettleCurrency_tyo = mongo_result_tyo['mopSettleCurrency']
                        #     wopSettleAmount_tyo = mongo_result_tyo['wopSettleAmount']
                        #     wopSettleCurrency_tyo = mongo_result_tyo['wopSettleCurrency']
                        #     billingAmount_tyo = mongo_result_tyo['billingAmount']
                        #     billingCurrency_tyo = mongo_result_tyo['billingCurrency']
                        #     assert eval(mongo_expected)['mopSettleAmount'] == mopSettleAmount_tyo
                        #     assert eval(mongo_expected)['mopSettleCurrency'] == mopSettleCurrency_tyo
                        #     assert eval(mongo_expected)['wopSettleAmount'] == wopSettleAmount_tyo
                        #     assert eval(mongo_expected)['wopSettleCurrency'] == wopSettleCurrency_tyo
                        #     assert eval(mongo_expected)['billingAmount'] == billingAmount_tyo
                        #     assert eval(mongo_expected)['billingCurrency'] == billingCurrency_tyo
                        #     if mongo_result_tyo['mopConverterCurrencyFlag'] == True:
                        #         mopBaseSettleFXRate_tyo = mongo_result_tyo['mopBaseSettleFXRate']
                        #         mopSettleFXRate_tyo = mongo_result_tyo['mopSettleFXRate']
                        #         mopSettleSourceCurrency_tyo = mongo_result_tyo['mopSettleSourceCurrency']
                        #         mopSettleDestinationCurrency_tyo = mongo_result_tyo['mopSettleDestinationCurrency']
                        #         mccr_tyo = mongo_result_tyo['mccr']
                        #         assert eval(mongo_expected)['mopBaseSettleFXRate'] == mopBaseSettleFXRate_tyo
                        #         assert eval(mongo_expected)['mopSettleFXRate'] == mopSettleFXRate_tyo
                        #         assert eval(mongo_expected)['mopSettleSourceCurrency'] == mopSettleSourceCurrency_tyo
                        #         assert eval(mongo_expected)[
                        #                    'mopSettleDestinationCurrency'] == mopSettleDestinationCurrency_tyo
                        #         assert eval(mongo_expected)['mccr'] == mccr_tyo
                        #
                        #     if mongo_result_tyo['wopConverterCurrencyFlag'] == True:
                        #         wopBaseSettleFXRate_tyo = mongo_result_tyo['wopBaseSettleFXRate']
                        #         wopSettleFXRate_tyo = mongo_result_tyo['wopSettleFXRate']
                        #         wopSettleSourceCurrency_tyo = mongo_result_tyo['wopSettleSourceCurrency']
                        #         wopSettleDestinationCurrency_tyo = mongo_result_tyo['wopSettleDestinationCurrency']
                        #         wccr_tyo = mongo_result_tyo['wccr']
                        #         assert eval(mongo_expected)['wopBaseSettleFXRate'] == wopBaseSettleFXRate_tyo
                        #         assert eval(mongo_expected)['wopSettleFXRate'] == wopSettleFXRate_tyo
                        #         assert eval(mongo_expected)['wopSettleSourceCurrency'] == wopSettleSourceCurrency_tyo
                        #         assert eval(mongo_expected)[
                        #                    'wopSettleDestinationCurrency'] == wopSettleDestinationCurrency_tyo
                        #         assert eval(mongo_expected)['wccr'] == wccr_tyo
                        #
                        #     if mongo_result_tyo['billingConverterCurrencyFlag'] == True:
                        #         billingBaseFXRate_tyo = mongo_result_tyo['billingBaseFXRate']
                        #         billingFXRate_tyo = mongo_result_tyo['billingFXRate']
                        #         billingSourceCurrency_tyo = mongo_result_tyo['billingSourceCurrency']
                        #         billingDestinationCurrency_tyo = mongo_result_tyo['billingDestinationCurrency']
                        #         cccr_tyo = mongo_result_tyo['cccr']
                        #         assert eval(mongo_expected)['billingBaseFXRate'] == billingBaseFXRate_tyo
                        #         assert eval(mongo_expected)['billingFXRate'] == billingFXRate_tyo
                        #         assert eval(mongo_expected)['billingSourceCurrency'] == billingSourceCurrency_tyo
                        #         assert eval(mongo_expected)[
                        #                    'billingDestinationCurrency'] == billingDestinationCurrency_tyo
                        #         assert eval(mongo_expected)['cccr'] == cccr_tyo
                        #     if node == 'double':
                        #         if mongo_result_sgp['mopConverterCurrencyFlag'] == True:
                        #             mopBaseSettleFXRate_sgp = mongo_result_sgp['mopBaseSettleFXRate']
                        #             mopSettleFXRate_sgp = mongo_result_sgp['mopSettleFXRate']
                        #             mopSettleSourceCurrency_sgp = mongo_result_sgp['mopSettleSourceCurrency']
                        #             mopSettleDestinationCurrency_sgp = mongo_result_sgp['mopSettleDestinationCurrency']
                        #             mccr_sgp = mongo_result_sgp['mccr']
                        #             assert eval(mongo_expected)['mopBaseSettleFXRate'] == mopBaseSettleFXRate_sgp
                        #             assert eval(mongo_expected)['mopSettleFXRate'] == mopSettleFXRate_sgp
                        #             assert eval(mongo_expected)['mopSettleSourceCurrency'] == mopSettleSourceCurrency_sgp
                        #             assert eval(mongo_expected)[
                        #                        'mopSettleDestinationCurrency'] == mopSettleDestinationCurrency_sgp
                        #             assert eval(mongo_expected)['mccr'] == mccr_sgp
                        #         mopSettleAmount_sgp = mongo_result_sgp['mopSettleAmount']
                        #         mopSettleCurrency_sgp = mongo_result_sgp['mopSettleCurrency']
                        #         assert eval(mongo_expected)['mopSettleAmount'] == mopSettleAmount_sgp
                        #         assert eval(mongo_expected)['mopSettleCurrency'] == mopSettleCurrency_sgp
                    print("无数据库检验")
            except AssertionError as e:
                print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"], traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"], traceID))

        except AssertionError as e:

            if test_info["interface"] == 'MPM QR Verification':

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"], traceID))
            else:

                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"], traceID))
            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"], traceID))
