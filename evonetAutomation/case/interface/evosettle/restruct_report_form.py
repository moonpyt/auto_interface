import random, xlrd
from base.read_config import *
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evosettle.comm_funcs import CommonName
from common.evosettle.parmiko_module import Parmiko_Module
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData
from common.evosettle.task_funcs import TaskFuncs


class RestructReportForm(object):
    # 统一以 tyo  为wop节点;sgp  为mop节点
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
        self.sett_date = sett_date
        # 月报日期，每月四号生月报
        self.month_file_sett_date = '20200204'
        self.database_connect = DatabaseConnect(envirs)
        self.tyo_config_db = self.database_connect.tyo_config_db
        self.tyo_evosettle_db = self.database_connect.tyo_evosettle_db
        self.sgp_config_db = self.database_connect.sgp_config_db
        self.sgp_evosettle_db = self.database_connect.sgp_evosettle_db
        self.sftp_func = Parmiko_Module()
        self.tyo_func_url = self.evosettle_config.get_ini("tyo_func_url")  # tyo节点单个任务的url
        self.sgp_func_url = self.evosettle_config.get_ini("sgp_func_url")  # spg节点单个任务的url
        self.tyo_ip = self.evosettle_config.get_ini("tyo_ip")
        self.tyo_user = self.evosettle_config.get_ini("tyo_user")
        self.sgp_ip = self.evosettle_config.get_ini("sgp_ip")
        self.sgp_user = self.evosettle_config.get_ini("sgp_user")
        self.aes_decrypt = Aesecb(self.encrypt.decrypt(self.evosettle_config.get_ini("server_key")))
        self.common_name = CommonName()

    def wop_settle_task(self, owner_id, include_id, function):
        """
        清分任务task请求
        :param owner_type:  wop 或者 mop
        :param owner_id:    如果 owner_type为wopid，则 owner_id为wopid;如果 owner_type为mop，则owner_id为mopid
        :param includ_id:  列表类型
        :param function:    settle_task  要执行的  function
        :return:
        """
        self.task_func.settle_task_request(self.tyo_func_url, "wop", owner_id, include_id, self.sett_date,
                                           function, self.model, self.fileinit)

    def mop_settle_task(self, owner_id, include_id, function):
        """
        清分任务task请求
        :param owner_type:  wop 或者 mop
        :param owner_id:    如果 owner_type为wopid，则 owner_id为wopid;如果 owner_type为mop，则owner_id为mopid
        :param includ_id:
        :param function:    settle_task  要执行的  function
        :return:
        """

        self.task_func.settle_task_request(self.sgp_func_url, "mop", owner_id, include_id, self.sett_date,
                                           function, self.model, self.fileinit)

    def report_trans_list(self, wopid, mopid, settle_currency, trans_currency, every_date=None):
        # 为了退款计费而造的交易
        if every_date:
            report_date = every_date
        else:
            report_date = self.sett_date
        mpm_order_number = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_orig_cpm_evonet_order_nuber = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_order_number = str(random.randint(100000000000000000000, 900000000000000000000))

        mpm_sett_data = self.case_data.trans_data(wopid, mopid, report_date, "MPM Payment", mpm_order_number,
                                                  )
        orig_cpm_sett_data = self.case_data.trans_data(wopid, mopid, report_date, "CPM Payment",
                                                       refund_orig_cpm_evonet_order_nuber, )
        # CPM退款交易
        refund_cpm_sett_data = self.case_data.trans_data(wopid, mopid, report_date, "Refund", refund_order_number,
                                                         refund_orig_evonet_order_nuber=refund_orig_cpm_evonet_order_nuber)
        sett_trans_list = [mpm_sett_data, orig_cpm_sett_data, refund_cpm_sett_data]
        order_number_list = [mpm_order_number, refund_orig_cpm_evonet_order_nuber, refund_order_number]

        for i in sett_trans_list:
            i["wopSettleCurrency"] = settle_currency
            i["mopSettleCurrency"] = settle_currency
            i["transCurrency"] = trans_currency
        return (sett_trans_list, order_number_list)

    def evonet_mode_wop_function(self, wopid, mopid_list):
        self.wop_settle_task(wopid, mopid_list,
                             [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                              self.common_name.wop_trans_calc, self.common_name.wop_generate_file])

    def evonet_mode_mop_function(self, mopid, wopid_list):
        self.mop_settle_task(mopid, wopid_list,
                             [self.common_name.mop_trans_import, self.common_name.mop_self_sett,
                              self.common_name.mop_trans_calc, self.common_name.mop_generate_file])

    def generate_wop_month_report(self, wopid, mopid_list):
        self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, mopid_list, self.month_file_sett_date,
                                           [self.common_name.wop_fee_file], self.model, self.fileinit)

    def generate_mop_month_report(self, mopid, wopid_list):
        self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, wopid_list, self.month_file_sett_date,
                                           [self.common_name.mop_fee_file], self.model, self.fileinit)

    def wop_settlement_detail_assert(self, wopid, trans_fee_collection_method,
                                     fx_fee_collection_method, fxrebate_fee_collection_method):
        # details中的字段的校验
        file_path, file_name = self.db_operations.get_file_info_record("wop", wopid,
                                                                       self.common_name.file_type_Settlement,
                                                                       self.common_name.file_subtype_Details,
                                                                       self.common_name.file_extension_csv)
        remote_path = file_path + "/" + file_name
        local_path = file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         local_path)
        self.task_func.wop_settlement_daily_detail_assert(
            local_path, wopid, self.sett_date, self.model, trans_fee_collection_method,
            fx_fee_collection_method, fxrebate_fee_collection_method)
        os.remove(local_path)

    def mop_settlement_detail_assert(self, mopid, trans_fee_collection_method,
                                     fx_fee_collection_method, ):
        # details中的字段的校验
        file_path, file_name = self.db_operations.get_file_info_record("mop", mopid,
                                                                       self.common_name.file_type_Settlement,
                                                                       self.common_name.file_subtype_Details,
                                                                       self.common_name.file_extension_csv)
        remote_path = file_path + "/" + file_name
        local_path = file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.sgp_ip, self.sgp_user, remote_path,
                                         local_path)
        self.task_func.mop_settlement_daily_detail_assert(
            local_path, mopid, self.sett_date, self.model, trans_fee_collection_method,
            fx_fee_collection_method, )
        os.remove(local_path)

    def wop_summary_assert(self, wopid, mopid_list, trans_fee_collection_method,
                           fx_fee_collection_method, fxrebate_fee_collection_method):
        # 每日summary的 校验
        # 每日Summary的文件路径及 文件名
        file_path, file_name = self.db_operations.get_file_info_record("wop", wopid,
                                                                       self.common_name.file_type_Settlement,
                                                                       self.common_name.file_subtype_Summary,
                                                                       self.common_name.file_extension_xlsx)
        remote_path = file_path + "/" + file_name
        local_path = file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         local_path)
        self.task_func.wop_daily_summary_assert(
            local_path, wopid, mopid_list, self.sett_date, trans_fee_collection_method,
            fx_fee_collection_method, fxrebate_fee_collection_method)

        # os.remove(local_path)

    def mop_summary_assert(self, mopid, trans_fee_collection_method, fx_fee_collection_method):
        # 每日summary的 校验
        # 每日Summary的文件路径及 文件名
        file_path, file_name = self.db_operations.get_file_info_record("mop", mopid,
                                                                       self.common_name.file_type_Settlement,
                                                                       self.common_name.file_subtype_Summary,
                                                                       self.common_name.file_extension_xlsx)
        remote_path = file_path + "/" + file_name
        local_path = file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.sgp_ip, self.sgp_user, remote_path,
                                         local_path)
        self.task_func.mop_daily_summary_assert(
            local_path, mopid, self.sett_date, self.model, trans_fee_collection_method, fx_fee_collection_method)
        # os.remove(local_path)

    def evonet_mode_wop_settlement_details(self, trans_fee_collection_method, fx_fee_collection_method,
                                           fxrebate_fee_collection_method,
                                           trans_fee_calcu_method, fx_fee_calcu_method):
        # 测试evonet模式一个wopid对应两个mopId的交易

        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        mopid2 = self.task_func.generate_mopid()
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置wop表的配置
        self.tyo_config_db.delete_manys("wop",
                                        {"baseInfo.wopID": wopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid, mopid2, self.model, self.fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "settleInfo.fxRebateCollectionMethod": fxrebate_fee_collection_method
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for mopid in [mopid1, mopid2]:
                    self.tyo_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])
        # evonet模式执行正常function,生报表，
        # ---每日 setlement details校验
        self.evonet_mode_wop_function(wopid, [mopid1, mopid2])

        # 每日settlement_details的校验
        self.wop_settlement_detail_assert(wopid, trans_fee_collection_method,
                                          fx_fee_collection_method,
                                          fxrebate_fee_collection_method)

    def evonet_mode_wop_summary(self, trans_fee_collection_method, fx_fee_collection_method,
                                fxrebate_fee_collection_method,
                                trans_fee_calcu_method, fx_fee_calcu_method):
        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        mopid2 = self.task_func.generate_mopid()
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置wop表的配置
        self.tyo_config_db.delete_manys("wop",
                                        {"baseInfo.wopID": wopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid, mopid2, self.model, self.fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "settleInfo.fxRebateCollectionMethod": fxrebate_fee_collection_method
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for mopid in [mopid1, mopid2]:
                    self.tyo_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])
        # evonet模式执行正常function,生报表，
        # ---每日 setlement details校验
        self.evonet_mode_wop_function(wopid, [mopid1, mopid2])
        # # ----每日Summary校验
        self.wop_summary_assert(wopid, [mopid1, mopid2], trans_fee_collection_method,
                                fx_fee_collection_method,
                                fxrebate_fee_collection_method)

    def evonet_mode_wop_service_report(self, trans_fee_collection_method, fx_fee_collection_method,
                                       fxrebate_fee_collection_method,
                                       trans_fee_calcu_method, fx_fee_calcu_method):
        # 测试evonet模式一个wopid对应两个mopId月报的交易

        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        mopid2 = self.task_func.generate_mopid()
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置wop表的配置
        self.tyo_config_db.delete_manys("wop",
                                        {"baseInfo.wopID": wopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid, mopid2, self.model, self.fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "settleInfo.fxRebateCollectionMethod": fxrebate_fee_collection_method
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for mopid in [mopid1, mopid2]:
                    self.tyo_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])
        # evonet模式执行正常function,生报表，
        self.evonet_mode_wop_function(wopid, [mopid1, mopid2])
        # # 每日月报校验，通过这个后面校验一个月的月报
        self.generate_wop_month_report(wopid, [mopid1, mopid2])
        # 月报校验
        self.evonet_wop_daily_service_assert(wopid, trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             fxrebate_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method, )

    def evonet_mode_mop_summary(self, trans_fee_collection_method, fx_fee_collection_method,
                                trans_fee_calcu_method, fx_fee_calcu_method):
        mopid = self.task_func.generate_mopid()
        wopid1 = self.task_func.generate_wopid()
        wopid2 = self.task_func.generate_wopid()
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        self.db_operations.create_single_config(wopid1, mopid, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置wop表的配置
        self.tyo_config_db.delete_manys("mop",
                                        {"baseInfo.mopID": mopid})
        self.sgp_config_db.delete_manys("mop",
                                        {"baseInfo.mopID": mopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid2, mopid, self.model, self.fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for wopid in [wopid1, wopid2]:
                    self.sgp_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])
        # evonet模式执行正常function,生报表，
        # ---每日 setlement details校验
        self.evonet_mode_mop_function(mopid, [wopid1, wopid2])

        # # ----每日Summary校验
        self.mop_summary_assert(mopid, trans_fee_collection_method, fx_fee_collection_method
                                )

    def evonet_mode_mop_settlement_details(self, trans_fee_collection_method, fx_fee_collection_method,
                                           trans_fee_calcu_method, fx_fee_calcu_method):
        # 测试evonet模式一个wopid对应两个mopId的交易
        # 模式四则是 daily 和 monthly
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        mopid = self.task_func.generate_mopid()
        wopid1 = self.task_func.generate_wopid()
        wopid2 = self.task_func.generate_wopid()
        self.db_operations.create_single_config(wopid1, mopid, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置wop表的配置
        self.tyo_config_db.delete_manys("mop",
                                        {"baseInfo.mopID": mopid})
        self.sgp_config_db.delete_manys("wop",
                                        {"baseInfo.mopID": mopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid2, mopid, self.model, self.fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for wopid in [wopid1, wopid2]:
                    self.sgp_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])
        # evonet模式执行正常function,生报表，
        # ---每日 setlement details 校验
        self.evonet_mode_mop_function(mopid, [wopid1, wopid2])

        # 每日settlement_details的校验
        self.mop_settlement_detail_assert(mopid, trans_fee_collection_method,
                                          fx_fee_collection_method)

    def empty_settlement_details(self, ):
        for model in [self.common_name.bilateral, self.common_name.evonet]:
            if model == self.common_name.bilateral:
                for file_init in ['wop', self.common_name.evonet]:
                    wopid = self.task_func.generate_wopid()
                    mopid1 = self.task_func.generate_mopid()
                    self.db_operations.create_single_config(wopid, mopid1, model, file_init,
                                                            "monthly", "monthly",
                                                            str(random.randint(100000, 9900000)),
                                                            "sgp")
                    # ---每日 setlement details校验
                    self.wop_settle_task(wopid, [mopid1], [self.common_name.wop_generate_file])

                    # self.wop_settlement_detail_assert(wopid, 'monthly',
                    #                                   'monthly',
                    #                                   fxrebate_fee_collection_method="daily")
                    self.wop_summary_assert(wopid, [mopid1], "daily",
                                            "daily",
                                            "daily")

                    # self.mop_settle_task(mopid1, [wopid], [self.common_name.mop_generate_file])
                    # self.mop_settlement_detail_assert(mopid1, 'monthly', 'monthly')

            if model == self.common_name.evonet:
                file_init = self.common_name.evonet
                wopid = self.task_func.generate_wopid()
                mopid1 = self.task_func.generate_mopid()
                self.db_operations.create_single_config(wopid, mopid1, model, file_init,
                                                        "monthly", "monthly",
                                                        str(random.randint(100000, 9900000)),
                                                        "sgp")
                # ---每日 setlement details校验
                self.wop_settle_task(wopid, [mopid1], [self.common_name.wop_generate_file])

                self.wop_settlement_detail_assert(wopid, 'daily',
                                                  'daily',
                                                  fxrebate_fee_collection_method="daily")
                # self.mop_settle_task(mopid1, [wopid], [self.common_name.mop_generate_file])
                # self.mop_settlement_detail_assert(mopid1, 'daily', 'daily', )

    def bilateral_mode_wop_settlement_details(self, trans_fee_calcu_method, fx_fee_calcu_method):

        # 测试直清模式一个wopid对应一个 mopId的交易
        trans_fee_collection_method = "monthly"
        fx_fee_collection_method = "monthly"
        fxrebate_fee_collection_method = "daily"
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one(self.common_name.custom_config, {"wopID": wopid},
                                      {
                                          "settleCurrency": settle_currency,
                                          "transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "fxRebateCollectionMethod": fxrebate_fee_collection_method
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for mopid in [mopid1]:
                    self.tyo_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])

        # evonet模式执行正常function,生报表，
        # ---每日 setlement details校验
        if self.fileinit == "evonet":
            self.wop_settle_task(wopid, [mopid1], [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                                                   self.common_name.wop_trans_calc, self.common_name.wop_generate_file])
        else:
            self.tyo_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                           {"settleInfo.settleCurrency": settle_currency, })
            self.wop_settle_task(wopid, [mopid1], [self.common_name.wop_trans_import])
            # 修改interchangFee，并计费
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                              {"trans.wopID": wopid},
                                              {"settleInfo.interchangeFee": 33.33,
                                               "blendType": "selfSettle",
                                               "settleFlag": True})
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                              {"trans.wopID": wopid, "trans.transType": "Refund"},
                                              {"settleInfo.interchangeFee": 22.22})
            self.wop_settle_task(wopid, [mopid1], [self.common_name.wop_trans_calc,
                                                   self.common_name.wop_generate_file])

        # 每日settlement_details的校验
        self.wop_settlement_detail_assert(wopid, trans_fee_collection_method,
                                          fx_fee_collection_method,
                                          fxrebate_fee_collection_method="daily")

    def bilateral_mode_mop_settlement_details(self, trans_fee_calcu_method, fx_fee_calcu_method):

        # 测试直清模式一个mopid对应一个 mopId的交易
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        trans_fee_collection_method = "monthly"
        fx_fee_collection_method = "monthly"
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.sgp_config_db.update_one(self.common_name.custom_config, {"mopid": mopid},
                                      {
                                          "settleCurrency": settle_currency,
                                          "transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                      })
        for i in range(2):  # 造一个mopid对应两个mopid的交易，且mopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.sgp_evosettle_db.insert_many("trans",
                                                  self.report_trans_list(wopid, mopid,
                                                                         settle_currency,
                                                                         trans_currency)[0])

        # evonet模式执行正常function,生报表，
        # ---每日 setlement details校验
        if self.fileinit == "evonet":
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, self.common_name.mop_self_sett,
                                                  self.common_name.mop_trans_calc, self.common_name.mop_generate_file])
        else:
            self.sgp_config_db.update_many("mop", {"baseInfo.mopid": mopid},
                                           {"settleInfo.settleCurrency": settle_currency})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
            # 修改interchangFee，并计费
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                              {"trans.mopID": mopid},
                                              {"settleInfo.interchangeFee": 33.33,
                                               "blendType": "success",
                                               "settleFlag": True})
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                              {"trans.mopid": mopid, "trans.transType": "Refund"},
                                              {"settleInfo.interchangeFee": 22.22})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc,
                                                  self.common_name.mop_generate_file])

        # 每日settlement_details的校验
        self.mop_settlement_detail_assert(mopid, trans_fee_collection_method,
                                          fx_fee_collection_method,
                                          )

    def evonet_wop_daily_service_assert(self, wopid, trans_fee_collection_method,
                                        fx_fee_collection_method,
                                        fxrebate_fee_collection_method,
                                        trans_fee_calcu_method, fx_fee_calcu_method, model="evonet"):
        # 月报校验

        file_path, file_name = self.db_operations.get_file_info_record("wop", wopid,
                                                                       self.common_name.file_type_ServiceFee,
                                                                       self.common_name.file_subtype_Summary,
                                                                       self.common_name.file_extension_xlsx)
        remote_path = file_path + "/" + file_name
        local_path = file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         local_path)
        if model == "evonet":
            self.task_func.wop_daily_service_assert(local_path, trans_fee_collection_method,
                                                    fx_fee_collection_method,
                                                    fxrebate_fee_collection_method,
                                                    trans_fee_calcu_method, fx_fee_calcu_method)
        if model == self.common_name.bilateral:
            self.task_func.bilateral_wop_service_content_assert(local_path,
                                                                trans_fee_collection_method,
                                                                fx_fee_collection_method,
                                                                trans_fee_calcu_method, fx_fee_calcu_method)

        os.remove(local_path)

    def evonet_mop_daily_service_assert(self, mopid, trans_fee_collection_method,
                                        fx_fee_collection_method,
                                        trans_fee_calcu_method, fx_fee_calcu_method, model="evonet"):
        # 月报校验

        file_path, file_name = self.db_operations.get_file_info_record("mop", mopid,
                                                                       self.common_name.file_type_ServiceFee,
                                                                       self.common_name.file_subtype_Summary,
                                                                       self.common_name.file_extension_xlsx)
        remote_path = file_path + "/" + file_name
        local_path = file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.sftp_func.ssh_download_file("get", private_key, self.sgp_ip, self.sgp_user, remote_path,
                                         local_path)
        if model == "evonet":
            self.task_func.mop_daily_service_assert(mopid, local_path, self.month_file_sett_date,
                                                    trans_fee_collection_method,
                                                    fx_fee_collection_method,
                                                    trans_fee_calcu_method, fx_fee_calcu_method)
        if model == self.common_name.bilateral:
            self.task_func.bilateral_mop_service_content_assert(local_path,
                                                                trans_fee_collection_method,
                                                                fx_fee_collection_method,
                                                                trans_fee_calcu_method, fx_fee_calcu_method)

        os.remove(local_path)

    def custom_evonet_model_wop_report(self):
        # 给客户生的报表
        # 测试一个wopid对应两个mopId的交易
        # 这个evonet模式执行时需要三分钟
        wopid = "WOP_PayboocKR"
        mopid1 = "MOP_JcoinPayJP"
        mopid2 = "MOP_GrabPaySG"
        colllect_method = ["daily", ]
        for trans_fee_collection_method in colllect_method:
            for fx_fee_collection_method in colllect_method:
                for fxrebate_fee_collection_method in colllect_method:

                    # 数据插入到trans表,造两条交易
                    settle_currency = "USD"  # 修改币种及计费方式
                    for i in range(200):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
                        empty_data1 = []

                        data1 = self.report_trans_list(wopid,
                                                       mopid1, settle_currency,
                                                       "JPY")[0]

                        for i in data1:
                            amount = random.randint(10000, 50000)
                            i["transAmount"] = amount
                            settle_amount = self.task_func.round_four_five(amount * 0.00959981, 2)
                            i["wopSettleAmount"] = settle_amount
                            i["transCurrency"] = "JPY"
                            i["wopSettleCurrency"] = "USD"
                            empty_data1.append(i)
                        self.tyo_evosettle_db.insert_many("trans", empty_data1
                                                          )
                        # ---------------------------------
                        data2 = self.report_trans_list(wopid,
                                                       mopid2, settle_currency,
                                                       "SGD")[0]
                        empty_data2 = []
                        for i in data2:
                            amount = random.randint(10000, 50000)
                            i["transAmount"] = amount
                            settle_amount = self.task_func.round_four_five(amount * 0.752431, 2)
                            i["wopSettleAmount"] = settle_amount
                            i["transCurrency"] = "SGD"
                            i["wopSettleCurrency"] = "USD"
                            empty_data2.append(i)
                        self.tyo_evosettle_db.insert_many("trans", empty_data2)
                    # evonet模式执行正常 function,生报表，
        self.evonet_mode_wop_function(wopid, [mopid1, mopid2])

    def custom_envonet_model_mop_report(self):
        # 给客户生的报表
        # 测试一个wopid对应两个mopId的交易
        # 这个evonet模式执行时需要三分钟
        colllect_methos = ["daily", ]
        mopid = "MOP_PayboocKR"
        wopid1 = "WOP_JcoinJP"
        wopid2 = "WOP_GrabPaySG"
        for trans_fee_collection_method in colllect_methos:
            for fx_fee_collection_method in colllect_methos:
                for fxrebate_fee_collection_method in colllect_methos:

                    # 数据插入到trans表,造两条交易
                    settle_currency = "USD"  # 修改币种及计费方式
                    for i in range(200):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
                        empty_data1 = []

                        data1 = self.report_trans_list(wopid1,
                                                       mopid, settle_currency,
                                                       "JPY")[0]

                        for i in data1:
                            amount = random.randint(10000, 50000)
                            i["transAmount"] = amount
                            settle_amount = self.task_func.round_four_five(amount * 0.000909937, 2)
                            i["mopSettleAmount"] = settle_amount
                            i["transCurrency"] = "KRW"
                            i["mopSettleCurrency"] = "USD"
                            empty_data1.append(i)
                        self.sgp_evosettle_db.insert_many("trans", empty_data1
                                                          )
                        # ---------------------------------
                        data2 = self.report_trans_list(wopid2,
                                                       mopid, settle_currency,
                                                       "SGD")[0]
                        empty_data2 = []
                        for i in data2:
                            amount = random.randint(20000, 60000)
                            i["transAmount"] = amount
                            settle_amount = self.task_func.round_four_five(amount * 0.000909937, 2)
                            i["mopSettleAmount"] = settle_amount
                            i["transCurrency"] = "KRW"
                            i["mopSettleCurrency"] = "USD"
                            empty_data2.append(i)
                        self.sgp_evosettle_db.insert_many("trans", empty_data2)

                    # evonet模式执行正常function,生报表，
        self.evonet_mode_mop_function(mopid, [wopid1, wopid2])

    def super_wop_long_summary(self):
        # 测试超长PDF这个不能自动化
        colllect_methos = ["daily", ]
        for trans_fee_collection_method in colllect_methos:
            for fx_fee_collection_method in colllect_methos:
                for fxrebate_fee_collection_method in colllect_methos:
                    wopid = self.task_func.generate_wopid()
                    mopid1 = self.task_func.generate_mopid()
                    mopid2 = self.task_func.generate_mopid()
                    mopid3 = self.task_func.generate_mopid()
                    mopid4 = self.task_func.generate_mopid()
                    mopid5 = self.task_func.generate_mopid()
                    mopid6 = self.task_func.generate_mopid()
                    mopid7 = self.task_func.generate_mopid()
                    mopid8 = self.task_func.generate_mopid()
                    mopid9 = self.task_func.generate_mopid()
                    mopid10 = self.task_func.generate_mopid()
                    mopid11 = self.task_func.generate_mopid()
                    mopid12 = self.task_func.generate_mopid()

                    settle_currency = "CNY"  # 修改币种及计费方式
                    # 创建配置 1
                    for mopid in [mopid1, mopid2, mopid3, mopid4, mopid5, mopid6, mopid7, mopid8, mopid9, mopid10,
                                  mopid11, ]:
                        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                                "monthly", str(random.randint(100000, 9900000)),
                                                                "sgp")
                        # 删除配置wop表的配置
                        self.tyo_config_db.delete_manys(self.common_name.file_init_wop,
                                                        {"baseInfo.wopID": wopid})
                    self.db_operations.create_single_config(wopid, mopid12, self.model, self.fileinit, "monthly",
                                                            "monthly", str(random.randint(100000, 9900000)),
                                                            "sgp")
                    # 触发流水导入
                    # 数据插入到trans表,造两条交易
                    self.sgp_config_db.update_one("mop", {"baseInfo.mopID": wopid},
                                                  {"settleInfo.settleCurrency": settle_currency,
                                                   "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                                   "settleInfo.transProcessingFeeCalculatedMethod": "single",
                                                   "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                                   "settleInfo.fxProcessingFeeCalculatedMethod": "single",
                                                   "settleInfo.fxRebateCollectionMethod": fxrebate_fee_collection_method
                                                   })

                    for mopid in [mopid1, mopid2, mopid3, mopid4, mopid5, mopid6, mopid7, mopid8, mopid9, mopid10,
                                  mopid11]:  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
                        for i in range(2):
                            for trans_currency in ["CNY", "JPY"]:
                                self.tyo_evosettle_db.insert_many("trans",
                                                                  self.report_trans_list(wopid,
                                                                                         mopid,
                                                                                         settle_currency,
                                                                                         trans_currency)[
                                                                      0])

                    # evonet模式执行正常function,生报表，
                    # ---每日 setlement details校验
                    self.evonet_mode_wop_function(wopid,
                                                  [mopid1, mopid2, mopid3, mopid4, mopid5, mopid6, mopid7, mopid8,
                                                   mopid9,
                                                   mopid10, mopid11, mopid12])

                    # 触发生月报
                    self.generate_wop_month_report(wopid, [mopid1,
                                                           mopid2, mopid3, mopid4, mopid5, mopid6, mopid7,
                                                           mopid8, mopid9, mopid10, mopid11, mopid12])

    def super_mop_long_summary(self):
        # 测试超长PDF这个不能自动化
        colllect_methos = ["daily", ]
        for trans_fee_collection_method in colllect_methos:
            for fx_fee_collection_method in colllect_methos:
                mopid = self.task_func.generate_mopid()
                wopid1 = self.task_func.generate_wopid()
                wopid2 = self.task_func.generate_wopid()
                wopid3 = self.task_func.generate_wopid()
                wopid4 = self.task_func.generate_wopid()
                wopid5 = self.task_func.generate_wopid()
                wopid6 = self.task_func.generate_wopid()
                wopid7 = self.task_func.generate_wopid()
                wopid8 = self.task_func.generate_wopid()
                wopid9 = self.task_func.generate_wopid()
                wopid10 = self.task_func.generate_wopid()
                wopid11 = self.task_func.generate_wopid()
                wopid12 = self.task_func.generate_wopid()

                settle_currency = "CNY"  # 修改币种及计费方式
                # 创建配置 1
                for wopid in [wopid1, wopid2, wopid3, wopid4, wopid5, wopid6, wopid7, wopid8, wopid9, wopid10,
                              wopid11]:
                    self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                            "monthly", str(random.randint(100000, 9900000)),
                                                            "sgp")
                    # 删除配置wop表的配置
                    self.tyo_config_db.delete_manys("mop",
                                                    {"baseInfo.mopID": mopid})
                    self.sgp_config_db.delete_manys("mop",
                                                    {"baseInfo.mopID": mopid})
                self.db_operations.create_single_config(wopid12, mopid, self.model, self.fileinit, "monthly",
                                                        "monthly", str(random.randint(100000, 9900000)),
                                                        "sgp")
                # 触发流水导入
                # 数据插入到trans表,造两条交易
                self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                              {"settleInfo.settleCurrency": settle_currency,
                                               "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                               "settleInfo.transProcessingFeeCalculatedMethod": "single",
                                               "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                               "settleInfo.fxProcessingFeeCalculatedMethod": "single",

                                               })

                for wopid in [wopid1, wopid2, wopid3, wopid4, wopid5, wopid6, wopid7, wopid8, wopid9, wopid10,
                              wopid11, wopid12]:  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
                    for i in range(2):
                        for trans_currency in ["CNY", "JPY"]:
                            self.sgp_evosettle_db.insert_many("trans",
                                                              self.report_trans_list(wopid,
                                                                                     mopid,
                                                                                     settle_currency,
                                                                                     trans_currency)[
                                                                  0])

                # evonet模式执行正常function,生报表，
                # ---每日 setlement details校验
                self.evonet_mode_mop_function(mopid,
                                              [wopid1, wopid2, wopid3, wopid4, wopid5, wopid6, wopid7, wopid8, wopid9,
                                               wopid10, wopid11, wopid12])
                # 触发生月报
                self.generate_mop_month_report(mopid,
                                               [wopid1, wopid2, wopid3, wopid4, wopid5, wopid6, wopid7, wopid8, wopid9,
                                                wopid10, wopid11, wopid12])

    def evonet_mode_wop_service_assert(self, trans_fee_collection_method, fx_fee_collection_method,
                                       fxrebate_fee_collection_method,
                                       trans_fee_calcu_method, fx_fee_calcu_method):
        # 测试evonet模式一个wopid对应两个mopId的交易
        model = "evonet"
        fileinit = "evonet"
        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        mopid2 = self.task_func.generate_mopid()
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        self.db_operations.create_single_config(wopid, mopid1, model, fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置wop表的配置
        self.tyo_config_db.delete_manys("wop",
                                        {"baseInfo.wopID": wopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid, mopid2, model, fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "settleInfo.fxRebateCollectionMethod": fxrebate_fee_collection_method,
                                          "settleInfo_cpmInterchangeFeeRate": 0.0632658,
                                          "settleInfo.mpmInterchangeFeeRate": 0.08328446,
                                          "settleInfo.transactionProcessingFeeRate": 0.0585173,
                                          "settleInfo.fxProcessingFeeRate": 0.0712973,
                                      })
        self.tyo_config_db.update_one(self.common_name.custom_config, {"wopID": wopid},
                                      {
                                          "transactionProcessingFeeRate": 0.0385173,
                                          "fxProcessingFeeRate": 0.0212973
                                      })
        # transSummary,直接插入数据进入到，transSummay.wop
        summary_data = []
        for settle_date in range(20200101, 20200132):  # 造一个月的数据
            settle_data = self.case_data.evont_wop_trans_summary_data(wopid, mopid1, mopid2, str(settle_date),
                                                                      trans_fee_collection_method,
                                                                      fx_fee_collection_method,
                                                                      fxrebate_fee_collection_method,
                                                                      trans_fee_calcu_method, fx_fee_calcu_method)
            summary_data.extend(settle_data)
        self.tyo_evosettle_db.insert_many(self.common_name.trans_summary_wop, summary_data)

        # 触发生月报
        self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid1, mopid2], self.month_file_sett_date,
                                           [self.common_name.wop_fee_file], model, fileinit)

        self.evonet_wop_daily_service_assert(wopid,
                                             trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             fxrebate_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method,
                                             )

    def evonet_mode_mop_service_assert(self, trans_fee_collection_method, fx_fee_collection_method,
                                       trans_fee_calcu_method, fx_fee_calcu_method):
        # evonet模式一个mopid 对应连个wopid的月报
        model = "evonet"
        fileinit = "evonet"
        mopid = self.task_func.generate_mopid()
        wopid1 = self.task_func.generate_wopid()
        wopid2 = self.task_func.generate_wopid()
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        self.db_operations.create_single_config(wopid1, mopid, model, fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 删除配置mop表的配置
        self.tyo_config_db.delete_manys("mop",
                                        {"baseInfo.mopID": mopid})
        # 删除配置mop表的配置
        self.sgp_config_db.delete_manys("mop",
                                        {"baseInfo.mopID": mopid})
        # 创建配置 2
        self.db_operations.create_single_config(wopid2, mopid, model, fileinit,
                                                "monthly",
                                                "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.sgp_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                       {
                                           "settleInfo.settleCurrency": settle_currency,
                                           "settleInfo.transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                           "settleInfo.transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                           "settleInfo.fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                           "settleInfo.fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                           "settleInfo_cpmInterchangeFeeRate": 0.0632658,
                                           "settleInfo.mpmInterchangeFeeRate": 0.08328446,
                                           "settleInfo.transactionProcessingFeeRate": 0.0655173,
                                           "settleInfo.fxProcessingFeeRate": 0.0952973,

                                       })
        self.sgp_config_db.update_many(self.common_name.custom_config, {"mopID": mopid},
                                       {
                                           "transactionProcessingFeeRate": 0.0595173,
                                           "fxProcessingFeeRate": 0.0852973,
                                       })

        summary_data = []
        for settle_date in range(20200101, 20200132):  # 造一个月的数据
            settle_data = self.case_data.evont_mop_trans_summary_data(mopid, wopid1, wopid2, str(settle_date),
                                                                      trans_fee_collection_method,
                                                                      fx_fee_collection_method,
                                                                      trans_fee_calcu_method, fx_fee_calcu_method)
            summary_data.extend(settle_data)
        self.sgp_evosettle_db.insert_many(self.common_name.trans_summary_mop, summary_data)

        # 月报
        self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid1, wopid2], self.month_file_sett_date,
                                           [self.common_name.mop_fee_file], model, fileinit)

        self.evonet_mop_daily_service_assert(mopid,
                                             trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method,
                                             )

    def bilateral_mop_service_assert(self, trans_fee_calcu_method, fx_fee_calcu_method):

        # evonet模式一个mopid 对应连个wopid的月报
        model = self.common_name.bilateral
        mopid = self.task_func.generate_mopid()
        wopid = self.task_func.generate_wopid()
        trans_fee_collection_method = "monthly"
        fx_fee_collection_method = "monthly"
        settle_currency = "CNY"  # 修改币种及计费方式
        custom_settle_currency = "JPY"
        # 创建配置 1
        self.db_operations.create_single_config(wopid, mopid, model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid}, {"settleInfo.settleCurrency": settle_currency,
                                                                         # 0.0595173,生月报，这个用不到
                                                                         "settleInfo.transactionProcessingFeeRate": 0.09,
                                                                         # 生月报，这个手续费用不到
                                                                         "settleInfo.fxProcessingFeeRate": 0.05,
                                                                         })
        # 数据插入到trans表,造两条交易
        self.sgp_config_db.update_one(self.common_name.custom_config, {"mopID": mopid},
                                      {
                                          "settleCurrency": custom_settle_currency,
                                          "transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "cpmInterchangeFeeRate": 0.0632658,
                                          "mpmInterchangeFeeRate": 0.08328446,
                                          "transactionProcessingFeeRate": 0.0595173,  # 不要改
                                          "fxProcessingFeeRate": 0.0852973,  # 不要改
                                      })

        summary_data = []
        for settle_date in range(20200101, 20200132):  # 造一个月的数据
            settle_data = self.case_data.bilateral_trans_summary_data("mop", wopid, mopid, str(settle_date),
                                                                      trans_fee_collection_method,
                                                                      fx_fee_collection_method,
                                                                      trans_fee_calcu_method, fx_fee_calcu_method)
            summary_data.extend(settle_data)
        self.sgp_evosettle_db.insert_many(self.common_name.trans_summary_mop, summary_data)

        # 月报
        for fileinit in ["evonet", "wop"]:
            self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], self.month_file_sett_date,
                                               [self.common_name.mop_fee_file], model, fileinit)

        # 调用直清模式的月报
        self.evonet_mop_daily_service_assert(mopid,
                                             trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method,
                                             model=self.common_name.bilateral
                                             )

    def bilateral_wop_service_assert(self, trans_fee_calcu_method, fx_fee_calcu_method):
        # 月报是直接将数据插入到 trans_summary 表的
        # evonet模式一个mopid 对应连个wopid的月报
        model = self.common_name.bilateral
        fileinit = "evonet"
        mopid = self.task_func.generate_mopid()
        wopid = self.task_func.generate_wopid()
        trans_fee_collection_method = "monthly"
        fx_fee_collection_method = "monthly"
        fxrebate_fee_collection_method = "daily"  # 直清模式下这个字段无用，但是依然需要传
        settle_currency = "CNY"  # 修改币种及计费方式
        custom_settle_currency = "JPY"
        # 创建配置 1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid}, {"settleInfo.settleCurrency": settle_currency,
                                                                         "settleInfo.transactionProcessingFeeRate": 0.09,
                                                                         # 0.0595173 生月报用不到这个手续费
                                                                         "settleInfo.fxProcessingFeeRate": 0.09,
                                                                         # 0.0852973  生月报用不到这个手续费
                                                                         })
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one(self.common_name.custom_config, {"wopID": wopid},
                                      {
                                          "settleCurrency": custom_settle_currency,
                                          "transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "cpmInterchangeFeeRate": 0.0632658,
                                          "mpmInterchangeFeeRate": 0.08328446,
                                          "transactionProcessingFeeRate": 0.0595173,  # 不要改
                                          "fxProcessingFeeRate": 0.0852973,  # 不要改
                                      })

        summary_data = []
        for settle_date in range(20200101, 20200132):  # 造一个月的数据
            settle_data = self.case_data.bilateral_trans_summary_data("wop", wopid, mopid, str(settle_date),
                                                                      trans_fee_collection_method,
                                                                      fx_fee_collection_method,
                                                                      trans_fee_calcu_method, fx_fee_calcu_method)
            summary_data.extend(settle_data)
        self.tyo_evosettle_db.insert_many(self.common_name.trans_summary_wop, summary_data)

        # 月报
        # 直清模式只有模式二有月报,银联模式
        self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid], self.month_file_sett_date,
                                           [self.common_name.wop_fee_file], model, fileinit)

        # 调用直清模式的月报

        self.evonet_wop_daily_service_assert(wopid,
                                             trans_fee_collection_method,
                                             fx_fee_collection_method,
                                             fxrebate_fee_collection_method,
                                             trans_fee_calcu_method, fx_fee_calcu_method,
                                             model=self.common_name.bilateral)

    def download_file(self, node_type, wopid, mopid, file_type, file_subtype, file_extension):
        """
        下载文件
        :param node_type:wop 或者mop
        :param wopid:   当是evonet模式且 node_type是 mop 可以是EVONET
        :param mopid:   当是evonet模式且 node_type是 wop 可以是EVONET
        :param file_type:   fileinfo中的文件格式，根据这三个字段来判断下载哪个文件
        :param file_subtype:
        :param file_extension:
        :return:
        """

        if node_type == "wop":
            file_path, file_name = self.db_operations.get_file_info_record(node_type, wopid, file_type, file_subtype,
                                                                           file_extension)
        else:
            file_path, file_name = self.db_operations.get_file_info_record(node_type, mopid, file_type,
                                                                           file_subtype,
                                                                           file_extension)

        remote_path = file_path + "/" + file_name
        local_path = file_name
        if node_type == "wop":
            private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
            self.sftp_func.ssh_download_file("get", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                             local_path)
        if node_type == "mop":
            private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
            self.sftp_func.ssh_download_file("get", private_key, self.sgp_ip, self.sgp_user, remote_path,
                                             local_path)
        return local_path

    def summary_service_title_assert(self, node_type, summary_service, wopid, mopid, file_name, sett_date,
                                     model="bilateral"):
        """
        对summary和service的title进行校验
        :param node_type: wop或者mop
        :summary  summary or service
        :param wopid:
        :param mopid:
        :param file_name:
        :param settle_date: 清算日期
        :param settle_currency:  wop表或者mop表的清算币种
        :return:
        """
        # 月报按照每日的数据校验一遍
        data = xlrd.open_workbook(file_name)
        table = data.sheets()[0]  # 通过索引顺序获取
        assert table.cell_value(7, 0) == "Report ID:"

        # 校验title格式
        if summary_service == "summary":
            assert table.cell_value(12, 0) == "Total Net Settlement Amount:"
            assert table.cell_value(13, 0) == "Settlement Currency:"
            report_id = wopid + "-Settlement-Summary-" + mopid + "-" + sett_date + "-001"
            if model == "evonet" and node_type == "wop":
                report_id = wopid + "-Settlement-Summary-" + "EVONET" + "-" + sett_date + "-001"
            elif model == "evonet" and node_type == "mop":
                report_id = mopid + "-Settlement-Summary-" + "EVONET" + "-" + sett_date + "-001"
            elif model == "bilateral" and node_type == "wop":
                report_id = wopid + "-Settlement-Summary-" + mopid + "-" + sett_date + "-001"
            elif model == "bilateral" and node_type == "mop":
                report_id = mopid + "-Settlement-Summary-" + wopid + "-" + sett_date + "-001"

            if node_type == "wop":
                assert table.cell_value(5, 0) == "EVONET Settlement Summary Report (WOP)"
                if model == "bilateral":
                    assert table.cell_value(13, 3) == \
                           self.tyo_config_db.get_one(self.common_name.custom_config, {"wopID": wopid})[
                               "settleCurrency"]
                else:
                    assert table.cell_value(13, 3) == \
                           self.tyo_config_db.get_one("wop", {"baseInfo.wopID": wopid})["settleInfo"][
                               "settleCurrency"]
            else:
                assert table.cell_value(5, 0) == "EVONET Settlement Summary Report (MOP)"
                if model == "bilateral":
                    assert table.cell_value(13, 3) == \
                           self.sgp_config_db.get_one(self.common_name.custom_config, {"mopID": mopid})[
                               "settleCurrency"]
                else:
                    assert table.cell_value(13, 3) == \
                           self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"][
                               "settleCurrency"]
        if summary_service == "service":

            assert table.cell_value(12, 0) == "Total Service Fee:"
            assert table.cell_value(13, 0) == "Service Fee Currency:"
            report_id = wopid + "-ServiceFee-Summary-" + mopid + "-" + "20200204" + "-001"
            if model == "evonet" and node_type == "wop":
                report_id = wopid + "-ServiceFee-Summary-" + "EVONET" + "-" + "20200204" + "-001"
            elif model == "evonet" and node_type == "mop":
                report_id = mopid + "-ServiceFee-Summary-" + "EVONET" + "-" + "20200204" + "-001"
            elif model == "bilateral" and node_type == "wop":
                report_id = wopid + "-ServiceFee-Summary-" + mopid + "-" + "20200204" + "-001"
            elif model == "bilateral" and node_type == "mop":
                report_id = mopid + "-ServiceFee-Summary-" + wopid + "-" + "20200204" + "-001"
            if node_type == "wop":
                assert table.cell_value(5, 0) == "EVONET Service Fee Report (WOP)"
                # 后面开发修改之后在取消注释
                assert table.cell_value(13, 3) == \
                       self.tyo_config_db.get_one("wop", {"baseInfo.wopID": wopid})["settleInfo"]["settleCurrency"]
            else:
                assert table.cell_value(5, 0) == "EVONET Service Fee Report (MOP)"
                # 后面开发修改之后再取消注释
                assert table.cell_value(13, 3) == \
                       self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mopid})["settleInfo"]["settleCurrency"]
        assert table.cell_value(7, 3) == report_id

        if node_type == "wop":
            assert table.cell_value(9, 0) == "WOP Name:"
            assert table.cell_value(9, 3) == self.tyo_config_db.get_one("wop", {"baseInfo.wopID": wopid})["baseInfo"][
                "wopName"]
            # assert table.cell_value(16, 0) == self.tyo_config_db.get_one("mop", {"baseInfo.mopID": mopid})["baseInfo"][
            #     "mopName"]

            assert table.cell_value(10, 0) == "WOP ID:"
            assert table.cell_value(10, 3) == wopid
        else:
            assert table.cell_value(9, 0) == "MOP Name:"
            assert table.cell_value(9, 3) == self.sgp_config_db.get_one("mop", {"baseInfo.mopID": mopid})["baseInfo"][
                "mopName"]
            # assert table.cell_value(16, 0) == self.sgp_config_db.get_one("wop", {"baseInfo.wopID": wopid})["baseInfo"][
            #     "wopName"]
            assert table.cell_value(10, 0) == "MOP ID:"
            assert table.cell_value(10, 3) == mopid
        assert table.cell_value(15, 0) == "***NO DATA FOR THIS REPORT***"

    def wop_xlsx_title_assert(self, ):
        # 报表中空报表校验，报表title校验
        # Summary和service title的校验
        settle_currency = "CNY"  # 修改币种及计费方式  配置两个币种不一样
        for model in ["evonet", "bilateral"]:
            fileinits = ["evoent", "mop"]
            for fileinit in fileinits:
                if model == self.common_name.evonet and fileinit == "mop":
                    continue
                mopid = self.task_func.generate_mopid()
                wopid = self.task_func.generate_wopid()
                # 创建配置 1
                self.db_operations.create_single_config(wopid, mopid, model, fileinit,
                                                        "monthly", "monthly",
                                                        str(random.randint(100000, 9900000)),
                                                        "sgp")
                self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                              {"settleInfo.settleCurrency": settle_currency,
                                               "settleInfo.fxRebateCollectionMethod": "monthly"
                                               })

                settle_date = "20200101"

                self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid], str(settle_date),
                                                   [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                                                    self.common_name.wop_trans_calc], model, fileinit)

                self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid], str(settle_date),
                                                   [self.common_name.wop_generate_file], model, fileinit)
                local_path = self.download_file("wop", wopid, mopid, "Settlement", "Summary", "xlsx")
                self.summary_service_title_assert("wop", "summary", wopid, mopid, local_path, settle_date, model)
                os.remove(local_path)
                # -------------------------
                # 直清模式只有模式二有月报
                self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid], self.month_file_sett_date,
                                                   [self.common_name.wop_fee_file], model, "evonet")
                local_path = self.download_file("wop", wopid, mopid, "ServiceFee", "Summary", "xlsx")
                self.summary_service_title_assert("wop", "service", wopid, mopid, local_path, settle_date, model)
                os.remove(local_path)

    def mop_xlsx_title_assert(self, ):
        # 空月报service 校验，空日报 summary
        # Summary和service title的校验
        settle_currency = "CNY"  # 修改币种及计费方式
        custom_config_settle_currency = "JPY"
        for model in ["evonet", "bilateral"]:  # "bilateral""evonet"
            fileinits = ["evonet"]
            if model == "bilateral":
                fileinits = ["evonet", "wop"]
            for fileinit in fileinits:
                mopid = self.task_func.generate_mopid()
                wopid = self.task_func.generate_wopid()
                # 创建配置 1
                self.db_operations.create_single_config(wopid, mopid, model, fileinit,
                                                        "monthly", "monthly",
                                                        str(random.randint(100000, 9900000)),
                                                        "sgp")
                self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                              {"settleInfo.settleCurrency": settle_currency,
                                               "settleInfo.fxRebateCollectionMethod": "monthly"
                                               })

                settle_date = "20200101"

                try:
                    self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], str(settle_date),
                                                       [self.common_name.mop_generate_file], model, fileinit)
                except:
                    print("mop生文件有问题")
                local_path = self.download_file("mop", wopid, mopid, "Settlement", "Summary", "xlsx")
                self.summary_service_title_assert("mop", "summary", wopid, mopid, local_path, settle_date, model)
                os.remove(local_path)
                # -------------------------
                # 直清模式只有模式二有月报
                try:
                    self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid],
                                                       self.month_file_sett_date,
                                                       [self.common_name.mop_fee_file], model, fileinit)
                except:
                    print("mop生文件有问题")
                local_path = self.download_file("mop", wopid, mopid, "ServiceFee", "Summary", "xlsx")
                self.summary_service_title_assert("mop", "service", wopid, mopid, local_path, settle_date, model)
                os.remove(local_path)

    def bilateral_mode_mop_summary(self, trans_fee_calcu_method, fx_fee_calcu_method):
        # 测试直清模式一个 mopid 对应一个 wopId 的交易 ，直清模式
        settle_currency = "CNY"  # 修改币种及计费方式
        mop_settle_currency = "JPY"
        # 创建配置 1
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        trans_fee_collection_method = "monthly"
        fx_fee_collection_method = "monthly"
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.sgp_config_db.update_one("mop", {"baseInfo.mopid": mopid},
                                      {
                                          "settleInfo.settleCurrency": mop_settle_currency,
                                      })
        self.sgp_config_db.update_one(self.common_name.custom_config, {"mopID": mopid},
                                      {
                                          "settleCurrency": settle_currency,
                                          "transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "cpmInterchangeFeeRate": 0.0632658,  # 不要改
                                          "mpmInterchangeFeeRate": 0.08328446,  # 不要改
                                          "transactionProcessingFeeRate": 0.0595173,  # 不要改
                                          "fxProcessingFeeRate": 0.0852973,  # 不要改
                                      })
        for i in range(2):  # 造一个mopid对应两个mopid的交易，且mopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.sgp_evosettle_db.insert_many("trans",
                                                  self.report_trans_list(wopid, mopid,
                                                                         settle_currency,
                                                                         trans_currency)[0])

        self.sgp_evosettle_db.update_many("trans", {"wopID": wopid},
                                          {"mopSettleCurrency": settle_currency})

        self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], str(self.sett_date),
                                           [self.common_name.mop_trans_import, self.common_name.mop_self_sett,
                                            self.common_name.mop_trans_calc], self.common_name.bilateral, "evonet")
        # 按模式生文件
        self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], str(self.sett_date),
                                           [self.common_name.mop_generate_file], self.common_name.bilateral, 'evonet')

        # 下载文件进行校验，
        self.download_file("mop", wopid, mopid, self.common_name.file_type_Settlement,
                           self.common_name.file_subtype_Summary, self.common_name.file_extension_xlsx)

    def wop_exception_file(self, trans_fee_calcu_method, fx_fee_calcu_method):
        # 测试直清模式一个wopid对应一个 mopId的交易
        trans_fee_collection_method = "monthly"
        fx_fee_collection_method = "monthly"
        fxrebate_fee_collection_method = "daily"
        settle_currency = "CNY"  # 修改币种及计费方式
        # 创建配置 1
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit,
                                                "monthly", "monthly",
                                                str(random.randint(100000, 9900000)),
                                                "sgp")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one(self.common_name.custom_config, {"wopID": wopid},
                                      {
                                          "settleCurrency": settle_currency,
                                          "transProcessingFeeCollectionMethod": trans_fee_collection_method,
                                          "transProcessingFeeCalculatedMethod": trans_fee_calcu_method,
                                          "fxProcessingFeeCollectionMethod": fx_fee_collection_method,
                                          "fxProcessingFeeCalculatedMethod": fx_fee_calcu_method,
                                          "fxRebateCollectionMethod": fxrebate_fee_collection_method
                                      })
        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.tyo_evosettle_db.insert_many("trans",
                                                  self.report_trans_list(wopid, mopid,
                                                                         settle_currency,
                                                                         trans_currency)[0])

        self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid], str(self.sett_date),
                                           [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                                            self.common_name.wop_trans_calc], self.model, self.fileinit)
        # 因为没有 settleFlag为 false的交易，所以，数据为空,空exception 报表校验
        self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, [mopid], str(self.sett_date),
                                           [self.common_name.wop_generate_file], self.common_name.bilateral, "wop")
        local_path = self.download_file("wop", wopid, mopid, self.common_name.file_type_exception,
                                        self.common_name.file_subtype_Details, "csv")
        self.task_func.exceptions_file_assert()

    def sevice(self, local_path):
        data = xlrd.open_workbook(local_path)
        table = data.sheets()[0]
        content_list = []
        for i in range(15, 33):
            for j in range(1, 9):
                content_list.append(table.cell_value(i, j))

    def create_refund_data(self, mopid, settle_date, refund_data, number):
        # mop_trans_time, mop_order_number, trans_amount, trans_curreny, orig_evonet_order_number
        file_name = "{}_Batch_Refund_File_{}.csv".format(mopid, settle_date)
        with open(file_name, mode="w+t", encoding="utf-8") as file:
            file.write('"Total Count","{}"\n'.format(str(number)))
            file.write(
                '"MOP Transaction Time","MOP Order Number","Transaction Type","Mop User Reference","Transaction Amount","Transaction Currency","Original EVONET Order Number"' + "\n")
            file.write(refund_data)
            file.flush()
        return file_name

    def special_refund_resolve(self):
        # mop_trans_time, mop_order_number, trans_amount, trans_curreny, orig_evonet_order_number
        # 1 正常部分退款
        wopid = "WOP_Auto_JCoinPay_01"
        mopid = "MOP_Auto_GrabPay_01"
        # ------------------  正常解析
        settle_date = '20210511'
        file_data = ""
        file_count = 2
        for i in range(file_count):
            mop_trans_time = "2021-01-16 00:42:23 UTC +08:00"
            mop_order_number = str(random.randint(10000000000000, 90000000000000))
            refernece = str(random.randint(10000000000000, 90000000000000))
            trans_amount = 11
            trans_currency = "JPY"
            orig_evonet_order_number = "745163339658769377"

            refund_data = "{},{},{},{},{},{},{}{}".format(mop_trans_time, mop_order_number, "Refund",
                                                          refernece, trans_amount, trans_currency,
                                                          orig_evonet_order_number, "\n")
            file_data += refund_data
        file_name = self.create_refund_data(mopid, settle_date, file_data, file_count)
        remote_path = "/home/webapp/evofile/ins/" + mopid + "/in/" + settle_date + "/mop/" + file_name

        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        # 服务器上不存在文件触发请求
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, [wopid], '20200322',
                                           [self.common_name.mop_file_resolve], self.model, self.fileinit)

        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         file_name)
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {
            'fileName': file_name
        })
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, [wopid], settle_date,
                                           [self.common_name.mop_file_resolve], self.model, self.fileinit)
        os.remove(file_name)
        data = self.tyo_evosettle_db.get_one(self.common_name.trans_refund, {"mopOrderNumber": mop_order_number})
        assert data["mopID"] == mopid
        assert data["date"] == settle_date
        assert data["used"] == False
        assert data["transType"] == "Refund"
        assert data["mopUserReference"] == refernece
        assert data["transAmount"] == str(trans_amount)
        assert data["transCurrency"] == trans_currency
        assert data["originalEvonetOrderNumber"] == orig_evonet_order_number

        refund_info = self.tyo_evosettle_db.get_one(self.common_name.file_info, {
            'fileName': file_name})
        assert refund_info["resolveFlag"] == True
        assert refund_info["fileType"] == "Batch_Refund_File"
        assert refund_info["fileSubType"] == "Batch_Refund_File"



    def special_refund_trans_send(self):
        # mop_trans_time, mop_order_number, trans_amount, trans_curreny, orig_evonet_order_number
        # 1 正常部分退款
        wopid = "WOP_Auto_JCoinPay_01"
        mopid = "MOP_Auto_GrabPay_01"
        # ------------------  正常解析
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {"firstRole": mopid})
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_refund, {"mopID": mopid})

        # 正常的两笔交易退款，两笔退款金额小于原交易金额，最后退款交易都成功
        settle_date = '20210511'
        file_data = ""
        file_count = 2
        mop_order_number_list = []
        for i in range(file_count):
            mop_trans_time = "2021-09-16 00:42:23 UTC +08:00"
            # mop_trans_time=datetime.datetime.now()
            mop_order_number = str(random.randint(10000000000000, 90000000000000))
            refernece = str(random.randint(10000000000000, 90000000000000))
            trans_amount = 11
            trans_currency = "JPY"
            orig_evonet_order_number = "745163339658769377"
            refund_data = "{},{},{},{},{},{},{}{}".format(mop_trans_time, mop_order_number, "Refund",
                                                          refernece, trans_amount, trans_currency,
                                                          orig_evonet_order_number, "\n")
            file_data += refund_data
            mop_order_number_list.append(mop_order_number)
        file_name = self.create_refund_data(mopid, settle_date, file_data, file_count)
        remote_path = "/home/webapp/evofile/ins/" + mopid + "/in/" + settle_date + "/mop/" + file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        # 服务器上不存在文件触发请求
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         file_name)
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {
            'fileName': file_name
        })
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, [wopid], settle_date,
                                           [self.common_name.mop_file_resolve,
                                            self.common_name.mop_refund_trans_send, ], self.model, self.fileinit)
        os.remove(file_name)
        # 生成的文件结果的数据的校验

    def special_refund_file_assert(self):
        # 生成的 退款文件的校验
        # mop_trans_time, mop_order_number, trans_amount, trans_curreny, orig_evonet_order_number
        # 1 正常部分退款
        wopid = "WOP_Auto_JCoinPay_01"
        mopid = "MOP_Auto_GrabPay_01"
        # ------------------  正常解析
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {"firstRole": mopid})
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_refund, {"mopID": mopid})

        # 正常的两笔交易退款，两笔退款金额小于原交易金额，最后退款交易都成功
        settle_date = '20211211'
        file_data = ""
        file_count = 10  # 不要改
        mop_order_number_list = []
        for i in range(file_count):
            mop_trans_time = "2021-05-16 00:42:23 UTC +08:00"
            mop_order_number = str(random.randint(10000000000000, 90000000000000))
            refernece = str(random.randint(10000000000000, 90000000000000))
            trans_amount = 11
            trans_currency = "JPY"
            orig_evonet_order_number = "745163339658769377"
            refund_data = "{},{},{},{},{},{},{}{}".format(mop_trans_time, mop_order_number, "Refund",
                                                          refernece, trans_amount, trans_currency,
                                                          orig_evonet_order_number, "\n")
            file_data += refund_data
            mop_order_number_list.append(mop_order_number)
        file_name = self.create_refund_data(mopid, settle_date, file_data, file_count)
        remote_path = "/home/webapp/evofile/ins/" + mopid + "/in/" + settle_date + "/mop/" + file_name
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        # 服务器上不存在文件触发请求
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         file_name)
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {
            'fileName': file_name
        })
        os.remove(file_name)
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, [wopid], settle_date,
                                           [self.common_name.mop_file_resolve,
                                            self.common_name.mop_refund_trans_send,
                                            ], self.model, self.fileinit)
        time.sleep(5)
        self.tyo_evosettle_db.update_one(self.common_name.trans_refund,{"mopID":mopid},{"resp.result.code":"B0000"})
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, [wopid], settle_date,
                                           [
                                               self.common_name.mop_refund_file_generate], self.model, self.fileinit)

        result_file = self.tyo_evosettle_db.get_one(self.common_name.file_info, {"firstRole": mopid,
                                                                                 "fileType": "Refund_Result_File",
                                                                                 "fileSubType": "Refund_Result_File", })
        result_file_name = result_file["fileName"]
        remote_path = result_file["filePath"] + result_file_name
        # 下载文件
        self.sftp_func.ssh_download_file("get", private_key, self.tyo_ip, self.tyo_user, remote_path,
                                         result_file_name)
        time.sleep(2)
        with open(result_file_name, mode="r+t", encoding="utf-8") as file:
            first_line = file.readline()
            file_secone_line = file.readline()
            second_line = '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","EVONET Order Number","WOP Order Number","MOP Order Number","WOP ID","WOP Name","Transaction Result","Transaction Amount","Transaction Currency","Settlement Amount","Settlement Currency","Original EVONET Order Number"'
            assert first_line.strip() == '"Total Count","10"'
            assert second_line == file_secone_line.strip()
            data = file.readlines()
            for refund_data in data:
                evonet_order_create_time, wop_user_pay_time, mop_transaction_time, evonet_order_number, wop_order_number, \
                mop_order_number, wop_id, wop_name, transaction_result, transaction_amount, \
                transaction_currency, settlement_amount, settlement_currency, original_evonet_order_number = refund_data.strip().split(
                    ',')

                trans_refund_data = self.tyo_evosettle_db.get_one(self.common_name.trans_refund,
                                                                  {"mopOrderNumber": eval(mop_order_number)})
                trans_data = self.tyo_evosettle_db.get_one("trans",
                                                           {"mopOrderNumber": eval(mop_order_number)})
                resp_content = trans_refund_data["resp"]
                settle_amount=resp_content["settleAmount"]
                assert eval(evonet_order_number) == resp_content["evonetOrderNumber"]
                assert eval(wop_order_number) == trans_data["wopOrderNumber"]
                assert eval(mop_order_number) == resp_content["mopOrderNumber"]
                assert eval(wop_id) == resp_content["wopID"]
                assert eval(wop_name) == self.tyo_config_db.get_one("wop", {"baseInfo.wopID": wopid})["baseInfo"][
                    "wopName"]
                if resp_content["result"]["code"][0] == "S":
                    assert eval(transaction_result) == "succeeded"
                else:
                    assert eval(transaction_result) == "failed"
                assert float(eval(transaction_amount)) == float(trans_refund_data["transAmount"])
                assert eval(transaction_currency) == trans_refund_data["transCurrency"]
                assert float(eval(settlement_amount)) == float(settle_amount["value"])
                assert eval(settlement_currency) == settle_amount["currency"]
                assert eval(original_evonet_order_number) == trans_refund_data["originalEvonetOrderNumber"]
        # 生成的文件结果的数据的校验
        # 最后删除刚刚下载的文件
        os.remove(result_file_name)


