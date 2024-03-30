import pytest
from loguru import logger as log

from base.amount_check import amount_check
from base.read_file_path import ReadFile
from common.evopay.read_csv import ReadCSV
from base.transfer_initial import trans_initial
from base.post_interface import post_interface
from base.transfer_amount_check import transfer_amount

data_file_fxrate = ReadFile().read_data_file("evotransfer_fxrate", "tranfer_mode", "evopay")
fxrate_testdata = ReadCSV(data_file_fxrate).read_data()


class Testfxrate():
    def __init__(self, envirs):
        self.envirs = envirs

    @pytest.mark.parametrize('test_info', fxrate_testdata)
    def testfxrate(self, test_info):
        # 初始化参数，用csv中的参数去更新公共参数
        result, conf_params, body_params, traceID = self.request_fxrate()
        self.check_fxrate_response(result, test_info, conf_params, body_params, traceID)

    def request_fxrate(self, test_info):
        initial = trans_initial()
        body_params, conf_params = initial.common_params_init(test_info=test_info)
        post_fxrate = post_interface()
        res = post_fxrate.post_request(body_params, conf_params, test_info)
        headers = res.headers
        traceID = headers.get('Traceid')
        result = res.json()
        return result,conf_params,body_params,traceID


    def check_fxrate_response(self, result, test_info, conf_params, body_params, traceID):
        expected = test_info['expected']
        try:
            # 断言response的数据
            assert eval(expected)["code"] == result["result"]["code"]
            assert eval(expected)["message"] == result["result"]["message"]
            if result["result"]["code"] == 'S0000' and result["result"]["message"] == 'Success.':
                must_params = ["sourceCurrency", "destinationCurrency", "value"]
                # 去汇率表中获取3个bid的值，然后与返回结果进行比较
                expect_must_params, bid = self.calculate_fxrate(conf_params, body_params, must_params)
                for each in must_params:
                    assert result['fxRate'][each] == expect_must_params[each]
        except AssertionError as e:
            print("用例：{}--执行未通过,traceID为{}".format(test_info["title"], traceID))
            raise e

    def calculate_fxrate(self, conf_params, body_params, must_params):
        bids = transfer_amount()
        sop_rop_conf = bids.query_conf(conf_params, body_params)
        three_bid = bids.calculate_query_fxrate(body_params, sop_rop_conf['sop_settleCurrency'],
                                                sop_rop_conf['rop_settleCurrency'])
        bid = 1
        if isinstance(three_bid, list):
            for each in three_bid:
                bid = each * bid
        log.debug(f'bid的值为{bid}bidd的type类型{type(bid)}')
        bid = amount_check().accurate_format_fill_fxrate(bid)
        log.debug(f'bid的值为{bid}bidd的type类型{type(bid)}')

        expect_must_params_value = [body_params["sendCurrency"], body_params["receiveCurrency"], bid]
        expect_must_params = dict(zip(must_params, expect_must_params_value))
        return expect_must_params, bid
