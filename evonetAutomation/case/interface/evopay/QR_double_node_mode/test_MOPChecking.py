import pytest
from base.read_file_path import ReadFile
from common.evopay.read_csv import ReadCSV
from case.interface.evopay.QR_single_node_mode.test_MOPChecking import Testmopchecking as Testmopchecking_double
data_file=ReadFile().read_data_file("evopay_evonet_mopchecking","QR_double_node_mode","evopay")
mopchecking_testdata=ReadCSV(data_file).read_data()
class Testmopchecking():
    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize('test_info',mopchecking_testdata)
    def test_mopchecking(self,test_info):
        body_params, head_params = Testmopchecking_double(self.envirs).common_params_init(test_info, node='double')
        res = Testmopchecking_double(self.envirs).post_mopchecking(test_info, head_params, body_params, node='double')
        headers = res.headers
        traceID = headers['Traceid']
        result = res.json()
        Testmopchecking_double(self.envirs).response_check_mopchecking(result, test_info, traceID)



