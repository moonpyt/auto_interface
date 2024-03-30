from base.amount_check import amount_check
from common.evopay.conf_init import db_tyo_evoconfig


class transfer_amount():
    def query_conf(self, conf_params, body_params,transmode='online',node="single"):
        # 用于汇率查询接口和预下单接口
        currency_and_fee = {}

        if transmode == 'offline':
            query_params_customize = {"sopID": conf_params["participantID"], "location": body_params["location"],
                                      "ropID": body_params["participantID"],"tpspID": conf_params["participantID"]}
        else:
            query_params_customize = {"sopID": conf_params["participantID"], "location": body_params["location"],
                                      "ropID": body_params["participantID"]}

        # 预下单接口会比汇款查询接口上送的请求字段中多一个location字段
        if body_params.get("location"):
            query_params_customize["location"] = body_params["location"]

        # 查找优先级：优先于serviceFee表,再次sop,rop,tpsp
        res_cus = db_tyo_evoconfig.get_one("serviceFee", query_params_customize)

        if res_cus:
            if transmode == 'offline':
                temp = dict(sop_settleCurrency=res_cus["sopSettleFeeCurrency"],
                            sopServiceFee=res_cus["sopServiceFee"],
                            transfer_Currency=res_cus["transferCurrency"],
                            senderFee=res_cus["senderFee"],
                            rop_settleCurrency=res_cus["ropSettleFeeCurrency"],
                            ropServiceFee=res_cus["ropServiceFee"],
                            tpsp_settleCurrency = res_cus["ropSettleFeeCurrency"],
                            tpspRebateFee = res_cus["tpspRebateFee"]
                )
            else:
                temp = dict(sop_settleCurrency=res_cus["sopSettleFeeCurrency"],
                            sopServiceFee=res_cus["sopServiceFee"],
                            transfer_Currency=res_cus["transferCurrency"],
                            senderFee=res_cus["senderFee"],
                            rop_settleCurrency=res_cus["ropSettleFeeCurrency"],
                            ropServiceFee=res_cus["ropServiceFee"])
            currency_and_fee.update(temp)

            # 查询汇率时如果不上送PID，默认rop_settleCurrency = rop_settleCurrency
            # prePrder接口必须上传participantID，因为不会走到此逻辑
            if "participantID" not in body_params:
                temp = dict(rop_settleCurrency=body_params["rop_settleCurrency "])
            else:
                temp = dict(rop_settleCurrency=res_cus["ropSettleFeeCurrency"])
            currency_and_fee.update(temp)

        else:
            ##查找优先级：优先于serviceFee表,再次sop,rop,tpsp，此为sop,rop,tpsp逻辑，同上
            query_params_sop = {"baseInfo.sopID": conf_params['participantID']}
            if body_params.get("location"):
                query_params_sop["location"] = body_params["location"]

            res_sop = db_tyo_evoconfig.get_one(query_params_sop)
            if res_sop:
                currency_and_fee["sop_settleCurrency"] = res_sop["settleInfo.settleCurrency"]
                currency_and_fee["sopServiceFee"] = res_sop["sopServiceFee"]

            if transmode == "offline":
                query_params_tpsp = {"baseInfo.sopID": conf_params['participantID'],"baseInfo.tpspID": conf_params['participantID']}
                res_tpsp = db_tyo_evoconfig.get_one(query_params_tpsp)
                if res_tpsp:
                    currency_and_fee["tpsp_settleCurrency"] = res_tpsp["tpspSettleFeeCurrency"]
                    currency_and_fee["tpspRebateFee"] = res_tpsp["tpspRebateFee"]

            if "participantID" not in body_params:
                currency_and_fee["rop_settleCurrency"] = body_params["receiveCurrency"]
            else:
                query_params_rop = {"baseInfo.ropID": body_params['participantID']}
                res_rop = db_tyo_evoconfig.get_one(query_params_rop)
                if res_rop:
                    currency_and_fee["rop_settleCurrency"] = res_rop["settleInfo.settleCurrency"]
                    currency_and_fee["ropServiceFee"] = res_rop["ropServiceFee"]
            return currency_and_fee

    def calculate_query_fxrate(self, body_params, sop_settleCurrency, rop_settleCurrency):
        # 当sendCurrency == receiveCurrency，bid就为1
        # 当sop_settleCurrency=当sop_settleCurrency，bid2=1

        if body_params["sendCurrency"] == body_params["receiveCurrency"]:
            bid = 1
        else:
            check = amount_check()
            if body_params["sendCurrency"] == sop_settleCurrency:
                bid1 = 1
            else:
                bid1 = check.get_fx_rate(body_params["sendCurrency"], sop_settleCurrency)

            if sop_settleCurrency == rop_settleCurrency:
                bid2 = 1
            else:
                bid2 = check.get_fx_rate(sop_settleCurrency, rop_settleCurrency)

            if rop_settleCurrency == body_params["receiveCurrency"]:
                bid3 = 1
            else:
                bid3 = check.get_fx_rate(rop_settleCurrency, body_params["receiveCurrency"], transtype='transfer')
            bid = [bid1, bid2, bid3]
        return bid

    def case_caculate(self):
        pass

    def config_message(self):
        pass


if __name__ == '__main__':
    pass