if __name__ == '__main__':
    common_name = CommonName()
    import time

    funciton_test = RestructReportForm("test", "20200117", common_name.evonet,
                                       common_name.evonet)
    funciton_test.special_refund_resolve()
    funciton_test.special_refund_trans_send()
    funciton_test.special_refund_file_assert()
    # funciton_test.wop_exception_file("single", "single")
    # funciton_test.mop_settlement_detail_assert("MOP_SETTfxzzxl","daily","daily")
    # funciton_test.empty_settlement_details()
    # funciton_test.bilateral_mode_mop_summary("single", "single")
    # funciton_test.get_json()
    # funciton_test.wop_xlsx_title_assert()
    # funciton_test.mop_xlsx_title_assert()

    # funciton_test.sevice()
    # funciton_test.task_func.dual_db_init()
    # time1 = time.time()

    # 直清模式mop 侧service
    # funciton_test.bilateral_mop_service_assert('accumulation', 'accumulation')
    # funciton_test.bilateral_mop_service_assert( 'accumulation', 'single')
    #
    # funciton_test.bilateral_mop_service_assert('single', 'accumulation')
    #
    # funciton_test.bilateral_mop_service_assert( 'single', 'single')

    # #直清模式wop侧
    # funciton_test.bilateral_wop_service_assert('accumulation', 'accumulation')
    # funciton_test.bilateral_wop_service_assert( 'accumulation', 'single')
    # # # #
    # funciton_test.bilateral_wop_service_assert('single', 'accumulation')
    # # # #
    # funciton_test.bilateral_wop_service_assert('single', 'single')

    # """
    # daily monthly single accumulation
    # daily monthly single single
    # monthly daily accumulation single
    # monthly daily single single
    #
    # monthly monthly accumulation accumulation
    # monthly monthly accumulation single
    # monthly monthly single accumulation
    # monthly monthly single single
    # """
    # evonet 模式 mop service
    # funciton_test.evonet_mode_mop_service_assert('monthly', 'monthly', 'accumulation', 'accumulation')
    # funciton_test.evonet_mode_mop_service_assert('monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_mop_service_assert('daily', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_mop_service_assert('daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_mop_service_assert('monthly', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_mop_service_assert('monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_mop_service_assert('monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_mop_service_assert('monthly', 'monthly', 'single', 'accumulation')

    # evonet模式 wop service
    # funciton_test.evonet_mode_wop_service_assert('daily', 'daily', 'daily', 'single', 'single')

    # funciton_test.evonet_mode_wop_service_assert('daily', 'daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_service_assert('daily', 'monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_service_assert('daily', 'monthly', 'daily', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_service_assert('daily', 'monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_service_assert('daily', 'monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'daily', 'daily', 'single', 'single')
    #
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'daily', 'single', 'single')
    #
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'daily', 'daily', 'accumulation', 'single')
    #
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'daily', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'daily', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'daily', 'accumulation', 'accumulation')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_service_assert('monthly', 'monthly', 'monthly', 'accumulation', 'accumulation')
    # time2 = time.time()
    # print(time2 - time1)
    # 下面四个方式是在模式四即 模式和fileinit都是 evonet模式中才生报表，两个是文件格式，两个是pdf文件超长的PDF
    #

    # funciton_test.custom_evonet_model_wop_report()
    # funciton_test.custom_envonet_model_mop_report()
    # funciton_test.super_wop_long_summary()
    # funciton_test.super_mop_long_summary()

    # evonet模式 wop settlement details侧
    # funciton_test.evonet_mode_wop_settlement_details("daily", "daily", "daily", "single", "single")
    # funciton_test.evonet_mode_wop_settlement_details('daily', 'daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('daily', 'daily', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('daily', 'daily', 'daily', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_settlement_details('daily', 'monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('daily', 'monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'daily', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'daily', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'daily', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'daily', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'daily', 'accumulation', 'accumulation')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_settlement_details('monthly', 'monthly', 'monthly', 'accumulation', 'accumulation')

    # evonet模式 mop settlement details侧
    # funciton_test.evonet_mode_mop_settlement_details('daily', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_mop_settlement_details('daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_mop_settlement_details('daily', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_mop_settlement_details('monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_mop_settlement_details('monthly', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_mop_settlement_details('monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_mop_settlement_details('monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_mop_settlement_details('monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_mop_settlement_details('monthly', 'monthly', 'accumulation', 'accumulation')

    # 直清模式wop侧，mop侧
    # funciton_test.bilateral_mode_wop_settlement_details('single', 'single')
    # funciton_test.bilateral_mode_wop_settlement_details( 'single', 'accumulation')
    # funciton_test.bilateral_mode_wop_settlement_details( 'accumulation', 'single')
    # funciton_test.bilateral_mode_wop_settlement_details( 'accumulation', 'accumulation')

    # funciton_test.bilateral_mode_mop_settlement_details('monthly', 'monthly', 'single', 'single')
    # funciton_test.bilateral_mode_mop_settlement_details('monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.bilateral_mode_mop_settlement_details('monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.bilateral_mode_mop_settlement_details('monthly', 'monthly', 'accumulation', 'accumulation')

    # 客户验收报表
    # funciton_test.custom_mop_report()
    # funciton_test.custom_wop_report()

    # 直清模式每日 wop侧每日Summary

    # funciton_test.evonet_mode_wop_summary("daily", "daily", "daily", "single", "single")
    # funciton_test.evonet_mode_wop_summary('daily', 'daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('daily', 'monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('daily', 'monthly', 'daily', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_summary('daily', 'monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('daily', 'monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_summary('monthly', 'daily', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'daily', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'daily', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'daily', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'daily', 'accumulation', 'accumulation')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_wop_summary('monthly', 'monthly', 'monthly', 'accumulation', 'accumulation')
    #
    # # 直清模式mop侧的每日Sumamry
    # funciton_test.evonet_mode_mop_summary('daily', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_mop_summary('daily', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_mop_summary('daily', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_mop_summary('monthly', 'daily', 'single', 'single')
    # funciton_test.evonet_mode_mop_summary('monthly', 'daily', 'accumulation', 'single')
    # funciton_test.evonet_mode_mop_summary('monthly', 'monthly', 'single', 'single')
    # funciton_test.evonet_mode_mop_summary('monthly', 'monthly', 'single', 'accumulation')
    # funciton_test.evonet_mode_mop_summary('monthly', 'monthly', 'accumulation', 'single')
    # funciton_test.evonet_mode_mop_summary('monthly', 'monthly', 'accumulation', 'accumulation')
