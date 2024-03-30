import pytest

from base.read_file_path import ReadFile
from common.evopay.read_csv import ReadCSV
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification as Testmpmqrverification_double
data_file=ReadFile().read_data_file("evopay_evonet_mpmqrverification","QR_double_node_mode","evopay")
mpmqrverification_testdata=ReadCSV(data_file).read_data()
class Testmpmqrverification():
    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize('test_info',mpmqrverification_testdata)
    def test_mpmqrverification(self,test_info):
        body_params,head_params = Testmpmqrverification_double(self.envirs).common_params_init(test_info,node='double')
        res = Testmpmqrverification_double(self.envirs).post_mpmqrverification(test_info,head_params,body_params,node='double')
        headers = res.headers
        traceID = headers['Traceid']
        result = res.json()
        Testmpmqrverification_double(self.envirs).check_response_mpmqrverify(result,test_info,head_params,body_params,traceID,node='double')









