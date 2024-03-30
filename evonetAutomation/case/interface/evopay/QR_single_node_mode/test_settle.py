import pytest

from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evologs
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
data_file=ReadFile().read_data_file("evopay_evonet_settle","QR_single_node_mode","evopay")
settle_testdata=ReadCSV(data_file).read_data()
class Testsettle():
    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',settle_testdata)
    def test_settle(self,test_info):


        #判断接口是MPM_QR_Verification
        if test_info["interface"]=='MPM QR Verification':
        #获取URL
            check_sign_url = test_info['url']
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = test_info['method']
            # 判断是否有数据进行替换,获取body
            data = multi_replace(str(test_info['data']))

            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()
            # 获取participantID
            participantID = test_info['wopParticipantID']

            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                                 msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)

            # 发送请求
            res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
            result = res.json()
            headers = res.headers
            traceID = headers['Traceid']
            print(result)
            #获取接口返回的evonetReference
            evonetReference=result['evonetReference']
            print(evonetReference)
            setattr(case, 'evonetReference', evonetReference)


        #MPM_Payment_Authentication接口
        elif test_info["interface"] == 'MPM Payment Authentication':
            check_sign_url = test_info['url']
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = test_info['method']
            # 判断是否有数据进行替换,获取body
            data = multi_replace(str(test_info['data']))

            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()
            # 获取participantID，替换数据
            participantID = test_info['wopParticipantID']

            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                                 msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)

            # 发送请求
            res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
            result = res.json()
            headers = res.headers
            traceID = headers['Traceid']
            # 获取接口返回的evonetReference
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'MPMevonetOrderNumber', evonetOrderNumber)
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
        # MPM_Payment_Authentication接口
        elif test_info["interface"] == 'Payment Notification':
            check_sign_url = test_info['url']
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = test_info['method']
            # 判断是否有数据进行替换
            data = multi_replace(str(test_info['data']))


            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()

            participantID = test_info['wopParticipantID']
            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                                 msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)
            # 发送请求
            res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
            result = res.json()
            headers = res.headers
            traceID = headers['Traceid']
            # CPM_token接口
        elif test_info["interface"] == 'CPM Token':
            # 获取URL

            check_sign_url = test_info['url']
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = test_info['method']
            # 判断是否有数据进行替换,获取body
            data = multi_replace(str(test_info['data']))


            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()
            # 获取participantID
            participantID = test_info['wopParticipantID']

            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                                 msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)

            # 发送请求
            res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
            result = res.json()
            headers = res.headers
            traceID = headers['Traceid']
            # 获取接口返回的mopToken
            mopToken = result['mopToken']
            for item in mopToken:
                if item['type'] == 'Barcode':
                    mopToken_barcode_value = item['value']
                    setattr(case, 'mopToken', mopToken_barcode_value)
                else:
                    mopToken_quickResponseCode_value = item['value']
                    setattr(case, 'mopToken', mopToken_quickResponseCode_value)
        # CPM_payment接口
        elif test_info["interface"] == 'CPM Payment':
            check_sign_url = test_info['url']
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = test_info['method']
            # 判断是否有数据进行替换,获取body
            data = multi_replace(str(test_info['data']))

            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()
            participantID = test_info['mopParticipantID']
            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                                 msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)
            # 发送请求
            res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
            result = res.json()
            headers = res.headers
            traceID = headers['Traceid']
            # 获取接口返回的evonetReference
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
            #判断是否需要更新trans表数据
            if test_info['update_mongo']:
                #获取查询语句
                mongo_query = test_info["check_mongo"].replace("#evonetOrderNumber#", evonetOrderNumber)
                #更新数据库语句
                db_tyo_evopay.update_one(table='trans', query_params=eval(mongo_query), updata_params=eval(test_info['update_mongo']))



        else:

            check_sign_url = test_info['url']
            base_url = evopay_conf.base_url_wop
            url = base_url + check_sign_url
            # 获取method
            method = test_info['method']
            # 判断是否有数据进行替换
            data = multi_replace(str(test_info['data']))


            # 获取url需要的各项参数
            datetime = Moudle().create_datetime()
            header_method = method.upper()
            msgID = Moudle().create_msgId()

            participantID = test_info['mopParticipantID']
            if test_info['pre-update table']:
                if test_info['pre-update mongo']:
                    Update_Mongo_Data(node='single',database=test_info['pre-update database']).updata_data(table=test_info['pre-update table'],
                                                    query_params=eval(test_info['pre-query mongo']),
                                                    update_params=eval(test_info['pre-update mongo']))
                else:
                    Update_Mongo_Data(node='single',database=test_info['pre-update database']).delete_data(table=test_info['pre-update table'],
                                                    query_params=eval(test_info['pre-query mongo']))

            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                                 msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)
            # 发送请求
            res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
            result = res.json()
            headers = res.headers
            traceID = headers['Traceid']
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node='single',database=test_info['pre-update database']).update_data_reset(table=test_info['pre-update table'],
                                                      query_params=eval(test_info['pre-query mongo']),
                                                      update_params=eval(test_info['pre-update mongo']))
            else:
                Update_Mongo_Data(node='single',database=test_info['pre-update database']).delete_data_reset(table=test_info['pre-update table'])

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
                        if 'payment' in str(test_info['check_mongo']):
                            #校验数据库原交易的数据

                            #payment交易需要替换的数据

                            mongo_query_payment=str(eval(test_info["check_mongo"])["payment"]).replace("#originalEvonetOrderNumber#", getattr(case,'originalEvonetOrderNumber'))
                            print(mongo_query_payment)
                            # 查询原交易payment的交易
                            mongo_result_payment = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_payment))
                            #获取数据库数据
                            mongo_status_payment = mongo_result_payment['status']
                            mongo_wopStatus_payment=mongo_result_payment['wopStatus']
                            mongo_mopStatus_payment = mongo_result_payment['mopStatus']

                            # 获取测试数据（payment）数据库的断言
                            mongo_expected_payment = eval(test_info["check_mongo_expected"])["payment"]
                            print(mongo_expected_payment)

                            # 断言数据库里payment的字段
                            assert mongo_expected_payment["status"] == mongo_status_payment
                            assert mongo_expected_payment["wopStatus"] == mongo_wopStatus_payment
                            assert mongo_expected_payment["mopStatus"] == mongo_mopStatus_payment

                        elif 'refund' in str(test_info['check_mongo']):
                            #refund交易需要替换的数据
                            result_evonetOrderNumber = eval(data)['evonetOrderNumber']
                            mongo_query_refund = str(eval(test_info["check_mongo"])["refund"]).replace("#evonetOrderNumber#", result_evonetOrderNumber)


                            # 查询退款的交易
                            # 检查数据库必填值得存入
                            mongo_result_refund = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_query_refund))

                            mongo_result = db_tyo_evopay.get_one(table='trans', query_params=eval(mongo_result_refund))
                            # 数据库查询出的traceID
                            traceID = mongo_result['traceID']
                            # 校验发送给parnter的数据
                            Check_evonet_to_partner(db_tyo_evologs).check_evonet_to_partner_refund(
                                mongo_query={"traceID": traceID}, participantID=participantID, body=eval(data))

                            Checkmongo().check_trans_mongo(test_data_interface="Refund", db_data=mongo_result)

                            # 校验成功的数据的某些字段
                            Checkmongo().check_trans_success(test_data_interface="Refund", db_data=mongo_result)


                            # 获取数据库的数据
                            mongo_status_refund = mongo_result_refund['status']
                            mongo_wopStatus_refund = mongo_result_refund['wopStatus']
                            mongo_mopStatus_refund = mongo_result_refund['mopStatus']
                            # 获取测试数据数据库的断言
                            mongo_expected_refund = eval(test_info["check_mongo_expected"])["refund"]

                            #断言数据库里refund的字段
                            assert mongo_expected_refund["status"] == mongo_status_refund
                            assert mongo_expected_refund['wopStatus']==mongo_wopStatus_refund
                            assert mongo_expected_refund['mopStatus'] == mongo_mopStatus_refund


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








