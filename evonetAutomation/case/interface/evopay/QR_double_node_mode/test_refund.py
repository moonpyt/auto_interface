import pytest
import json
from common.evopay.conf_init import evopay_conf, db_sgp_evopay, db_tyo_evopay, db_tyo_evoconfig, db_sgp_evologs
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
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken as Testcpmtoken_double
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment as Testcpmpayment_double
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification as Testmpmqrverification_double
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication as Testmpmpaymentauthentication_double
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification as Testpaymentnotification_double
from case.interface.evopay.QR_single_node_mode.test_cancellation import Testcancellation as Testcancellation_double
from case.interface.evopay.QR_single_node_mode.test_paymentinquiry import Testpaymentinquiry as Testpaymentinquiry_double
from case.interface.evopay.QR_single_node_mode.test_refund import Testrefund as Testrefund_double


data_file=ReadFile().read_data_file("evopay_evonet_refund","QR_double_node_mode","evopay")
refund_testdata=ReadCSV(data_file).read_data()
class Testrefund():
    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',refund_testdata)
    def test_refund(self,test_info):
        if test_info["interface"] == 'MPM QR Verification':
            body_params, head_params = Testmpmqrverification_double(self.envirs).common_params_init(test_info,node='double')
            res = Testmpmqrverification_double(self.envirs).post_mpmqrverification(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)

            # MPM_Payment_Authentication接口
        elif test_info["interface"] == 'MPM Payment Authentication':
            body_params, head_params = Testmpmpaymentauthentication_double(self.envirs).common_params_init(test_info,node='double')
            res,config_currency = Testmpmpaymentauthentication_double(self.envirs).post_mpmauthentication(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            setattr(case, 'MPMevonetOrderNumber', evonetOrderNumber)
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)


        elif test_info["interface"] == 'Payment Notification':
            body_params, head_params = Testpaymentnotification_double(self.envirs).common_params_init(test_info,node='double')
            billing_key = {}
            billing_csv = json.loads(test_info['data'])
            if 'billingAmount' in billing_csv:
                body_params['billingAmount'] = billing_csv['billingAmount']
            if 'billingFXRate' in billing_csv:
                body_params['billingFXRate'] = billing_csv['billingFXRate']
            if 'settleAmount' in billing_csv:
                body_params['settleAmount'] = billing_csv['settleAmount']
            if 'settleFXRate' in billing_csv:
                body_params['settleFXRate'] = billing_csv['settleFXRate']
            res = Testpaymentnotification_double(self.envirs).post_mpmnotify(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')

            # CPM_token接口
        elif test_info["interface"] == 'CPM Token':
            # 获取URL
            body_params, head_params = Testcpmtoken_double(self.envirs).common_params_init(test_info,node='double')
            res = Testcpmtoken_double(self.envirs).post_cpmtoken(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')
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
            body_params, head_params = Testcpmpayment_double(self.envirs).common_params_init(test_info,node='double')
            res,config_currency = Testcpmpayment_double(self.envirs).post_cpmpayment(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)

            # 查询接口
        elif test_info["interface"] == 'Payment Inquiry':
            # 查询URL中是否有替换的数据,获取url
            body_params, head_params = Testpaymentinquiry_double(self.envirs).common_params_init(test_info,node='double')
            check_sign_url = multi_replace(str(head_params['url']))
            base_url = evopay_conf.base_url_mop
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
                    Update_Mongo_Data(node='double', database=test_info['pre-update database']).updata_data(
                        table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']),
                        update_params=eval(test_info['pre-update mongo']))
                else:

                    Update_Mongo_Data(node='double', database=test_info['pre-update database']).delete_data(
                        table=test_info['pre-update table'], query_params=eval(test_info['pre-query mongo']))

            # self,method,url,participantID,msgID,datetime,signkey,data
            header = CheckSign().check_sign_get(method=header_method, url=check_sign_url, participantID=participantID,
                                                msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey)
            # 发送请求
            res = HttpRequest().send(url=url, method=method, headers=header)
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')
            if test_info['pre-update mongo']:
                Update_Mongo_Data(node='double', database=test_info['pre-update database']).update_data_reset(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']),
                    update_params=eval(test_info['pre-update mongo']))
            else:
                Update_Mongo_Data(node='double', database=test_info['pre-update database']).delete_data_reset(
                    table=test_info['pre-update table'])
        else:
            body_params, head_params = Testrefund_double(self.envirs).common_params_init(test_info,node='double')
            res = Testrefund_double(self.envirs).post_refund(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testrefund_double(self.envirs).responce_check_refund(result, test_info, head_params, body_params, traceID,node='double')






