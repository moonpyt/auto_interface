import pytest

# from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_sgp_evopay, db_sgp_evologs
# from common.evopay.reponse_check import Checkresponse
# from common.evopay.read_data import EvopayTestCase
from base.read_file_path import ReadFile
# from common.evopay.moudle import Moudle
# from common.evopay.check_sign import CheckSign
# from base.read_config import Conf
# from base.http_request import HttpRequest
# from base.encrypt import Encrypt
# from base.db import MongoDB
from common.evopay.read_csv import ReadCSV
# from common.evopay.replace_data import multi_replace,case
# from common.evopay.mongo_data_check import Checkmongo
# from common.evopay.evonet_to_partner_check import Check_evonet_to_partner
# from common.evopay.mongo_data import Update_Mongo_Data
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken as Testcpmtoken_single
data_file=ReadFile().read_data_file("evopay_evonet_cpmtoken","QR_double_node_mode","evopay")
cpmtoken_testdata=ReadCSV(data_file).read_data()

class Testcpmtoken():
    def __init__(self,envirs):
            self.envirs=envirs

    @pytest.mark.parametrize('test_info',cpmtoken_testdata)
    def test_cpmtoken(self,test_info):
        body_params,head_params=Testcpmtoken_single(self.envirs).common_params_init(test_info,node='double')
        res = Testcpmtoken_single(self.envirs).post_cpmtoken(test_info,head_params,body_params,node='double')
        headers = res.headers
        traceID = headers['Traceid']
        result = res.json()
        Testcpmtoken_single(self.envirs).response_check(result,test_info,head_params,body_params,traceID,node='double')








