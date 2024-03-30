import pytest
from base.read_file_path import ReadFile
from common.evopay.read_csv import ReadCSV
from common.evopay.replace_data import  case
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment as Testcpmpayment_double
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken as Testcpmtoken_double

data_file = ReadFile().read_data_file("evopay_evonet_cpmpayment", "QR_double_node_mode", "evopay")
cpmpayment_testdata = ReadCSV(data_file).read_data()


class Testcpmpayment():
    def __init__(self, envirs):
        self.envirs = envirs

    @pytest.mark.parametrize('test_info', cpmpayment_testdata)
    def test_cpmpayment(self, test_info):
        # 设置全局
        mongo_result_tyo = {}
        # 获取sgp evopay数据库连接
        # 判断接口是否是CPM Payment，不是CPM Payment
        if test_info["interface"] != 'CPM Payment':
            # 获取URL
            body_params,head_params = Testcpmtoken_double(self.envirs).common_params_init(test_info,node='double')
            res = Testcpmtoken_double(self.envirs).post_cpmtoken(test_info,head_params,body_params,node='double')
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



        # 是CPM Payment接口
        else:
            body_params, head_params = Testcpmpayment_double(self.envirs).common_params_init(test_info, node='double')
            res,config_currency = Testcpmpayment_double(self.envirs).post_cpmpayment(test_info, head_params, body_params, node='double')
            headers = res.headers
            traceID = headers['Traceid']
            result = res.json()
            Testcpmpayment_double(self.envirs).check_resopnse_cpmpayment(result,test_info,head_params,body_params,traceID,config_currency,node='double')



