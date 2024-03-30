import random, zipfile, hashlib, shutil
from common.evosettle.task_funcs import TaskFuncs
from base.read_config import *
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evosettle.comm_funcs import CommonName
from common.evosettle.create_report_data import CreateReportData
from common.evosettle.parmiko_module import Parmiko_Module
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData


class UpiFunction(object):
    # 银联模式  双节点时，tyo 为mop节点，sgp为 wop节点：单节点则是 tyo即时mop节点 又是 wop节点
    # 重构之后其它模式只需要调用对应的方法并传入对应的参数就执对应的方法了，不需要每个模式都再写一遍，有需要的话，只需要在这里修改了，还可以通过多线程的方式调用case
    def __init__(self, envirs, sett_date, model, fileinit,
                 path=None, title=None, ):
        if path == None:
            path = abspath(__file__, '../../../config/evosettle/evosettle_' + envirs + '.ini')
        if title == None:
            title = 'trans_data'
        self.evosettle_config = ConfigIni(path, title)
        self.encrypt = Encrypt()
        self.task_func = TaskFuncs(envirs)
        self.db_operations = DatabaseOperations(envirs)
        self.model = model
        self.fileinit = fileinit
        self.case_data = CaseData()
        self.trans_type_list = ["CPM Payment", "MPM Payment", "Refund"]
        self.create_report_data = CreateReportData()
        self.sett_date = sett_date
        # 月报日期，每月四号生月报
        self.month_file_sett_date = '20210204'
        self.database_connect = DatabaseConnect(envirs)
        self.tyo_config_db = self.database_connect.tyo_config_db
        self.tyo_evosettle_db = self.database_connect.tyo_evosettle_db
        self.sgp_config_db = self.database_connect.sgp_config_db
        self.sgp_evosettle_db = self.database_connect.sgp_evosettle_db
        self.sgp_evopay_db = self.database_connect.sgp_evopay_db
        self.sftp_func = Parmiko_Module()
        self.tyo_func_url = self.evosettle_config.get_ini("tyo_func_url")  # tyo节点单个任务的url
        self.sgp_func_url = self.evosettle_config.get_ini("sgp_func_url")  # sgp节点单个任务的url
        self.tyo_ip = self.evosettle_config.get_ini("tyo_ip")
        self.tyo_user = self.evosettle_config.get_ini("tyo_user")
        self.sgp_ip = self.evosettle_config.get_ini("sgp_ip")
        self.sgp_user = self.evosettle_config.get_ini("sgp_user")
        self.aes_decrypt = Aesecb(self.encrypt.decrypt(self.evosettle_config.get_ini("server_key")))
        self.common_name = CommonName()
        #  删除的查询参数   {"baseInfo.wopID" :{"$regex":"^WOP_Auto"}}

    def mop_settle_task(self, owner_id, include_id, function):
        """
        清分任务task请求
        :param owner_type:  wop 或者 mop
        :param owner_id:    如果 owner_type为wopid，则 owner_id为wopid;如果 owner_type为mop，则owner_id为mopid
        :param includ_id:  列表类型
        :param function:    settle_task  要执行的  function
        :return:
        """
        self.task_func.settle_task_request(self.tyo_func_url, "mop", owner_id, include_id, self.sett_date,
                                           function, self.model, self.fileinit)

    def wop_settle_task(self, owner_id, include_id, function):
        """
        清分任务task请求
        :param owner_type:  wop 或者 mop
        :param owner_id:    如果 owner_type为wopid，则 owner_id为wopid;如果 owner_type为mop，则owner_id为mopid
        :param includ_id:
        :param function:    settle_task  要执行的  function
        :return:
        """

        self.task_func.settle_task_request(self.sgp_func_url, "wop", owner_id, include_id, self.sett_date,
                                           function, self.model, self.fileinit, )

    def assert_func_result(self, wopid, func_name):
        result = \
            self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid, "function": func_name})[
                "result"]

    def upi_download_file(self, wopid, file_type, file_subtype, file_extension, currency=None):
        # 月报校验

        file_record = self.sgp_evosettle_db.get_one("fileInfo",
                                                    {"firstRole": wopid, "fileType": file_type,
                                                     "fileSubType": file_subtype, "extension": file_extension})
        if currency:
            file_record = self.sgp_evosettle_db.get_one("fileInfo",
                                                        {"firstRole": wopid, "fileType": file_type,
                                                         "fileSubType": file_subtype, "extension": file_extension,
                                                         "currency": currency})
        file_name = file_record["fileName"]
        file_path = file_record["filePath"]
        remote_path = file_path + "/" + file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.sgp_ip, self.sgp_user, remote_path,
                                         file_name)
        return file_name

    def upload_upi_zip(self, file_name, remote_path):
        # 上传造的银联zip文件，上传到mop侧下载的文件记录
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.ssh_download_file("put", private_key, self.sgp_ip, self.sgp_user, remote_path=remote_path,
                                         local_path=file_name
                                         )

    def update_config(self, wopid, mopid):
        # 修改节点的 nodeID
        self.sgp_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                       {"baseInfo.nodeID": "sgp", "version": int(2)})
        self.sgp_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                       {"baseInfo.nodeID": "tyo", "version": int(2)})

        self.tyo_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                       {"baseInfo.nodeID": "sgp", "version": int(2)})
        self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                       {"baseInfo.nodeID": "tyo", "version": int(2)})

    def update_config_currency(self, wopid, wop_config_currency, custom_currency, wop_settle_currency, trans_currency,
                               trans_amount, wop_settle_amount, trans_fee_rate, trans_mccr_obj=[{"currency": "JPY"}],
                               trans_fee_collect="daily",
                               trans_fee_calc="single",

                               ):

        """
        :param wopid:
        :param wop_config_currency:  wop配置表的settleCurrency
        :param custom_currency:      custom配置表的settleCurrency
        :param wop_settle_currency:  trans表的settleCurrency
        :param trans_currency:       trans表的transCurrency
        :param trans_amount:         trans表的 transAmount
        :param wop_settle_amount:    trans表的 wopsettleAmount
        :param trans_fee_rate        transFee的手续费
        :return:
        """

        self.sgp_evosettle_db.update_many("trans", {"wopID": wopid},
                                          {"transCurrency": trans_currency, "wopSettleCurrency": wop_settle_currency,
                                           "transAmount": trans_amount, "wopSettleAmount": wop_settle_amount})
        self.sgp_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                       {"settleInfo.settleCurrency": wop_config_currency})
        # 手续费收取方式为daily single

        self.sgp_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                                       {"settleCurrency": custom_currency,
                                        "transactionProcessingFeeRate": trans_fee_rate,
                                        "transProcessingFeeCalculatedMethod": trans_fee_calc,
                                        "transProcessingFeeCollectionMethod": trans_fee_collect,
                                        "transCurrencies": trans_mccr_obj
                                        })

    def assert_upi_trans_fee(self, wopid, trans_fee, trans_collect="single"):
        upi_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                         {"trans.wopID": wopid, "trans.category": "Card"})
        for trans_data in upi_settle_data:
            if trans_collect == "single":
                if trans_data["trans"]["transType"] in ["Account Credit", "Account Debit"]:
                    assert trans_data["settleInfo"]["processingFee"] == trans_fee

                else:
                    # 银联退款类交易
                    assert trans_data["settleInfo"]["processingFee"] == 0
                # 校验计费的交易的状态
            else:
                assert trans_data["settleInfo"]["processingFee"] == 0.0
            assert trans_data["clearFlag"] == True
            assert trans_data["feeFlag"] == True

    def upi_trans_import(self):
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()

        # # wopid = "WOP_SETkrddhb"
        # # mopid = "MOP_SETwrqsml"
        # wopid = "WOP_Jcoin"
        # mopid = "UnionPay"
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)
        data = self.case_data.upi_trans_list(wopid, mopid, self.sett_date, self.model)
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 触发交易流水同步
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        # 校验,transSett.wop表的数据是 一致的，但是会有码和卡的交易
        assert self.sgp_evosettle_db.count("trans", {"wopID": wopid,
                                                     "wopSettleDate": self.sett_date}) == self.sgp_evosettle_db.count(
            self.common_name.trans_settle_wop, {"trans.wopID": wopid, "settleDate": self.sett_date})
        # 检验同步的数据字段正确,校验wop侧
        for number in data[1]:
            # 每次查询一条交易进行校验交易流水导入的初始化的值
            # 传参数 mop 时，是去 sgp相关的数据的库找数据的
            self.task_func.trans_import_assert("wop", number, "upi")
        self.assert_func_result(wopid, self.common_name.wop_trans_import)

    def upi_calcc(self):
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        data = self.case_data.upi_trans_list(wopid, mopid, self.sett_date, self.model)
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # wopid, wop_config_currency, custom_currency, wop_settle_currency, trans_currency, trans_amount, wop_settle_amount

        trans_amount = 1300
        wop_settle_amount = 2300
        trans_fee_rate = 0.05634
        # upi计费1  -----------------------------
        self.update_config_currency(wopid, "CNY", "CNY", "CNY", "CNY",
                                    trans_amount, wop_settle_amount, trans_fee_rate)
        # 触发交易流水同步
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success"})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.assert_upi_trans_fee(wopid, 129.58)
        # 计费2 交易币种和 wop表清算币种一致 --------------------------
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "CNY", "JPY", "JPY", "CNY",
                                    trans_amount, wop_settle_amount, trans_fee_rate)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success",
                                           })

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.assert_upi_trans_fee(wopid, 73.24)
        # 计费3 交易中wopsettlecurrency wop表的settlecurrency不一致且交易币种和 wop表清算币种不一致 --------------------------
        jpy_cny = 0.06368
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        trans_currencies = [
            {
                "mccr": 0.8,
                "currency": "JPY"
            },
            {
                "currency": "CNY",
                "mccr": 0.9
            }
        ]
        self.update_config_currency(wopid, "CNY", "JPY", "USD", "JPY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, trans_currencies)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success",
                                           })
        self.task_func.fx_rate_set("upi", "JPY", "CNY", jpy_cny)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        # 计算公式  交易金额费乘以fxrate(汇率转换)乘以(1+mccr)乘以手续

        # 1300 * jpy_cny * 1.8 * 0.05634
        self.assert_upi_trans_fee(wopid, 8.4)
        # 计费4 交易中wopsettlecurrency wop表的settlecurrency不一致且交易币种和 wop表清算币种不一致 --------------------------
        #   mccr测试  取通用的mccr 计费
        jpy_cny = 0.06368
        mccr = 0.47
        self.task_func.fx_rate_set("upi", "JPY", "CNY", jpy_cny)
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "CNY", "JPY", "USD", "JPY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, )
        self.sgp_config_db.update_many(self.common_name.custom_config, {"wopID": wopid}, {"mccr": mccr})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success",
                                           })
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        # 计算公式  交易金额费乘以fxrate(汇率转换)乘以(1+mccr)乘以手续  (mccr区分 通用和交易的mccr)
        # 1300 * jpy_cny * 1.47 * 0.05634
        self.assert_upi_trans_fee(wopid, 6.86)
        # 计费5 计费方式的测试 ------------------
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "CNY", "JPY", "JPY", "CNY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, trans_fee_calc="monthly",
                                    trans_fee_collect="single")
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success",
                                           })

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.assert_upi_trans_fee(wopid, 73.24)

        # 计费6 清算币种交易币种都是 JPY的测试(小数位的测试) ------------------
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "JPY", "JPY", "JPY", "JPY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, )
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success",
                                           })

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.assert_upi_trans_fee(wopid, 130)

        # 计费6 计费前置条件的测试 ------------------
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "JPY", "JPY", "JPY", "JPY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, )
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        for key in ["clearFlag", "feeFlag", "settleFlag"]:
            flag = True
            if key == "settleFlag":
                flag = False
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                              {"trans.wopID": wopid, "trans.category": "Card"},
                                              {"blendType": "success", key: flag,
                                               "settleInfo.processingFee": 0.0
                                               })
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
            upi_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                      {"trans.wopID": wopid, "trans.category": "Card"})
            for fee_data in upi_data:
                assert fee_data["settleInfo"]["processingFee"] == 0.0
        # 计费 计费状态的测试
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "JPY", "JPY", "JPY", "JPY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, )
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        for status in ["succeeded", "partially refunded", "fully refunded"]:
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                              {"trans.wopID": wopid, "trans.category": "Card"},
                                              {"settleFlag": True, "blendType": "success", "trans.status": status,
                                               "clearFlag": False, "feeFlag": False, "settleInfo.processingFee": 0.0
                                               })

            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
            self.assert_upi_trans_fee(wopid, 130)
        # 非正常交易状态计费(因为交易状态不符合计费条件)--------
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success", "trans.status": "evonet_status",
                                           "clearFlag": False, "feeFlag": False, "settleInfo.processingFee": 0.0
                                           })

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        wrong_status_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {"trans.wopID": wopid, "trans.category": "Card"})
        for status_data in wrong_status_data:
            assert status_data["clearFlag"] == False
            assert status_data["feeFlag"] == False

        # 计费6 计费方式的测试 monthly,accumulation------------------
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "CNY", "JPY", "JPY", "CNY",
                                    trans_amount, wop_settle_amount, trans_fee_rate, trans_fee_calc="accumulation",
                                    trans_fee_collect="monthly")
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success",
                                           })

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.assert_upi_trans_fee(wopid, 0.0, "accumulation")

        # 计费7 隔日退款 monthly,accumulation ------------------
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.update_config_currency(wopid, "CNY", "JPY", "JPY", "CNY",
                                    trans_amount, wop_settle_amount, trans_fee_rate)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        yesterday = str(int(self.sett_date) - 1)
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card",
                                           "trans.transType": {"$in": ["Account Debit", "Account Credit"]}},
                                          {"settleFlag": True, "blendType": "success",
                                           "settleDate": yesterday}
                                          )
        # 前一天计费
        self.task_func.settle_task_request(self.sgp_func_url, "wop", wopid, [mopid], yesterday,
                                           [self.common_name.wop_trans_calc], self.model, self.fileinit)
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card",
                                           "trans.transType": "Refund"},
                                          {"settleFlag": True, "blendType": "success"})

        # 第二天计费
        self.task_func.settle_task_request(self.sgp_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_trans_calc], self.model, self.fileinit)
        refund_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                     {"trans.wopID": wopid, "trans.transType": "Refund",
                                                      "trans.category": "Card"})
        for data in refund_data:
            assert data["clearFlag"] == True
            assert data["feeFlag"] == True

    def upi_settlement_details(self):
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        m = []
        data = self.case_data.upi_trans_list(wopid, mopid, self.sett_date, self.model)

        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 触发交易流水同步
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleFlag": True, "blendType": "success"})
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"settleInfo.feeReceivable": 2.0, "settleInfo.feePayable": 3.0})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_generate_file])

        file_name = self.upi_download_file(wopid, self.common_name.file_type_Settlement,
                                           self.common_name.file_subtype_Details, self.common_name.file_extension_csv)
        self.task_func.upi_settlement_detail_content_assert(file_name)
        os.remove( file_name)
    def upi_fee_collection_details_assert(self):
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID

        for i in range(2):
            self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upifee,
                                              self.case_data.upi_fee_data(wopid, mopid, self.sett_date))
        # 删除nettoken pan 做前置条件
        card_reference = hashlib.sha256("6210948000000243".encode('utf-8')).hexdigest()
        token_pan = "evonet_test_token_pan"
        self.sgp_evopay_db.delete_manys(self.common_name.net_work_token_pan, {
            "cardReference": card_reference})
        # 插入token pan
        self.sgp_evopay_db.insert_one(self.common_name.net_work_token_pan,
                                      {"evonetUserReference": "a2c6594ac1de480752a8e0ddeaaad014",
                                       "wopID": wopid,
                                       "mopID": mopid,
                                       "networkTokenPan": token_pan,
                                       "cardReference": card_reference,
                                       "brandID": "UnionPay",
                                       "status": "active",
                                       "deleteFlag": False})

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_generate_file])

        file_name = self.upi_download_file(wopid, self.common_name.file_type_feecollection,
                                           self.common_name.file_subtype_Details, self.common_name.file_extension_csv)
        self.task_func.upi_feecollection_detail_content_assert(file_name, token_pan)
        os.remove(file_name)

    def upi_feecollection_detail_resolve_assert(self):
        # 需要先造文件上传至服务器，然后触发清分任务，进行下载并解析，然后校验数据库中的数据是否和解析规则一致
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        new_file_name = wopid + "-MOPFile-Complex-" + mopid + "-" + self.sett_date + "-001.zip"
        upi_fcp_file_name = "IFD" + self.sett_date[2:-1] + "01FCP"
        self.create_report_data.upi_fee_data(upi_fcp_file_name)
        with zipfile.ZipFile(new_file_name, mode="w") as file:
            file.write(upi_fcp_file_name)
        # 这个远程路径是自己造的，服务器上有的，假如目录不存在再重新创建即可
        remote_path = "/home/webapp/evofile/rawData/wop/" + wopid + "/in/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.run_cmd(private_key, self.sgp_ip, self.sgp_user, "mkdir -p " + remote_path)
        # fileInfo插入下载的文件记录
        self.sgp_evosettle_db.insert_one(self.common_name.file_info,
                                         self.common_name.upi_file_record(wopid, mopid, self.sett_date, new_file_name,
                                                                          remote_path))
        # 上传造好的银联zip文件,然后执行wop下载文件和解析
        self.upload_upi_zip(new_file_name, remote_path + new_file_name)
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_settle_file_resolve])
        # 文件解析后的校验
        self.task_func.upi_feecollection_details_content_resolve(upi_fcp_file_name)
        # 使用shutil强制刪除文件
        os.remove(upi_fcp_file_name)
        os.remove(new_file_name)

    def upi_dispute_detail_resolve_assert(self):
        # 需要先造文件上传至服务器，然后触发清分任务，进行下载并解析，然后校验数据库中的数据是否和解析规则一致,然后校验生成的报表的数据和文件的是否一致
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        new_file_name = wopid + "-MOPFile-Complex-" + mopid + "-" + self.sett_date + "-001.zip"
        upi_ierrn_file_name = "IFD" + self.sett_date[2:-1] + "01IERRN"
        self.create_report_data.upi_ierrn_data(upi_ierrn_file_name)
        with zipfile.ZipFile(new_file_name, mode="w") as file:
            file.write(upi_ierrn_file_name)
        # 这个远程路径是自己造的，服务器上有的，假如目录不存在再重新创建即可
        remote_path = "/home/webapp/evofile/rawData/wop/" + wopid + "/in/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.run_cmd(private_key, self.sgp_ip, self.sgp_user, "mkdir -p " + remote_path)
        # fileInfo插入下载的文件记录
        self.sgp_evosettle_db.insert_one(self.common_name.file_info,
                                         self.common_name.upi_file_record(wopid, mopid, self.sett_date, new_file_name,
                                                                          remote_path))
        # 上传造好的银联zip文件,然后执行wop下载文件和解析
        self.upload_upi_zip(new_file_name, remote_path + new_file_name)
        # 文件解析和生成文件
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_settle_file_resolve])
        # Credit Adjustment  Debit Adjustment  Chargeback

        # 文件解析后的校验
        self.task_func.upi_ierrn_details_resolve_content_resolve(upi_ierrn_file_name)
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_generate_file])
        dispute_file_name = self.upi_download_file(wopid, self.common_name.file_type_dispute,
                                                   self.common_name.file_subtype_Details,
                                                   self.common_name.file_extension_csv)
        # dispute，生成dispute的文件的校验
        self.task_func.upi_dispute_detail_content_assert(dispute_file_name)
        # 使用shutil强制刪除文件
        os.remove(upi_ierrn_file_name)
        os.remove(new_file_name)

    def upi_exception_details_assert(self):
        # 银联的多清少清的文件的校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)
        data = self.case_data.upi_trans_list(wopid, mopid, self.sett_date, self.model)
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 触发交易流水同步
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.category": "Card"},
                                          {"blendType": "Extra", "settleFlag": True})

        # 修改 blnndType
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.transType": "Account Credit"},
                                          {"blendType": "Lack", "settleFlag": False})
        # 计费生文件
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc, self.common_name.wop_generate_file])
        # 下载文件
        exception_file_name = self.upi_download_file(wopid, self.common_name.file_type_exception,
                                                     self.common_name.file_subtype_Details,
                                                     self.common_name.file_extension_csv)
        # 按照生成 exception文件的规则，校验exception文件中的内容
        self.task_func.upi_exception_detail_content_assert(exception_file_name)
        os.remove(exception_file_name)

    def upi_icom_detail_resolve_assert(self):
        # 需要先造文件上传至服务器，然后触发清分任务，进行下载并解析，然后校验数据库中的数据是否和解析规则一致
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        new_file_name = wopid + "-MOPFile-Complex-" + mopid + "-" + self.sett_date + "-001.zip"
        upi_icom_file_name = "IFD" + self.sett_date[2:-1] + "01ICOMN"
        self.create_report_data.icom_detail_data(upi_icom_file_name)
        with zipfile.ZipFile(new_file_name, mode="w") as file:
            file.write(upi_icom_file_name)
        # 这个远程路径是自己造的，服务器上有的，假如目录不存在再重新创建即可
        remote_path = "/home/webapp/evofile/rawData/wop/" + wopid + "/in/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.run_cmd(private_key, self.sgp_ip, self.sgp_user, "mkdir -p " + remote_path)
        # fileInfo插入下载的文件记录
        self.sgp_evosettle_db.insert_one(self.common_name.file_info,
                                         self.common_name.upi_file_record(wopid, mopid, self.sett_date, new_file_name,
                                                                          remote_path))
        # 上传造好的银联zip文件,然后执行wop下载文件和解析
        self.upload_upi_zip(new_file_name, remote_path + new_file_name)
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_settle_file_resolve])
        # 文件解析后的校验
        self.task_func.upi_icom_details_content_resolve(upi_icom_file_name)
        # # 使用shutil强制刪除文件
        os.remove(upi_icom_file_name)
        os.remove(new_file_name)

    def upi_daily_summary_assert(self):
        # 银联每日Sumamry校验
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        settle_currency = "CNY"
        self.sgp_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                                       {"transProcessingFeeCollectionMethod": "monthly",
                                        "transProcessingFeeCalculatedMethod": "single",
                                        "settleCurrency": settle_currency})

        self.sgp_evosettle_db.update_many("wop", {"baseInfo.wopID": wopid},
                                          {
                                              "settleInfo,settleCurrency": settle_currency})
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        fee_receiveable_amount = 22
        fee_payable_amount = 33
        sumamry_data = []
        # 清算币种为 CNY
        for trans_currency in ["JPY", "CNY"]:
            for trans_type in ["Account Debit", "Account Credit", "Refund"]:
                sumamry_data.extend(
                    self.case_data.upi_daily_summary_data(wopid, mopid, self.sett_date, trans_type, trans_currency,
                                                          "CNY", fee_receiveable_amount, fee_payable_amount))
        self.sgp_evosettle_db.insert_many(self.common_name.trans_settle_wop, sumamry_data)
        self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upierr,
                                          self.case_data.upi_err_data(wopid, mopid, self.sett_date, "JPY", "CNY"))
        # 造 ierr 文件
        self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upierr,
                                          self.case_data.upi_err_data(wopid, mopid, self.sett_date, "CNY", "CNY"))
        # 造 feeCollection文件
        self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upifee,
                                          self.case_data.upi_sumamry_fee_data(wopid, mopid, self.sett_date))
        # 清算币种为 JPY
        sumamry_data = []
        for trans_currency in ["JPY", "CNY"]:
            for trans_type in ["Account Debit", "Account Credit", "Refund"]:
                sumamry_data.extend(
                    self.case_data.upi_daily_summary_data(wopid, mopid, self.sett_date, trans_type, trans_currency,
                                                          "JPY", fee_receiveable_amount, fee_payable_amount))
        self.sgp_evosettle_db.insert_many(self.common_name.trans_settle_wop, sumamry_data)

        self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upierr,
                                          self.case_data.upi_err_data(wopid, mopid, self.sett_date, "JPY", "JPY"))
        # 造 ierr 文件
        self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upierr,
                                          self.case_data.upi_err_data(wopid, mopid, self.sett_date, "CNY", "JPY"))
        # 造 feeCollection文件
        self.sgp_evosettle_db.insert_many(self.common_name.trans_file_upifee,
                                          self.case_data.upi_sumamry_fee_data(wopid, mopid, self.sett_date, "JPY"))

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_generate_file])

        # 银联summary校验#
        file_name = self.upi_download_file(wopid, self.common_name.file_type_Settlement,
                                           self.common_name.file_subtype_Summary, self.common_name.file_extension_xlsx,
                                           "CNY")
        self.task_func.upi_summary_assert(file_name, wopid, mopid, self.sett_date, "CNY")
        os.remove(file_name)
        # 银联summary校验
        file_name = self.upi_download_file(wopid, self.common_name.file_type_Settlement,
                                           self.common_name.file_subtype_Summary, self.common_name.file_extension_xlsx,
                                           "JPY")
        self.task_func.upi_summary_assert(file_name, wopid, mopid, self.sett_date, "JPY")
        os.remove(file_name)

    def upi_icom_reconcile_assert(self):
        # 需要先造文件上传至服务器，然后触发清分任务，进行下载并解析，触发勾兑,先多清，再勾兑平，再少清
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.update_config(wopid, mopid)  # 修改银联的nodeID
        new_file_name = wopid + "-MOPFile-Complex-" + mopid + "-" + self.sett_date + "-001.zip"
        upi_icom_file_name = "IFD" + self.sett_date[2:-1] + "01ICOMN"
        self.create_report_data.icom_detail_data(upi_icom_file_name)
        with zipfile.ZipFile(new_file_name, mode="w") as file:
            file.write(upi_icom_file_name)
        # 这个远程路径是自己造的，服务器上有的，假如目录不存在再重新创建即可
        remote_path = "/home/webapp/evofile/rawData/wop/" + wopid + "/in/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.run_cmd(private_key, self.sgp_ip, self.sgp_user, "mkdir -p " + remote_path)
        # fileInfo插入下载的文件记录
        self.sgp_evosettle_db.insert_one(self.common_name.file_info,
                                         self.common_name.upi_file_record(wopid, mopid, self.sett_date, new_file_name,
                                                                          remote_path))
        # 上传造好的银联zip文件,然后执行wop下载文件和解析
        self.upload_upi_zip(new_file_name, remote_path + new_file_name)
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_settle_file_resolve])
        # # 使用shutil强制刪除文件
        os.remove(upi_icom_file_name)
        os.remove(new_file_name)
        # 下面的流程，是多清的校验
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_trans_reconcile])
        # 校验transSettle.wop 表的数据  settleFlag为True ,blendType为 Extra
        trans_sett_datas = self.sgp_evosettle_db.get_many(self.common_name.trans_file_upi, {"wopID": wopid})
        # 总的订单号
        evonet_numbers = []
        for data in trans_sett_datas:
            evonet_number = data["blendKey"]
            evonet_numbers.append(evonet_number)
        for evonet_number in evonet_numbers:
            trans_file_upi_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upi,
                                                                {"wopID": wopid, "blendKey": evonet_number})
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                       {"trans.wopID": wopid, "blendKey": evonet_number})
            assert trans_data["blendType"] == "Extra"
            assert trans_data["settleFlag"] == True
            assert trans_data["settleInfo"]["settleAmount"] == trans_file_upi_data['trans']["settleAmount"]
            assert trans_data["settleInfo"]["settleCurrency"] == trans_file_upi_data["trans"]["settleCurrency"]
        # 修改transSettle.wop表的数据
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid}, {"blendType": "default", "settleFlag": False,
                                                                   "settleInfo.settleCurrency": "test_currency",
                                                                   "settleInfo.settleAmount": 22.22})
        # 再触发勾兑,并校验勾兑平
        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_trans_reconcile])
        for evonet_number in evonet_numbers:
            trans_file_upi_data = self.sgp_evosettle_db.get_one(self.common_name.trans_file_upi,
                                                                {"wopID": wopid, "blendKey": evonet_number})
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                       {"trans.wopID": wopid, "blendKey": evonet_number})
            assert trans_data["blendType"] == "success"
            assert trans_data["settleFlag"] == True
            assert trans_data["settleInfo"]["settleAmount"] == trans_file_upi_data['trans']["settleAmount"]
            assert trans_data["settleInfo"]["settleCurrency"] == trans_file_upi_data["trans"]["settleCurrency"]
        # ----------------
        # 在全部删除，transFile.upi的数据，再触发勾兑，就为少清了
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_file_upi,
                                           {"wopID": wopid})
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid}, {"blendType": "default", "settleFlag": False, })

        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_trans_reconcile])
        for evonet_number in evonet_numbers:
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                       {"trans.wopID": wopid, "blendKey": evonet_number})
            assert trans_data["blendType"] == "Lack"
            assert trans_data["settleFlag"] == False
        # ---------------------
        # 勾兑条件校验，校验category为card才可以勾兑
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"blendType": "default", "settleFlag": False, "trans.category": "QR"})

        self.wop_settle_task(wopid, [mopid],
                             [self.common_name.wop_trans_reconcile])
        for evonet_number in evonet_numbers:
            trans_data = self.sgp_evosettle_db.get_one(self.common_name.trans_settle_wop,
                                                       {"trans.wopID": wopid, "blendKey": evonet_number})
            assert trans_data["blendType"] == "default"
            assert trans_data["settleFlag"] == False
        # 修改状态使之勾兑平

    def upi_service_fee_report(self):
        for calc_method in ["complex"]:  # accumulation  single
            wopid = self.task_func.generate_wopid()
            mopid = self.task_func.generate_mopid()
            self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            settle_currency = "CNY"
            self.sgp_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                                           {"transProcessingFeeCollectionMethod": "monthly",
                                            "transProcessingFeeCalculatedMethod": "single",
                                            "transactionProcessingFeeRate": 0.0585173,  # 这个不要改,但是，wop表的要和这个不一样
                                            "settleCurrency": "JPY"
                                            })
            self.sgp_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                           {"settleInfo.settleCurrency": settle_currency,
                                            "settleInfo.transactionProcessingFeeRate": 0.0585173
                                            })
            service_data = []

            if calc_method != "complex":
                # 手续费收取方式全是monthly, single, accumulation
                for settle_date in range(20210101, 20210102):  # 共31天的数据
                    for trans_currency in ["CNY", "JPY"]:
                        service_data.extend(
                            self.case_data.upi_servicefee_report(wopid, mopid, trans_currency, str(settle_date),
                                                                 calc_method))
                self.sgp_evosettle_db.insert_many(self.common_name.trans_summary_wop, service_data)
                self.task_func.settle_task_request(self.sgp_func_url, "wop", wopid, [mopid],
                                                   self.month_file_sett_date,
                                                   [self.common_name.wop_fee_generate], self.model, self.fileinit)
            else:
                # 手续费， 手续费收取方式monthly，且 奇数天为single,偶数天为 accumulation
                for settle_date in range(20210101, 20210132):  # 共31天的数据
                    for trans_currency in ["CNY", "JPY"]:
                        if settle_date % 2 == 1:
                            method = "single"
                        else:
                            method = "accumulation"
                        service_data.extend(
                            self.case_data.upi_servicefee_report(wopid, mopid, trans_currency, str(settle_date),
                                                                 method))
                self.sgp_evosettle_db.insert_many(self.common_name.trans_summary_wop, service_data)
                self.task_func.settle_task_request(self.sgp_func_url, "wop", wopid, [mopid],
                                                   self.month_file_sett_date,
                                                   [self.common_name.wop_fee_generate], self.model, self.fileinit)

            accum = self.sgp_evosettle_db.get_one(self.common_name.trans_summary_wop,
                                                  {"serviceFeeFlag.processingCalculatedMethod": "accumulation",
                                                   "wopID": wopid,
                                                   "summary.transType": {"$in": ["Account Credit", ]}})["summary"][
                "transProcessingFeeSettleAmount"]
            sing = self.sgp_evosettle_db.get_one(self.common_name.trans_summary_wop,
                                                 {"serviceFeeFlag.processingCalculatedMethod": "single",
                                                  "wopID": wopid,
                                                  "summary.transType": {"$in": ["Account Credit", ]}})["summary"][
                "transProcessingFee"]

            file_name = self.upi_download_file(wopid, "ServiceFee",
                                               self.common_name.file_subtype_Summary,
                                               self.common_name.file_extension_xlsx)
            self.task_func.upi_servicefee_assert(file_name, wopid, mopid, self.month_file_sett_date, calc_method)

        # 月报校验


