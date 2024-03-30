import pytest
import json
from common.evopay.conf_init import db_sgp_evopay, evopay_conf, db_tyo_evopay, db_sgp_evologs
from common.evopay.reponse_check import Checkresponse
from base.read_file_path import ReadFile
from common.evopay.replace_data import multi_replace,case
from base.db import MongoDB
from base.encrypt import Encrypt
from common.evopay.read_csv import ReadCSV
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification as Testmpmqrverification_double
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication as Testmpmpaymentauthentication_double
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification as Testpaymentnotification_double
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken as Testcpmtoken_double
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment as Testcpmpayment_double
from case.interface.evopay.QR_single_node_mode.test_refund import Testrefund as Testrefund_double
from case.interface.evopay.QR_single_node_mode.test_paymentinquiry import Testpaymentinquiry as Testpaymentinquiry_double
from case.interface.evopay.QR_single_node_mode.test_cancellation import Testcancellation as Testcancellation_double

data_file=ReadFile().read_data_file("evopay_evonet_cancellation","QR_double_node_mode","evopay")
cancellation_testdata=ReadCSV(data_file).read_data()

class Testcancellation():
    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',cancellation_testdata)
    def test_cancellation(self,test_info):
        if test_info["interface"] == 'MPM QR Verification':
            body_params, head_params = Testmpmqrverification_double(self.envirs).common_params_init(test_info,node='double')
            res = Testmpmqrverification_double(self.envirs).post_mpmqrverification(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info,body_params, traceID,node='double')
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)

        # MPM_Payment_Authentication接口
        elif test_info["interface"] == 'MPM Payment Authentication':
            body_params, head_params = Testmpmpaymentauthentication_double(self.envirs).common_params_init(test_info,node='double')
            res,config_currency  =Testmpmpaymentauthentication_double(self.envirs).post_mpmauthentication(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info, body_params,traceID,node='double')
            # 获取接口返回的evonetReference
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            # 获取evonetOrderNumber，用于反向交易传参
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
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info, traceID,body_params,node='double')

            # CPM_token接口
        elif test_info["interface"] == 'CPM Token':
            # 获取URL
            body_params, head_params = Testcpmtoken_double(self.envirs).common_params_init(test_info,node='double')
            res = Testcpmtoken_double(self.envirs).post_cpmtoken(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info, body_params,traceID,node='double')
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
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info,body_params, traceID,node='double')
            # 获取evonetOrderNumber，用于反向交易传参
            evonetOrderNumber = result['evonetOrderNumber']
            setattr(case, 'originalEvonetOrderNumber', evonetOrderNumber)
            setattr(case, 'evonetOrderNumber', evonetOrderNumber)
            mopOrderNumber = result['mopOrderNumber']
            setattr(case, 'originalMopOrderNumber', mopOrderNumber)
            if test_info['update_mongo']:
                mongo_query = multi_replace(str(test_info["check_mongo"]))
                db_tyo_evopay.update_one(table='trans', query_params=eval(mongo_query),
                                         updata_params=eval(test_info["update_mongo"]))

        elif test_info["interface"] == 'Refund':
            body_params, head_params = Testrefund_double(self.envirs).common_params_init(test_info,node='double')
            res = Testrefund_double(self.envirs).post_refund(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info,body_params, traceID,node='double')

        else:
            body_params, head_params = Testcancellation_double(self.envirs).common_params_init(test_info,node='double')
            res = Testcancellation_double(self.envirs).post_cancel(test_info, head_params, body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testcancellation_double(self.envirs).responce_check_cancel(result, test_info,body_params, traceID,node='double')
