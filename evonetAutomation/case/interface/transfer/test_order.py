import pytest
from loguru import logger as log
from base.read_file_path import ReadFile
from common.evopay.conf_init import db_tyo_evopay
from common.evopay.read_csv import ReadCSV
from base.transfer_initial import trans_initial
from base.post_interface import post_interface
from common.evopay.replace_data import multi_replace,case
from case.interface.transfer.test_preorder import Testpreorder
from common.evopay_transfer.mongo_verify import mongo_verify
from common.evopay_transfer.every_interface import every_interface

data_file_order = ReadFile().read_data_file("evotransfer_order", "tranfer_mode", "evopay")
order_testdata = ReadCSV(data_file_order).read_data()


class Testorder():
    def __init__(self, envirs):
        self.envirs = envirs

    @pytest.mark.parametrize('test_info', order_testdata)
    def testorder(self, test_info):
        result, conf_params, body_params, traceID = self.request_order(test_info)
        self.check_order_response(result, test_info, conf_params, body_params, traceID)

    def request_order(self,test_info):
        # 在发起order接口，初始化参数，用csv中的参数去更新公共参数
        initial = trans_initial()
        body_params, conf_params = initial.common_params_init(test_info=test_info)

        preorder = every_interface()
        preorder_result = preorder.exteral_post_preorder(head_participant=conf_params['particaipant'],body_participant=body_params['particaipant'])

        #先发起一笔pre_order的订单
        if body_params['evonetOrderNumber'] == "?evonetOrderNumber?":
            body_params['evonetOrderNumber'] = preorder_result['evonetOrderNumber']
        post_order = post_interface()
        res = post_order.post_request(body_params, conf_params, test_info)
        headers = res.headers
        traceID = headers.get('Traceid')
        result = res.json()
        if test_info['evonetOrderNumber'] == 'repeat':
            post_order = post_interface()
            res = post_order.post_request(body_params, conf_params, test_info)
            headers = res.headers
            traceID = headers.get('Traceid')
            result = res.json()
        return result, conf_params, body_params, traceID

    def check_order_response(self,result, test_info, conf_params, body_params, traceID):
        expected = test_info['expected']
        try:
            # 断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]

            if result["result"]["code"] == 'S0000' and result["result"]["message"] == 'Success.':
                evonetOrderNumber = body_params['evonetOrderNumber']
                check_mongo = {"evonetOrderNumber": evonetOrderNumber}
                mongo_result = db_tyo_evopay.get_one(table='transfer', query_params=eval(check_mongo))

                # 校验trans表中mongo中除了金额其他字段存储的值
                mongo_verify_obj = mongo_verify()
                mongo_verify_obj.mongo_verify(test_info['interface'], mongo_result)

        except AssertionError as e:
            raise e


