import pytest
from loguru import logger as log
from base.read_file_path import ReadFile
from common.evopay.conf_init import db_tyo_evopay
from common.evopay.read_csv import ReadCSV
from base.transfer_initial import trans_initial
from base.post_interface import post_interface
from common.evopay.replace_data import multi_replace,case
from case.interface.transfer.test_preorder import Testpreorder
from common.evopay_transfer.every_interface import every_interface

from common.evopay_transfer.mongo_verify import mongo_verify
from common.evopay_transfer.evonet_amount_fee import evonet_amount_fee
from common.evopay_transfer.responce_check import responce_check

data_file_soptransfercode = ReadFile().read_data_file("evotransfer_soptransfercode", "tranfer_mode", "evopay")
soptransfercode_testdata = ReadCSV(data_file_soptransfercode).read_data()


class Testsoptransfercode():
    @pytest.mark.parametrize('test_info', data_file_soptransfercode)
    def testsoptransfercode(self, test_info):
        result, conf_params, body_params, traceID = self.soptransfercode(test_info)
        self.check_soptransfercode_response(result, test_info, conf_params, body_params, traceID)

    def soptransfercode(self, test_info):
        # 初始化参数，用csv中的参数去更新公共参数
        initial = trans_initial()
        body_params, conf_params = initial.common_params_init(test_info=test_info)
        # 前置条件：获取汇率值
        if body_params.get("fxRate"):
            if type(body_params.get("fxRate")) == dict:
                head_participant = conf_params["participantID"]
                body_participant = body_params["participantID"]
                sendCurrency = body_params["sendAmount"]["currency"]
                receiveCurrency = body_params["receiveAmount"]["currency"]
                if "?fxrate_value?" == body_params.get("fxRate").get("value"):
                    fxrate_interface = every_interface()
                    receiveAmount_pre = fxrate_interface.exteral_post_fxrate(head_participant=head_participant,
                                                                             body_participant=body_participant,
                                                                             sendCurrency=sendCurrency,
                                                                             receiveCurrency=receiveCurrency)
                    body_params.update({"fxRate": receiveAmount_pre["fxRate"]})

        # 前置条件：获取sop evonetUserReference
        if body_params.get('senderInfo'):
            if type(body_params.get('senderInfo')) == dict:
                head_participant = conf_params["participantID"]
                if "?senderInfo.evonetUserReference?" == body_params.get('senderInfo').get('evonetUserReference'):
                    account_create_interface = every_interface()
                    account_create_interface_pre = account_create_interface.exteral_post_sop_account_create(
                        head_participant=head_participant,
                        body_participant=head_participant)
                    body_params.update({"senderInfo": account_create_interface_pre["userInfo"]})

        # 前置条件：获取rop evonetUserReference
        if body_params.get('receiverInfo'):
            if type(body_params.get('receiverInfo')) == dict:
                head_participant = body_params["participantID"]
                if "?receiverInfo.evonetUserReference?" == body_params.get('receiverInfo').get('evonetUserReference'):
                    account_create_interface = every_interface()
                    account_create_interface_pre = account_create_interface.exteral_post_rop_account_create(
                        head_participant=head_participant,
                        body_participant=head_participant)
                    body_params.update({"receiverInfo": account_create_interface_pre["userInfo"]})

        post_preorder = post_interface()
        res = post_preorder.post_request(body_params, conf_params, test_info)
        headers = res.headers
        traceID = headers.get('Traceid')
        result = res.json()
        return result, conf_params, body_params, traceID

    def check_soptransfercode_response(self, result, test_info, conf_params, body_params, traceID):
        expected = test_info['expected']
        try:
            # 断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]

            if result["result"]["code"] in ['S0000', 'S0005'] and result["result"]["message"] == 'Success.':
                evonetOrderNumber = result['evonetOrderNumber']
                setattr(case, 'evonetOrderNumber', evonetOrderNumber)
                check_mongo = '{"evonetOrderNumber": "#evonetOrderNumber#"}'
                mongo_query = multi_replace(check_mongo)
                mongo_result = db_tyo_evopay.get_one(table='transfer', query_params=eval(mongo_query))

                # 校验trans表中mongo中除了金额其他字段存储的值
                mongo_verify_obj = mongo_verify()
                mongo_verify_obj.mongo_verify(test_info['interface'], mongo_result)

                # 校验响应中除了金额其他字段存储的值
                responce_check_obj = responce_check()
                responce_check_obj.response_verify(test_info['interface'], result)

                # 校验成功的pre_order订单金额，包含返回值和数据库存储的值
                evonet_amount_fee_obj = evonet_amount_fee(self.envirs)
                settlement_Mode = evonet_amount_fee_obj.read_conf(conf_params, body_params)
                result_expect, mongo_expect = evonet_amount_fee_obj.calculate_expect_amount(settlement_Mode,
                                                                                            conf_params, body_params)
                evonet_amount_fee_obj.amount_check(result_expect, mongo_expect, result, mongo_result)

        except AssertionError as e:
            print("用例执行不通过")
            log.debug(f'traceID的字段为{traceID}')
            raise e
