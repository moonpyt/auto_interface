from base.read_config import *
import requests
import time
import random
from base.db import MongoDB
from common.evosettle.comm_funcs import CommonName
from base.encrypt import Encrypt, Aesecb
from common.evosettle.mongo_data import CreateConfig


class DatabaseConnect(object):
    def __init__(self, envirs, path=None, title=None):
        if path == None:
            self.path = abspath(__file__, '../../config/evosettle/evosettle_' + envirs + '.ini')
        if title == None:
            self.title = 'trans_data'
        else:
            self.title = title
        self.evosettle_config = ConfigIni(self.path, self.title)
        self.encrypt = Encrypt()
        self.aes_decrypt = Aesecb(self.encrypt.decrypt(self.evosettle_config.get_ini("server_key")))
        self.decrypt_info = Encrypt()
        self.tyo_config_db = MongoDB(self.decrypt_info.decrypt(self.evosettle_config.get_ini("tyo_config_url")),
                                     "evoconfig")
        self.tyo_evosettle_db = MongoDB(self.decrypt_info.decrypt(self.evosettle_config.get_ini("tyo_settle_url")),
                                        "evosettle")

        self.sgp_evosettle_db = MongoDB(self.decrypt_info.decrypt(self.evosettle_config.get_ini("sgp_settle_url")),
                                        "evosettle")
        self.sgp_config_db = MongoDB(self.decrypt_info.decrypt(self.evosettle_config.get_ini("sgp_config_url")),
                                     "evoconfig")
        self.sgp_evopay_db = MongoDB(
            self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_evopay_url")), "evopay")
        self.tyo_evopay_db = MongoDB(
            self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_evopay_url")), "evopay")
        self.performance_evoconfig_db = MongoDB(
            self.aes_decrypt.decrypt(self.evosettle_config.get_ini("performance_evoconfig_url")),
            "evoconfig")
        self.performance_evosettle_db = MongoDB(
            self.aes_decrypt.decrypt(self.evosettle_config.get_ini("performance_evosetltle_url")),
            "evosettle")
        self.comm_name = CommonName()


class DatabaseOperations(object):

    # 获取 tyo 或者 sgp 节点中的相关表的中的字段并进行操作
    def __init__(self, envirs, path=None, title=None):
        if path == None:
            self.path = abspath(__file__, '../../config/evosettle/evosettle_' + envirs + '.ini')
        if title == None:
            self.title = 'trans_data'
        self.evosettle_config = ConfigIni(self.path, self.title)
        self.decrypt_info = Encrypt()
        # 初始化tyo,sgp数据连接对象
        self.database_connect = DatabaseConnect(envirs)
        self.tyo_config_db = self.database_connect.tyo_config_db
        self.tyo_evosettle_db = self.database_connect.tyo_evosettle_db
        self.sgp_config_db = self.database_connect.sgp_config_db
        self.sgp_evosettle_db = self.database_connect.sgp_evosettle_db
        self.create_config = CreateConfig()
        self.comm_name = CommonName()

    def get_file_info_record(self, owner_type, first_role, file_type, file_sub_type, extension):
        """
        :param wopid:
        :param file_type:
        :param file_sub_type:
        :param extension:
        :return:
        """
        if owner_type == "wop":
            db = self.tyo_evosettle_db
        if owner_type == "mop":
            db = self.sgp_evosettle_db
        file_name = db.get_one("fileInfo",
                               {"firstRole": first_role, "fileType": file_type,
                                "fileSubType": file_sub_type, "extension": extension})[
            "fileName"]
        file_path = db.get_one("fileInfo",
                               {"firstRole": first_role, "fileType": file_type,
                                "fileSubType": file_sub_type, "extension": extension})[
            "filePath"]
        return file_path, file_name

    def get_evonet_detail_info_record(self, id, sett_date):
        file_name = self.evosettle_db.get_one("fileInfo",
                                              {"firstRole": id, "secondRole": "EVONET", "fileType": "Settlement",
                                               "fileSubType": "Details", "settleDate": sett_date})["fileName"]
        file_path = self.evosettle_db.get_one("fileInfo",
                                              {"firstRole": id, "fileType": "Settlement",
                                               "fileSubType": "Details", "settleDate": sett_date})["filePath"]
        return file_path, file_name

    def get_settlement_detail_info_record(self, owner_type, wopid, mopid, sett_date, file_type="Settlement",
                                          file_subtype="Details"):
        if owner_type == "wop":
            id_one = wopid
            id_two = mopid
        else:
            id_one = mopid
            id_two = wopid

        file_name = self.evosettle_db.get_one("fileInfo",
                                              {"firstRole": id_one, "secondRole": id_two, "fileType": file_type,
                                               "fileSubType": file_subtype, "settleDate": sett_date})["fileName"]
        file_path = self.evosettle_db.get_one("fileInfo",
                                              {"firstRole": id_one, "secondRole": id_two, "fileType": file_type,
                                               "fileSubType": file_subtype})["filePath"]
        return file_path, file_name

    def delete_direct_single_config(self, wopid, mopid):
        # 删除配置
        for conn in [self.tyo_config_db, self.sgp_config_db]:
            conn.delete_manys("wop", {"baseInfo.wopID": wopid})
            conn.delete_manys("mop", {"baseInfo.mopID": mopid})
            conn.delete_manys("customizeConfig", {"wopID": wopid})
            conn.delete_manys("customizeConfig", {"mopID": mopid})
            conn.delete_manys("relation", {"wopID": wopid})
            conn.delete_manys("relation", {"mopID": mopid})
        for conn in [self.tyo_evosettle_db, self.sgp_evosettle_db]:
            conn.delete_manys("wop", {"baseInfo.wopID": wopid})
            conn.delete_manys("mop", {"baseInfo.mopID": mopid})
            conn.delete_manys("customizeConfig", {"wopID": wopid})
            conn.delete_manys("customizeConfig", {"mopID": mopid})
            conn.delete_manys("settleTask", {"ownerID": wopid})
            conn.delete_manys("settleTask", {"ownerID": mopid})

    def create_single_config(self, wopid, mopid, model, fileinit, date_monthly_type, date_daily_type, brand_id,
                             mop_node_id):
        # 创建直清模式的配置，根据mop_node_ide来区分单双节点
        wop_date, mop_date, custom_date, relation_data = self.create_config.create_config_info(wopid,
                                                                                               mopid,
                                                                                               model,
                                                                                               fileinit,
                                                                                               date_monthly_type,
                                                                                               date_daily_type,
                                                                                               brand_id,
                                                                                               mop_node_id)
        # 插入tyo节点，同步任务会将数据同步到sgp节点
        self.tyo_config_db.insert_one("wop", wop_date)
        self.tyo_config_db.insert_one("mop", mop_date)
        self.tyo_config_db.insert_one("customizeConfig", custom_date)
        self.tyo_config_db.insert_one("relation", relation_data)
        # ---------------------
        # self.sgp_config_db.insert_one("wop", wop_date)
        # self.sgp_config_db.insert_one("mop", mop_date)
        # self.sgp_config_db.insert_one("customizeConfig", custom_date)
        # self.sgp_config_db.insert_one("relation", relation_data)

    def mdaq_create_single_config(self, wopid, mopid, model, fileinit, date_monthly_type, date_daily_type, brand_id,
                                  mop_node_id):
        # 创建直清模式的配置，根据mop_node_ide来区分单双节点
        wop_date, mop_date, custom_date, relation_data = self.create_config.create_config_info(wopid,
                                                                                               mopid,
                                                                                               model,
                                                                                               fileinit,
                                                                                               date_monthly_type,
                                                                                               date_daily_type,
                                                                                               brand_id,
                                                                                               mop_node_id)
        self.tyo_config_db.insert_one("wop", wop_date)
        self.tyo_config_db.insert_one("customizeConfig", custom_date)
        self.tyo_config_db.insert_one("relation", relation_data)

    def delete_trans_summary(self, wopid, mopid):
        for table in ["transSummary.mop", "transSummary.wop"]:
            self.tyo_evosettle_db.delete_manys(table, {"$or": [{"wopID": wopid}, {"mopID": mopid}]})
            self.sgp_evosettle_db.delete_manys(table, {"$or": [{"wopID": wopid}, {"mopID": mopid}]})

    def delete_trans_file_wop_record(self, wopid, mopid):
        # 删除wopfile的记录解析的记录
        self.tyo_evosettle_db.delete_manys("transFile.wop", {"$or": [{"wopID": wopid}, {"mopID": mopid}]})
        self.sgp_evosettle_db.delete_manys("transFile.wop", {"$or": [{"wopID": wopid}, {"mopID": mopid}]})

    def delete_fileinfo_file_wop(self, wopid, mopid, sett_date):
        # 删除 fileinfo中的 wopfile的记录
        self.evosettle_db.delete_manys("fileInfo", {"firstRole": mopid, "secondRole": wopid, "settleDate": sett_date,
                                                    "fileType": "WOPFile", "fileSubType": "Details"})

    def delete_trans_data(self, wopid, mopid):
        self.tyo_evosettle_db.delete_manys("trans", {"$or": [{"wopID": wopid}, {"mopID": mopid}]})
        self.sgp_evosettle_db.delete_manys("trans", {"$or": [{"wopID": wopid}, {"mopID": mopid}]})

    def delete_sftp_info(self, wopid):
        self.tyo_evosettle_db.delete_manys("sftpInfo", {"ownerID": wopid})
        self.sgp_evosettle_db.delete_manys("sftpInfo", {"ownerID": wopid})

    def delete_direct_fileinfo(self, wopid, mopid):
        # 删除 fileinfo记录，wopid为wop_auto_开头，或者，mopid以mop_auto开头
        self.tyo_evosettle_db.delete_manys("fileInfo", {"$or": [{"firstRole": wopid}, {"firstRole": mopid}]})
        self.sgp_evosettle_db.delete_manys("fileInfo", {"$or": [{"firstRole": wopid}, {"firstRole": mopid}]})

    def delet_trans_sett_table_data(self, wopid, mopid):
        # 删除transSett.wop，或者mop的数据
        for table in ["transSettle.wop", "transSettle.mop"]:
            self.tyo_evosettle_db.delete_manys(table,
                                               {"$or": [{"trans.wopID": wopid}, {"trans.mopID": mopid}]})
            self.sgp_evosettle_db.delete_manys(table,
                                               {"$or": [{"trans.wopID": wopid}, {"trans.mopID": mopid}]})

    def get_fxrate_fee(self, owner_type, source_currency, dst_currency):
        # 获取fxrate的value
        if owner_type == "wop":
            return self.tyo_config_db.get_one("fxRate",
                                              {"sourceCurrency": source_currency, "destinationCurrency": dst_currency,
                                               "fxRateOwner": "evonet"})["value"]
        else:
            return self.sgp_config_db.get_one("fxRate",
                                              {"sourceCurrency": source_currency, "destinationCurrency": dst_currency,
                                               "fxRateOwner": "evonet"})["value"]

    def get_converter_currency_flag(self, evonet_order_number):
        return \
            self.evosettle_db.get_one(self.trans_sett_table, {"trans.evonetOrderNumber": evonet_order_number})[
                "trans"][
                self.converter_currency_flag]

    def get_mop_converter_currency_flag(self, wopid, mopid, evonet_order_number, table="transSettle.wop"):
        return \
            self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)["trans"][
                "mopConverterCurrencyFlag"]

    def get_currency_decimal(self, ownere_type, currency_code):
        if ownere_type == "wop":
            return self.tyo_config_db.get_one("currency", {"code": currency_code})["decimal"]
        if ownere_type == "mop":
            return self.sgp_config_db.get_one("currency", {"code": currency_code})["decimal"]

    def get_self_sett_date(self, wopid, mopid, sett_date):
        # 获取自主清算的数据
        return self.evosettle_db.get_many(self.trans_sett_table,
                                          {"trans.wopID": wopid, "trans.mopID": mopid, "settleDate": sett_date})

    def get_cpm_mpm_data(self, owner_type, wopid, mopid, sett_date):
        # 获取正向cpm,mpm类型的交易,且计费成功的数据
        if owner_type == "wop":
            db = self.tyo_evosettle_db
            table = self.comm_name.trans_settle_wop
        if owner_type == "mop":
            db = self.sgp_evosettle_db
            table = self.comm_name.trans_settle_mop
        return db.get_many(table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                   "trans.transType": {
                                       "$in": ["CPM Payment", "MPM Payment"]},
                                   "settleDate": sett_date, })

    def get_self_sett_data(self, wopid, mopid, sett_date):
        return self.evosettle_db.get_many(self.trans_sett_table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                  "settleDate": sett_date, "clearFlag": True,
                                                                  "blendType": "selfSettle"
                                                                  })

    def get_sett_data(self, wopid, mopid, sett_date):
        return self.evosettle_db.get_many(self.trans_sett_table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                                  "settleDate": sett_date, "clearFlag": True,
                                                                  "settleFlag": True
                                                                  })

    def get_trans_file_wop_node(self, wopid, mopid, sett_date):
        return self.evosettle_db.get_many("transFile.wopNode", {"wopID": wopid, "mopID": mopid,
                                                                "settleDate": sett_date,
                                                                })

    def get_self_sett_data_counts(self, wopid, mopid, sett_date):
        # 获取 transSett.wop表中自主清算的数据 counts
        return self.evosettle_db.count(self.trans_sett_table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                               "settleDate": sett_date, "settleFlag": True
                                                               })

    def get_wopnode_self_sett_counts(self, wopid, mopid, sett_date):
        # 获取解析出文件的数据的count
        return self.evosettle_db.count("transFile.wopNode", {"wopID": wopid, "mopID": mopid,
                                                             "settleDate": sett_date,
                                                             })

    def delete_trans_file_wop_node(self, wopid, mopid):
        self.tyo_evosettle_db.delete_manys("transFile.wopNode", {"wopID": wopid})
        self.sgp_evosettle_db.delete_manys("transFile.wopNode", {"mopID": mopid})

    def delete_settle_func_log(self, wopid, mopid):
        self.tyo_evosettle_db.delete_manys(self.comm_name.settle_funcLog, {"$or": [{"wopID": wopid}, {"mopID": mopid}]})
        self.sgp_evosettle_db.delete_manys(self.comm_name.settle_funcLog, {"$or": [{"wopID": wopid}, {"mopID": mopid}]})

    def tyo_wop_settlement_info(self, wopid):
        return self.tyo_config_db.get_one("wop", {"baseInfo.wopID": wopid})[
            "settleInfo"]

    def get_settlement_info(self, owner_type, id):
        # table  wop表或者mop表
        # id   为 wopid  mopid
        if owner_type == "wop":
            return self.tyo_config_db.get_one("wop", {"baseInfo.wopID": id})[
                "settleInfo"]
        else:
            return self.sgp_config_db.get_one("mop", {"baseInfo.mopID": id})[
                "settleInfo"]

    def mop_settlement_info(self, mopid):
        return self.config_db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"]

    def custom_settlement_info(self, wopid, mopid):
        return self.config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})

    def wop_service_fee_info(self, wopid):
        # 获取wop表的的service
        return self.config_db.get_one("wop", {"baseInfo.wopID": wopid})["settleInfo"]

    def mop_service_fee_info(self, mopid):
        # 获取wop表的的service
        return self.config_db.get_one("mop", {"mopID": mopid})["settleInfo"]

    def custom_config_service_fee_info(self, owner_type, wopid, mopid):
        # 个性化表
        if owner_type == "wop":
            return self.tyo_config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})
        if owner_type == "mop":
            return self.sgp_config_db.get_one("customizeConfig", {"wopID": wopid, "mopID": mopid})

    def trans_refund_data(self, wopid, mopid, sett_date):
        # 获取trans表refund的交易类型的数据
        return self.evosettle_db.get_many("trans", {"wopID": wopid, "mopID": mopid,
                                                    "wopSettleDate": sett_date,
                                                    "mopSettleDate": sett_date, "transType": "Refund"})

    def cpm_mpm_trans(self, wopid, mopid, sett_date):
        # 获取trans表中cpm,mpm交易的数据
        return self.evosettle_db.get_many("trans",
                                          {"wopID": wopid, "mopID": mopid, "wopSettleDate": sett_date,
                                           "mopSettleDate": sett_date,
                                           "transType": {
                                               "$in": ["CPM Payment", "MPM Payment"]}})

    def trans_sett_cpm_mpm_trans(self, table_name, wopid, mopid, sett_date):
        # 获取清算表中cpm,mpm交易的数据
        return self.evosettle_db.get_many(table_name,
                                          {"trans.wopID": wopid, "trans.mopID": mopid, "settleDate": sett_date,
                                           "trans.transType": {
                                               "$in": ["CPM Payment", "MPM Payment"]}})

    def trans_sett_refund_trans(self, table_name, wopid, mopid, sett_date):
        # 获取transSett.wop或mop的refund
        return self.evosettle_db.get_many(table_name, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                       "trans.transType": "Refund",
                                                       "settleDate": sett_date})

    def refund_update_status(self, wopid, mopid, sett_date, table):
        return self.evosettle_db.update_many(table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                     "trans.transType": "Refund",
                                                     "settleDate": sett_date},
                                             {"trans.status": "evonet_status_test"})

    def cpm_mpm_update_status(self, wopid, mopid, sett_date, table):
        # 修改状态为 status
        return self.evosettle_db.update_many(table, {"trans.wopID": wopid, "trans.mopID": mopid,
                                                     "trans.transType": {
                                                         "$in": ["CPM Payment", "MPM Payment"]},
                                                     "settleDate": sett_date},
                                             {"trans.status": "evonet_test_status"})

    def update_clear_fee_flag(self, node_type, wopid, mopid, ):
        # 修改的前置条件
        if node_type == "wop":
            db = self.tyo_evosettle_db
            table = self.comm_name.trans_settle_wop
        else:
            db = self.sgp_evosettle_db
            table = self.comm_name.trans_settle_mop

        db.update_many(table,
                       {"trans.wopID": wopid, "trans.mopID": mopid},
                       {"clearFlag": False, "feeFlag": False, "settleInfo.processingFee": 0.0,
                        "settleInfo.fxProcessingFee": 0.0,
                        "settleInfo.interchangeFee": 0.0,
                        "settleFlag": True,
                        "blendType": "success"})

    def unset_mccr(self, wopid, mopid, table_name):
        if table_name == "customizeConfig":
            self.evosettle_db.unset_many(table_name, {"wopID": wopid, "mopID": mopid}, ["mccr"])
        if table_name == "mop":
            self.evosettle_db.unset_many(table_name, {"baseInfo.wopID": wopid, "baseInfo.mopID": mopid}, ["mccr"])

    def set_trans_currency(self, wopid, mopid, table, trans_currency):
        # 设置此币种对应的mop 表或者 customizeconfig 表中交易币种的mccr 为空
        trans_currencies = [{"currency": trans_currency}]
        if table == "customizeConfig":
            # 查询出的是列表
            self.config_db.update_one(table, {"mopID": mopid, "wopID": wopid},
                                      {"transCurrencies": trans_currencies})
        if table == "mop":
            self.config_db.update_one(table, {"mopID": mopid, "wopID": wopid},
                                      {"transCurrencies": trans_currencies})

    def trans_obj(self, evonet_order_number):
        # 取trans表中的evonetOrderNumber对应的body
        return self.evosettle_db.get_one("trans", {"evonetOrderNumber": evonet_order_number})

    def trans_sett_wop_obj(self, wopid, mopid, evonet_order_number, table):
        # 取清算表表中的 trans.evonetOrderNumber对应的body
        return self.evosettle_db.get_one(table,
                                         {"trans.evonetOrderNumber": evonet_order_number, "trans.wopID": wopid,
                                          "trans.mopID": mopid})
        # 获取transSettle.wop trans的 整体

    def trans_status(self, evonet_order_number):
        return self.evosettle_db.get_one(self.trans_sett_table, {"trans.evonetOrderNumber": evonet_order_number})[
            "trans"]["status"]  # 获取transSettle.wop trans的 状态

    def blendkey_from(self, wopid, mopid, evonet_order_number, table):
        # 取
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "trans"]["evonetOrderNumber"]

    def blendkey(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "blendKey"]

    def blend_type(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "blendType"]

    def clear_flag(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "clearFlag"]

    def fee_flag(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "feeFlag"]

    def sett_flag(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "settleFlag"]

    def trans_currency_outside(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "transCurrency"]

    def trans_currency_inside(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "trans"]["transCurrency"]

    def trans_amount_outside(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "transAmount"]

    def sett_currency_inside(self, wopid, mopid, evonet_order_number, table, settle_currency):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "trans"][settle_currency]

    def sett_currency_outside(self, wopid, mopid, evonet_order_number, table):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["settleCurrency"]

    def sett_amount_inside(self, wopid, mopid, evonet_order_number, table, settle_amt):
        # 取清算表
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "trans"][settle_amt]

    def trans_amount_inside(self, owner_type, evonet_order_number):
        # 取清算表

        if owner_type == "wop":
            db = self.tyo_evosettle_db
            table = self.comm_name.trans_settle_wop
        if owner_type == "mop":
            db = self.sgp_evosettle_db
            table = self.comm_name.trans_settle_mop
        return db.get_one(table, {"trans.transType": {
            "$in": ["CPM Payment", "MPM Payment"]}, "trans.evonetOrderNumber": evonet_order_number})["trans"][
            "transAmount"]

    def sett_amount_outside(self, owner_type, evonet_order_number):
        if owner_type == "wop":
            db = self.tyo_evosettle_db
            table = self.comm_name.trans_settle_wop
        if owner_type == "mop":
            db = self.sgp_evosettle_db
            table = self.comm_name.trans_settle_mop
        return db.get_one(table, {"trans.transType": {
            "$in": ["CPM Payment", "MPM Payment"]}, "trans.evonetOrderNumber": evonet_order_number})["settleInfo"][
            "settleAmount"]

    def inter_chang_fee(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["interchangeFee"]

    def fee_receive_able(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)['settleInfo'][
            "feeReceivable"]

    def fee_payable(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)['settleInfo'][
            "feePayable"]

    def fee_error_flag(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字f段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)['settleInfo'][
            "feeErrorFlag"]

    def amount_erroe_flag(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)["amountErrorFlag"]

    def get_wop_settle_currency(self, wopid, mopid, evonet_order_number, table):
        return \
            self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
                "trans"]["wopSettleCurrency"]

    def get_mop_settle_currency(self, wopid, mopid, evonet_order_number, table):
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)["trans"][
            "mopSettleCurrency"]

    def inter_change_fee_refund(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["interchangeFeeRefund"]

    def trans_processing_fee(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["processingFee"]

    def fxprocessing_fee(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["fxProcessingFee"]

    def rebate(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["rebate"]

    def rebate_ccr(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            'settleInfo']["rebateCCR"]

    def settle_date(self, wopid, mopid, evonet_order_number, table):
        # 取清算表 settleInfo json 报文的字段
        return self.trans_sett_wop_obj(wopid, mopid, evonet_order_number, table)[
            "settleDate"]

    def sett_model(self, evonet_order_number):
        # 取清算表 settleInfo json 报文的字段
        return self.evosettle_db.get_one(self.trans_sett_table, {"trans.evonetOrderNumber": evonet_order_number})[
            'settleInfo']["settleMode"]

    @property
    def function_result(self):
        # 获取清算表中 settlefunc.log 中的result
        return \
            self.evosettle_db.get_one("settleFuncLog", {"wopID": self.wopid, "mopID": self.mopid})["result"]
