from base.amount_check import amount_check
from base.transfer_amount_check import transfer_amount
from case.interface.transfer.test_fxrate import Testfxrate
from common.evopay.conf_init import db_tyo_evoconfig, db_tyo_evopay


class evonet_amount_fee():
    def __init__(self, envirs):
        self.envirs = envirs

    # 金额和币种的返回值和数据库存储的校验
    def amount_check(self, result_expect, mongo_expect, result, mongo_result):
        try:
            for each in result_expect:
                assert result_expect[each] == result[each]

            for each in mongo_expect:
                assert mongo_expect[each] == mongo_result[each]

        except AssertionError as e:
            print("用例执行不通过")
            raise e

    def read_conf(self, conf_params, body_params):
        query_params = {"sopID": body_params["participantID"], "ropID": conf_params["participantID"],
                        "location": body_params["location"]}
        result = db_tyo_evoconfig.get_one('relationTransfer', query_params)
        settlementMode = 'EVONET'
        if result:
            if result.get("settlementMode"):
                settlementMode = result["settlementMode"]
        return settlementMode

    def read_conf_tpsp(self, conf_params, body_params):
        query_params = {"sopID": body_params["participantID"], "ropID": conf_params["participantID"],
                        "location": body_params["location"], "tpsp": body_params["tpsp"]}
        result = db_tyo_evoconfig.get_one('relationTransfer', query_params)
        settlementMode = 'EVONET'
        if result:
            if result.get("settlementMode"):
                settlementMode = result["settlementMode"]
        return settlementMode

    # online 模式下金额计算
    def calculate_expect_amount(self, settlement_Mode, conf_params, body_params):
        expect = {}
        mongo = {}
        # 获取配置的币种和fee,evonet模式和direct模式计算逻辑一致
        conf_currency_fee = transfer_amount()
        currency_and_fee = conf_currency_fee.query_conf(conf_params, body_params)
        # 返回的sendAmount
        expect["sendAmount"] = body_params["sendAmount"]
        # 返回的transferFee
        expect["transferFee"] = {"value": currency_and_fee["senderFee"],
                                 "currency": currency_and_fee["transfer_Currency"]}
        amount_check().accurate_format_transamount(expect["transferFee"]["value"],
                                                   expect["transferFee"]["currency"])
        # 返回的settleAmountsenderTotalAmount
        expect["senderTotalAmount"]["value"] = eval(expect["sendAmount"]["value"]) + eval(
            expect["transferFee"]["value"])
        expect["senderTotalAmount"]["currency"] = expect["sendAmount"]["currency"]
        amount_check().accurate_format_transamount(expect["senderTotalAmount"]["value"],
                                                   expect["senderTotalAmount"]["currency"])

        if settlement_Mode == 'EVONET':
            # 获取fxrate
            must_params_fxrate = ["sourceCurrency", "destinationCurrency", "value"]
            fxrate = Testfxrate(self.envirs)
            expect_must_params, bid = fxrate.calculate_fxrate(conf_params, body_params, must_params_fxrate)

            # 返回的settleAmount
            expect["settleAmount"]["currency"] = currency_and_fee["sop_settleCurrency"]
            three_bid = conf_currency_fee.calculate_query_fxrate(body_params, currency_and_fee['sop_settleCurrency'],
                                                                 currency_and_fee['rop_settleCurrency'])
            expect["settleAmount"]["value"] = body_params["sendAmount"]["value"] * three_bid[0]
            amount_check().accurate_format_transamount(expect["settleAmount"]["value"],
                                                       expect["settleAmount"]["currency"])

            # 返回的receiveAmount
            expect["receiveAmount"]["currency"] = body_params["sendAmount"]["currency"]
            expect["receiveAmount"]["value"] = body_params["sendAmount"]["currency"] * three_bid[0] * three_bid[1] * \
                                               three_bid[2]
            amount_check().accurate_format_transamount(expect["receiveAmount"]["value"],
                                                       expect["receiveAmount"]["currency"])

            # 返回的fxRate
            expect["fxRate"] = expect_must_params

            mongo["sendAmount"] = expect["sendAmount"]
            mongo["sopSettleAmount"] = expect["settleAmount"]

            mongo["ropSettleAmount"]["amount"] = mongo["sendAmount"] * three_bid[0] * three_bid[1]
            mongo["ropSettleAmount"]["currency"] = currency_and_fee["rop_settleCurrency"]
            amount_check().accurate_format_transamount(mongo["ropSettleAmount"]["value"],
                                                       mongo["ropSettleAmount"]["currency"])

            mongo["receiveAmount"] = expect["receiveAmount"]
            mongo["transferFee"] = expect["transferFee"]
            mongo["sopServiceFee"] = currency_and_fee["sopServiceFee"]
            mongo["ropServiceFee"] = currency_and_fee["ropServiceFee"]
            mongo["sopNetSettleAmount"] = currency_and_fee["ropServiceFee"] + mongo["sopSettleAmount"]
            mongo["ropNetSettleAmount"] = currency_and_fee["ropServiceFee"] + mongo["ropSettleAmount"]

        else:
            mongo["sendAmount"] = body_params["sendAmount"]
            mongo["sopSettleAmount"] = body_params["settleAmount"]
            mongo["ropSettleAmount"] = body_params["settleAmount"]
            mongo["receiveAmount"] = body_params["receiveAmount"]
            mongo["transferFee"] = expect["transferFee"]
            mongo["sopServiceFee"] = currency_and_fee["sopServiceFee"]
            mongo["ropServiceFee"] = currency_and_fee["ropServiceFee"]
            mongo["sopNetSettleAmount"] = currency_and_fee["sopServiceFee"] + mongo["sopSettleAmount"]
            mongo["ropNetSettleAmount"] = currency_and_fee["ropServiceFee"] + mongo["ropSettleAmount"]
        return expect, mongo

    # offline模式下金额计算
    def calculate_expect_amount_tpsp(self, settlement_Mode, conf_params, body_params):
        expect = {}
        mongo = {}
        # 获取配置的币种和fee,evonet模式和direct模式计算逻辑一致
        conf_currency_fee = transfer_amount()
        currency_and_fee = conf_currency_fee.query_conf(conf_params, body_params)
        # 返回的sendAmount
        expect["sendAmount"] = body_params["sendAmount"]
        # 返回的transferFee
        expect["transferFee"] = {"value": currency_and_fee["senderFee"],
                                 "currency": currency_and_fee["transfer_Currency"]}
        amount_check().accurate_format_transamount(expect["transferFee"]["value"],
                                                   expect["transferFee"]["currency"])
        # 返回的settleAmountsenderTotalAmount
        expect["senderTotalAmount"]["value"] = eval(expect["sendAmount"]["value"]) + eval(
            expect["transferFee"]["value"])
        expect["senderTotalAmount"]["currency"] = expect["sendAmount"]["currency"]
        amount_check().accurate_format_transamount(expect["senderTotalAmount"]["value"],
                                                   expect["senderTotalAmount"]["currency"])

        if settlement_Mode == 'EVONET':
            # 获取fxrate
            must_params_fxrate = ["sourceCurrency", "destinationCurrency", "value"]
            fxrate = Testfxrate(self.envirs)
            expect_must_params, bid = fxrate.calculate_fxrate(conf_params, body_params, must_params_fxrate)

            # 返回的settleAmount
            expect["settleAmount"]["currency"] = currency_and_fee["sop_settleCurrency"]
            three_bid = conf_currency_fee.calculate_query_fxrate(body_params, currency_and_fee['sop_settleCurrency'],
                                                                 currency_and_fee['rop_settleCurrency'])
            expect["settleAmount"]["value"] = body_params["sendAmount"]["value"] * three_bid[0]
            amount_check().accurate_format_transamount(expect["settleAmount"]["value"],
                                                       expect["settleAmount"]["currency"])

            # 返回的receiveAmount
            expect["receiveAmount"]["currency"] = body_params["sendAmount"]["currency"]
            expect["receiveAmount"]["value"] = body_params["sendAmount"]["currency"] * three_bid[0] * three_bid[1] * \
                                               three_bid[2]
            amount_check().accurate_format_transamount(expect["receiveAmount"]["value"],
                                                       expect["receiveAmount"]["currency"])

            # 返回的fxRate
            expect["fxRate"] = expect_must_params

            mongo["sendAmount"] = expect["sendAmount"]
            mongo["sopSettleAmount"]["value"] = 0
            mongo["sopSettleAmount"]["currency"] = expect["settleAmount"]["currency"]

            mongo["ropSettleAmount"]["amount"] = mongo["sendAmount"] * three_bid[0] * three_bid[1]
            mongo["ropSettleAmount"]["currency"] = currency_and_fee["rop_settleCurrency"]
            amount_check().accurate_format_transamount(mongo["ropSettleAmount"]["value"],
                                                       mongo["ropSettleAmount"]["currency"])

            bid_special = amount_check().get_fx_rate(currency_and_fee["sop_settleCurrency"],
                                                     currency_and_fee["tpsp_SettleCurrency"])
            mongo["tpspSettleAmount"]["amount"] = mongo["sendAmount"] * three_bid[0] * bid_special
            mongo["tpspSettleAmount"]["currency"] = currency_and_fee["tpsp_SettleCurrency"]
            amount_check().accurate_format_transamount(mongo["tpspSettleAmount"]["amount"],
                                                       mongo["tpspSettleAmount"]["currency"])

            mongo["receiveAmount"] = expect["receiveAmount"]
            mongo["transferFee"] = expect["transferFee"]
            mongo["sopServiceFee"] = currency_and_fee["sopServiceFee"]
            mongo["ropServiceFee"] = currency_and_fee["ropServiceFee"]
            mongo["tpspRebateFee"] = currency_and_fee["tpspRebateFee"]

            mongo["sopNetSettleAmount"] = currency_and_fee["sopServiceFee"] + mongo["sopSettleAmount"] - mongo[
                "transferFee"] * three_bid[0]
            mongo["ropNetSettleAmount"] = currency_and_fee["ropServiceFee"] + mongo["ropSettleAmount"]
            mongo["tpspNetSettleAmount"] = currency_and_fee["tpspSettleAmount"] + mongo["transferFee"] * three_bid[
                0] * bid_special - mongo["tpspRebateFee"]
        return expect, mongo
