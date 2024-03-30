import pytest
import json
from base.read_file_path import ReadFile
from common.evopay.replace_data import case
from common.evopay.read_csv import ReadCSV
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification as Testpaymentnotification_double
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification as Testmpmqrverification_double
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication as Testmpmpaymentauthentication_double
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken as Testcpmtoken_double
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment as Testcpmpayment_double
data_file=ReadFile().read_data_file("evopay_evonet_paymentnotification","QR_double_node_mode","evopay")
paymentnotification_testdata=ReadCSV(data_file).read_data()
class Testpaymentnotification():
    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',paymentnotification_testdata)
    def test_paymentnotification(self,test_info):
        #判断接口是MPM_QR_Verification
        if test_info["interface"]=='MPM QR Verification':
            if test_info["interface"] == 'MPM QR Verification':
                body_params, head_params = Testmpmqrverification_double(self.envirs).common_params_init(test_info,node='double')
                res = Testmpmqrverification_double(self.envirs).post_mpmqrverification(test_info, head_params, body_params,node='double')
                headers = res.headers
                traceID = headers['Traceid']
                result = res.json()
                expected = test_info['expected']
                assert eval(expected)["code"] == result["result"]["code"]
                assert eval(expected)["message"] == result["result"]["message"]
                # 获取接口返回的evonetReference
                evonetReference = result['evonetReference']
                setattr(case, 'evonetReference', evonetReference)

            # MPM_Payment_Authentication接口
            elif test_info["interface"] == 'MPM Payment Authentication':
                body_params, head_params = Testmpmpaymentauthentication_double(self.envirs).common_params_init(test_info,node='double')
                res,config_currency = Testmpmpaymentauthentication_double(self.envirs).post_mpmauthentication(test_info, head_params,body_params,node='double')
                headers = res.headers
                result = res.json()
                expected = test_info['expected']
                assert eval(expected)["code"] == result["result"]["code"]
                assert eval(expected)["message"] == result["result"]["message"]
                evonetOrderNumber = result['evonetOrderNumber']
                setattr(case, 'evonetOrderNumber', evonetOrderNumber)

            elif test_info["interface"] == 'CPM Token':
                body_params, head_params = Testcpmtoken_double(self.envirs).common_params_init(test_info,node='double')
                res = Testcpmtoken_double(self.envirs).post_cpmtoken(test_info, head_params, body_params,node='double')
                headers = res.headers
                traceID = headers['Traceid']
                result = res.json()
                expected = test_info['expected']
                assert eval(expected)["code"] == result["result"]["code"]
                assert eval(expected)["message"] == result["result"]["message"]

                mopToken = result['mopToken']
                for item in mopToken:
                    if item['type'] == 'Barcode':
                        mopToken_barcode_value = item['value']
                        setattr(case, 'mopToken', mopToken_barcode_value)
                    else:
                        mopToken_quickResponseCode_value = item['value']
                        setattr(case, 'mopToken', mopToken_quickResponseCode_value)
            elif test_info["interface"] == 'CPM Payment':
                body_params, head_params = Testcpmpayment_double(self.envirs).common_params_init(test_info,node='double')
                res,config_currency = Testcpmpayment_double(self.envirs).post_cpmpayment(test_info, head_params, body_params,node='double')
                headers = res.headers
                traceID = headers['Traceid']
                result = res.json()
                expected = test_info['expected']
                assert eval(expected)["code"] == result["result"]["code"]
                assert eval(expected)["message"] == result["result"]["message"]
                evonetOrderNumber = result['evonetOrderNumber']
                setattr(case, 'evonetOrderNumber', evonetOrderNumber)

            else:
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
                Testpaymentnotification_double(self.envirs).check_resopnse_mpmnotify(result, test_info, head_params, body_params, traceID,node='double')






