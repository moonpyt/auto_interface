import pytest

from base.read_file_path import ReadFile
from common.evopay.replace_data import case
from common.evopay.read_csv import ReadCSV
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification as Testmpmqrverification_double
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication as Testmpmpaymentauthentication_double
data_file=ReadFile().read_data_file("evopay_evonet_mpmpaymentauthentication","QR_double_node_mode","evopay")
mpmpaymentauthentication_testdata=ReadCSV(data_file).read_data()
class Testmpmpaymentauthentication():

    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',mpmpaymentauthentication_testdata)
    def test_mpmpaymentauthentication(self,test_info):
        if test_info["interface"]!='MPM Payment Authentication':
            body_params, head_params = Testmpmqrverification_double(self.envirs).common_params_init(test_info, node='double')
            res = Testmpmqrverification_double(self.envirs).post_mpmqrverification(test_info, head_params, body_params,node='double')
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            # 获取接口返回的evonetReference
            evonetReference = result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)
        else:
            body_params, head_params = Testmpmpaymentauthentication_double(self.envirs).common_params_init(test_info, node='double')
            res,config_currency = Testmpmpaymentauthentication_double(self.envirs).post_mpmauthentication(test_info, head_params, body_params, node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testmpmpaymentauthentication_double(self.envirs).check_resopnse_mpmauthentication(result, test_info, body_params,head_params,traceID,config_currency,node='double')








