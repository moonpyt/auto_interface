import pytest

from base.read_file_path import ReadFile
from common.evopay.replace_data import multi_replace,case
from common.evopay.read_csv import ReadCSV
from loguru import logger as log
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification as Testmpmqrverification_double
from case.interface.evopay.QR_single_node_mode.test_MPMPayment import Testmpmpayment as Testmpmpayment_double
data_file=ReadFile().read_data_file("evopay_evonet_mpmpayment","QR_double_node_mode","evopay")
mpmpayment_testdata=ReadCSV(data_file).read_data()
class Testmpmpayment():

    def __init__(self,envirs):
        self.envirs=envirs
    @pytest.mark.parametrize('test_info',mpmpayment_testdata)
    def test_mpmpayment(self,test_info):
        if test_info["interface"]!='MPM Payment':
            body_params,head_params=Testmpmqrverification_double(self.envirs).common_params_init(test_info,node='double')
            res = Testmpmqrverification_double(self.envirs).post_mpmqrverification(test_info,head_params,body_params,node='double')
            headers = res.headers
            result = res.json()
            expected = test_info['expected']
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] ==result["result"]["message"]
            #获取接口返回的evonetReference
            evonetReference=result['evonetReference']
            setattr(case, 'evonetReference', evonetReference)

        #MPM_Payment接口
        else:
            body_params,head_params=Testmpmpayment_double(self.envirs).common_params_init(test_info,node='double')
            res,config_currency = Testmpmpayment_double(self.envirs).post_mpmpayment(test_info, head_params,body_params,node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testmpmpayment_double(self.envirs).check_resopnse_mpmpayment(result,test_info,head_params,body_params,traceID,config_currency,node='double')
