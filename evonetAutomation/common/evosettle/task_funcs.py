import csv, xlrd, json
import random
import requests
from base.read_config import *
from decimal import Decimal, ROUND_HALF_UP, Context
from base.date_format import DateUtil
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evosettle.comm_funcs import CommFuncs, CommonName


class TaskFuncs():
    # 清分模式一
    def __init__(self, envirs, path=None, title=None):
        "node传参要么是wop,要么是mop"
        if path == None:
            self.path = abspath(__file__, '../../config/evosettle/evosettle_' + envirs + '.ini')
        if title == None:
            self.title = 'trans_data'
        # 测试的时候以tyo为 WOP节点，sgp为 MOP节点
        self.database_connect = DatabaseConnect(envirs)
        self.tyo_config_db = self.database_connect.tyo_config_db
        self.tyo_evosettle_db = self.database_connect.tyo_evosettle_db
        self.sgp_config_db = self.database_connect.sgp_config_db
        self.sgp_evosettle_db = self.database_connect.sgp_evosettle_db
        self.sgp_evopay_db = self.database_connect.sgp_evopay_db
        # 数据库操作func
        self.database_operations = DatabaseOperations(envirs)  # tyo数据库操作
        self.db_operations = DatabaseOperations(envirs)
        self.comm_funcs = CommFuncs()
        self.common_name = CommonName()
        self.get_config = ConfigIni(self.path, self.title)

    date_util = DateUtil()

    def random_char(self):
        words = ''
        for i in range(6):
            words += chr(random.randint(97, 122))
        return words

    def round_four_five(self, number, decimal):
        if number < 0:
            _float = float(number)
            if len(str(_float).split('.')[1]) <= decimal:
                return round(number, decimal)
            elif str(_float)[-1] == '5':
                return round(float(str(_float)[:-1] + '6'), decimal)
            else:
                return round(number, decimal)
        if int(number) > 0:
            decimal = decimal + str(number).find('.')  # 有效位包括整数部分
        if int(number) == 0 and decimal == 0:
            if number >= 0.5:
                return 1.0
            else:
                return 0.0
        return float(Context(prec=decimal, rounding=ROUND_HALF_UP).create_decimal(str(number)))

    def trans_import_assert(self, node_type, evonet_number, file_init=None
                            ):
        """
            交易流水导入校验，兼容wop侧和mop侧
           :param url:  请求的  wop节点url或者mop节点url
           :param node_type:  请求的节点 wop 或者 mop
           :param sett_date:    请求时的清算日期
           :return:
           """
        if file_init == "upi":
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans, {"evonetOrderNumber": evonet_number})
            trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]
            settle_currency = "wopSettleCurrency"
            settle_amt = "wopSettleAmount"
        elif node_type == "wop":
            trans_data = self.tyo_evosettle_db.get_one(self.common_name.trans, {"evonetOrderNumber": evonet_number})
            trans_settle_data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]
            settle_currency = "wopSettleCurrency"
            settle_amt = "wopSettleAmount"
        elif node_type == "mop":
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans, {"evonetOrderNumber": evonet_number})
            trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]
            settle_currency = "mopSettleCurrency"
            settle_amt = "mopSettleAmount"
        # 先不要删除下面注释的
        # for key in ['mopOrderNumber', 'wopOrderNumber', 'evonetOrderNumber', 'mopSettleDate', 'wopSettleDate',
        #             'wopConverterCurrencyFlag', 'mopConverterCurrencyFlag', 'billingConverterCurrencyFlag',
        #             'transAmount', 'transCurrency', 'status', 'wopStatus', 'mopStatus', 'mopSettleAmount',
        #             'mopSettleCurrency', 'wopSettleAmount', 'wopSettleCurrency', 'wopSettleSourceCurrency', 'transType',
        #             'category', 'wopID', 'mopID', 'lockFlag', 'settleMode']:
        #     assert trans_data[key] == trans_settle_data["trans"][key]
        assert trans_data == trans_settle_data["trans"]

        # 校验 blendType
        assert trans_settle_data["blendType"] == "default"
        # 校验三个flag初始值为false
        assert trans_settle_data["clearFlag"] == False
        assert trans_settle_data["feeFlag"] == False

        assert trans_settle_data["amountErrorFlag"] == False
        assert trans_settle_data["settleFlag"] == False
        # 校验初始化interchangefee ,interchangefeerefund,processingfee,fxprocessingfee初始状态为 0.0
        assert settle_info["interchangeFee"] == 0.0
        assert settle_info["interchangeFeeRefund"] == 0.0
        assert settle_info["processingFee"] == 0.0
        assert settle_info["fxProcessingFee"] == 0.0
        assert settle_info["rebate"] == 0.0
        assert settle_info["feeReceivable"] == 0.0
        assert settle_info["feeReceivable"] == 0.0
        # 校验 transSett.wop表中的 trans内的body中的币种，交易金额 和外层测币种，交易金额 一致
        # wop侧赋值和mop侧赋值逻辑一样:将wopsettlecurrency 和wopsettleamount赋值给  settlecurrency，settleamount

        # 校验清算币种和清算金额的取值；
        assert settle_info["settleCurrency"] == trans_data[settle_currency]
        assert settle_info["settleAmount"] == trans_data[settle_amt]
        if file_init == "upi":
            upi_data = trans_settle_data["trans"]["rawData"]
            upi_blend_key = upi_data["forwardingIIN"] + \
                            upi_data["systemTraceAuditNum"] + upi_data["transmissionDateTime"]
            if trans_data["category"] == "Card":
                assert trans_settle_data["blendKey"] == upi_blend_key
            if trans_data["category"] == "QR":
                assert trans_settle_data["blendKey"] == 'QR' + upi_blend_key

        else:
            assert trans_settle_data["blendKey"] == trans_data["evonetOrderNumber"]

    def trans_sync_count_assert(self, table_name, wopid, mopid, sett_date):
        trans_counts = self.db_operations.evosettle_db.count("trans", {"wopID": wopid, "mopID": mopid,
                                                                       "wopSettleDate": sett_date})
        trans_sett_counts = self.db_operations.evosettle_db.count(table_name,
                                                                  {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                   "settleDate": sett_date})
        assert trans_counts == trans_sett_counts

    def mop_trans_sync_count_assert(self, table_name, wopid, mopid, sett_date):
        trans_counts = self.db_operations.evosettle_db.count("trans", {"wopID": wopid, "mopID": mopid,
                                                                       "mopSettleDate": sett_date})
        trans_sett_counts = self.db_operations.evosettle_db.count(table_name,
                                                                  {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                   "settleDate": sett_date})

        assert trans_counts == trans_sett_counts

    def wop_get_calc_fee_assert(self, wopid, mopid, sett_date, model, fileinit, trans_currency=None, recon_flag=False):
        # 对wop侧获取手续费并进行计费校验
        """
        :param wopid:
        :param mopid:
        :param sett_date:
        :param model:
        :param fileinit:
        :param trans_currency 交易币种，交易中的交易币种,当需要用到 mccr 的时候才会用到，即交易币种，清算币种，配置表中的清算币种都不一致的时候才会传
        :return:
        """
        # 计费只对 状态为 "trans.status": "succeeded"，交易类行为 CPM，MPM进行校验
        # 获取wop表mop，customizeconfig 中的四个手续费费率和wccr
        settle_info = self.tyo_config_db.get_one("wop", {"baseInfo.wopID": wopid})[
            "settleInfo"]
        if "transactionProcessingFeeRate" in settle_info:
            trans_process_fee_rate = settle_info["transactionProcessingFeeRate"]
        if "fxProcessingFeeRate" in settle_info:
            fx_process_fee_rate = settle_info["fxProcessingFeeRate"]
        if "cpmInterchangeFeeRate" in settle_info:
            cpm_interchange_fee_rate = settle_info["cpmInterchangeFeeRate"]
        if "mpmInterchangeFeeRate" in settle_info:
            mpm_interchange_fee_rate = settle_info["mpmInterchangeFeeRate"]

        if "transProcessingFeeCollectionMethod" in settle_info:
            trans_fee_method = settle_info["transProcessingFeeCollectionMethod"]
        if "fxProcessingFeeCollectionMethod" in settle_info:
            fx_fee_method = settle_info["fxProcessingFeeCollectionMethod"]
        if "transProcessingFeeCalculatedMethod" in settle_info:
            trans_fee_calc_method = settle_info["transProcessingFeeCalculatedMethod"]
        if "fxProcessingFeeCalculatedMethod" in settle_info:
            fx_fee_calc_method = settle_info["fxProcessingFeeCalculatedMethod"]

        # mccr只有 mop表和customizeconfig表有值

        # 当wop 或者mop表中没有对应的手续费时则去customizecofnig 获取手续费，即优先获取custom表的手续费

        service_fee_info = self.tyo_config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})
        if service_fee_info:
            if "transactionProcessingFeeRate" in service_fee_info:
                trans_process_fee_rate = service_fee_info["transactionProcessingFeeRate"]

            if "fxProcessingFeeRate" in service_fee_info:
                fx_process_fee_rate = service_fee_info["fxProcessingFeeRate"]

            if "cpmInterchangeFeeRate" in service_fee_info:
                cpm_interchange_fee_rate = service_fee_info["cpmInterchangeFeeRate"]

            if "mpmInterchangeFeeRate" in service_fee_info:
                mpm_interchange_fee_rate = service_fee_info["mpmInterchangeFeeRate"]

            if "transProcessingFeeCollectionMethod" in service_fee_info:
                trans_fee_method = service_fee_info["transProcessingFeeCollectionMethod"]

            if "fxProcessingFeeCollectionMethod" in service_fee_info:
                fx_fee_method = service_fee_info["fxProcessingFeeCollectionMethod"]

            if "transProcessingFeeCalculatedMethod" in service_fee_info:
                trans_fee_calc_method = service_fee_info["transProcessingFeeCalculatedMethod"]

            if "fxProcessingFeeCalculatedMethod" in service_fee_info:
                fx_fee_calc_method = service_fee_info["fxProcessingFeeCalculatedMethod"]

        mccr_rate = self.get_mccr(wopid, mopid, trans_currency)
        # 费率计算；wop额计费的所有逻辑
        self.wop_service_fee_assert(wopid, mopid, sett_date, trans_process_fee_rate, fx_process_fee_rate,
                                    cpm_interchange_fee_rate, mpm_interchange_fee_rate, mccr_rate, model, fileinit,
                                    trans_fee_method, fx_fee_method, trans_fee_calc_method, fx_fee_calc_method,
                                    recon_flag)

    def get_mccr(self, wopid, mopid, trans_currency, ):
        # 获取mccr ,当三种币种都不一致的时候，fxfee transfee会用到mccr
        # 交易金额费乘以fxrate(汇率转换)乘以(1+mccr)乘以手续 (模式一和模式二中才会出现
        # 先去customizeconfig，根据trans_currency 找对应的mccr
        # 先获取 customizeconfig表的数据

        # 假如 customizeconfig表不存在对应的 wopid mopid 数据，则找mop表的 mccr
        # 判断是否存在 customizeconfig配置
        trans_currency_list = self.db_operations.custom_config_service_fee_info("wop",
                                                                                wopid, mopid)

        if trans_currency_list:
            if "transCurrencies" in trans_currency_list:
                mccr_list = trans_currency_list["transCurrencies"]
                for i in range(len(mccr_list)):
                    if mccr_list[i]["currency"] == trans_currency:
                        if "mccr" in mccr_list[i]:
                            mccr_rate = mccr_list[i]["mccr"]
                            return mccr_rate
            if "mccr" in trans_currency_list:
                return trans_currency_list["mccr"]

    def wop_service_fee_assert(self, wopid, mopid, sett_date, trans_process_fee_rate, fx_process_fee_rate,
                               cpm_interchange_fee_rate, mpm_interchange_fee_rate, mccr_rate, model, fileinit,
                               trans_fee_method, fx_fee_method, trans_fee_calc_method, fx_fee_calc_method, recon_flag,

                               ):

        # 获取配置表中的清算币种
        # interchangfee取目标清算币种时是有优先级关系的，fxfee和procesingfee的目标清算币种是直接取wop 表和mop表的
        settle_info = self.db_operations.tyo_wop_settlement_info(wopid)
        if "settleCurrency" in settle_info:
            inter_settle_currency = settle_info["settleCurrency"]
        service_fee_info = self.tyo_config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})
        # interchange_fee的settlecurrency优先选择 customizeconfig表的 settle_currency,且做交易时，wopsettlecurrency,mopsettlecurrency
        # 取得就是 customizeconfig 的 settlecurrency
        if service_fee_info:
            if "settleCurrency" in service_fee_info:
                inter_settle_currency = service_fee_info["settleCurrency"]
        # 获取interchangefee清算金额的小数位
        interchangefee_currency_decimal = self.db_operations.get_currency_decimal(self.common_name.owner_type_wop,
                                                                                  inter_settle_currency)

        # 获取wop表中  fxfee,transprocessingfee的清算币种并计算清算币种的小数位
        settle_currency = settle_info["settleCurrency"]
        currency_decimal = self.db_operations.get_currency_decimal("wop", settle_currency)

        # 获取正向cpm,mpm类型的交易,且计费成功的数据；反向的交易没有进行计费校验
        cpm_mpm_data = self.db_operations.get_cpm_mpm_data("wop", wopid, mopid, sett_date)
        # 对费率进行校验，"$in": ["CPM Payment", "MPM Payment"]},"settleDate": sett_date, "clearFlag": True,"feeFlag": True,
        # "trans.status": "succeeded"
        for trans_data in cpm_mpm_data:  # trans_data交易数据；cpm_mpm_data 交易集
            evonet_number = trans_data["trans"]["evonetOrderNumber"]
            # 先校验两个清算币种是否一致，币种一致时直接取清算金额进行计算费率
            # 如果trans表存在这个  wopsettlecurrency字段
            if "wopSettleCurrency" in trans_data["trans"]:
                # 当源清算币种和目标清算币种一致时计算interchangfee
                sett_amt = self.db_operations.sett_amount_outside("wop", evonet_number)
                trans_amt = self.db_operations.trans_amount_inside("wop", evonet_number)
                # 计算wop侧  interchangfee；共三种情况，这个参数是清算金额
                # wop侧 interchangfee 计费逻辑--------------------------------------
                self.wop_interchangfee_sett_fee_assert(trans_data, evonet_number,
                                                       cpm_interchange_fee_rate, mpm_interchange_fee_rate,
                                                       interchangefee_currency_decimal, model,
                                                       fileinit, sett_amt, wopid, mopid, recon_flag)

                # ----------------------------------------------------------------------------
                # 计算wop 侧fxfee trans_fe;共三种情况
                # 最后一个擦拭农户sett_amt是 清算交易金额

                if settle_currency == trans_data["settleInfo"]["settleCurrency"]:
                    self.wop_fx_trans_fee_sett_fee_assert(evonet_number, fx_process_fee_rate,
                                                          trans_process_fee_rate,
                                                          currency_decimal, sett_amt, trans_fee_method, fx_fee_method,
                                                          trans_fee_calc_method, fx_fee_calc_method, wopid, mopid)
                else:
                    # 当交易币种和 和配置表的清算币种一致时的情况，最后一个参数是交易金额
                    if settle_currency == trans_data["trans"]["transCurrency"]:
                        self.wop_fx_trans_fee_sett_fee_assert(evonet_number, fx_process_fee_rate,
                                                              trans_process_fee_rate,
                                                              currency_decimal, trans_amt, trans_fee_method,
                                                              fx_fee_method, trans_fee_calc_method, fx_fee_calc_method,
                                                              wopid, mopid)
                    else:
                        # 当三个币种都不一致时
                        self.wop_fx_trans_three_fee_currency_assert(evonet_number, trans_process_fee_rate,
                                                                    fx_process_fee_rate, currency_decimal,
                                                                    settle_currency, mccr_rate, trans_fee_method,
                                                                    fx_fee_method, trans_fee_calc_method,
                                                                    fx_fee_calc_method, wopid, mopid)

    def wop_interchangfee_sett_fee_assert(self, trans_data, evonet_number,
                                          cpm_interchange_fee_rate, mpm_interchange_fee_rate,
                                          interchangefee_currency_decimal, model,
                                          fileinit, sett_amt, wopid, mopid, recon_flag):
        # 直清模式 wop出文件，不计算interchagnfee
        if fileinit == "wop":
            # 单独assert
            pass
        else:
            # 直清模式 evonet 出文件，或者模式四 evonet 出文件
            interchangefee_currency = \
                self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                              {"trans.evonetOrderNumber": evonet_number})["trans"][
                    "wopSettleCurrency"]
            interchangefee_currency_decimal = self.db_operations.get_currency_decimal("wop", interchangefee_currency)
            if trans_data["trans"]["transType"] == "CPM Payment":
                cpm_interchange_fee = self.round_four_five(cpm_interchange_fee_rate * sett_amt,
                                                           interchangefee_currency_decimal)
                assert cpm_interchange_fee == self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                                            {"trans.evonetOrderNumber": evonet_number})[
                    'settleInfo']["interchangeFee"]

            if trans_data["trans"]["transType"] == "MPM Payment":
                mpm_interchange_fee = self.round_four_five(mpm_interchange_fee_rate * sett_amt,
                                                           interchangefee_currency_decimal)
                assert mpm_interchange_fee == self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                                            {"trans.evonetOrderNumber": evonet_number})[
                    'settleInfo']["interchangeFee"]

    def wop_fx_trans_fee_sett_fee_assert(self, evonet_number, fx_process_fee_rate,
                                         trans_process_fee_rate,
                                         currency_decimal, sett_amt, trans_fee_method, fx_fee_method,
                                         trans_fee_calc_method, fx_fee_calc_method, wopid, mopid):
        # trans_fee
        data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                             {"trans.evonetOrderNumber": evonet_number})
        settle_info = data["settleInfo"]
        if trans_fee_method == "monthly" and trans_fee_calc_method == "accumulation":
            assert settle_info["processingFee"] == 0.0
        else:
            trans_process_fee = self.round_four_five(trans_process_fee_rate * sett_amt, currency_decimal)
            assert trans_process_fee == settle_info["processingFee"]
        # fx_trans_fee
        if fx_fee_method == "monthly" and fx_fee_calc_method == "accumulation":
            assert settle_info["fxProcessingFee"] == 0.0
        else:
            if data["trans"]["wopConverterCurrencyFlag"] == False:
                assert settle_info["fxProcessingFee"] == 0.00
            else:
                fx_process_fee = self.round_four_five(fx_process_fee_rate * sett_amt, currency_decimal)
                assert fx_process_fee == settle_info["fxProcessingFee"]

    def wop_interchangfee_three_fee_currency_assert(self, trans_data, evonet_number, cpm_interchange_fee_rate,
                                                    mpm_interchange_fee_rate,
                                                    inter_settle_currency, interchangefee_currency_decimal,
                                                    mccr_rate, model, fileinit, wopid, mopid):
        # 当三个币种都不一致时计费
        mccr_rate = mccr_rate + 1
        # 当配置表中的清算币种和transSett.wop表中的清算币种不一致且和交易币种不一致是执行如下流程
        trans_currency = self.db_operations.trans_currency_inside(evonet_number)
        # 获取 根据交易币种和目标币种获取 fxrate；逻辑上只有模式四 wop侧 会用到
        fxrate_fee = self.db_operations.get_fxrate_fee(trans_currency, inter_settle_currency)
        trans_amt = self.db_operations.trans_amount_inside(evonet_number)
        if model == "bilateral" and fileinit == "wop":
            # # 当是直清模式时，mop侧的 interchangefee不进行计算
            assert self.db_operations.inter_chang_fee(evonet_number) == 0.0
        else:

            # interchangfee 不存在这种三种币种都不一致的情况
            # 直清模式 evonet 出文件
            if trans_data["trans"]["transType"] == "CPM Payment":
                cpm_interchange_fee = self.round_four_five(
                    cpm_interchange_fee_rate * trans_amt * fxrate_fee * mccr_rate,
                    interchangefee_currency_decimal)
                assert cpm_interchange_fee == self.db_operations.inter_chang_fee(evonet_number)
            if trans_data["trans"]["transType"] == "MPM Payment":
                mpm_interchange_fee = self.round_four_five(
                    mpm_interchange_fee_rate * trans_amt * fxrate_fee * mccr_rate,
                    interchangefee_currency_decimal)
                assert mpm_interchange_fee == self.db_operations.inter_chang_fee(evonet_number)
            assert 2 == 3

    def get_currency_code(self, node_type, currency):
        if node_type == "wop":
            db = self.tyo_config_db
        if node_type in ["mop", "upi"]:
            db = self.sgp_config_db

        return db.get_one("currency", {"code": currency})["number"]

    def fx_rate_set(self, owner_type, orig_curency, dst_currency, upi_fx_rate=None):
        """
        :param owner_type: 参数 wop mop upi
        :param orig_curency:  源币种
        :param dst_currency:  目标币种
        :param upi_fx_rate:   只有owner_type为 upi 时的银联手续费
        :return:
        """
        if owner_type == "wop":
            db = self.tyo_config_db
        if owner_type == "mop":
            db = self.sgp_config_db
        if owner_type != "upi":
            db.delete_manys(self.common_name.fx_rate,
                            {"ccyPair": "{}/{}".format(orig_curency, dst_currency),
                             "ccy1": orig_curency,
                             "ccy2": dst_currency,
                             "fxRateOwner": "evonet"})
            db.insert_one(self.common_name.fx_rate, {"ccyPair": "{}/{}".format(orig_curency, dst_currency),
                                                     "ccy1": orig_curency,
                                                     "ccy1Code": self.get_currency_code(owner_type, orig_curency),
                                                     "ccy2": dst_currency,
                                                     "ccy2Code": self.get_currency_code(owner_type, dst_currency),
                                                     "bid": self.get_currency_fxrate(orig_curency,dst_currency),
                                                     "ask": self.get_currency_fxrate(orig_curency,dst_currency),
                                                     "mid": self.get_currency_fxrate(orig_curency,dst_currency),
                                                     "fxRateOwner": "evonet",
                                                     "deleteFlag": False,
                                                     "fxRateSource": "MDAQ",
                                                     "version": int(0),
                                                     "operationalNode": [
                                                         "tyo"]})
        if owner_type == "upi":
            db = self.sgp_config_db
            db.delete_manys(self.common_name.fx_rate,
                            {"ccyPair": "{}/{}".format(orig_curency, dst_currency),
                             "ccy1": orig_curency,
                             "ccy2": dst_currency,
                             "fxRateOwner": "evonet"})
            db.insert_one(self.common_name.fx_rate, {"ccyPair": "{}/{}".format(orig_curency, dst_currency),
                                                     "ccy1": orig_curency,
                                                     "ccy1Code": self.get_currency_code(owner_type, orig_curency),
                                                     "ccy2": dst_currency,
                                                     "ccy2Code": self.get_currency_code(owner_type, dst_currency),
                                                     "bid": upi_fx_rate,
                                                     "ask": upi_fx_rate,
                                                     "mid": upi_fx_rate,
                                                     "fxRateOwner": "evonet",
                                                     "deleteFlag": False,
                                                     "fxRateSource": "MDAQ",
                                                     "version": int(0),
                                                     "operationalNode": [
                                                         "sgp"]})

    def assert_fee(self, trans, fee):
        # trans  交易
        # 校验计费后的 processing_fee transaction_fee
        assert trans['feeFlag'] == True
        assert trans['clearFlag'] == True
        assert trans['settleInfo']['processingFee'] == fee
        assert trans['settleInfo']['fxProcessingFee'] == fee

    def delete_fx_rate(self, owner_type, currency_list: list):
        if owner_type == "wop":
            db = self.tyo_config_db
        if owner_type == "mop":
            db = self.sgp_config_db
        for orig_currency, dst_currency in currency_list:
            db.delete_manys(self.common_name.fx_rate, {
                "ccyPair": "{}/{}".format(orig_currency, dst_currency),
                "fxRateOwner": "evonet"})

    def get_currency_fxrate(self, orig_curency, dst_currency):
        if orig_curency == "SGD" and dst_currency == "JPY":
            ask = 82.82
            bid = 79.88
        elif orig_curency == "JPY" and dst_currency == "SGD":
            ask = 0.01222
            bid = 0.0101
        elif orig_curency == "SGD" and dst_currency == "USD":
            ask = 0.754
            bid = 0.748
        elif orig_curency == "USD" and dst_currency == "JPY":
            ask = 109
            bid = 106

        elif orig_curency == "JPY" and dst_currency == "USD":
            ask = 0.0094
            bid = 0.009

        elif orig_curency == "USD" and dst_currency == "SGD":
            ask = 1.34
            bid = 1.32

        elif orig_curency == "CNY" and dst_currency == "JPY":
            ask = 16.98
            bid = 16.70

        elif orig_curency == "JPY" and dst_currency == "CNY":
            ask = 0.0597
            bid = 0.0567
        elif orig_curency == "CNY" and dst_currency == "USD":
            ask = 0.1563
            bid = 0.1543

        elif orig_curency == "USD" and dst_currency == "CNY":
            ask = 6.3973
            bid = 6.2273
        mid = (ask + bid) / 2
        return ask, mid, bid

    def evonet_rate_set(self, owner_type, orig_curency, dst_currency, wopid=None):
        """
        :param owner_type: 参数 wop mop upi
        :param orig_curency:  源币种
        :param dst_currency:  目标币种
        :return:
        """

        ask, mid, bid = self.get_currency_fxrate(orig_curency, dst_currency)

        if owner_type == "wop":
            db = self.tyo_config_db
            settle_db = self.tyo_evosettle_db
            table = self.common_name.trans_settle_wop
        if owner_type == "mop":
            db = self.sgp_config_db
            settle_db = self.sgp_evosettle_db
            table = self.common_name.trans_settle_mop
        db.delete_manys(self.common_name.fx_rate,
                        {
                            "ccyPair": "{}/{}".format(orig_curency, dst_currency),
                            "fxRateOwner": "evonet"})
        db.insert_one(self.common_name.fx_rate, {"ccyPair": "{}/{}".format(orig_curency, dst_currency),
                                                 "ccy1": orig_curency,
                                                 "ccy1Code": self.get_currency_code(owner_type, orig_curency),
                                                 "ccy2": dst_currency,
                                                 "ccy2Code": self.get_currency_code(owner_type, dst_currency),
                                                 "bid": bid,
                                                 "ask": ask,
                                                 "mid": mid,
                                                 "fxRateOwner": "evonet",
                                                 "deleteFlag": False,
                                                 "fxRateSource": "MDAQ",
                                                 "version": int(0),
                                                 "operationalNode": [
                                                     "tyo"]})
        settle_db.update_many(table,
                              {"trans.wopID": wopid},
                              {"settleFlag": True,
                               "blendType": "success",
                               "settleInfo.interchangeFee": 0.0,
                               "feeFlag": False,
                               "clearFlag": False})

    def wop_fx_trans_three_fee_currency_assert(self, evonet_number, trans_process_fee_rate,
                                               fx_process_fee_rate, currency_decimal,
                                               settle_currency, mccr_rate, trans_fee_method, fx_fee_method,
                                               trans_fee_calc_method, fx_fee_calc_method, wopid, mopid):
        # 当三个币种都不一致时计费
        mccr_rate = mccr_rate + 1

        # 当配置表中的清算币种和transSett.wop表中的清算币种不一致且和交易币种不一致是执行如下流程
        data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                             {"trans.evonetOrderNumber": evonet_number})
        settle_info = data["settleInfo"]
        trans_currency = data["trans"]["transCurrency"]

        trans_amt = data["trans"]["transAmount"]
        if trans_fee_method == "monthly" and trans_fee_calc_method == "accumulation":
            assert settle_info["processingFee"] == 0.0

        else:
            fxrate_fee = self.tyo_config_db.get_one(self.common_name.fx_rate,
                                                    {"ccyPair": "{}/{}".format(trans_currency, settle_currency),
                                                     "fxRateOwner": "evonet"})["ask"]
            trans_process_fee = self.round_four_five(trans_process_fee_rate * trans_amt * fxrate_fee * mccr_rate,
                                                     currency_decimal)
            assert trans_process_fee == settle_info["processingFee"]
        if fx_fee_method == "monthly" and fx_fee_calc_method == "accumulation":
            assert settle_info["fxProcessingFee"] == 0.0
        else:
            if data["trans"]["wopConverterCurrencyFlag"] == False:
                assert settle_info["fxProcessingFee"] == 0.0
            else:
                fxrate_fee = self.tyo_config_db.get_one(self.common_name.fx_rate,
                                                        {"ccyPair": "{}/{}".format(trans_currency, settle_currency),
                                                         "fxRateOwner": "evonet"})["ask"]
                fx_process_fee = self.round_four_five(fx_process_fee_rate * trans_amt * fxrate_fee * mccr_rate,
                                                      currency_decimal)
                assert fx_process_fee == settle_info["fxProcessingFee"]

    def mop_get_calc_fee_assert(self, wopid, mopid, sett_date, model, fileinit, trans_currency=None,
                                table="transSettle.mop", recon_flag=False):
        # 对mop侧获取手续费并进行计费校验
        """
        :param wopid:
        :param mopid:
        :param sett_date:
        :param model:
        :param fileinit:
        :param owner_type: wop节点或者mop节点
        :return:
        """
        # 计费只对 状态为 "trans.status": "succeeded"，交易类行为 CPM，MPM进行校验
        # 获取mop表mop，customizeconfig 中的四个手续费费率和wccr
        mop_settle_info = self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"]
        if "transactionProcessingFeeRate" in mop_settle_info:
            trans_process_fee_rate = mop_settle_info["transactionProcessingFeeRate"]

        if "fxProcessingFeeRate" in mop_settle_info:
            fx_process_fee_rate = mop_settle_info["fxProcessingFeeRate"]
        if "cpmInterchangeFeeRate" in mop_settle_info:
            cpm_interchange_fee_rate = mop_settle_info["cpmInterchangeFeeRate"]
        if "mpmInterchangeFeeRate" in mop_settle_info:
            mpm_interchange_fee_rate = mop_settle_info["mpmInterchangeFeeRate"]
        if "transProcessingFeeCollectionMethod" in mop_settle_info:
            trans_fee_method = mop_settle_info["transProcessingFeeCollectionMethod"]
        if "fxProcessingFeeCollectionMethod" in mop_settle_info:
            fx_fee_method = mop_settle_info["fxProcessingFeeCollectionMethod"]
        if "transProcessingFeeCalculatedMethod" in mop_settle_info:
            trans_fee_calc_method = mop_settle_info["transProcessingFeeCalculatedMethod"]
        if "fxProcessingFeeCalculatedMethod" in mop_settle_info:
            fx_fee_calc_method = mop_settle_info["fxProcessingFeeCalculatedMethod"]
        service_fee_info = self.sgp_config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})
        if service_fee_info:
            # 当wop 或者mop表中没有对应的手续费时则去customizecofnig 获取手续费，即优先获取custom表的手续费
            if "transactionProcessingFeeRate" in service_fee_info:
                trans_process_fee_rate = service_fee_info["transactionProcessingFeeRate"]

            if "fxProcessingFeeRate" in service_fee_info:
                fx_process_fee_rate = service_fee_info["fxProcessingFeeRate"]

            if "cpmInterchangeFeeRate" in service_fee_info:
                cpm_interchange_fee_rate = service_fee_info["cpmInterchangeFeeRate"]

            if "mpmInterchangeFeeRate" in service_fee_info:
                mpm_interchange_fee_rate = service_fee_info["mpmInterchangeFeeRate"]

            # 费率方式获取
            if "transProcessingFeeCollectionMethod" in service_fee_info:
                trans_fee_method = service_fee_info["transProcessingFeeCollectionMethod"]

            if "fxProcessingFeeCollectionMethod" in service_fee_info:
                fx_fee_method = service_fee_info["fxProcessingFeeCollectionMethod"]

            if "transProcessingFeeCalculatedMethod" in service_fee_info:
                trans_fee_calc_method = service_fee_info["transProcessingFeeCalculatedMethod"]

            if "fxProcessingFeeCalculatedMethod" in service_fee_info:
                fx_fee_calc_method = service_fee_info["fxProcessingFeeCalculatedMethod"]

        mccr_rate = self.get_mccr(wopid, mopid, trans_currency)
        # 费率计算；mop侧计费的所有逻辑
        self.mop_service_fee_assert(wopid, mopid, sett_date, trans_process_fee_rate, fx_process_fee_rate,
                                    cpm_interchange_fee_rate, mpm_interchange_fee_rate, mccr_rate, model, fileinit,
                                    trans_fee_method, fx_fee_method, trans_fee_calc_method, fx_fee_calc_method,
                                    table,
                                    recon_flag)

    def mop_service_fee_assert(self, wopid, mopid, sett_date, trans_process_fee_rate, fx_process_fee_rate,
                               cpm_interchange_fee_rate, mpm_interchange_fee_rate, mccr_rate, model, fileinit,
                               trans_fee_method, fx_fee_method, trans_fee_calc_method, fx_fee_calc_method,
                               table, recon_flag):
        mop_settle_info = self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"]
        service_fee_info = self.sgp_config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})
        # 获取配置表中的清算币种
        # interchangfee取目标清算币种时是有优先级关系的，fxfee和procesingfee的目标清算币种是直接取wop 表和mop表的
        if "settleCurrency" in mop_settle_info:
            inter_settle_currency = mop_settle_info["settleCurrency"]
        if service_fee_info:
            if "settleCurrency" in service_fee_info:
                inter_settle_currency = service_fee_info["settleCurrency"]
        # 获取interchangefee清算金额的小数位
        interchangefee_currency_decimal = self.db_operations.get_currency_decimal("mop", inter_settle_currency)

        # 获取mop表中  fxfee,transprocessingfee的清算币种并计算清算币种的小数位
        settle_currency = mop_settle_info["settleCurrency"]
        currency_decimal = self.db_operations.get_currency_decimal("mop", settle_currency)

        # 获取正向cpm,mpm类型的交易,且计费成功的数据；反向的交易没有进行计费校验
        cpm_mpm_data = self.db_operations.get_cpm_mpm_data("mop", wopid, mopid, sett_date)
        # 对费率进行校验，"$in": ["CPM Payment", "MPM Payment"]},"settleDate": sett_date,
        # "trans.status": "succeeded"
        for trans_data in cpm_mpm_data:  # trans_data交易数据；cpm_mpm_data 交易集
            evonet_number = trans_data["trans"]["evonetOrderNumber"]
            # 先校验两个清算币种是否一致，币种一致时直接取清算金额进行计算费率
            # 如果trans表存在这个  wopsettlecurrency字段
            if "wopSettleCurrency" in trans_data["trans"]:
                # 当源清算币种和目标清算币种一致时计算interchangfee
                sett_amt = self.db_operations.sett_amount_outside("mop", evonet_number)
                trans_amt = self.db_operations.trans_amount_inside("mop", evonet_number)
                # 计算mop侧  interchangfee；共三种情况，这个参数是清算金额
                # mop侧 interchangfee 计费逻辑--------------------------------------
                self.mop_interchangfee_sett_fee_assert(trans_data, evonet_number,
                                                       cpm_interchange_fee_rate, mpm_interchange_fee_rate,
                                                       interchangefee_currency_decimal, model,
                                                       fileinit, sett_amt, table, wopid, mopid, recon_flag)

                # ----------------------------------------------------------------------------
                # 计算mop侧fxfee trans_fe;共三种情况
                # 最后一个擦拭农户sett_amt是 清算交易金额
                # 这个  settlecurrencyshi mop表配置的 settlecurrency
                if settle_currency == trans_data["settleInfo"]["settleCurrency"]:
                    self.mop_fx_trans_fee_sett_fee_assert(evonet_number, fx_process_fee_rate,
                                                          trans_process_fee_rate,
                                                          currency_decimal, sett_amt, trans_fee_method,
                                                          fx_fee_method,
                                                          trans_fee_calc_method, fx_fee_calc_method, table, wopid,
                                                          mopid)
                else:
                    # 当交易币种和 和配置表的清算币种一致时的情况，最后一个参数是交易金额
                    if settle_currency == trans_data["trans"]["transCurrency"]:
                        self.mop_fx_trans_fee_sett_fee_assert(evonet_number, fx_process_fee_rate,
                                                              trans_process_fee_rate,
                                                              currency_decimal, trans_amt, trans_fee_method,
                                                              fx_fee_method, trans_fee_calc_method,
                                                              fx_fee_calc_method,
                                                              table, wopid, mopid)
                    else:
                        # 当三个币种都不一致时
                        self.mop_fx_trans_three_fee_currency_assert(evonet_number, trans_process_fee_rate,
                                                                    fx_process_fee_rate, currency_decimal,
                                                                    settle_currency, mccr_rate, fileinit,
                                                                    trans_fee_method, fx_fee_method,
                                                                    trans_fee_calc_method, fx_fee_calc_method,
                                                                    table,
                                                                    wopid, mopid)

    def mop_interchangfee_sett_fee_assert(self, trans_data, evonet_number,
                                          cpm_interchange_fee_rate, mpm_interchange_fee_rate,
                                          interchangefee_currency_decimal, model,
                                          fileinit, sett_amt, table, wopid, mopid, recon_flag):
        interchange_fee = \
            self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop,
                                          {"trans.evonetOrderNumber": evonet_number})["settleInfo"][
                "interchangeFee"]
        # 直清模式 wop出文件，因为勾对的时候计算了interchangFee,所以不计算interchagnfee
        if fileinit == "wop":
            pass
        else:
            interchangefee_currency = \
                self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop, {"trans.wopID": wopid})["trans"][
                    "mopSettleCurrency"]

            interchangefee_currency_decimal = self.db_operations.get_currency_decimal("mop",
                                                                                      interchangefee_currency)
            # 直清模式 evonet 出文件
            if trans_data["trans"]["transType"] == "CPM Payment":
                cpm_interchange_fee = self.round_four_five(cpm_interchange_fee_rate * sett_amt,
                                                           interchangefee_currency_decimal)
                assert cpm_interchange_fee == interchange_fee
            if trans_data["trans"]["transType"] == "MPM Payment":
                mpm_interchange_fee = self.round_four_five(mpm_interchange_fee_rate * sett_amt,
                                                           interchangefee_currency_decimal)
                assert mpm_interchange_fee == interchange_fee

    def mop_fx_trans_fee_sett_fee_assert(self, evonet_number, fx_process_fee_rate,
                                         trans_process_fee_rate,
                                         currency_decimal, sett_amt, trans_fee_method, fx_fee_method,
                                         trans_fee_calc_method, fx_fee_calc_method, table, wopid, mopid):
        trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop, {"trans.mopID": mopid,
                                                                                              "trans.evonetOrderNumber": evonet_number})
        settle_info = trans_settle_data["settleInfo"]

        # trans_fee
        if trans_fee_method == "monthly" and trans_fee_calc_method == "accumulation":
            assert settle_info["processingFee"] == 0.0
        else:
            trans_process_fee = self.round_four_five(trans_process_fee_rate * sett_amt, currency_decimal)
            assert trans_process_fee == settle_info["processingFee"]
        # fx_trans_fee
        if fx_fee_method == "monthly" and fx_fee_calc_method == "accumulation":
            assert settle_info["fxProcessingFee"] == 0.0
        else:
            if trans_settle_data["trans"]["mopConverterCurrencyFlag"] == False:
                assert settle_info["fxProcessingFee"] == 0.00
            else:
                fx_process_fee = self.round_four_five(fx_process_fee_rate * sett_amt, currency_decimal)
                assert fx_process_fee == settle_info["fxProcessingFee"]

    def mop_fx_trans_three_fee_currency_assert(self, evonet_number, trans_process_fee_rate,
                                               fx_process_fee_rate, currency_decimal,
                                               settle_currency, mccr_rate, fileinit, trans_fee_method,
                                               fx_fee_method,
                                               trans_fee_calc_method, fx_fee_calc_method, table, wopid, mopid):
        trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop, {"trans.mopID": mopid,
                                                                                              "trans.evonetOrderNumber": evonet_number})
        settle_info = trans_settle_data["settleInfo"]
        # 当三个币种都不一致时计费
        mccr_rate = mccr_rate + 1
        # 当配置表中的清算币种和transSett.wop表中的清算币种不一致且和交易币种不一致是执行如下流程
        trans_currency = trans_settle_data["trans"]["transCurrency"]

        trans_amt = trans_settle_data["trans"]["transAmount"]
        if trans_fee_method == "monthly" and trans_fee_calc_method == "accumulation":
            assert settle_info["processingFee"] == 0.0
        else:
            fxrate_fee = self.sgp_config_db.get_one(self.common_name.fx_rate,
                                                    {"ccyPair": "{}/{}".format(trans_currency, settle_currency),
                                                     "fxRateOwner": "evonet"})["ask"]
            trans_process_fee = self.round_four_five(trans_process_fee_rate * trans_amt * fxrate_fee * mccr_rate,
                                                     currency_decimal)
            assert trans_process_fee == settle_info["processingFee"]
        if fx_fee_method == "monthly" and fx_fee_calc_method == "accumulation":
            assert settle_info["fxProcessingFee"] == 0.0
        else:
            if trans_settle_data["trans"]["mopConverterCurrencyFlag"] == False:
                assert settle_info["fxProcessingFee"] == 0.00
            else:
                fxrate_fee = self.sgp_config_db.get_one(self.common_name.fx_rate,
                                                        {"ccyPair": "{}/{}".format(trans_currency, settle_currency),
                                                         "fxRateOwner": "evonet"})["ask"]
                fx_process_fee = self.round_four_five(fx_process_fee_rate * trans_amt * fxrate_fee * mccr_rate,
                                                      currency_decimal)
                assert fx_process_fee == settle_info["fxProcessingFee"]

    def get_interchang_currency_decimal(self, owner_type, wopid, mopid, ):
        """
        :param owner_type: wop 节点，或者mop节点
        :param wopid:
        :param mopid:
        :return:
        """
        # table，wop 表或者mop 表
        if owner_type == "wop":
            db = self.tyo_config_db
            settle_info = db.get_one("wop", {"baseInfo.wopID": wopid})["settleInfo"]
        else:
            db = self.sgp_config_db
            settle_info = db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"]
        custom_info = db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})
        if "settleCurrency" in settle_info:
            inter_settle_currency = settle_info["settleCurrency"]
        if custom_info:
            if "settleCurrency" in custom_info:
                inter_settle_currency = custom_info["settleCurrency"]
        # 获取interchangefee清算金额的小数位
        interchangefee_currency_decimal = db.get_one("currency", {"code": inter_settle_currency})[
            "decimal"]
        return interchangefee_currency_decimal
        # wop表或者mop表肯定有配置，customizeconfig表不一定有配置

    def refund_interchange_fee_assert(self, owner_type, wopid, mopid):
        # table  wop或者mop
        # trans_set_table  transSettle.wop 或者 transSettle.mop表
        # 查找退款交易
        if owner_type == "wop":
            db = self.tyo_evosettle_db
            table = self.common_name.trans_settle_wop
        else:
            db = self.sgp_evosettle_db
            table = self.common_name.trans_settle_wop

        refund_data = db.get_many(table,
                                  {"trans.wopID": wopid, "trans.transType": "Refund"})
        for trans_data in refund_data:
            # 退款交易的 interchangfee和交易金额
            refund_interchange_fee = trans_data["settleInfo"]["interchangeFee"]
            clear_flag = trans_data["clearFlag"]
            fee_flag = trans_data["feeFlag"]
            refund_trans_amount = trans_data["trans"]["transAmount"]
            # 原交易的交易订单号，交易金额，interchangfee
            orig_evonet_number = trans_data["trans"]["originalEVONETOrderNumber"]
            orig_trans_amount = db.get_one(table,
                                           {"trans.wopID": wopid,
                                            "trans.evonetOrderNumber": orig_evonet_number})[
                "trans"]["transAmount"]

            # 原交易的interchangfee
            orig_interchange_fee = db.get_one(table,
                                              {"trans.wopID": wopid,
                                               "trans.evonetOrderNumber": orig_evonet_number})[
                "settleInfo"]["interchangeFee"]
            interchang_currenc_decial = self.get_interchang_currency_decimal("wop", wopid, mopid, )
            # 正确的interchangfee的计算
            if orig_interchange_fee == 0.0:
                assert refund_interchange_fee == 0.0
            else:
                correct_interchang_fee = self.round_four_five(
                    refund_trans_amount / orig_trans_amount * orig_interchange_fee, interchang_currenc_decial)
                assert refund_interchange_fee == correct_interchang_fee
            assert clear_flag == True
            assert fee_flag == True

    def get_wccr(self, wopid, mopid):
        # 当wop 或者mop表中没有对应的手续费时则去customizecofnig 获取手续费，即优先获取custom表的手续费
        service_fee_info = self.db_operations.custom_config_service_fee_info('mop', wopid, mopid)
        if service_fee_info:
            if "wccr" in service_fee_info:
                wccr_rate = service_fee_info["wccr"]
                return wccr_rate
        if "wccr" in service_fee_info:
            wccr_rate = service_fee_info["wccr"]
            return wccr_rate

    def get_wop_settle_currency_decimal(self, wopid, mopid):
        # 先去customizecofnig 获取手续费，即优先获取custom表的settlecurrency
        service_fee_info = self.tyo_config_db.get_one(self.common_name.custom_config,
                                                      {"wopID": wopid, "mopID": mopid})
        if service_fee_info:
            if "settleCurrency" in service_fee_info:
                settle_currency = service_fee_info["settleCurrency"]
                return self.db_operations.get_currency_decimal("wop", settle_currency)
        settle_info = self.tyo_evosettle_db.get_one("wop", {"baseInfo.wopID": wopid})["settleInfo"]
        if "settleCurrency" in settle_info:
            settle_currency = settle_info["settleCurrency"]
            return self.db_operations.get_currency_decimal("wop", settle_currency)

    def cpm_mpm_rebate_fee_assert(self, wopid, mopid):
        # rebate计算只会出现在  wop侧 的transSettle.wop
        forward_trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                            {"trans.wopID": wopid, "trans.transType": {
                                                                "$in": ["CPM Payment", "MPM Payment"]}})
        wccr_rate = self.get_wccr(wopid, mopid)
        for trans_data in forward_trans_data:
            # transSettle.wop表中的esettlmount和
            settle_amount = trans_data["settleInfo"]["settleAmount"]
            trans_rebate = trans_data["settleInfo"]["rebate"]
            currenc_decial = self.db_operations.get_currency_decimal("wop", trans_data["settleInfo"][
                "settleCurrency"])

            # 计算我们自己计算出rebate
            calc_rebate = self.round_four_five(settle_amount * wccr_rate / (1 + wccr_rate), currenc_decial)
            assert trans_rebate == calc_rebate
            assert trans_data["clearFlag"] == True
            assert trans_data["feeFlag"] == True

    def refund_rebate_fee_assert(self, wopid, ):
        # 退款 rebate 值的校验
        sett_table = self.common_name.trans_settle_wop
        refund_trans_data = self.tyo_evosettle_db.get_many(sett_table,
                                                           {"trans.wopID": wopid,
                                                            "trans.transType": "Refund"})

        for trans_data in refund_trans_data:
            orig_evonet_number = trans_data["trans"]["originalEVONETOrderNumber"]
            orig_trans_amount = self.tyo_evosettle_db.get_one(sett_table,
                                                              {"trans.wopID": wopid,
                                                               "trans.evonetOrderNumber": orig_evonet_number})[
                "trans"]["transAmount"]
            refund_trans_amount = trans_data["trans"]["transAmount"]
            orig_trans_rebate = self.tyo_evosettle_db.get_one(sett_table,
                                                              {"trans.wopID": wopid,
                                                               "trans.evonetOrderNumber": orig_evonet_number})[
                "settleInfo"]["rebate"]

            refund_trans_rebate = trans_data["settleInfo"]["rebate"]

            currenc_decial = self.db_operations.get_currency_decimal("wop", trans_data["settleInfo"][
                "settleCurrency"])

            # 计算我们自己计算出rebate
            calc_rebate = self.round_four_five(refund_trans_amount / orig_trans_amount * orig_trans_rebate,
                                               currenc_decial)
            assert refund_trans_rebate == calc_rebate
            assert trans_data["clearFlag"] == True
            assert trans_data["feeFlag"] == True

    def setlf_sett_assert(self, wopid, mopid, sett_date, table=None):
        # 自主清算的校验
        self_data = self.db_operations.get_self_sett_date(wopid, mopid, sett_date)
        for i in self_data:
            if i["clearFlag"] == True:
                assert i["blendType"] == "selfSettle"
                assert i["settleFlag"] == True
            else:
                assert i["blendType"] == "default"
                assert i["settleFlag"] == False

    def generate_wopid(self):
        return "WOP_SETT" + self.random_char()

    def generate_mopid(self):
        return "MOP_SETT" + self.random_char()

    def dual_db_init(self):
        # 删除以Wop_auto_walker  开头的wopid和mopid
        wopid = {"$regex": "^WOP_SETT"}
        mopid = {"$regex": "^MOP_SETT"}

        self.db_operations.delete_sftp_info(wopid)
        self.db_operations.delete_trans_file_wop_record(wopid, mopid)
        # 删除trans表记录
        self.db_operations.delete_trans_data(wopid, mopid)
        # 删除fileinfo记录
        self.db_operations.delete_direct_fileinfo(wopid, mopid)
        # 初始化config库的配置
        self.db_operations.delete_direct_single_config(wopid, mopid)
        # 删除transSett表的相关的数据
        self.db_operations.delet_trans_sett_table_data(wopid, mopid)
        # 删除日志
        self.db_operations.delete_settle_func_log(wopid, mopid)
        # 删除transSummary数据
        self.db_operations.delete_trans_summary(wopid, mopid)

        # 删除 wopNode数据
        self.db_operations.delete_trans_file_wop_node(wopid, mopid)

        # ------------

    def single_db_init(self, tyo, wopid, mopid, sett_date):
        tyo.delete_direct_fileinfo(wopid, mopid, sett_date)
        tyo.delete_trans_file_wop_record(wopid, mopid, sett_date)
        tyo.delete_fileinfo_file_wop(wopid, mopid, sett_date)
        # 删除transSett.wop表的相关的数据
        tyo.evosettle_db.delete_manys("transSettle.wop",
                                      {"trans.wopID": wopid, "trans.mopID": mopid,
                                       "settleDate": sett_date})
        # 删除transSett.mop和  transSett.wop表的相关数据
        tyo.delet_trans_sett_table_data("transSettle.mop", wopid, mopid, sett_date)
        tyo.delet_trans_sett_table_data("transSettle.wop", wopid, mopid, sett_date)

        tyo.delete_trans_file_wop_node(wopid, mopid, sett_date)
        # 删除日志
        tyo.delete_settle_func_log(wopid, mopid, sett_date)
        tyo.delete_trans_summary("transSummary.wop", wopid, mopid, )
        tyo.delete_trans_summary("transSummary.mop", wopid, mopid, )
        tyo.delete_file_info_service(wopid, mopid)

    def direct_wop_settlement_assert(self, local_path, wopid, sett_date, table_name, trans_fee_collection_method,
                                     fx_fee_collection_method, fxrebate_fee_collection_method):
        with open(local_path, "r", encoding="utf-8") as file:
            first_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            second_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            third_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            # (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0])
            fourth_line = file.readline().split(",")
            total_count_name, counts = first_line[0], first_line[1]
            total_settlement_amount, sett_amount_all = second_line[0], second_line[1]
            net_settlement_mount_name, net_amount_all = third_line[0], third_line[1]
            trans_sett_obj = self.db_operations.evosettle_db.get_many(table_name,
                                                                      {"trans.wopID": wopid,
                                                                       "settleDate": sett_date, "settleFlag": True})
            trans_sett_obj_counts = self.db_operations.evosettle_db.count(table_name,
                                                                          {"trans.wopID": wopid,
                                                                           "settleDate": sett_date,
                                                                           "settleFlag": True})

            if trans_sett_obj_counts == 0:
                # settlement details 空文件校验
                file.seek(0)
                first_line = file.readline().strip().encode('utf-8').decode('utf-8-sig')
                second_line = file.readline().strip()
                third_line = file.readline().strip()
                fourth_line = file.readline().strip()
                pass
                assert first_line == '"Total Count","0"'
                assert second_line == '"Total Settlement Amount","0"'  # "Total Settlement Amount","0.00"
                assert third_line == '"Total Net Settlement Amount","0"'  # "Total Net Settlement Amount","0.00"
                assert fourth_line == '"***NO DATA FOR THIS FILE***"'
            else:
                # 文件是 bom 文件
                # 校验第一行
                assert eval(total_count_name.encode('utf-8').decode('utf-8-sig')) == "Total Count"
                # 校验第二行
                assert total_settlement_amount == "Total Settlement Amount"
                # 校验第三行
                assert net_settlement_mount_name == "Total Net Settlement Amount"
                assert int(eval(counts)) == len(file.readlines())
                assert trans_sett_obj_counts == int(eval(counts))
                file.seek(0)  # 回首行
                for i in range(3):
                    file.readline()
                file_title = file.readline()
                if trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly":
                    title_demo = '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","EVONET Order Number","WOP Order Number","MOP Order Number","Transaction Type","MOP ID","MOP Name","Transaction Amount","Transaction Currency","Settlement Amount","Settlement Currency","Interchange Fee","Net Settlement Amount","Original EVONET Order Number","Original MOP Order Number","Store ID","Store English Name","Store Local Name","MCC","City","Country","Terminal Number"'

                # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
                assert title_demo.strip() == file_title.strip()
                # 校验文件中的数据
                settlement_data = file.readlines()
                # 生成的文件中的交易数据的校验

                file_settle_amount = 0
                file_net_settle_amount = 0
                for trans in trans_sett_obj:
                    for file_trans_data in settlement_data:
                        separator = "|||!@|||!@||!@|||"
                        if trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly":
                            data = separator.join(
                                (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                            evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, mop_order_number, transaction_type, \
                            mop_id, mop_name, transaction_amount, transaction_currency, settlement_amount, settlement_currency, interchange_fee, net_settlement_amount, original_evonet_order_number, \
                            original_mop_order_number, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                                separator)

                        if trans["trans"]["evonetOrderNumber"] == evonet_order_number:
                            if "wopOrderNumber" in trans["trans"]:
                                assert trans["trans"]["wopOrderNumber"] == wop_order_number
                            if "mopOrderNumber" in trans["trans"]:
                                assert trans["trans"]["mopOrderNumber"] == mop_order_number
                            if "transType" in trans["trans"]:
                                assert trans["trans"]["transType"] == transaction_type
                            if "mopID" in trans["trans"]:
                                assert trans["trans"]["mopID"] == mop_id
                            if "transAmount" in trans["trans"]:
                                transaction_amount = self.comm_funcs.amount_conver(transaction_amount)
                                m = trans["trans"]["transAmount"]
                                assert trans["trans"]["transAmount"] == transaction_amount
                            if "transCurrency" in trans["trans"]:
                                assert trans["trans"]["transCurrency"] == transaction_currency
                            # settlement 和interchangefee 根据不同的交易类型显示不同的正负号
                            if "settleAmount" in trans["settleInfo"]:
                                if trans["trans"]["transType"] in ["Refund", "Credit Adjustment"]:
                                    assert self.comm_funcs.amount_conver(settlement_amount) == trans["settleInfo"][
                                        "settleAmount"] * -1
                                if trans["trans"]["transType"] in ["CPM Payment", "MPM Payment",
                                                                   "Debit Adjustment"]:
                                    assert self.comm_funcs.amount_conver(settlement_amount) == trans["settleInfo"][
                                        "settleAmount"]
                                file_settle_amount += self.comm_funcs.amount_conver(settlement_amount)
                                file_net_settle_amount += self.comm_funcs.amount_conver(net_settlement_amount)
                            # interchangfee 小数位
                            if "settleCurrency" in trans["settleInfo"]:
                                assert settlement_currency == trans["settleInfo"]["settleCurrency"]
                            if "settleCurrency" in settle_info:
                                inter_settle_currency = settle_info["settleCurrency"]
                            if "settleCurrency" in self.db_operations.custom_settlement_info(wopid, mopid):
                                inter_settle_currency = self.db_operations.custom_settlement_info(wopid, mopid)[
                                    "settleCurrency"]
                            # 获取interchangefee清算金额的小数位
                            interchangefee_currency_decimal = self.db_operations.get_currency_decimal(
                                inter_settle_currency)
                            change_fee = trans["settleInfo"]["interchangeFee"]
                            change_fee = self.round_four_five(change_fee, interchangefee_currency_decimal)
                            if "interchangeFee" in trans["settleInfo"]:
                                if trans["trans"]["transType"] in ["CPM Payment", "MPM Payment",
                                                                   "Debit Adjustment"]:
                                    assert self.comm_funcs.amount_conver(interchange_fee) == change_fee * -1
                                if trans["trans"]["transType"] in ["Refund", "Credit Adjustment"]:
                                    assert self.comm_funcs.amount_conver(interchange_fee) == change_fee

                            if model == "evonet" and culated == "daily":
                                # transaction_processing_fee, fx_processing_fee, fx_rebate
                                if transaction_type in ["CPM Payment", "MPM Payment"]:
                                    assert self.comm_funcs.amount_conver(transaction_processing_fee) == \
                                           trans["settleInfo"][
                                               "processingFee"]
                                    assert self.comm_funcs.amount_conver(fx_processing_fee) == trans["settleInfo"][
                                        "fxProcessingFee"]
                                if transaction_type in ["Refund", "Credit Adjustment", "Debit Adjustment"]:
                                    assert self.comm_funcs.amount_conver(transaction_processing_fee) == 0.00
                                    assert self.comm_funcs.amount_conver(fx_processing_fee) == 0.00
                                if transaction_type in ["CPM Payment", "MPM Payment"]:
                                    assert self.comm_funcs.amount_conver(fx_rebate) == trans["settleInfo"][
                                        "rebate"] * -1
                                if transaction_type in ["Refund", "Credit Adjustment"]:
                                    assert self.comm_funcs.amount_conver(fx_rebate) == trans["settleInfo"]["rebate"]

                            if "originalEVONETOrderNumber" in trans["trans"]:
                                assert trans["trans"]["originalEVONETOrderNumber"] == original_evonet_order_number
                            if "originalMOPOrderNumber" in trans["trans"]:
                                assert trans["trans"]["originalMOPOrderNumber"] == original_mop_order_number
                            # 校验storeinfo信息
                            if "storeInfo" in trans["trans"]:
                                store_info = trans["trans"]["storeInfo"]
                                if "id" in store_info:
                                    assert store_id == store_info["id"]
                                if "englishName" in store_info:
                                    assert store_english_name == store_info["englishName"]
                                if "localName" in store_info:
                                    assert store_local_name == store_info["localName"]
                                if "mcc" in store_info:
                                    assert mcc == store_info["mcc"]
                                if "city" in store_info:
                                    assert city == store_info["city"]
                                if "country" in store_info:
                                    assert country == store_info["country"]
                                if "terminalNumber" in store_info:
                                    assert terminal_number == store_info["terminalNumber"]
                # 计算表中的两个金额计算正确;
                assert file_net_settle_amount == self.comm_funcs.amount_conver(net_amount_all)
                assert file_settle_amount == self.comm_funcs.amount_conver(sett_amount_all)
        os.remove(local_path)

    def wop_settlement_daily_detail_assert(self, local_path, wopid, sett_date, model, trans_fee_collection_method,
                                           fx_fee_collection_method, fxrebate_fee_collection_method):
        table_name = "transSettle.wop"
        with open(local_path, "r", encoding="utf-8") as file:
            first_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            second_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            third_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            fourth_line = file.readline().split(",")
            total_count_name, counts = first_line[0], first_line[1]
            total_settlement_amount, sett_amount_all = second_line[0], second_line[1]
            net_settlement_mount_name, net_amount_all = third_line[0], third_line[1]
            # 应该出的数据的数量
            trans_sett_obj_counts = self.tyo_evosettle_db.count(table_name,
                                                                {"trans.wopID": wopid,
                                                                 "settleDate": sett_date, "settleFlag": True})

            if trans_sett_obj_counts == 0:
                # settlement details 空文件校验
                file.seek(0)
                first_line = file.readline().strip().encode('utf-8').decode('utf-8-sig')
                second_line = file.readline().strip()
                third_line = file.readline().strip()
                fourth_line = file.readline().strip()
                assert first_line == '"Total Count","0"'
                assert second_line == '"Total Settlement Amount","0"'  # "Total Settlement Amount","0.00"
                assert third_line == '"Total Net Settlement Amount","0"'  # "Total Net Settlement Amount","0.00"
                assert fourth_line == '"***NO DATA FOR THIS FILE***"'
            else:
                # 文件是 bom 文件
                # 校验第一行
                assert total_count_name == "Total Count"
                # 校验第二行
                assert total_settlement_amount == "Total Settlement Amount"
                # 校验第三行
                assert net_settlement_mount_name == "Total Net Settlement Amount"
                assert int(eval(counts)) == len(file.readlines())
                assert trans_sett_obj_counts == int(counts)
                file.seek(0)  # 回首行
                for i in range(3):
                    file.readline()
                file_title = file.readline()
                # 费率收取方式
                # daily daily daily #
                # monthly monthly daily #
                # monthly daily monthly #
                # monthly daily daily#
                # daily monthly monthly #
                # daily monthly daily  #
                # daily daily monthly #

                title_demo = self.get_config.get_ini("daily_daily_daily_title")
                # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
                assert title_demo.strip() == file_title.strip()
                # 校验文件中的数据
                settlement_data = file.readlines()
                # 生成的文件中的交易数据的校验

                file_settle_amount = Decimal(str(0))
                file_net_settle_amount = Decimal(str(0))
                conten_count = 0
                for file_trans_data in settlement_data:
                    conten_count += 1
                    separator = "||@||"
                    data = separator.join(
                        (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                    evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, mop_order_number, transaction_type, \
                    mop_id, mop_name, transaction_amount, transaction_currency, settlement_amount, settlement_currency, interchange_fee, trans_fee, fx_fee, fxrebate, net_settlement_amount, original_evonet_order_number, \
                    original_mop_order_number, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                        separator)

                    trans = self.tyo_evosettle_db.get_one(table_name,
                                                          {"trans.evonetOrderNumber": evonet_order_number})
                    config_mop_name = \
                        self.tyo_config_db.get_one("mop", {"baseInfo.mopID": mop_id})["baseInfo"]["mopName"]

                    assert trans["trans"]["wopOrderNumber"] == wop_order_number
                    assert trans["trans"]["mopOrderNumber"] == mop_order_number
                    assert trans["trans"]["transType"] == transaction_type
                    assert trans["trans"]["mopID"] == mop_id
                    assert mop_name == config_mop_name
                    assert trans["trans"]["transAmount"] == self.comm_funcs.amount_conver(transaction_amount)
                    assert trans["trans"]["transCurrency"] == transaction_currency
                    # 计费字段校验逻辑 https://ciloa.feishu.cn/sheets/shtcnqbEdYOYWIY3ofvjT1QpkZg?sheet=Jx9nQk
                    # settlement 和interchangefee 根据不同的交易类型显示不同的正负号
                    if trans["trans"]["transType"] in ["Refund"]:
                        assert self.comm_funcs.amount_conver(settlement_amount) == trans["settleInfo"][
                            "settleAmount"] * -1
                        assert self.comm_funcs.amount_conver(interchange_fee) == trans["settleInfo"][
                            "interchangeFee"]
                    if trans["trans"]["transType"] in ["CPM Payment", "MPM Payment", ]:
                        assert self.comm_funcs.amount_conver(settlement_amount) == abs(trans["settleInfo"][
                                                                                           "settleAmount"])
                        assert self.comm_funcs.amount_conver(interchange_fee) == trans["settleInfo"][
                            "interchangeFee"] * -1

                    # net_settlement的校验
                    net_amount = Decimal(str(self.comm_funcs.amount_conver(interchange_fee))) + Decimal(
                        str(self.comm_funcs.amount_conver(
                            settlement_amount)))
                    if trans_fee_collection_method == "daily":
                        net_amount += Decimal(str(self.comm_funcs.amount_conver(trans_fee)))
                    if fx_fee_collection_method == "daily":
                        net_amount += Decimal(str(self.comm_funcs.amount_conver(fx_fee)))
                    if model == "evonet":
                        net_amount += Decimal(str(self.comm_funcs.amount_conver(fxrebate)))
                    assert self.comm_funcs.amount_conver(net_settlement_amount) == float(net_amount)
                    file_settle_amount += Decimal(str(self.comm_funcs.amount_conver(settlement_amount)))
                    file_net_settle_amount += Decimal(str(self.comm_funcs.amount_conver(net_settlement_amount)))
                    assert settlement_currency == trans["settleInfo"]["settleCurrency"]

                    # interchangFee的值的校验
                    if trans["trans"]["transType"] in ["CPM Payment", "MPM Payment", ]:
                        assert self.comm_funcs.amount_conver(interchange_fee) == trans["settleInfo"][
                            "interchangeFee"] * -1
                    if trans["trans"]["transType"] in ["Refund", ]:
                        assert self.comm_funcs.amount_conver(interchange_fee) == abs(
                            trans["settleInfo"]["interchangeFee"])
                    # ------------------
                    if trans_fee_collection_method == "daily":
                        #     # transaction_processing_fee, fx_processing_fee, fx_rebate
                        if transaction_type in ["CPM Payment", "MPM Payment"]:
                            assert self.comm_funcs.amount_conver(trans_fee) == \
                                   trans["settleInfo"]["processingFee"]

                        if transaction_type in ["Refund", "Credit Adjustment", "Debit Adjustment"]:
                            assert self.comm_funcs.amount_conver(trans_fee) == 0.00
                    # ------------------
                    if fx_fee_collection_method == "daily":
                        #     # transaction_processing_fee, fx_processing_fee, fx_rebate
                        if transaction_type in ["CPM Payment", "MPM Payment"]:
                            assert self.comm_funcs.amount_conver(fx_fee) == trans["settleInfo"][
                                "fxProcessingFee"]
                        if transaction_type in ["Refund", "Credit Adjustment", "Debit Adjustment"]:
                            assert self.comm_funcs.amount_conver(fx_fee) == 0.00

                    # ------------------
                    if model == self.common_name.evonet:
                        if transaction_type in ["CPM Payment", "MPM Payment"]:
                            assert self.comm_funcs.amount_conver(fxrebate) == trans["settleInfo"][
                                "rebate"] * -1
                        if transaction_type in ["Refund", "Credit Adjustment"]:
                            assert self.comm_funcs.amount_conver(fxrebate) == trans["settleInfo"]["rebate"]
                    # 当手续费是按月收取时的手续费的取值
                    # ------------------

                    if trans_fee_collection_method == "monthly":
                        assert trans_fee == ""
                    # ------------------
                    if fx_fee_collection_method == "monthly":
                        assert fx_fee == ""

                    # ------------------
                    if model == self.common_name.bilateral:
                        assert fxrebate == ""

                    if transaction_type == "Refund":
                        assert trans["trans"]["originalEVONETOrderNumber"] == original_evonet_order_number
                        assert trans["trans"]["originalMOPOrderNumber"] == original_mop_order_number
                    # 校验storeinfo信息
                    store_info = trans["trans"]["storeInfo"]
                    if "id" in store_info:
                        assert store_id == store_info["id"]
                    if "englishName" in store_info:
                        assert store_english_name == store_info["englishName"]
                    if "localName" in store_info:
                        assert store_local_name == store_info["localName"]
                    if "mcc" in store_info:
                        assert mcc == store_info["mcc"]
                    if "city" in store_info:
                        assert city == store_info["city"]
                    if "country" in store_info:
                        assert country == store_info["country"]
                    if "terminalNumber" in store_info:
                        assert terminal_number == store_info["terminalNumber"]

                # 校验确实校验了文件中的数据
                assert conten_count == int(eval(counts))
                # # 计算表中的两个金额计算正确;
                assert float(file_net_settle_amount) == self.comm_funcs.amount_conver(net_amount_all)
                assert float(file_settle_amount) == self.comm_funcs.amount_conver(sett_amount_all)

    def upi_summary_assert(self, local_path, wopid, mopid, sett_date, settle_currency):
        # 每日Sumamry,title，header的相关校验
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取
        # 校验title格式
        assert table.cell_value(5, 0) == "Settlement Summary Report for UnionPay Transaction"
        assert table.cell_value(7, 0) == "Report ID:"
        report_id = wopid + "-Settlement-Summary-" + mopid + "-" + settle_currency + "-" + sett_date + "-001"
        assert table.cell_value(7, 3) == report_id
        assert table.cell_value(9, 0) == "WOP Name:"
        assert table.cell_value(9, 3) == wopid
        assert table.cell_value(10, 0) == "WOP ID:"
        assert table.cell_value(10, 3) == wopid
        assert table.cell_value(12, 0) == "Total Net Settlement Amount:"
        assert table.cell_value(13, 0) == "Settlement Currency:"

        demo_title = ['Scheme', 'Transaction Type', 'Transaction Currency', 'Counts', 'Transaction Amount',
                      'Settlement Amount', 'Fee Receivable', 'Fee Payable', 'Net Settlement Amount']
        assert table.cell_value(13, 3) == settle_currency
        file_title = []
        for i in range(9):
            file_title.append(table.cell_value(15, i))
        assert file_title == demo_title
        content_list = []

        for i in range(16, 34):
            for j in range(1, 9):
                content_list.append(table.cell_value(i, j))
        assert table.cell_value(12, 3) == table.cell_value(33, 8)
        if settle_currency == "CNY":
            assert content_list == self.common_name.upi_daily_summary_cny_content
        if settle_currency == "JPY":
            assert content_list == self.common_name.upi_daily_summary_jpy_content

    def upi_servicefee_assert(self, local_path, wopid, mopid, settle_date, calc_method):
        # 每日Sumamry,title，header的相关校验
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取
        # 校验title格式
        assert table.cell_value(5, 0) == "EVONET Service Fee Report (WOP)"
        assert table.cell_value(7, 0) == "Report ID:"
        report_id = "{}-ServiceFee-Summary-{}-{}-001".format(wopid, mopid, settle_date)
        assert table.cell_value(7, 3) == report_id
        assert table.cell_value(9, 0) == "WOP Name:"
        assert table.cell_value(9, 3) == wopid
        assert table.cell_value(10, 0) == "WOP ID:"
        assert table.cell_value(10, 3) == wopid
        assert table.cell_value(12, 0) == "Total Service Fee:"
        assert table.cell_value(13, 0) == "Service Fee Currency:"

        demo_title = ['Scheme', 'Transaction Type', 'Transaction Currency', 'Counts', 'Transaction Amount',
                      "Transaction Processing Fee"]
        assert table.cell_value(13, 3) == "CNY"
        file_title = []
        for i in range(6):
            file_title.append(table.cell_value(15, i))
        assert file_title == demo_title
        content_list = []
        assert table.cell_value(12, 3) == table.cell_value(24, 5)
        for i in range(16, 25):
            for j in range(1, 6):
                content_list.append(table.cell_value(i, j))
        if calc_method == "single":
            assert content_list == self.common_name.upi_servicefee_single_content
        if calc_method == "accumulation":
            assert content_list == self.common_name.upi_servicefee_accumulation_content

    def mop_daily_summary_assert(self, local_path, mopid, sett_date, model, trans_fee_collection_method,
                                 fx_fee_collection_method, wopid=None):
        # 每日Sumamry,title，header的相关校验
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取

        # 校验title格式
        assert table.cell_value(5, 0) == "EVONET Settlement Summary Report (MOP)"
        assert table.cell_value(7, 0) == "Report ID:"
        if model == "evonet":
            wopid = "EVONET-"
        else:
            mopid = mopid
        report_id = mopid + "-Settlement-Summary-" + wopid + sett_date + "-001"
        assert table.cell_value(7, 3) == report_id

        assert table.cell_value(9, 0) == "MOP Name:"
        # assert table.cell_value(9, 3) == self.get_wop_name(wopid)

        assert table.cell_value(10, 0) == "MOP ID:"
        assert table.cell_value(10, 3) == mopid

        assert table.cell_value(12, 0) == "Total Net Settlement Amount:"

        assert table.cell_value(13, 0) == "Settlement Currency:"
        settle_currency = "CNY"
        assert table.cell_value(13, 3) == settle_currency
        demo_title = ['WOP Name', 'Transaction Type', 'Transaction Currency', '', 'Counts', 'Transaction Amount',
                      'Settlement Amount', 'Interchange Fee', 'Transaction\nProcessing Fee', 'FX Processing Fee',
                      'Net Settlement Amount']
        file_title = []
        for i in range(11):
            file_title.append(table.cell_value(15, i))

        assert file_title == demo_title
        # 根据 wopid 获取mopid list
        wopid_set = set()
        summary_trans = self.sgp_evosettle_db.get_many(self.common_name.trans_summary_mop, {"mopID": mopid})
        for i in summary_trans:
            wopid_set.add(i["wopID"])
        # mopid排序并校验
        wopid_list = list(wopid_set)
        wopid_list.sort()
        assert table.cell_value(16, 0) == \
               self.sgp_config_db.get_one("wop", {"baseInfo.wopID": wopid_list[0]})["baseInfo"]["wopName"]
        # 第二个mopid assert
        assert table.cell_value(24, 0) == \
               self.sgp_config_db.get_one("wop", {"baseInfo.wopID": wopid_list[1]})["baseInfo"]["wopName"]
        self.mop_summary_content_assert(table, settle_currency, mopid, wopid_list, trans_fee_collection_method,
                                        fx_fee_collection_method)

    def wop_daily_summary_assert(self, local_path, wopid, mopid_list, sett_date, trans_fee_collection_method,
                                 fx_fee_collection_method, fxrebate_fee_collection_method):
        # 每日Sumamry,title，header的相关校验
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取

        # 校验title格式
        assert table.cell_value(5, 0) == "EVONET Settlement Summary Report (WOP)"
        assert table.cell_value(7, 0) == "Report ID:"

        mopid = "EVONET"
        report_id = wopid + "-Settlement-Summary-" + mopid + "-" + sett_date + "-001"
        assert table.cell_value(7, 3) == report_id

        assert table.cell_value(9, 0) == "WOP Name:"

        assert table.cell_value(10, 0) == "WOP ID:"
        assert table.cell_value(10, 3) == wopid

        assert table.cell_value(12, 0) == "Total Net Settlement Amount:"

        assert table.cell_value(13, 0) == "Settlement Currency:"
        settle_currency = "CNY"
        assert table.cell_value(13, 3) == settle_currency
        demo_title = ['MOP Name', 'Transaction Type', 'Transaction Currency', 'Counts', 'Transaction Amount',
                      'Settlement Amount',
                      'Interchange Fee', 'Transaction\nProcessing Fee', 'FX Processing Fee', 'FX Rebate',
                      'Net Settlement Amount']

        file_title = []
        for i in range(11):
            file_title.append(table.cell_value(15, i))
        assert file_title == demo_title
        self.wop_summary_content_assert(table, settle_currency, wopid, mopid_list, trans_fee_collection_method,
                                        fx_fee_collection_method, fxrebate_fee_collection_method, )

    def wop_summary_content_assert(self, table, settle_currency, wopid, mopid_list, trans_fee_collection_method,
                                   fx_fee_collection_method, fxrebate_fee_collection_method, ):
        demo_trans_types = ["CPM Payment", "MPM Payment", "Refund", "Sub-Total"]
        file_trans_type = []
        for i in range(16, 20):
            file_trans_type.append(table.cell_value(i, 1))
        assert file_trans_type == demo_trans_types
        # 校验第一个mopid的交易币种为CNY的数据进行校验
        total_sum_count = 0
        total_sum_transaction_amount = 0
        total_sum_settle_amount = 0
        total_sum_interchang_fee = 0
        total_sum_net_settlement = 0
        count = 0
        header_length = 16
        while count < 4:
            trans_type_lenth = len(demo_trans_types)
            if count == 0 or count == 2:
                trans_currency = "CNY"
            else:
                trans_currency = "JPY"
            if count in [0, 1]:
                mopid = mopid_list[0]
            else:
                mopid = mopid_list[1]
            sum_count = 0
            sum_transaction_amount = 0
            sum_settle_amount = 0
            sum_interchang_fee = 0
            sum_trans_fee = 0
            sum_fx_fee = 0
            sum_fx_rebate = 0
            sum_net_settle_amount = 0
            for i in range(header_length, header_length + trans_type_lenth - 1):
                assert table.cell_value(header_length, 2) == trans_currency
                trans_type = table.cell_value(i, 1)
                cny_data = self.tyo_evosettle_db.get_one(self.common_name.trans_summary_wop, {"wopID": wopid,
                                                                                              "mopID": mopid,
                                                                                              "summary.transCurrency": trans_currency,
                                                                                              "summary.transType": trans_type
                    , })["summary"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 3)) == cny_data["counts"]  # 校验数量
                sum_count += cny_data["counts"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 4)) == cny_data["transAmount"]
                sum_transaction_amount += cny_data["transAmount"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 5)) == cny_data["settleAmount"]
                sum_settle_amount += cny_data["settleAmount"]
                if trans_fee_collection_method == "monthly":
                    assert table.cell_value(i, 7) == "-"
                if fx_fee_collection_method == "monthly":
                    assert table.cell_value(i, 8) == "-"
                if fxrebate_fee_collection_method == "monthly":
                    assert table.cell_value(i, 9) == "-"

                if trans_fee_collection_method == "daily":
                    assert self.comm_funcs.amount_conver(table.cell_value(i, 7)) == cny_data["transProcessingFee"]
                    sum_trans_fee += cny_data["transProcessingFee"]
                if fx_fee_collection_method == "daily":
                    assert self.comm_funcs.amount_conver(table.cell_value(i, 8)) == cny_data["fxProcessingFee"]
                    sum_fx_fee += cny_data["fxProcessingFee"]
                if fxrebate_fee_collection_method == "daily":
                    assert self.comm_funcs.amount_conver(table.cell_value(i, 9)) == cny_data["fxRebate"]
                    sum_fx_rebate += cny_data["fxRebate"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 6)) == cny_data["interchangeFee"]
                sum_interchang_fee += cny_data["interchangeFee"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 10)) == cny_data["netSettleAmount"]
                sum_net_settle_amount += cny_data["netSettleAmount"]

            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 3)) == sum_count
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 4)) == sum_transaction_amount
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 5)) == sum_settle_amount
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 6)) == self.round_four_five(
                sum_interchang_fee, self.db_operations.get_currency_decimal("wop", settle_currency))
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 10)) == self.round_four_five(
                sum_net_settle_amount, self.db_operations.get_currency_decimal("wop", settle_currency))

            total_sum_count += sum_count
            total_sum_transaction_amount += sum_transaction_amount
            total_sum_settle_amount += sum_settle_amount
            total_sum_interchang_fee += sum_interchang_fee
            total_sum_net_settlement += self.round_four_five(
                sum_net_settle_amount, self.db_operations.get_currency_decimal("wop", settle_currency))
            if trans_fee_collection_method == "monthly":
                assert table.cell_value(i + 1, 7) == "-"
            if fx_fee_collection_method == "monthly":
                assert table.cell_value(i + 1, 8) == "-"
            if fxrebate_fee_collection_method == "monthly":
                assert table.cell_value(i + 1, 9) == "-"

            if trans_fee_collection_method == "daily":
                assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 7)) == sum_trans_fee
            if fx_fee_collection_method == "daily":
                assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 8)) == sum_fx_fee
            if fxrebate_fee_collection_method == "daily":
                assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 9)) == sum_fx_rebate
            header_length += trans_type_lenth
            count += 1
        # 最后total一行的校验
        assert table.cell_value(i + 2, 0) == "Total"
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 3)) == total_sum_count
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 5)) == total_sum_settle_amount
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 6)) == self.round_four_five(
            total_sum_interchang_fee, self.db_operations.get_currency_decimal("wop", settle_currency))
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 10)) == self.round_four_five(
            total_sum_net_settlement, self.db_operations.get_currency_decimal("wop", settle_currency))

    def mop_summary_content_assert(self, table, settle_currency, mopid, wopid_list, trans_fee_collection_method,
                                   fx_fee_collection_method):
        demo_trans_types = ["CPM Payment", "MPM Payment", "Refund", "Sub-Total"]
        file_trans_type = []
        for i in range(16, 20):
            file_trans_type.append(table.cell_value(i, 1))
        assert file_trans_type == demo_trans_types
        # 校验第一个mopid的交易币种为CNY的数据进行校验
        total_sum_count = 0
        total_sum_transaction_amount = 0
        total_sum_settle_amount = 0
        total_sum_interchang_fee = 0
        total_sum_net_settlement = 0
        count = 0
        header_length = 16
        while count < 4:
            trans_type_lenth = len(demo_trans_types)
            if count == 0 or count == 2:
                trans_currency = "CNY"
            else:
                trans_currency = "JPY"
            if count in [0, 1]:
                wopid = wopid_list[0]
            else:
                wopid = wopid_list[1]
            sum_count = 0
            sum_transaction_amount = 0
            sum_settle_amount = 0
            sum_interchang_fee = 0
            sum_trans_fee = 0
            sum_fx_fee = 0
            sum_net_settle_amount = 0
            for i in range(header_length, header_length + trans_type_lenth - 1):
                assert table.cell_value(header_length, 2) == trans_currency
                trans_type = table.cell_value(i, 1)
                cny_data = self.sgp_evosettle_db.get_one(self.common_name.trans_summary_mop, {"wopID": wopid,
                                                                                              "mopID": mopid,
                                                                                              "summary.transCurrency": trans_currency,
                                                                                              "summary.transType": trans_type
                    , })["summary"]
                assert float(table.cell_value(i, 4)) == cny_data["counts"]  # 校验数量
                sum_count += cny_data["counts"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 5)) == cny_data["transAmount"]
                sum_transaction_amount += cny_data["transAmount"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 6)) == cny_data["settleAmount"]
                sum_settle_amount += cny_data["settleAmount"]
                if trans_fee_collection_method == "monthly":
                    assert table.cell_value(i, 8) == "-"
                if fx_fee_collection_method == "monthly":
                    assert table.cell_value(i, 9) == "-"

                if trans_fee_collection_method == "daily":
                    assert self.comm_funcs.amount_conver(table.cell_value(i, 8)) == cny_data["transProcessingFee"]
                    sum_trans_fee += cny_data["transProcessingFee"]
                if fx_fee_collection_method == "daily":
                    assert self.comm_funcs.amount_conver(table.cell_value(i, 9)) == cny_data["fxProcessingFee"]
                    sum_fx_fee += cny_data["fxProcessingFee"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 7)) == cny_data["interchangeFee"]
                sum_interchang_fee += cny_data["interchangeFee"]
                assert self.comm_funcs.amount_conver(table.cell_value(i, 10)) == cny_data["netSettleAmount"]
                sum_net_settle_amount += cny_data["netSettleAmount"]

            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 4)) == sum_count
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 5)) == sum_transaction_amount
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 6)) == sum_settle_amount
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 7)) == self.round_four_five(
                sum_interchang_fee, self.db_operations.get_currency_decimal("wop", settle_currency))
            assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 10)) == self.round_four_five(
                sum_net_settle_amount, self.db_operations.get_currency_decimal("wop", settle_currency))

            total_sum_count += sum_count
            total_sum_transaction_amount += sum_transaction_amount
            total_sum_settle_amount += sum_settle_amount
            total_sum_interchang_fee += sum_interchang_fee
            total_sum_net_settlement += self.round_four_five(
                sum_net_settle_amount, self.db_operations.get_currency_decimal("wop", settle_currency))
            if trans_fee_collection_method == "monthly":
                assert table.cell_value(i + 1, 8) == "-"
            if fx_fee_collection_method == "monthly":
                assert table.cell_value(i + 1, 9) == "-"

            if trans_fee_collection_method == "daily":
                assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 8)) == sum_trans_fee
            if fx_fee_collection_method == "daily":
                assert self.comm_funcs.amount_conver(table.cell_value(i + 1, 9)) == sum_fx_fee
            header_length += trans_type_lenth
            count += 1
        # 最后total一行的校验
        assert table.cell_value(i + 2, 0) == "Total"
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 4)) == total_sum_count
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 6)) == total_sum_settle_amount
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 7)) == self.round_four_five(
            total_sum_interchang_fee, self.db_operations.get_currency_decimal("wop", settle_currency))
        assert self.comm_funcs.amount_conver(table.cell_value(i + 2, 10)) == self.round_four_five(
            total_sum_net_settlement, self.db_operations.get_currency_decimal("wop", settle_currency))

    def wop_daily_service_assert(self, local_path, trans_fee_collection_method,
                                 fx_fee_collection_method,
                                 fxrebate_fee_collection_method,
                                 trans_fee_calcu_method, fx_fee_calcu_method):
        """
        :param local_path:   文件名称
        :param trans_fee_collection_method:     monthly,daily  收取手续费的方式
        :param fx_fee_collection_method:        monthly,daily  收取手续费的方式
        :param fxrebate_fee_collection_method:  monthly,daily  收取手续费的方式
        :param trans_fee_calculate_method:      single,accumulation  每笔交易计费，清算金额计费
        :param fx_fee_calculate_method:         single,accumulation  每笔交易计费，清算金额计费
        :param fxrebate_fee_calculate_method:   single,accumulation  每笔交易计费，清算金额计费
        :return:
        """
        # 月报按照每日的数据校验一遍
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取
        self.wop_daily_service_content_assert(table, trans_fee_collection_method,
                                              fx_fee_collection_method,
                                              fxrebate_fee_collection_method,
                                              trans_fee_calcu_method, fx_fee_calcu_method)

    def wop_daily_service_content_assert(self, table, trans_fee_collection_method,
                                         fx_fee_collection_method,
                                         fxrebate_fee_collection_method,
                                         trans_fee_calcu_method, fx_fee_calcu_method):

        # 先做出demo,然后再assert
        content_list = []
        for i in range(15, 33):
            for j in range(1, 9):
                content_list.append(table.cell_value(i, j))  # accumulation
        if trans_fee_collection_method == "daily" and fx_fee_collection_method == "daily" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_daily_daily_monthly_single_single

        elif trans_fee_collection_method == "daily" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_daily_monthly_daily_single_single

        elif trans_fee_collection_method == "daily" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_wop_daily_monthly_daily_single_accumulation

        elif trans_fee_collection_method == "daily" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_daily_monthly_monthly_single_single

        elif trans_fee_collection_method == "daily" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_wop_daily_monthly_monthly_single_accumulation

        # ------------
        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "daily" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_daily_daily_single_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "daily" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_daily_daily_accumulation_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "daily" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_daily_monthly_single_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "daily" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_daily_monthly_accumulation_single

        # --------------------------------------
        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_daily_single_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_daily_single_accumulation

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_daily_accumulation_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "daily" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_daily_accumulation_accumulation

        # -------------------
        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_monthly_single_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_monthly_single_accumulation

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_monthly_accumulation_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and fxrebate_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_wop_monthly_monthly_monthly_accumulation_accumulation

    def mop_daily_service_content_assert(self, table, trans_fee_collection_method,
                                         fx_fee_collection_method,
                                         trans_fee_calcu_method, fx_fee_calcu_method):

        # 先做出demo,然后再assert
        content_list = []
        for i in range(15, 33):
            for j in range(1, 9):
                content_list.append(table.cell_value(i, j))  # accumulation
        if trans_fee_collection_method == "daily" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_mop_service_daily_monthly_single_single

        elif trans_fee_collection_method == "daily" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_mop_service_daily_monthly_single_accumulation


        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "daily" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_mop_service_monthly_daily_accumulation_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "daily" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_mop_service_monthly_daily_single_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.evonet_mop_service_monthly_monthly_accumulation_accumulation

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_mop_service_monthly_monthly_accumulation_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_mop_service_monthly_monthly_single_accumulation

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.evonet_mop_service_monthly_monthly_single_single

    def bilateral_mop_service_content_assert(self, local_path,
                                             trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method):

        # 先做出demo,然后再assert
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取
        content_list = []
        for i in range(15, 25):
            for j in range(1, 9):
                content_list.append(table.cell_value(i, j))  # accumulation
        if trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.bilateral_mop_service_monthly_monthly_accumulation_accumulation

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.bilateral_mop_service_monthly_monthly_accumulation_single

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.bilateral_mop_service_monthly_monthly_single_accumulation

        elif trans_fee_collection_method == "monthly" and fx_fee_collection_method == "monthly" and trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.bilateral_mop_service_monthly_monthly_single_single

    def bilateral_wop_service_content_assert(self, local_path,
                                             trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method):

        # 先做出demo,然后再assert
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取
        content_list = []
        for i in range(15, 25):
            for j in range(1, 9):
                content_list.append(table.cell_value(i, j))  # accumulation
        if trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "accumulation":
            assert content_list == self.common_name.bilateral_wop_service_monthly_monthly_accumulation_accumulation

        elif trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.bilateral_wop_service_monthly_monthly_accumulation_single

        elif trans_fee_calcu_method == "accumulation" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.bilateral_wop_service_monthly_monthly_single_accumulation

        elif trans_fee_calcu_method == "single" and fx_fee_calcu_method == "single":
            assert content_list == self.common_name.bilateral_wop_service_monthly_monthly_single_single

    def mop_daily_service_assert(self, mopid, local_path, sett_date, trans_fee_collection_method,
                                 fx_fee_collection_method,
                                 trans_fee_calcu_method, fx_fee_calcu_method):
        """
        :param local_path:   文件名称
        :param wopid:        wopid
        :param sett_date:
        :param model:        清算模式
        :param trans_fee_collection_method:     monthly,daily  收取手续费的方式
        :param fx_fee_collection_method:        monthly,daily  收取手续费的方式
        :param fxrebate_fee_collection_method:  monthly,daily  收取手续费的方式
        :param trans_fee_calculate_method:      single,accumulation  每笔交易计费，清算金额计费
        :param fx_fee_calculate_method:         single,accumulation  每笔交易计费，清算金额计费
        :param fxrebate_fee_calculate_method:   single,accumulation  每笔交易计费，清算金额计费
        :param mopid:                           直清模式时mopid
        :return:
        """
        # 月报按照每日的数据校验一遍
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]  # 通过索引顺序获取

        self.mop_daily_service_content_assert(table, trans_fee_collection_method,
                                              fx_fee_collection_method,
                                              trans_fee_calcu_method, fx_fee_calcu_method)

    def direct_mop_resolve_assert(self, local_path, wopid, mopid, model):
        # 直清模式 一 wop生成的文件解析到mop侧 transfile.wopNode的校验
        with open(local_path, "r", encoding="utf-8") as file:
            file.seek(0)  # 回首行
            for i in range(4):
                file.readline()

            # # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
            # 获取文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验
            trans_sett_obj = self.db_operations.evosettle_db.get_many("transFile.wopNode",
                                                                      {"wopID": wopid, "mopID": mopid,
                                                                       })
            m = 0
            for i in trans_sett_obj:
                m = m + 1
            assert len(settlement_data) == m  # 校验解析的数据的数量正确
            for trans in trans_sett_obj:
                for file_trans_data in settlement_data:
                    separator = "|||!@|||!@||!@|||"
                    if model == "evonet":
                        data = separator.join(
                            (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                        evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, mop_order_number, transaction_type, \
                        mop_id, mop_name, transaction_amount, transaction_currency, settlement_amount, settlement_currency, interchange_fee, \
                        transaction_processing_fee, fx_processing_fee, fx_rebate, net_settlement_amount, original_evonet_order_number, \
                        original_mop_order_number, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                            separator)
                    else:
                        data = separator.join(
                            (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                        self.assert_file_date(data, trans, separator)
        os.remove(local_path)

    def trans_summary_wop_assert(self, wopid, mopid, sett_date):
        # cpm校验
        pass
        # mpm校验
        # refund校验

    def mop_settlement_daily_detail_assert(self, local_path, mopid, sett_date, model, trans_fee_collection_method,
                                           fx_fee_collection_method, ):
        with open(local_path, "r", encoding="utf-8") as file:
            first_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            second_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            third_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            fourth_line = file.readline().split(",")
            total_count_name, counts = first_line[0], first_line[1]
            total_settlement_amount, sett_amount_all = second_line[0], second_line[1]
            net_settlement_mount_name, net_amount_all = third_line[0], third_line[1]
            trans_sett_obj_counts = self.sgp_evosettle_db.count(self.common_name.trans_settle_mop,
                                                                {"trans.mopID": mopid,
                                                                 "settleDate": sett_date, "settleFlag": True,
                                                                 "clearFlag": True})
            if trans_sett_obj_counts == 0:
                file.seek(0)
                first_line = file.readline().strip().encode('utf-8').decode('utf-8-sig')
                second_line = file.readline().strip()
                third_line = file.readline().strip()
                fourth_line = file.readline().strip()
                assert first_line == '"Total Count","0"'
                assert second_line == '"Total Settlement Amount","0"'  # "Total Settlement Amount","0.00"
                assert third_line == '"Total Net Settlement Amount","0"'  # "Total Net Settlement Amount","0.00"
                assert fourth_line == '"***NO DATA FOR THIS FILE***"'
            else:
                # 文件是 bom 文件
                assert total_count_name == "Total Count"
                # s=eval(eval(total_settlement_amount))
                assert total_settlement_amount == "Total Settlement Amount"
                assert net_settlement_mount_name == "Total Net Settlement Amount"
                # 校验需要进入 settle mentdetail 的数量
                assert int(eval(counts)) == len(file.readlines())
                file.seek(0)  # 回首行
                for i in range(3):
                    file.readline()
                title_demo = '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","EVONET Order Number","WOP Order Number","MOP Order Number","Transaction Type","WOP ID","WOP Name","Transaction Amount","Transaction Currency","Settlement Amount","Settlement Currency","Interchange Fee","Transaction Processing Fee","FX Processing Fee","Net Settlement Amount","Original EVONET Order Number","Original MOP Order Number","Store ID","Store English Name","Store Local Name","MCC","City","Country","Terminal Number"'

                file_title = file.readline()
                # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
                assert title_demo.strip() == file_title.strip()
                # 校验文件中的数据
                settlement_data = file.readlines()
                # 生成的文件中的交易数据的校验

                file_settle_amount = 0
                file_net_settle_amount = 0

                for file_trans_data in settlement_data:
                    separator = "|||!@|||!@||!@|||"
                    data = separator.join(
                        (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                    evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, mop_order_number, transaction_type, \
                    mop_idd, mop_name, transaction_amount, transaction_currency, settlement_amount, settlement_currency, interchange_fee, \
                    transaction_processing_fee, fx_processing_fee, net_settlement_amount, original_evonet_order_number, \
                    original_mop_order_number, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                        separator)
                    trans = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop,
                                                          {"trans.evonetOrderNumber": evonet_order_number})
                    assert trans["trans"]["evonetOrderNumber"] == evonet_order_number
                    if "wopOrderNumber" in trans["trans"]:
                        assert trans["trans"]["wopOrderNumber"] == wop_order_number
                    if "mopOrderNumber" in trans["trans"]:
                        assert trans["trans"]["mopOrderNumber"] == mop_order_number
                    if "transType" in trans["trans"]:
                        assert trans["trans"]["transType"] == transaction_type
                    if "mopID" in trans["trans"]:
                        assert trans["trans"]["wopID"] == mop_idd
                    if "transAmount" in trans["trans"]:
                        transaction_amount = self.comm_funcs.amount_conver(transaction_amount)
                        assert trans["trans"]["transAmount"] == transaction_amount
                    if "transCurrency" in trans["trans"]:
                        assert trans["trans"]["transCurrency"] == transaction_currency
                    # settlement 和interchangefee 根据不同的交易类型显示不同的正负号
                    if "settleAmount" in trans["settleInfo"]:
                        if trans["trans"]["transType"] in ["Refund", "Debit Adjustment"]:
                            assert self.comm_funcs.amount_conver(settlement_amount) == trans["settleInfo"][
                                "settleAmount"] * -1
                        if trans["trans"]["transType"] in ["CPM Payment", "MPM Payment", "Credit Adjustment"]:
                            assert self.comm_funcs.amount_conver(settlement_amount) == trans["settleInfo"][
                                "settleAmount"]
                        file_settle_amount += Decimal(str(self.comm_funcs.amount_conver(settlement_amount)))
                        file_net_settle_amount += Decimal(str(self.comm_funcs.amount_conver(net_settlement_amount)))

                    assert settlement_currency == trans["settleInfo"]["settleCurrency"]
                    if trans["trans"]["transType"] in ["CPM Payment", "MPM Payment", "Credit Adjustment"]:
                        assert self.comm_funcs.amount_conver(interchange_fee) == trans["settleInfo"][
                            "interchangeFee"] * -1
                    if trans["trans"]["transType"] in ["Refund", "Debit Adjustment"]:
                        assert self.comm_funcs.amount_conver(interchange_fee) == trans["settleInfo"][
                            "interchangeFee"]
                    # wop_name 取值为wop 表的 wopname
                    if trans_fee_collection_method == "daily":
                        if transaction_type in ["CPM Payment", "MPM Payment"]:
                            assert self.comm_funcs.amount_conver(transaction_processing_fee) == trans["settleInfo"][
                                "processingFee"] * -1

                        if transaction_type in ["Refund", "Credit Adjustment", "Debit Adjustment"]:
                            assert self.comm_funcs.amount_conver(transaction_processing_fee) == 0.00
                    if trans_fee_collection_method == "monthly":
                        assert transaction_processing_fee == ""

                    if fx_fee_collection_method == "daily":
                        if transaction_type in ["CPM Payment", "MPM Payment"]:
                            assert self.comm_funcs.amount_conver(fx_processing_fee) == trans["settleInfo"][
                                "fxProcessingFee"] * -1
                        if transaction_type in ["Refund", "Credit Adjustment", "Debit Adjustment"]:
                            assert self.comm_funcs.amount_conver(fx_processing_fee) == 0.00
                    if fx_fee_collection_method == "monthly":
                        assert fx_processing_fee == ""

                    if "originalEVONETOrderNumber" in trans["trans"]:
                        assert trans["trans"]["originalEVONETOrderNumber"] == original_evonet_order_number
                    if "originalMOPOrderNumber" in trans["trans"]:
                        assert trans["trans"]["originalMOPOrderNumber"] == original_mop_order_number
                    # 校验storeinfo信息
                    if "storeInfo" in trans["trans"]:
                        store_info = trans["trans"]["storeInfo"]
                        if "id" in store_info:
                            assert store_id == store_info["id"]
                        if "englishName" in store_info:
                            assert store_english_name == store_info["englishName"]
                        if "localName" in store_info:
                            assert store_local_name == store_info["localName"]
                        if "mcc" in store_info:
                            assert mcc == store_info["mcc"]
                        if "city" in store_info:
                            assert city == store_info["city"]
                        if "country" in store_info:
                            assert country == store_info["country"]
                        if "terminalNumber" in store_info:
                            assert terminal_number == store_info["terminalNumber"]
                # 计算表中的两个金额计算正确
                assert float(file_net_settle_amount) == self.comm_funcs.amount_conver(net_amount_all)
                assert float(file_settle_amount) == self.comm_funcs.amount_conver(sett_amount_all)

    def exceptions_file_assert(self, local_path, owner_type, wopid, mopid, sett_date, table_name):
        # owner_type  wop生文件 或者 mop 侧文件
        # exception文件校验
        with open(local_path, "r", encoding="utf-8") as file:
            first_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            total_count_name, counts = first_line[0], first_line[1]
            # 文件是 bom 文件
            assert eval(total_count_name.encode('utf-8').decode('utf-8-sig')) == "Total Count"
            assert int(eval(counts)) == len(file.readlines()) - 1
            file.readline()
            if owner_type == "mop":
                title_demo = '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","Exception Type","EVONET Order Number","WOP Order Number","MOP Order Number","Transaction Type","WOP ID","WOP Name","Transaction Amount","Transaction Currency","Original EVONET Order Number","Original MOP Order Number","Store ID","Store English Name","Store Local Name","MCC","City","Country","Terminal Number"'
            else:
                title_demo = '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","Exception Type","EVONET Order Number","WOP Order Number","MOP Order Number","Transaction Type","MOP ID","MOP Name","Transaction Amount","Transaction Currency","Original EVONET Order Number","Original MOP Order Number","Store ID","Store English Name","Store Local Name","MCC","City","Country","Terminal Number"'
            # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
            file.seek(0)
            file.readline()
            file_title = file.readline()
            assert title_demo.strip() == file_title.strip()
            # 校验文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验,后面加一个少清 lack
            if owner_type == 'wop':
                table_name = self.common_name.trans_settle_wop
                trans_sett_obj = self.tyo_evosettle_db.get_many(table_name,
                                                                {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                 "settleDate": sett_date, })
            else:
                table_name = self.common_name.trans_settle_wop
                trans_sett_obj = self.sgp_evosettle_db.get_many(table_name,
                                                                {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                 "settleDate": sett_date, })
            for trans in trans_sett_obj:
                for file_trans_data in settlement_data:
                    separator = "|||!@|||!@||!@|||"

                    data = separator.join(
                        (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                    evonet_order_create_time, wop_user_pay_time, mop_transaction_time, exception_type, evonet_order_number, wop_order_number, mop_order_number, transaction_type, \
                    idd, wop_mop_name, transaction_amount, transaction_currency, original_evonet_order_number, \
                    original_mop_order_number, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                        separator)

                    if trans["trans"]["evonetOrderNumber"] == evonet_order_number:  # 查询出异常数据
                        assert trans["blendType"] == exception_type
                        if "wopOrderNumber" in trans["trans"]:
                            assert trans["trans"]["wopOrderNumber"] == wop_order_number
                        if "mopOrderNumber" in trans["trans"]:
                            assert trans["trans"]["mopOrderNumber"] == mop_order_number
                        if "transType" in trans["trans"]:
                            assert trans["trans"]["transType"] == transaction_type
                        if owner_type == "mop":
                            if "wopID" in trans["trans"]:
                                assert trans["trans"]["wopID"] == idd
                        if owner_type == "wop":
                            if "mopID" in trans["trans"]:
                                assert trans["trans"]["mopID"] == idd

                        if wop_mop_name:
                            pass  # 这个那么取值的时候取值为 各自 wop,mop表中的 wop mop 的 name
                        if "transAmount" in trans["trans"]:
                            transaction_amount = self.comm_funcs.amount_conver(transaction_amount)
                            assert trans["trans"]["transAmount"] == transaction_amount
                        if "transCurrency" in trans["trans"]:
                            assert trans["trans"]["transCurrency"] == transaction_currency
                        # wop_name 取值为wop 表的 wopname
                        if "originalEVONETOrderNumber" in trans["trans"]:
                            assert trans["trans"]["originalEVONETOrderNumber"] == original_evonet_order_number
                        if "originalMOPOrderNumber" in trans["trans"]:
                            assert trans["trans"]["originalMOPOrderNumber"] == original_mop_order_number
                        # 校验storeinfo信息
                        if "storeInfo" in trans["trans"]:
                            store_info = trans["trans"]["storeInfo"]
                            if "id" in store_info:
                                assert store_id == store_info["id"]
                            if "englishName" in store_info:
                                assert store_english_name == store_info["englishName"]
                            if "localName" in store_info:
                                assert store_local_name == store_info["localName"]
                            if "mcc" in store_info:
                                assert mcc == store_info["mcc"]
                            if "city" in store_info:
                                assert city == store_info["city"]
                            if "country" in store_info:
                                assert country == store_info["country"]
                            if "terminalNumber" in store_info:
                                assert terminal_number == store_info["terminalNumber"]
            os.remove(local_path)

    def wop_system_file_generate(self, wopid, mopid, sett_date, file_name):
        # 生成wop_system的文件
        trans_sett_data = self.tyo_evosettle_db.get_many("transSettle.wop",
                                                         {"settleDate": sett_date, "trans.wopID": wopid,
                                                          "trans.mopID": mopid, "clearFlag": False,
                                                          "feeFlag": False, "trans.transType": {
                                                             "$in": ["CPM Payment", "MPM Payment", "Refund"]}})
        count = self.tyo_evosettle_db.count(self.common_name.trans_settle_wop,
                                            {"settleDate": sett_date, "trans.wopID": wopid,
                                             "trans.mopID": mopid, "clearFlag": False,
                                             "feeFlag": False})
        with open(file_name, "w") as file:
            file.write('"Total Count",' + str(count) + '\n')  # 写入第一行,行数
            # 写入title
            file.write(
                '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","EVONET Order Number","WOP Order Number","MOP Order Number","Transaction Type","MOP ID","MOP Name","Transaction Amount","Transaction Currency","Settlement Amount","Settlement Currency","Interchange Fee","Net Settlement Amount","Original EVONET Order Number","Original MOP Order Number","Store ID","Store English Name","Store Local Name","MCC","City","Country","Terminal Number"\n')
            for trans in trans_sett_data:
                evonet_order_number = trans["trans"]["evonetOrderNumber"]
                wop_order_number = str(random.randint(10000000000000000000, 90000000000000000000))
                mop_order_number = str(random.randint(10000000000000000000, 90000000000000000000))
                transaction_type = trans["trans"]["transType"]
                trans_amt = str(trans["trans"]["transAmount"])
                tranx_currency = trans["trans"]["transCurrency"]
                settle_currency = trans["settleInfo"]["settleCurrency"]
                settle_amts = trans["settleInfo"]["settleAmount"]

                interchange_fees = 3.0
                if transaction_type == "Refund":
                    orig_evonet_number = trans["trans"]["originalEVONETOrderNumber"]
                else:
                    orig_evonet_number = "forward_trans"
                net_sett_amt = str(settle_amts + interchange_fees)
                if transaction_type in ["CPM Payment", "MPM Payment", "Debit Adjustment"]:
                    interchange_fee = str(interchange_fees * -1)
                if transaction_type in ["Refund", "Credit Adjustment"]:
                    interchange_fee = str(interchange_fees)
                if transaction_type in ["Refund", "Credit Adjustment"]:
                    settle_amt = str(settle_amts * -1)
                if transaction_type in ["CPM Payment", "MPM Payment", "Debit Adjustment"]:
                    settle_amt = str(settle_amts)
                term_number = str(random.randint(10000000, 90000000))

                write_date = '"2020-09-12 10:41:28 UTC +08:00","2020-09-07 20:00:01 UTC +08:00","2020-09-12 10:41:27 UTC +08:00",' + '"' + evonet_order_number + '"' + ',' + '"' + wop_order_number + '"' + ',' + '"' + mop_order_number + '"' + ',' + '"' + transaction_type + '"' + ',' + '"' + mopid + '"' + ',"auto_test",' + '"' + trans_amt + '"' + ',' + '"' + tranx_currency + '"' + ',' + '"' + settle_amt + '"' + ',' + '"' + settle_currency + '"' + ',' + '"' + interchange_fee + '"' + ',' + '"' + net_sett_amt + '"' + ',' + '"' + orig_evonet_number + '"' + ',"origmopnumber","storeid","evonet_test","storelocalname","7011","shanghai","china",' + '"' + term_number + '"' + '\n'

                file.write(write_date)

    def assert_file_date(self, data, separator):
        # 校验数据
        evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, mop_order_number, transaction_type, \
        mop_id, mop_name, transaction_amount, transaction_currency, settlement_amount, settlement_currency, interchange_fee, net_settlement_amount, original_evonet_order_number, \
        original_mop_order_number, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
            separator)
        trans = self.tyo_evosettle_db.get_one(self.common_name.trans_file_wop,
                                              {"trans.evonetOrderNumber": evonet_order_number})
        assert trans["blendKey"] == evonet_order_number
        if wop_order_number:
            assert trans["trans"]["wopOrderNumber"] == wop_order_number
        if mop_order_number:
            assert trans["trans"]["mopOrderNumber"] == mop_order_number
        if transaction_type:
            assert trans["trans"]["transType"] == transaction_type
        # 勾兑，只是将transFile.wopNode，和文件中的数据做对比
        if mop_id:
            assert mop_id == trans["mopID"]
        if transaction_amount:
            assert trans["trans"]["transAmount"] == float(
                self.comm_funcs.amount_conver(transaction_amount))
        if transaction_currency:
            assert trans["trans"]["transCurrency"] == transaction_currency
        if settlement_amount:
            assert trans["trans"]["settleAmount"] == float(
                self.comm_funcs.amount_conver(settlement_amount))
        if settlement_currency:
            assert trans["trans"]["settleCurrency"] == settlement_currency
        if "interchangeFee" in trans["trans"]:
            assert trans["trans"]["interchangeFee"] == float(
                self.comm_funcs.amount_conver(interchange_fee))
        if "netSettleAmount" in trans["trans"]:
            assert trans["trans"]["netSettleAmount"] == float(
                self.comm_funcs.amount_conver(net_settlement_amount))
        if original_evonet_order_number:
            assert trans["trans"]["originalEVONETOrderNum"] == original_evonet_order_number
        if original_mop_order_number:
            assert trans["trans"]["originalMOPOrderNum"] == original_mop_order_number
        if store_english_name:
            assert trans["trans"]["storeEnglishName"] == store_english_name
        if mcc:
            assert trans["trans"]["mcc"] == mcc
        if terminal_number:
            assert trans["trans"]["terminalNumber"] == terminal_number
        if store_id:
            assert trans["trans"]["storeID"] == store_id
        if store_local_name:
            assert trans["trans"]["storeLocalName"] == store_local_name
        if city:
            assert trans["trans"]["city"] == city
        if country:
            assert trans["trans"]["country"] == country

    def wop_system_filerecon_assert(self, local_path, wopid, mopid, sett_date, ):
        # wopflle解析校验
        with open(local_path, "r", encoding="utf-8") as file:
            # second_line = list(csv.reader(file.readline().strip().splitlines(), skipinitialspace=True))[0]
            # 读两行title
            file.readline()
            file.readline()
            # 读取文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验
            trans_file_obj = self.tyo_evosettle_db.get_many("transFile.wop",
                                                            {"wopID": wopid, "mopID": mopid,
                                                             "settleDate": sett_date, })

            for file_trans_data in settlement_data:
                separator = "|||!@|||!@||!@|||"

                data = separator.join(
                    (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))

                self.assert_file_date(data, separator)

    def bilateral_wop_recon_sucess(self, wopid, mopid, sett_date):
        # 勾兑成功校验
        # 获取 transFile.wop 表中的数据
        trans_file_obj = self.db_operations.evosettle_db.get_many("transFile.wop",
                                                                  {"wopID": wopid, "mopID": mopid,
                                                                   "settleDate": sett_date, })
        # 获取 transSett.wop表中的数据
        trans_sett_obj = self.db_operations.evosettle_db.get_many("transSettle.wop",
                                                                  {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                   "settleDate": sett_date, "clearFlag": True,
                                                                   "feeFlag": True})

        for i in trans_file_obj:
            for j in trans_sett_obj:
                if i["blendKey"] == j["blendKey"]:
                    assert j["blendType"] == "success"
                    assert j["settleFlag"] == True
                    assert abs(i["trans"]["interchangeFee"]) == j["settleInfo"]["interchangeFee"]

    def self_sett(self, wopid, mopid, sett_date, sett_table):
        "自主清算"

        # 自主清算
        trans = self.db_operations.evosettle_db.get_many(sett_table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                      "settleDate": sett_date, })
        for i in trans:
            assert i["blendType"] == "selfSettle"
            assert i["settleFlag"] == True
        # clearFlag为false

    def self_settle_default(self, wopid, mopid, sett_date, sett_table):
        # 自主未清算
        trans = self.db_operations.evosettle_db.get_many(sett_table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                      "settleDate": sett_date, })
        for i in trans:
            assert i["blendType"] == "default"
            assert i["settleFlag"] == False

    def exception_recon(self, wopid, mopid, trans_sett_list, orig_table, trans_sett_table):
        # orig_table 勾兑的原数据
        # trans_sett_table  勾兑的目标表
        # 勾兑成功校验
        # 获取 transFile.wop 表中的数据
        trans_file_obj = self.db_operations.evosettle_db.get_many(orig_table,
                                                                  {"wopID": wopid, "mopID": mopid,
                                                                   })

        # 多清 少清计算
        trans_file_list = []
        for file_trans in trans_file_obj:
            trans_file_list.append(file_trans["blendKey"])

        # 多清, trans表中的数据不存在时走的逻辑
        for m in trans_file_list:
            if m not in trans_sett_list:
                # 获取transFile.wop的数据
                file_date = self.db_operations.evosettle_db.get_one(orig_table,
                                                                    {"wopID": wopid, "mopID": mopid,
                                                                     "blendKey": m})
                extra_data = self.db_operations.evosettle_db.get_one(trans_sett_table,
                                                                     {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                      "trans.evonetOrderNumber": m})

                assert extra_data["trans"]["wopConverterCurrencyFlag"] == False
                assert extra_data["trans"]["mopConverterCurrencyFlag"] == False
                assert extra_data["trans"]["transCurrency"] == file_date["trans"]["transCurrency"]
                assert extra_data["trans"]["wopSettleCurrency"] == file_date["trans"]["settleCurrency"]
                assert extra_data["trans"]["mopSettleAmount"] == abs(file_date["trans"]["settleAmount"])
                assert extra_data["trans"]["wopSettleAmount"] == abs(file_date["trans"]["settleAmount"])
                assert extra_data["trans"]["mopSettleCurrency"] == file_date["trans"]["settleCurrency"]
                assert extra_data["clearFlag"] == True
                assert extra_data["feeFlag"] == True
                assert extra_data["settleFlag"] == True
                assert extra_data["trans"]["wopOrderNumber"] == file_date["trans"]["wopOrderNumber"]
                assert extra_data["trans"]["mopOrderNumber"] == file_date["trans"]["mopOrderNumber"]
                assert extra_data["settleInfo"]["settleCurrency"] == file_date["trans"]["settleCurrency"]
                assert extra_data["settleInfo"]["settleAmount"] == abs(file_date["trans"]["settleAmount"])
                assert extra_data["settleInfo"]["interchangeFee"] == abs(file_date["trans"]["interchangeFee"])
                assert extra_data["blendType"] == "Extra"
                assert extra_data["settleFlag"] == True

    def assert_extra_trans_sett(self, node_type, evonet_number, ):
        """
        多清的时候能在tans表找到交易但是在transSettle表找不到交易时的勾兑后的校验
        :param node_type: wop节点或者mop节点
        :param evonet_number: 交易中的evonetOrderNumber
        :return:
        """
        #
        # 校验 blendType
        if node_type == "wop":
            trans_data = self.tyo_evosettle_db.get_one(self.common_name.trans, {"evonetOrderNumber": evonet_number})
            trans_settle_data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]

            trans_file_data = self.tyo_evosettle_db.get_one(self.common_name.trans_file_wop,
                                                            {"trans.evonetOrderNumber": evonet_number})["trans"]
        if node_type == "mop":
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans, {"evonetOrderNumber": evonet_number})
            trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]

            trans_file_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_wop_node,
                                                            {"trans.evonetOrderNumber": evonet_number})["trans"]
        # trans的结构体重要字段校验
        # for key in ['mopOrderNumber', 'wopOrderNumber', 'evonetOrderNumber', 'mopSettleDate', 'wopSettleDate',
        #             'wopConverterCurrencyFlag', 'mopConverterCurrencyFlag', 'billingConverterCurrencyFlag',
        #             'transAmount', 'transCurrency', 'status', 'wopStatus', 'mopStatus', 'mopSettleAmount',
        #             'mopSettleCurrency', 'wopSettleAmount', 'wopSettleCurrency', 'wopSettleSourceCurrency', 'transType',
        #             'category', 'wopID', 'mopID', 'lockFlag', 'settleMode']:
        assert trans_data == trans_settle_data["trans"]
        # 校验 blendType
        # 校验三个flag初始值为false
        assert trans_settle_data["blendType"] == "Extra"
        assert trans_settle_data["clearFlag"] == False
        assert trans_settle_data["feeFlag"] == False
        assert trans_settle_data["settleFlag"] == True
        # 多清interchangFee的校验

        # processingfee,fxprocessingfee初始状态为 0.0

        assert settle_info["processingFee"] == 0.0
        assert settle_info["fxProcessingFee"] == 0.0
        assert settle_info["rebate"] == 0.0
        assert settle_info["feeReceivable"] == 0.0
        assert settle_info["feeReceivable"] == 0.0
        # 校验 transSett.wop表中的 trans内的body中的币种，交易金额 和外层测币种，交易金额 一致
        # wop侧赋值和mop侧赋值逻辑一样:将wopsettlecurrency 和wopsettleamount赋值给  settlecurrency，settleamount

        assert trans_settle_data["blendKey"] == trans_data["evonetOrderNumber"]

        # 校验清算币种和清算金额的取值；
        assert settle_info["settleCurrency"] == trans_file_data["settleCurrency"]
        assert settle_info["settleAmount"] == abs(trans_file_data["settleAmount"])
        assert settle_info["interchangeFeeRefund"] == abs(trans_file_data["interchangeFee"])
        assert settle_info["interchangeFee"] == abs(trans_file_data["interchangeFee"])

    def full_extra_sett(self, node_type, evonet_number, ):
        """
        多清的时候能在tans和transSettle表都找不到交易时的勾兑后的校验
        :param node_type: wop节点或者mop节点
        :param evonet_number: 交易中的evonetOrderNumber
        :file_init 谁出文件  wop,mop,evonet
        :return:
        """
        # 校验 blendType
        if node_type == "wop":
            trans_file_data = self.tyo_evosettle_db.get_one(self.common_name.trans_file_wop,
                                                            {"trans.evonetOrderNumber": evonet_number})["trans"]
            trans_settle_data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]

            trans_file = self.tyo_evosettle_db.get_one(self.common_name.trans_file_wop,
                                                       {"trans.evonetOrderNumber": evonet_number})
        if node_type == "mop":
            trans_file_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_wop_node,
                                                            {"trans.evonetOrderNumber": evonet_number})["trans"]
            trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]
            trans_file = self.sgp_evosettle_db.get_one(self.common_name.trans_file_wop_node,
                                                       {"trans.evonetOrderNumber": evonet_number})
        # trans的结构体重要字段校验
        for key in ['mopOrderNumber', 'wopOrderNumber', 'evonetOrderNumber',
                    'transAmount', 'transCurrency', 'transType',
                    ]:
            assert trans_file_data[key] == trans_settle_data["trans"][key]
        # 校验 blendType
        # 校验三个flag初始值为false
        assert trans_settle_data["blendType"] == "Extra"
        assert trans_settle_data["clearFlag"] == False
        assert trans_settle_data["feeFlag"] == False
        assert trans_settle_data["settleFlag"] == True

        # 多清interchangFee的校验
        assert settle_info["interchangeFeeRefund"] == abs(trans_file_data["interchangeFee"])
        assert settle_info["interchangeFee"] == abs(trans_file_data["interchangeFee"])
        # processingfee,fxprocessingfee初始状态为 0.0

        assert settle_info["processingFee"] == 0.0
        assert settle_info["fxProcessingFee"] == 0.0
        assert settle_info["rebate"] == 0.0
        assert settle_info["feeReceivable"] == 0.0
        assert settle_info["feeReceivable"] == 0.0
        assert trans_settle_data["blendKey"] == trans_file_data["evonetOrderNumber"]
        # 校验 transSett.wop表中的 trans内的body中的币种，交易金额 和外层测币种，交易金额 一致
        # wop侧赋值和mop侧赋值逻辑一样:将wopsettlecurrency 和wopsettleamount赋值给  settlecurrency，settleamount
        # 校验清算币种和清算金额的取值；
        # trans_settle表对应的 trans 结构体
        trans_body = trans_settle_data["trans"]
        assert trans_body["status"] == "succeeded"
        # 'category', 'status',
        assert trans_body["category"] == "QR"
        assert trans_body["wopID"] == trans_file["wopID"]
        assert trans_body["mopID"] == trans_file["mopID"]
        assert trans_body["billingConverterCurrencyFlag"] == False
        assert trans_body["wopConverterCurrencyFlag"] == False
        assert trans_body["mopConverterCurrencyFlag"] == False
        assert trans_body["wopSettleAmount"] == abs(trans_file_data["settleAmount"])
        assert trans_body["mopSettleAmount"] == abs(trans_file_data["settleAmount"])
        assert trans_body["wopSettleCurrency"] == trans_file_data["settleCurrency"]
        assert trans_body["mopSettleCurrency"] == trans_file_data["settleCurrency"]
        assert settle_info["settleCurrency"] == trans_file_data["settleCurrency"]
        assert settle_info["settleAmount"] == abs(trans_file_data["settleAmount"])

    def mop_recon_file_assert(self, evonet_number):
        # wop侧生文件，mop侧勾对文件，校验mop侧 transFile.wopNode的数据和wop侧的 transSettle.wop表一致

        trans_sett_data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                        {"trans.evonetOrderNumber": evonet_number})
        trans_file_data = self.tyo_evosettle_db.get_one(self.common_name.trans_file_wop_node,
                                                        {"trans.evonetOrderNumber": evonet_number})
        trans_sett_body = trans_sett_data["trans"]
        trans_file_body = trans_file_data["trans"]
        for key in ["evonetOrderNumber", "wopOrderNumber", "mopOrderNumber", "transType", "mopID", "transAmount",
                    "transCurrency", "settleAmount"]:
            assert trans_file_body[key] == trans_sett_body[key]

    def chec_recon_result(self, node_type, evonet_number):
        """
        模式一 wop侧 ，mop侧正常勾兑字段校验校验
        :param node_type:
        :param evonet_number:
        :return:
        """
        # 校验 blendType
        if node_type == "wop":
            trans_file_data = self.tyo_evosettle_db.get_one(self.common_name.trans_file_wop,
                                                            {"trans.evonetOrderNumber": evonet_number})["trans"]
            trans_settle_data = self.tyo_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]

        if node_type == "mop":
            trans_file_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_wop_node,
                                                            {"trans.evonetOrderNumber": evonet_number})["trans"]
            trans_settle_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_mop,
                                                              {"trans.evonetOrderNumber": evonet_number})
            settle_info = trans_settle_data["settleInfo"]

        assert trans_settle_data["settleFlag"] == True
        assert trans_settle_data["blendType"] == "success"
        assert trans_settle_data["feeFlag"] == False
        assert trans_settle_data["clearFlag"] == False
        assert trans_settle_data["amountErrorFlag"] == True
        assert settle_info["settleCurrency"] == trans_file_data["settleCurrency"]
        assert settle_info["settleAmount"] == abs(trans_file_data["settleAmount"])
        assert settle_info["interchangeFee"] == abs(trans_file_data["interchangeFee"])

    def upi_settlement_detail_content_assert(self, local_path, ):
        """
        :param local_path: 文件名称
        :return:
        """
        title_demo = self.get_config.get_ini("upi_settlement_detail")
        with open(local_path, "r", encoding="utf-8") as file:
            # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
            first_line = file.readline()
            assert first_line.strip() == '"Total Count","3"'
            assert file.readline().strip() == title_demo
            # 校验文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验

            for file_trans_data in settlement_data:
                separator = "||@||"
                data = separator.join(
                    (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, mop_order_number, \
                system_trace_audit_number, acquirer_iin, forwarding_iin, transmission_date_time, pan, transaction_type, evonet_qr_order_number, \
                wop_qr_order_number, network_token_pan, qr_transaction_type, mop_id, mop_name, transaction_amount, transaction_currency, settlement_amount, \
                settlement_currency, fee_receivable, fee_payable, net_settlement_amount, original_evonet_order_number, original_wop_order_number, \
                original_mop_order_number, original_system_trace_audit_number, original_acquirer_iin, original_forwarding_iin, \
                original_transmission_date_time, store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                    separator)
                sett_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                          {
                                                              "trans.evonetOrderNumber": evonet_order_number,
                                                              "trans.category": "Card"})
                trans_data = sett_data["trans"]
                settle_info = sett_data["settleInfo"]
                store_info = trans_data["storeInfo"]
                card_data = trans_data["card"]
                raw_data = trans_data["rawData"]
                qr_trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                              {"trans.qrcVoucherNo": sett_data["trans"][
                                                                  "qrcVoucherNo"]})["trans"]
                assert wop_order_number == trans_data["wopOrderNumber"]
                assert mop_order_number == trans_data["mopOrderNumber"]
                assert system_trace_audit_number == raw_data["systemTraceAuditNum"]
                assert acquirer_iin == raw_data["acquirerIIN"]
                assert forwarding_iin == raw_data["forwardingIIN"]
                assert transmission_date_time == raw_data["transmissionDateTime"]
                assert pan == card_data["maskedNumber"]
                assert transaction_type == trans_data["transType"]
                if transaction_type == "Account Debit":
                    assert qr_transaction_type == "MPM Payment"
                if transaction_type == "Refund":
                    assert qr_transaction_type == "Refund"
                # assert network_token_pan ==card_data["networkTokenPan"]  #后面和明琪沟通
                assert mop_id == trans_data["mopID"]
                assert mop_name == self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mop_id})["baseInfo"][
                    "mopName"]
                assert self.comm_funcs.amount_conver(transaction_amount) == trans_data["transAmount"]
                assert transaction_currency == trans_data["transCurrency"]
                settlement_amount = self.comm_funcs.amount_conver(settlement_amount)
                if transaction_type in ["Account Credit", "Refund"]:
                    assert settlement_amount * -1 == settle_info["settleAmount"]
                # Account Debit  校验
                settlement_amount == settle_info["settleAmount"]
                # Account Debit 的settlement为正数
                assert settlement_currency == settle_info["settleCurrency"]
                assert float(fee_receivable) == settle_info["feeReceivable"] * -1
                assert float(fee_payable) == settle_info["feePayable"]
                assert self.comm_funcs.amount_conver(net_settlement_amount) == settlement_amount + float(
                    fee_receivable) + float(fee_payable)

                if transaction_type == "Refund":
                    assert original_evonet_order_number == trans_data["originalEVONETOrderNumber"]
                    orig_trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop, {
                        "trans.evonetOrderNumber": original_evonet_order_number})
                    assert original_wop_order_number == orig_trans_data["trans"]["wopOrderNumber"]
                    assert original_mop_order_number == orig_trans_data["trans"]["mopOrderNumber"]
                    orig_raw_data = orig_trans_data["trans"]["rawData"]
                    assert original_system_trace_audit_number == orig_raw_data["systemTraceAuditNum"]
                    assert original_acquirer_iin == orig_raw_data["acquirerIIN"]
                    assert original_forwarding_iin == orig_raw_data["forwardingIIN"]
                    assert original_transmission_date_time == orig_raw_data["transmissionDateTime"]
                assert store_id == store_info["id"]
                assert store_english_name == store_info["englishName"]
                assert store_local_name == store_info["localName"]
                assert mcc == store_info["mcc"]
                assert city == store_info["city"]
                assert country == store_info["country"]
                assert terminal_number == store_info["terminalNumber"]
                if transaction_type == "Account Credit":
                    continue  # 后面不执行了  因为accout Credit 没有对应的扫码交易
                assert evonet_qr_order_number == qr_trans_data["evonetOrderNumber"]  # 取值为 evonetordernumber
                assert wop_qr_order_number == qr_trans_data["wopOrderNumber"]  # 根据qrcVoucherNo 找到扫码的 wopordernumber

    def upi_feecollection_details_content_resolve(self, fcp_file_name):
        # 根据银联规则解析校验进入数据库的数据是否正确
        with open(fcp_file_name, "r", ) as fcp_file:
            for line in fcp_file:
                trans_code = line[0:3]
                settle_amount = line[4:17]
                reason_code = line[18:22]
                sender1 = line[23:34]
                sender2 = line[35:46]
                receiver1 = line[47:58]
                receiver2 = line[59:70]
                trans_date_time = line[71:81]
                trace_number = line[82:88]
                # pan解析出来是加密的
                # pan = line[89:108]
                settle_currency = line[109:112]
                reserve = line[113:309]  # 后面优化到再取消注释
                # 根据  tras_date_time去 trans_file_upi查找数据并进行逻辑校验
                data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upifee,
                                                     {"upiFee.transDatetime": trans_date_time})
                trans_data = data["trans"]
                upi_trans = data["upiTrans"]
                upi_fee = data["upiFee"]
                assert upi_fee["transCode"] == trans_code
                assert upi_fee["settleAmount"] == settle_amount
                assert upi_fee["reasonCode"] == reason_code
                assert upi_fee["sender1"] == sender1
                assert upi_fee["sender2"] == sender2
                assert upi_fee["receiver1"] == receiver1
                assert upi_fee["receiver2"] == receiver2
                assert upi_fee["traceNumber"] == trace_number
                assert upi_fee["pan"] != False
                assert upi_fee["settleCurrency"] == settle_currency
                if settle_currency == "156":
                    assert trans_data["settleCurrency"] == "CNY"
                    assert trans_data["transCurrency"] == "CNY"
                if settle_currency == "392":
                    assert trans_data["settleCurrency"] == "JPY"
                    assert trans_data["transCurrency"] == "JPY"

                if trans_code == "E20":
                    assert trans_data["transType"] == "Fee Collection"
                if trans_code == "E30":
                    assert trans_data["transType"] == "Fund Disbursement"
                if settle_amount.startswith("C"):
                    assert upi_trans["feePayable"] == 0.0
                    # 前置条件已经将银联的文件中的币种修改为了 156
                    fee_settle_amount = list(settle_amount[1:].lstrip("0"))
                    fee_settle_amount.insert(-2, ".")
                    fee_settle_amount = "".join(fee_settle_amount)
                    assert upi_trans["feeReceivable"] == float(fee_settle_amount)
                if settle_amount.startswith("D"):
                    fee_settle_amount = list(settle_amount[1:].lstrip("0"))
                    fee_settle_amount = "".join(fee_settle_amount)
                    assert upi_trans["feePayable"] == float(fee_settle_amount)
                    assert upi_trans["feeReceivable"] == 0.0

    def upi_icom_details_content_resolve(self, fcp_file_name):
        # 根据银联规则解析校验进入数据库的数据是否正确
        with open(fcp_file_name, "r", ) as fcp_file:
            for line in fcp_file:
                trans_type = ""  # 先放这里
                trans_currency = line[203:206]
                settle_curency = line[211:214]  # 这个前置条件中做了设置
                account_number = line[42:61]
                trans_amount = line[62:74]
                settle_amount = line[215:227]
                trace_number = line[24:30]
                trans_datetime = line[31:41]
                author_ization_code = line[174:180]
                retrieval_reference_number = line[158:170]
                upi_settle_date = line[237:241]
                acquirer_iin = line[0:11]
                forwarding_iin = line[12:23]
                processing_code = line[80:86]
                message_type = line[75:79]
                fee_receive_amount = line[273:286]
                fee_payable_amount = line[286:299]
                # 根据  tras_date_time去 trans_file_upi查找数据并进行逻辑校验
                data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upi,
                                                     {"upiTrans.transDatetime": trans_datetime})
                trans_data = data["trans"]
                upi_trans = data["upiTrans"]

                if trans_currency == "156":
                    assert trans_data["transCurrency"] == "CNY"
                    assert trans_data["settleCurrency"] == "CNY"
                    if fee_payable_amount == "000000000000":
                        fee_receive_amount = list(fee_receive_amount).insert(-2, ".")
                        feeReceivable = list(feeReceivable)
                        feeReceivable.insert(-3, ".")
                        feeReceivable = "".join(feeReceivable)
                        assert upi_trans["feeReceivable"] == float(str(feeReceivable))
                    if fee_payable_amount == "000000000000":
                        fee_payable_amount = list(fee_payable_amount)
                        fee_payable_amount.insert(-3, ".")
                        fee_payable_amount = "".join(fee_payable_amount)
                        assert upi_trans["feePayable"] == float(str(fee_payable_amount))

                if trans_currency == "392":
                    assert trans_data["transCurrency"] == "JPY"
                    assert trans_data["settleCurrency"] == "JPY"
                    if fee_payable_amount == "000000000000":
                        assert upi_trans["feeReceivable"] == float(fee_receive_amount)
                    if fee_receive_amount == "000000000000":
                        assert upi_trans["feePayable"] == float(fee_payable_amount)

                assert trans_data["transAmount"] == self.get_amount(trans_amount, trans_currency)
                assert trans_data["settleAmount"] == self.get_amount(settle_amount, trans_currency)
                assert upi_trans["maskedAccountNumber"] == account_number[0:6] + "****" + account_number[-4:]
                assert upi_trans["traceNumber"] == trace_number
                assert upi_trans["authorizationCode"] == author_ization_code
                assert upi_trans["retrievalReferenceNumber"] == retrieval_reference_number
                assert upi_trans["upiSettleDate"] == upi_settle_date
                assert upi_trans["acquirerIIN"] == acquirer_iin
                assert upi_trans["forwardingIIN"] == forwarding_iin
                assert upi_trans["processingCode"] == processing_code
                assert upi_trans["messageType"] == message_type
                assert data["blendKey"] == forwarding_iin + trace_number + trans_datetime
                # feereceivable   和 feePayable

                # 交易类型校验
                if message_type == "0200":
                    assert trans_data["transType"] == "Account Debit"
                if message_type == "0220":
                    if processing_code in ["00x000", "22x000", "02x000", "29x000"]:
                        assert trans_data["transType"] == "Account Debit"
                    if processing_code == "20x000":
                        assert trans_data["transType"] == "Refund"
                    if processing_code == "19x000":
                        assert trans_data["transType"] == "Account Credit"
                if message_type == "0422":
                    if processing_code in ["22x000", "02x000"]:
                        assert trans_data["transType"] == "Account Credit"

    def get_amount(self, settle_amount, currency):
        """
        将金额转化为人民币模式,带逗号分隔,保留小数点两位,四舍五入
        :param args:
        :return:
        """
        if currency == "156":
            amount = list(settle_amount)
            amount.insert(-2, ".")
            amount = "".join(amount)
        if currency == "392":
            amount = list(settle_amount)
            amount = "".join(amount)
        return float(amount)

    def get_start_end_position(self, end_position, length):
        start_position = end_position + 1
        ends_position = start_position + length
        return (start_position, ends_position)

    def upi_ierrn_details_resolve_content_resolve(self, ierrn_file_name):
        # 根据银联规则解析校验进入数据库的数据是否正确
        with open(ierrn_file_name, "r", ) as ierrn_file:
            for line in ierrn_file:
                acquirer_iin_length = 11
                forwarding_iin_length = 11
                trace_num_length = 6
                trans_datetime_length = 10
                account_number_length = 19
                trans_amount_length = 12
                message_type_length = 4
                processing_code_length = 6
                mcc_length = 4
                terminal_number_length = 8
                store_id_length = 15
                store_english_name_length = 40
                retrieval_reference_number_length = 12
                authorization_code_length = 6

                start_position = 0
                end_position = start_position + forwarding_iin_length
                acquirer_iin = line[start_position:end_position]  # 0 11
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           acquirer_iin_length)
                forwarding_iin = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           trace_num_length)

                trace_num = line[start_position:end_position]

                start_position, end_position = self.get_start_end_position(end_position,
                                                                           trans_datetime_length)
                trans_datetime = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           account_number_length)
                account_number = line[start_position:end_position]  # 未保存
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           trans_amount_length)
                trans_amount = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           message_type_length)
                message_type = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           processing_code_length)
                processing_code = line[start_position:end_position]

                start_position, end_position = self.get_start_end_position(end_position,
                                                                           mcc_length)
                mcc = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           terminal_number_length)
                terminal_number = line[start_position:end_position]

                start_position, end_position = self.get_start_end_position(end_position,
                                                                           store_id_length)
                store_id = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           store_english_name_length)

                store_english_name = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           retrieval_reference_number_length)
                retrieval_reference_number = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           2)  # 这个长度固定，暂时用不到
                service_code = line[start_position:end_position]
                start_position, end_position = self.get_start_end_position(end_position,
                                                                           authorization_code_length)
                authorization_code = line[start_position:end_position]
                # 这几个参数不连续，所以不通过位置来取了
                trans_currency = line[203:206]
                settle_currency = line[211:214]
                settle_amount = line[215:227]
                upi_settle_date = line[237:241]
                fee_receivable = line[273:285]
                fee_payable = line[286:298]
                message_type = line[75:79]
                blendkey = acquirer_iin + trace_num + trans_datetime
                data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upierr,
                                                     {"blendKey": blendkey})
                trans_data = data["trans"]
                upi_trans = data["upiTrans"]

                if processing_code == "220000" and service_code in ["00", "83"]:
                    assert trans_data["transType"] == "Credit Adjustment"
                if processing_code == "020000" and service_code == "00":
                    assert trans_data["transType"] == "Debit Adjustment"
                if processing_code == "020000" and service_code == "17" or service_code == "17":
                    assert trans_data["transType"] == "Chargeback"
                assert trans_data["storeID"] == store_id
                assert trans_data["storeEnglishName"] == store_english_name
                assert trans_data["mcc"] == mcc
                assert trans_data["terminalNumber"] == terminal_number
                assert upi_trans["traceNumber"] == trace_num
                assert upi_trans["transDatetime"] == trans_datetime
                assert upi_trans["authorizationCode"] == authorization_code
                assert upi_trans["retrievalReferenceNumber"] == retrieval_reference_number
                assert upi_trans["upiSettleDate"] == upi_settle_date
                assert upi_trans["acquirerIIN"] == acquirer_iin
                assert upi_trans["forwardingIIN"] == forwarding_iin.strip()
                assert upi_trans["processingCode"] == processing_code
                assert upi_trans["maskedAccountNumber"][0:6] == account_number[0:6]
                assert upi_trans["maskedAccountNumber"][-4:] == account_number[-4:]
                assert upi_trans["maskedAccountNumber"][6:10] == "****"
                trans_amount = self.get_amount(trans_amount, trans_currency)
                settle_amount = self.get_amount(settle_amount, trans_currency)
                assert trans_data["transAmount"] == trans_amount
                assert trans_data["settleAmount"] == settle_amount
                fee_payable = self.get_amount(fee_payable, settle_currency)
                fee_receivable = self.get_amount(fee_receivable, settle_currency)
                assert upi_trans["feePayable"] == fee_payable
                assert upi_trans["feeReceivable"] == fee_receivable

                net_settle_amount = settle_amount - fee_receivable + fee_payable
                if trans_currency == "156":
                    assert trans_data["transCurrency"] == "CNY"
                    assert trans_data["settleCurrency"] == "CNY"
                    net_settle_amount = self.round_four_five(net_settle_amount, 2)
                if trans_currency == "392":
                    assert trans_data["transCurrency"] == "JPY"
                    assert trans_data["settleCurrency"] == "JPY"

    def upi_feecollection_detail_content_assert(self, local_path, token_pan):
        """
        :param local_path: 文件名称
        :return:
        """
        title_demo = self.get_config.get_ini("upi_feecollection_detail")
        with open(local_path, "r", encoding="utf-8") as file:
            # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
            first_line = file.readline()
            assert first_line.strip() == '"Total Count","4"'
            assert file.readline().strip() == title_demo
            # 校验文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验

            for file_trans_data in settlement_data:
                separator = "||@||"
                data = separator.join(
                    (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                mop_id, mop_name, system_trace_audit_number, transmission_date_time, pan, network_token_pan, transaction_type, \
                reason_code, level_1_sender, level_2_sender, level_1_receiver, level_2_receiver, settlement_currency, fee_receivable, \
                fee_payable, net_settlement_amount = data.split(
                    separator)
                # 获取每条upiFee的数据
                sett_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upifee,
                                                          {"upiFee.transDatetime": transmission_date_time})
                trans_data = sett_data["trans"]
                upi_trans = sett_data["upiTrans"]
                upifee_info = sett_data["upiFee"]
                assert mop_id == trans_data["mopID"]
                assert mop_name == self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mop_id})["baseInfo"][
                    "mopName"]
                assert system_trace_audit_number == upifee_info["traceNumber"]
                assert pan == "621094****0243"
                assert network_token_pan == token_pan
                assert transaction_type == trans_data["transType"]  # 交易类型在解析的时候进行校验
                assert reason_code == upifee_info["reasonCode"]
                assert level_1_sender == upifee_info["sender1"]
                assert level_2_sender == upifee_info["sender2"]
                assert level_1_receiver == upifee_info["receiver1"]
                assert level_2_receiver == upifee_info["receiver2"]
                fee_receivable_amount = self.comm_funcs.amount_conver(fee_receivable)
                fee_payable_amount = self.comm_funcs.amount_conver(fee_payable)
                assert fee_receivable_amount == upi_trans["feeReceivable"] * -1
                assert fee_payable_amount == upi_trans["feePayable"]
                assert self.comm_funcs.amount_conver(
                    net_settlement_amount) == fee_receivable_amount + fee_payable_amount

    def upi_dispute_detail_content_assert(self, local_path):
        """
        #校验 生成的dispute中的数据
        :param local_path: 文件名称
        :return:
        """
        title_demo = self.get_config.get_ini("upi_dipute_detail")
        with open(local_path, "r", encoding="utf-8") as file:
            # 校验文件中的title和demo中的title一致;模式一，模式二中的表demo是一致的，因为都是按月生的
            first_line = file.readline()
            # assert first_line.strip() == '"Total Count","4"'
            assert file.readline().strip() == title_demo
            # 校验文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验

            for file_trans_data in settlement_data:
                separator = "||@||"
                data = separator.join(
                    (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                mop_transaction_time, mop_order_number, system_trace_audit_number, acquirer_iin, forwarding_iin, transmission_date_time, \
                pan, transaction_type, mop_id, mop_name, transaction_amount, transaction_currency, settlement_amount, settlement_currency, \
                fee_receivable, fee_payable, net_settlement_amount, store_id, store_english_name, mcc, terminal_number = data.split(
                    separator)
                # 获取每条upiFee的数据
                sett_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upierr,
                                                          {
                                                              "upiTrans.transDatetime": transmission_date_time.strip()})
                trans_data = sett_data["trans"]
                upi_trans = sett_data["upiTrans"]
                assert mop_transaction_time != False
                assert mop_order_number == upi_trans["retrievalReferenceNumber"]
                assert system_trace_audit_number == upi_trans["traceNumber"]
                assert acquirer_iin == upi_trans["acquirerIIN"]
                assert acquirer_iin == upi_trans["acquirerIIN"]
                assert forwarding_iin == upi_trans["forwardingIIN"]
                assert len(pan) == 14  # 校验卡的长度
                assert transaction_type == trans_data["transType"]
                assert mop_id == trans_data["mopID"]
                assert mop_name == self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mop_id})["baseInfo"][
                    "mopName"]
                assert trans_data["transAmount"] == self.comm_funcs.amount_conver(transaction_amount)
                if transaction_type == "Debit Adjustment":
                    assert trans_data["settleAmount"] == self.comm_funcs.amount_conver(settlement_amount)
                else:
                    assert trans_data["settleAmount"] * -1 == self.comm_funcs.amount_conver(settlement_amount)
                assert transaction_currency == trans_data["transCurrency"]
                assert settlement_currency == trans_data["settleCurrency"]
                assert upi_trans["feePayable"] == self.comm_funcs.amount_conver(fee_payable)
                assert upi_trans["feeReceivable"] * -1 == self.comm_funcs.amount_conver(fee_receivable)
                assert trans_data["storeID"] == store_id
                assert trans_data["storeEnglishName"] == store_english_name
                assert trans_data["mcc"] == mcc
                assert trans_data["terminalNumber"] == terminal_number

    def upi_exception_detail_content_assert(self, local_path):
        """
        #校验 生成的dispute中的数据
        :param local_path: 文件名称
        :return:
        """
        title_demo = self.get_config.get_ini("upi_exception_details")
        with open(local_path, "r", encoding="utf-8") as file:
            # 校验文件中的title和demo中的title一致;
            first_line = file.readline()
            assert first_line.strip() == '"Total Count","3"'
            assert file.readline().strip() == title_demo
            # 校验文件中的数据
            settlement_data = file.readlines()
            # 生成的文件中的交易数据的校验
            count = 0
            for file_trans_data in settlement_data:
                separator = "||@||"
                data = separator.join(
                    (list(csv.reader(file_trans_data.strip().splitlines(), skipinitialspace=True))[0]))
                evonet_order_create_time, wop_user_pay_time, mop_transaction_time, exception_type, evonet_order_number, wop_order_number, \
                mop_order_number, system_trace_audit_number, acquirer_iin, forwarding_iin, transmission_date_time, pan, transaction_type, \
                evonet_qr_order_number, wop_qr_order_number, network_token_pan, qr_transaction_type, mop_id, mop_name, transaction_amount, \
                transaction_currency, original_evonet_order_number, original_wop_order_number, original_mop_order_number, \
                original_system_trace_audit_number, original_acquirer_iin, original_forwarding_iin, original_transmission_date_time, \
                store_id, store_english_name, store_local_name, mcc, city, country, terminal_number = data.split(
                    separator)
                # 获取每条upiFee的数据
                sett_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                          {"trans.evonetOrderNumber": evonet_order_number})
                trans_data = sett_data["trans"]
                card_data = trans_data["card"]
                store_info = trans_data["storeInfo"]
                raw_data = trans_data["rawData"]
                assert exception_type == sett_data["blendType"]
                assert wop_order_number == trans_data["wopOrderNumber"]
                assert mop_order_number == trans_data["mopOrderNumber"]
                assert system_trace_audit_number == raw_data["systemTraceAuditNum"]
                assert acquirer_iin == raw_data["acquirerIIN"]
                assert forwarding_iin == raw_data["forwardingIIN"]
                assert transmission_date_time == raw_data["transmissionDateTime"]
                assert pan == card_data["maskedNumber"]
                assert transaction_type == trans_data["transType"]
                if transaction_type != "Account Credit":
                    qr_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                            {"trans.mopID": mop_id,
                                                             "trans.qrcVoucherNo": sett_data["trans"][
                                                                 "qrcVoucherNo"]})[
                        "trans"]
                    assert evonet_qr_order_number == qr_data["evonetOrderNumber"]
                    assert wop_qr_order_number == qr_data["wopOrderNumber"]
                    assert qr_transaction_type == qr_data["transType"]
                    assert network_token_pan == card_data["networkTokenPan"]

                assert mop_id == trans_data["mopID"]
                assert mop_name == self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mop_id})["baseInfo"][
                    "mopName"]
                assert trans_data["transAmount"] == self.comm_funcs.amount_conver(transaction_amount)
                assert transaction_currency == trans_data["transCurrency"]
                assert store_info["id"] == store_id
                assert store_info["englishName"] == store_english_name
                assert store_info["mcc"] == mcc
                assert store_info["city"] == city
                assert store_info["country"] == country
                assert store_info["terminalNumber"] == terminal_number
                if transaction_type == "Refund":
                    orig_rawdata = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                                 {
                                                                     "trans.evonetOrderNumber": original_evonet_order_number})[
                        "trans"]["rawData"]

                    assert original_system_trace_audit_number == orig_rawdata["systemTraceAuditNum"]
                    assert original_acquirer_iin == orig_rawdata["acquirerIIN"]
                    assert original_forwarding_iin == orig_rawdata["forwardingIIN"]
                    assert original_transmission_date_time == orig_rawdata["transmissionDateTime"]
                count += 1
            assert count == 3  # 校验进入到文件中的数据的数量正确

    def mdaq_resolve_assert(self, file_name):
        # mdap文件解析校验
        with open(file_name, mode="rt", encoding="utf-8") as file:
            file.readline()
            file_content = file.readlines()
            for line in file_content:
                batch_id, advice_type, advice_id, transaction_id, account_name, ccy_pair, related_advice_id, side, \
                transaction_currency, consumer_currency, transaction_currency_type, amount, transaction_type, scenario, settlement_amount, \
                settlement_currency, payment_provider, transaction_timestamp, requested_pricing_ref_id, client_ref, actual_pricing_ref_id, price, \
                contra_amount, value_date, mdaq_price, contra_amount_mrate, profit_ccy, profit_amount, fixing_adjustment, status, error_code, error_reason, \
                process_timestamp, receive_timestamp, profit_value_date, m_value_date, valid_timestamp, original_profit_amount, beneficiary_alias, \
                derived_transaction_type, service_fee = line.strip().split(
                    ",")
                data = self.tyo_evosettle_db.get_one(self.common_name.advice_file, {'adviceId': advice_id})
                assert data['batchId'] == batch_id
                assert data['adviceType'] == advice_type
                assert data['adviceId'] == advice_id
                assert data['transactionId'] == transaction_id
                assert data['accountName'] == account_name
                assert data['ccyPair'] == ccy_pair
                assert data['relatedAdviceId'] == related_advice_id
                assert data['side'] == side
                assert data['transactionCcy'] == transaction_currency
                assert data['consumerCcy'] == consumer_currency
                assert data['transactionCcyType'] == transaction_currency_type
                assert data['transactionType'] == transaction_type
                assert data['scenario'] == scenario
                assert data['settlementCcy'] == settlement_currency
                assert data['paymentProvider'] == payment_provider
                assert data['transactionTimestamp'] == transaction_timestamp
                assert data['requestedPricingRefId'] == requested_pricing_ref_id
                assert data['clientRef'] == client_ref
                assert data['actualPricingRefId'] == actual_pricing_ref_id
                assert data['valueDate'] == value_date
                assert data['profitCcy'] == profit_ccy
                assert data['status'] == status
                assert data['errorCode'] == error_code
                assert data['errorReason'] == error_reason
                assert data['processTimestamp'] == process_timestamp
                assert data['receiveTimestamp'] == receive_timestamp
                assert data['profitValueDate'] == profit_value_date
                assert data['mValueDate'] == m_value_date
                assert data['validTimestamp'] == valid_timestamp
                assert data['beneficiaryAlias'] == beneficiary_alias
                assert data['derivedTransactionType'] == derived_transaction_type
                assert data['originalProfitAmount'] == float(original_profit_amount)
                assert data['serviceFee'] == service_fee  # 这个就应该是字符串、
                assert data['amount'] == float(amount)
                assert data['settlementAmount'] == float(settlement_amount)
                assert data['price'] == float(price)
                assert data['contraAmount'] == float(contra_amount)
                assert data['mdaqPrice'] == float(mdaq_price)
                assert data['contraAmountMRate'] == float(contra_amount_mrate)
                assert data['profitAmount'] == float(profit_amount)
                assert data['fixingAdjustment'] == float(fixing_adjustment)
                assert data['reconFlag'] == int(2)
                assert data["expectValueDate"] == "".join(value_date.split("-"))

    def mdaq_recon_file_assert(self, recon_file_name):
        with open(recon_file_name, mode="rt", encoding="utf-8") as file:
            assert file.readline().strip() == self.common_name.mdaq_recon_file_title
            file_content = file.readlines()  # 读取所有行为列表

            for line in file_content:
                traceid, batch_id, advice_type, advice_id, transaction_id, related_advice_id, account_name, \
                ccy_pair, side, transaction_currency, consumer_currency, transaction_currency_type, amount, \
                transaction_type, scenario, settlement_amount, settlement_currency, payment_provider, \
                transaction_timestamp, requested_pricing_ref_id, beneficiary, beneficiary_alias, client_ref, \
                status, actual_pricing_ref_id, price, contra_amount, value_date, m_value_date, mdaq_rate, mdaq_price, \
                contra_amount_mrate, profit_ccy, profit_amount, original_profit_amount, profit_value_date, fixing_adjustment, \
                fxg_adj_client_profit, original_batch_id, error_code, error_reason, process_timestamp, receive_timestamp, \
                valid_timestamp, derived_transaction_type, service_fee, evonet_order_number, orig_evonet_order_number, \
                settle_date, expect_value_date, recon_flag, advice_time, create_time = line.strip().split(
                    ',')
                # 组一一对应的列表
                file_orig_data = self.tyo_evosettle_db.get_one(self.common_name.advice, {"adviceId": advice_id})
                data_list = [
                    ['batchId', batch_id], ['adviceType', advice_type], ['adviceId', advice_id],
                    ['transactionId', transaction_id], ['relatedAdviceId', related_advice_id],
                    ['accountName', account_name], ['ccyPair', ccy_pair], ['side', side],
                    ['transactionCcy', transaction_currency], ['consumerCcy', consumer_currency],
                    ['transactionCcyType', transaction_currency_type], ['amount', float(amount)],
                    ['transactionType', transaction_type], ['scenario', scenario],
                    ['settlementAmount', float(settlement_amount)],
                    ['settlementCcy', settlement_currency], ['paymentProvider', payment_provider],
                    ['transactionTimestamp', transaction_timestamp],
                    ['requestedPricingRefId', requested_pricing_ref_id],
                    ['beneficiaryAlias', beneficiary_alias], ['clientRef', client_ref], ['status', status],
                    ['actualPricingRefId', actual_pricing_ref_id], ['price', float(price)],
                    ['contraAmount', float(contra_amount)], ['valueDate', value_date],
                    ['mValueDate', m_value_date],
                    ['contraAmountMRate', float(contra_amount_mrate)],
                    ['profitCcy', profit_ccy], ['profitAmount', float(profit_amount)],
                    ['originalProfitAmount', float(original_profit_amount)],
                    ['profitValueDate', profit_value_date],
                    ['fixingAdjustment', float(fixing_adjustment)], ['errorCode', error_code],
                    ['errorReason', error_reason],
                    ['processTimestamp', process_timestamp], ['receiveTimestamp', receive_timestamp],
                    ['validTimestamp', valid_timestamp], ['derivedTransactionType', derived_transaction_type],
                    ['expectValueDate', expect_value_date], ['reconFlag', int(recon_flag)],
                    ['mdaqPrice', float(mdaq_price)],
                    ['serviceFee', service_fee],
                ]
                for m in data_list:
                    assert file_orig_data[m[0]] == m[1]
                for data in [['origEvonetOrderNumber', orig_evonet_order_number], ['settleDate', settle_date],
                             ['beneficiary', beneficiary], ['fxgAdjClientProfit', float(fxg_adj_client_profit)],
                             ['originalBatchId', original_batch_id], ['evonetOrderNumber', evonet_order_number],
                             ['mdaqRate', float(mdaq_rate)]]:
                    if file_orig_data.get(data[0]):
                        assert file_orig_data.get(data[0]) == data[1]
            # [advice_time],[settle_date], [beneficiary], [fxg_adj_client_profit],
            # [original_batch_id], [evonet_order_number], [orig_evonet_order_number], [mdaq_rate],
            # ['createTime', create_time], advice_time这两个字段不校验

    def trans_message_assert(self, mopid, wopid1, wopid2, wopid3, wop_settlecurrency, settle_currency, settle_date):
        for wopid in [wopid1, wopid2, wopid3]:
            fee = 0
            settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_summary_mop, {"wopID": wopid})
            for data in settle_data:
                data = data["summary"]
                every_fee = Decimal(str(data["interchangeFee"])) + Decimal(
                    str(data["transProcessingFee"])) + Decimal(
                    str(data["fxProcessingFee"]))
                fee += every_fee
            fee = float(fee)
            trans_message_data = self.tyo_evosettle_db.get_one(self.common_name.trans_message, {"wopID": wopid})
            if fee == 0:
                assert trans_message_data == None
                continue  # 后面就不执行了，执行下一轮
            # 获取trans_message表的数据
            trans_message_data = self.tyo_evosettle_db.get_one(self.common_name.trans_message, {"wopID": wopid})
            mopid_currency = self.tyo_config_db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"][
                "beneficiary"]
            assert trans_message_data["transType"] == "Fee"
            assert trans_message_data["wopSettleCurrency"] == wop_settlecurrency
            assert trans_message_data["wopSettleAmount"] == 0.0
            assert trans_message_data["mopSettleCurrency"] == settle_currency
            assert trans_message_data["mopSettleAmount"] == fee
            assert trans_message_data["sopSettleAmount"] == 0.0
            assert trans_message_data["ropSettleAmount"] == 0.0
            assert trans_message_data["settleDate"] == settle_date
            assert trans_message_data["beneficiary"] == mopid_currency
            assert trans_message_data["mopID"] == mopid
            evonet_number = trans_message_data["evonetOrderNumber"]
            advice_data = self.tyo_evosettle_db.get_one(self.common_name.advice,
                                                        {"evonetOrderNumber": evonet_number})
            ccpair = "{}/{}".format(settle_currency, wop_settlecurrency)

            re_fid = self.tyo_config_db.get_one('raw_fx_rate_current', {'ccyPair': ccpair})['refID']
            assert advice_data["adviceType"] == "EA"
            assert advice_data["transactionId"] == evonet_number
            assert advice_data["ccyPair"] == ccpair  # 就是mopsetlecurrency和mopsettlecurrency的对比
            assert advice_data["transactionCcy"] == settle_currency  # mop清算币种
            # 假如transSumamry手续费小于0 则如下

            if fee < 0:
                assert advice_data["consumerCcy"] == settle_currency
            if fee > 0:
                assert advice_data["consumerCcy"] == wop_settlecurrency  # wop清算币种
            assert advice_data["transactionCcyType"] == "DELIV"  # 默认就是这个  requestedPricingRefId
            assert advice_data["requestedPricingRefId"] == re_fid
            assert advice_data["amount"] == abs(fee)
            assert advice_data["transactionType"] == "SALE"
            assert advice_data["scenario"] == "OFFLINE_PAYMENT"
            assert advice_data["beneficiary"] == mopid_currency
            assert advice_data["docStatus"] == "INITIAL"
            assert advice_data["settleDate"] == settle_date
            assert advice_data["expectValueDate"] == str(int(settle_date) + 1)  # 日期类型转换
            assert advice_data["reconFlag"] == int(0)
            if fee != 0:
                # 删除 trans_message的数据，advice表的数据，为第二次生报表做准备
                self.tyo_evosettle_db.delete_manys(self.common_name.trans_summary_mop, {"wopID": wopid})
                self.tyo_evosettle_db.delete_manys(self.common_name.trans_message,
                                                   {'evonetOrderNumber': evonet_number})
                self.tyo_evosettle_db.delete_manys(self.common_name.advice, {'evonetOrderNumber': evonet_number})

    def settle_task_request(self, url, owner_type, owner_id, includ_id, sett_date, function, model, file_init,
                            node_type="dual", ):
        """
        :param url: 请求的url
        :param owner_type:  wop  或者mop
        :param owner_id:    wopid 或者 mopid
        :param includ_id:   wopid 或者mopid
        :param model:       直清，非直清
        :param function:
        :param file_init:
        :param sett_date:
        :return:
        """
        data = {
            "settleTask": {
                "ownerID": owner_id,
                "ownerType": owner_type,
                "parameters": {
                    "functions":
                        function
                    ,
                    "includeWOPIDs":
                        includ_id
                    ,
                    "includeMOPIDs":
                        includ_id
                    ,
                    "model": model,
                    "fileInitiator": file_init,
                    "nodeType": node_type
                }
            },
            "settleDate": sett_date

        }

        print(data)
        if file_init == "mop":
            data["settleTask"]["parameters"]["specialType"] = "UPI"
        header = {
            'Content-Type': 'application/json'
        }

        result = requests.post(url, headers=header, json=data)
        # 清分返回的tranceID,当出现异常时会返回对应的function的唯一 标志
        result = result.json()
        result["request_data"] = data
        print(result)
        assert result["data"]["Result"] == 'success'

    def mdaq_request(self, task_name, task_handler, settle_date):
        header = {
            'Content-Type': 'application/json'
        }

        data = {
            "taskName": task_name,
            "handler": task_handler,
            "settleDate": settle_date
        }
        result = requests.post(url=self.get_config.get_ini("mdap_func_url"), headers=header, json=data)
