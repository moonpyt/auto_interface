import pytest

from base.amount_check import amount_check, get_config_currency
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evologs,db_sgp_evopay,db_sgp_evologs
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
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from common.evopay.common_functions.mpm.mpmpaymentauthentication import MPMpaymentauthentication
from common.evopay.common_functions.mpm.mpmqrverify import MPMqrverify
from common.evopay.Initialization import initialization
from common.evopay.mongo_restore_billing_settle_rate import mongo_restore_billing_settle_rate
data_file=ReadFile().read_data_file("evopay_evonet_mpmpaymentauthentication","QR_single_node_mode","evopay")
mpmpaymentauthentication_testdata=ReadCSV(data_file).read_data()
class Testmpmpaymentauthentication():

    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize('test_info',mpmpaymentauthentication_testdata)
    def test_mpmpaymentauthentication(self,test_info):
        #判断接口是否是MPM Payment Authentication，不是MPM Payment Authentication
        if test_info["interface"]!='MPM Payment Authentication':
            body_params,head_params = self.common_params_init(test_info,node='single')
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
            body_params,head_params = self.common_params_init(test_info,node='single')
            res,config_currency  = self.post_mpmauthentication(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.check_resopnse_mpmauthentication(result,test_info,body_params,head_params,traceID,config_currency)


    def common_params_init(self,test_info,node='single'):
        if test_info["interface"]!='MPM Payment Authentication':
            if node=='double':
                common_params = MPMqrverify()
                common_params_Conf = common_params.MPMqrverify_Conf_double
                common_params_body = common_params.MPMqrverify_Body_double

            else:

                common_params = MPMqrverify()
                common_params_Conf = common_params.MPMqrverify_Conf
                common_params_body = common_params.MPMqrverify_Body
        else:
            if node == 'double':
                common_params = MPMpaymentauthentication()
                common_params_Conf = common_params.MPMpaymentauthentication_Conf_double
                common_params_body = common_params.MPMpaymentauthentication_Body_double
            else:
                common_params = MPMpaymentauthentication()
                common_params_Conf = common_params.MPMpaymentauthentication_Conf
                common_params_body = common_params.MPMpaymentauthentication_Body
        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        #兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params

    def post_mpmauthentication(self,test_info,conf_params,body_params,node='single'):
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

        if result['result']['code'] == "S0000":
            evonetOrderNumber = result['evonetOrderNumber']

        if "billingCurrency" in test_info["check_mongo_expected"]:
            config_currency = get_config_currency(conf_params)
            config_currency = config_currency.get()
        else:
            config_currency = None

        if test_info['update_mongo']:
            # 获取查询语句
            mongo_query = test_info["check_mongo"].replace("#evonetOrderNumber#", evonetOrderNumber)
            # 更新数据库语句
            db_tyo_evopay.update_one(table='trans', query_params=eval(mongo_query),
                                     updata_params=eval(test_info['update_mongo']))
            if node == 'double':
                db_sgp_evopay.update_one(table='trans', query_params=eval(mongo_query),
                                         updata_params=eval(test_info['update_mongo']))
        return res,config_currency

    def check_resopnse_mpmauthentication(self,result,test_info,body_params,head_params,traceID,config_currency,node='single'):
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
                    Checkresponse().check_MPMPaymentAuthentication_res(interface, result)

            # 断言数据库
            try:
                # 判断是否有数据库校验语句
                if test_info['check_mongo']:
                    # 判断接口是MPM Payment Authentication
                    if interface == 'MPM Payment Authentication':
                        result_evonetOrderNumber = result["evonetOrderNumber"]
                        mongo_query = str(test_info["check_mongo"]).replace("#evonetOrderNumber#",
                                                                            result_evonetOrderNumber)
                        # 数据库查询出的traceID
                        traceID = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))['traceID']
                        # 校验发送给parnter的数据
                        Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_MPMPaymentAuthentication(
                            mongo_query={"traceID": traceID}, participantID=head_params['wopParticipantID'], body=body_params)
                        # 检查数据库必填值得存入
                        mongo_result = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))
                        Checkmongo().check_trans_mongo(test_data_interface="MPM Payment Authentication",
                                                       db_data=mongo_result)
                        # 校验成功的数据的某些字段
                        Checkmongo().check_trans_success(test_data_interface="MPM Payment Authentication",
                                                         db_data=mongo_result)
                        # 校验测试用例的预期，比如billingAount,settleAmount,mccr,cccr,status,wopID,settDate等值
                        if ('mopSettleCurrency' in test_info['check_mongo_expected']) and (
                                'wopSettleCurrency' in test_info['check_mongo_expected']):
                            amountcheck = amount_check()
                            amountcheck.get(eval(test_info['check_mongo_expected']), head_params,
                                                       config_currency)
                            amount = amountcheck.case_caculate()
                            amount.update(eval(test_info['check_mongo_expected']))
                            test_info['check_mongo_expected'] = str(amount)
                        single_check_authntication = mongo_restore_billing_settle_rate()
                        single_check_authntication.billing_settle_rate(mongo_result,test_info,head_params,body_params,traceID,node='single')

                        if node=='double':
                            # 检查sgp数据库必填值得存入
                            mongo_result_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query))
                            Checkmongo().check_trans_mongo(test_data_interface="MPM Payment Authentication",
                                                           db_data=mongo_result_sgp)
                            # 校验测试用例的预期，比如billingAount,settleAmount,mccr,cccr,status,wopID,settDate等值
                            if ('mopSettleCurrency' in test_info['check_mongo_expected']) and (
                                    'wopSettleCurrency' in test_info['check_mongo_expected']):
                                amountcheck = amount_check()
                                amountcheck.get(eval(test_info['check_mongo_expected']), head_params,
                                                           config_currency)
                                amount = amountcheck.case_caculate()
                                amount.update(eval(test_info['check_mongo_expected']))
                                test_info['check_mongo_expected'] = str(amount)
                            #校验测试用例的预期，比如billingAount,settleAmount,mccr,cccr,status,wopID,settDate等值
                            double_check_authntication = mongo_restore_billing_settle_rate()
                            double_check_authntication.billing_settle_rate(mongo_result_sgp, test_info, head_params,
                                                                           body_params, traceID, node='double')


                else:
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











