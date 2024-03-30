import pytest
from loguru import logger as log
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evoconfig, db_tyo_evologs, db_sgp_evopay,db_sgp_evologs
from common.evopay.reponse_check import Checkresponse
from common.evopay.mongo_restore_billing_settle_rate import mongo_restore_billing_settle_rate
from common.evopay.read_data import EvopayTestCase
from base.read_file_path import ReadFile
from common.evopay.moudle import Moudle
from common.evopay.check_sign import CheckSign
from base.read_config import Conf
from base.http_request import HttpRequest
from base.db import MongoDB
from base.encrypt import Encrypt
from common.evopay.read_csv import ReadCSV
from common.evopay.replace_data import multi_replace,case
from common.evopay.mongo_data_check import Checkmongo
from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.common_functions.cpm.cpm_token import CPM_Token_Message
from common.evopay.common_functions.cpm.cpm_payment import CPM_Payment_Message
from common.evopay.Initialization import initialization
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from base.amount_check import amount_check, get_config_currency
from common.evopay.exception_operation_yapi import Exception_Yapi
import time
data_file=ReadFile().read_data_file("evopay_evonet_cpmpayment","QR_single_node_mode","evopay")
cpmpayment_testdata=ReadCSV(data_file).read_data()

class Testcpmpayment():
    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize('test_info',cpmpayment_testdata)
    def test_cpmpayment(self,test_info):
        #判断接口是否是CPM Payment，不是CPM Payment
        if test_info["interface"]!='CPM Payment':
            body_params,head_params=self.common_params_init(test_info)
            # 获取URL
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
        else:
            body_params,head_params = self.common_params_init(test_info)
            res,config_currency = self.post_cpmpayment(test_info, head_params,body_params)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            self.check_resopnse_cpmpayment(result,test_info,head_params,body_params,traceID,config_currency)

    def post_cpmpayment(self,test_info,head_params,body_params,node='single'):
        check_sign_url = head_params['url']
        if node=='single':
            base_url = evopay_conf.base_url_wop
        else:
            base_url = evopay_conf.base_url_mop
        url = base_url + check_sign_url
        # 获取method
        method = head_params['method']
        # 判断是否有数据进行替换,获取body
        data = multi_replace(str(body_params))
        if not test_info['pre-update database']:
            test_info['pre-update database'] = 'tyo'
        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()
        participantID = head_params['mopParticipantID']
        if test_info['pre-update table']:
            if test_info['pre-update table'] == 'tokenVault':
                test_info['pre-query mongo'] = multi_replace(test_info['pre-query mongo'])
                Update_Mongo_Data(node=node, database=test_info['pre-update database'],database_name='evopay').updata_data(
                    table=test_info['pre-update table'],query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))

            elif test_info['pre-update mongo'] and "transCurrencies.0.mccr" not in test_info['pre-update mongo']:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).updata_data(
                    table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            elif "transCurrencies.0.mccr" in test_info['pre-update mongo']:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).unset_many_data(
                    table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            else:

                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data(
                    table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']))

        # self,method,url,participantID,msgID,datetime,signkey,data
        header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)
        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
        result = res.json()
        headers = res.headers
        traceID = headers['Traceid']
        setattr(case, 'traceID', traceID)

        # result_evonetOrderNumber = result["evonetOrderNumber"]
        # setattr(case, 'evonetOrderNumber', result_evonetOrderNumber)
        if "billingCurrency" in test_info["check_mongo_expected"]:
            config_currency = get_config_currency(head_params)
            config_currency = config_currency.get()
        else:
            config_currency = None

        if test_info['pre-update table']:
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).update_data_reset(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))

            else:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data_reset(
                    table=test_info['pre-update table'])
        if result["result"]["code"] == 'S0000':
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)

        if test_info['update_mongo']:
            # 获取查询语句
            mongo_query = test_info["check_mongo"].replace("#evonetOrderNumber#", evonetOrderNumber)
            # 更新数据库语句
            db_tyo_evopay.update_one(table='trans', query_params=eval(mongo_query),
                                     updata_params=eval(test_info['update_mongo']))
            if node == 'double':
                # 获取查询语句
                mongo_query = test_info["check_mongo"].replace("#evonetOrderNumber#", evonetOrderNumber)
                # 更新数据库语句
                db_sgp_evopay.update_one(table='trans', query_params=eval(mongo_query),
                                         updata_params=eval(test_info['update_mongo']))
        return res,config_currency

    def common_params_init(self,test_info,node='single'):
        if test_info["interface"] == 'CPM Token':
            common_params = CPM_Token_Message()
            if node=='single':
                common_params_Conf = common_params.CPM_Token_Conf
                common_params_body = common_params.CPM_Token_Body
            else:
                common_params_Conf = common_params.CPM_Token_Conf_double
                common_params_body = common_params.CPM_Token_Body_double
        else :
            common_params = CPM_Payment_Message()
            if node == 'single':
                common_params_Conf = common_params.CPM_Payment_Conf
                common_params_body = common_params.CPM_Payment_Body
            else:
                common_params_Conf = common_params.CPM_Payment_Conf_double
                common_params_body = common_params.CPM_Payment_Body_double
        init = initialization(common_params_Conf, common_params_body)
        body_params = init.init_body(test_info['data'])
        head_params = init.ini_conf(test_info['conf'])
        # 兼容之前用例wopID,mopID。wopID,mopID优先级高于conf中wopID，mopID
        if test_info["wopParticipantID"]:
            head_params["wopParticipantID"] = test_info["wopParticipantID"]
        if test_info["mopParticipantID"]:
            head_params["mopParticipantID"] = test_info["mopParticipantID"]
        return body_params,head_params

    def check_resopnse_cpmpayment(self,result,test_info,head_params,body_params,traceID,config_currency,node='single'):
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

            if result["result"]["code"]=='S0000' and  result["result"]["message"]=='Success.':
                if interface=='CPM Token':
                    Checkresponse().check_CPMToken_res(interface,result)
                elif interface=='CPM Payment':
                    Checkresponse().check_CPMPayment_res(interface, result)
            try:
                #断言数据库和发送给parnter的数据
                if test_info['check_mongo']:
                    if interface == 'CPM Payment':
                        # result_evonetOrderNumber=result["evonetOrderNumber"]
                        # mongo_query = test_info["check_mongo"].replace("#evonetOrderNumber#", result_evonetOrderNumber)
                        mongo_query = multi_replace(str(test_info['check_mongo']))
                        # 检查数据库必填值得存入
                        mongo_result = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))
                        Checkmongo().check_trans_mongo(test_data_interface="CPM Payment", db_data=mongo_result)
                        # 数据库查询出的traceID
                        traceID = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query))['traceID']

                        #校验成功的数据的某些字段
                        if result["result"]["code"] == 'S0000' and result["result"]["message"] == 'Success.':
                            Checkmongo().check_trans_success(test_data_interface="CPM Payment",db_data=mongo_result)
                        # 校验发送给parnter的数据
                        participantID = head_params['mopParticipantID']
                        Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_CPMPayment(
                            mongo_query={"traceID": traceID}, participantID=participantID, body=body_params)

                        # 校验测试用例的预期，比如billingAount,settleAmount,mccr,cccr,status,wopID,settDate等值
                        if ('mopSettleCurrency' in test_info['check_mongo_expected'])and('wopSettleCurrency' in test_info['check_mongo_expected']):
                            amountcheck = amount_check()
                            amountcheck.get(eval(test_info['check_mongo_expected']), head_params, config_currency)
                            amount = amountcheck.case_caculate()
                            amount.update(eval(test_info['check_mongo_expected']))
                            test_info['check_mongo_expected'] = str(amount)
                        single = mongo_restore_billing_settle_rate()
                        single.billing_settle_rate(mongo_result,test_info,head_params,body_params,traceID,node='single')


                    if node=='double':
                        mongo_query = multi_replace(str(test_info['check_mongo']))

                        mongo_result_sgp = db_sgp_evopay.get_one(table='trans', query_params=eval(mongo_query))
                        Checkmongo().check_trans_mongo(test_data_interface="CPM Payment", db_data=mongo_result_sgp)

                        # 校验发送给parnter的数据
                        participantID = test_info['mopParticipantID']
                        Check_evonet_to_partner(db_sgp_evologs).check_evonet_to_partner_CPMPayment(
                            mongo_query=eval(mongo_query), participantID=participantID, body=body_params)

                        # 校验测试用例的预期，比如billingAount,settleAmount,mccr,cccr,status,wopID,settDate等值
                        if ('mopSettleCurrency' in test_info['check_mongo_expected'])and('wopSettleCurrency' in test_info['check_mongo_expected']):
                            amountcheck = amount_check()
                            amountcheck.get(eval(test_info['check_mongo_expected']), head_params, config_currency)
                            amount = amountcheck.case_caculate()
                            amount.update(eval(test_info['check_mongo_expected']))
                            test_info['check_mongo_expected'] = str(amount)
                        double = mongo_restore_billing_settle_rate()
                        double.billing_settle_rate(mongo_result_sgp, test_info, head_params, body_params, traceID,
                                                   node='double')
                else:
                    print("无数据库检验")
            except AssertionError as e:
                log.debug(f'用例执行未通过,请求参数为{body_params}')
                print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"],traceID))
                raise e
            else:
                print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"],traceID))
        except AssertionError as e:
            if test_info["interface"] == 'CPM Token':
                log.debug(f'用例执行未通过,请求参数为{body_params}')
                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"], traceID))

            else:
                log.debug(f'用例执行未通过,请求参数为{body_params}')
                print("用例：{}--执行未通过,traceID为{}".format(test_info["title"], traceID))
            raise e
        else:
            print("用例：{}---执行通过,traceID为{}".format(test_info["title"], traceID))