if __name__ == '__main__':
    # 双节点测试
    common_name = CommonName()
    funciton_test = UpiFunction("test", "20210110", common_name.bilateral,
                                "mop")


    # funciton_test.upi_calcc()  #有问题




    # -----------下面的没有报错
    # funciton_test.upi_settlement_details()
    # funciton_test.upi_icom_reconcile_assert()
    # funciton_test.upi_trans_import()
    funciton_test.upi_fee_collection_details_assert()
    # funciton_test.upi_feecollection_detail_resolve_assert()
    funciton_test.upi_dispute_detail_resolve_assert()
    #
    funciton_test.upi_exception_details_assert()
    # funciton_test.upi_icom_detail_resolve_assert()
    #
    funciton_test.upi_daily_summary_assert()
    # funciton_test.upi_service_fee_report()

    # funciton_test.upi_feecollection_detail_resolve_assert()



    # funciton_test.task_func.upi_servicefee_assert("WOP_SETTrpzrpa-ServiceFee-Summary-MOP_SETTqilsso-20210204-001.xlsx",
    #                                               "WOP_SETTrpzrpa", "MOP_SETTqilsso", "20210204", "single")

    # funciton_test.task_func.upi_summary_assert("WOP_SETTjfxvxv-Settlement-Summary-MOP_SETTuqdhsr-CNY-20210110-001.xlsx",
    #                                            "WOP_SETTjfxvxv", "MOP_SETTuqdhsr", "20210110")

    # funciton_test.task_func.upi_exception_detail_content_assert("WOP_SETTmmvwbe-Exception-Details-MOP_SETTcnbhfz-20210110-001.csv")
    # funciton_test.task_func.upi_dispute_detail_content_assert(
    #     "WOP_SETTzpgken-Dispute-Details-MOP_SETTuinvat-20210110-001.csv")

    # funciton_test.task_func.upi_ierrn_details_content_resolve("IFD2101101IERRNback")

    # funciton_test.upi_dispute_detail_assert()
    # funciton_test.assert_file("WOP_SETTgeoggl-FeeCollection-Details-MOP_SETTlsrkmz-20210110-001.csv")
