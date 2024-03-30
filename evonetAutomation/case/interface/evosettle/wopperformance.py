import random
import time
from base.db import MongoDB
from base.date_format import DateUtil
from base.read_config import *
from common.evosettle.task_funcs import TaskFuncs
from common.evosettle.comm_funcs import CommonName
from common.evosettle.parmiko_module import Parmiko_Module
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData
from common.evosettle.mongo_data import CreateConfig


class Performance(object):
    # 统一以 tyo  为wop节点;sgp  为mop节点
    # 重构之后其它模式只需要调用对应的方法并传入对应的参数就执对应的方法了，不需要每个模式都再写一遍，有需要的话，只需要在这里修改了，还可以通过多线程的方式调用case
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
        self.date_format = DateUtil()
        self.model = model
        self.fileinit = fileinit
        self.case_data = CaseData()
        self.trans_type_list = ["CPM Payment", "MPM Payment", "Refund"]
        self.aes_decrypt = Aesecb(self.encrypt.decrypt(self.evosettle_config.get_ini("server_key")))
        self.performance_evoconfig_db = DatabaseConnect().performance_evoconfig_db
        self.performance_evoconfig_db = DatabaseConnect().performance_evoconfig_db
        # config 和settle数据库的对象
        self.tyo_func_url = self.evosettle_config.get_ini("tyo_performance_request_url")  # tyo节点单个任务的url
        self.create_config = CreateConfig()
        self.model = model
        self.fileinit = fileinit
        self.case_data = CaseData()
        self.trans_type_list = ["CPM Payment", "MPM Payment", "Refund"]
        self.sett_date = sett_date
        # 月报日期，每月四号生月报
        self.monthly_sett_date = '20201004'
        self.sftp_func = Parmiko_Module()

        self.sgp_func_url = self.evosettle_config.get_ini("sgp_func_url")  # spg节点单个任务的url
        self.performance_tyo_ip = self.evosettle_config.get_ini("performance_tyo_ip")
        self.performance_tyo_user = self.evosettle_config.get_ini("performance_tyo_user")
        self.sgp_ip = self.evosettle_config.get_ini("sgp_ip")
        self.sgp_user = self.evosettle_config.get_ini("sgp_user")
        self.aes_decrypt = Aesecb("cardinfolink")

        self.common_name = CommonName()
        #  删除的查询参数   {"baseInfo.wopID" :{"$regex":"^WOP_Auto"}}

    def tyo_wop_settle_task(self, owner_id, include_id, function):
        """
        清分任务task请求
        :param owner_type:  wop 或者 mop
        :param owner_id:    如果 owner_type为wopid，则 owner_id为wopid;如果 owner_type为mop，则owner_id为mopid
        :param includ_id:  列表类型
        :param function:    settle_task  要执行的  function
        :return:
        """
        self.tyo_task_func.settle_task_request(self.tyo_func_url, "wop", owner_id, include_id, self.sett_date,
                                               function, self.model, self.fileinit)

    def tyo_mop_settle_task(self, owner_id, include_id, function):
        """
        清分任务task请求
        :param owner_type:  wop 或者 mop
        :param owner_id:    如果 owner_type为wopid，则 owner_id为wopid;如果 owner_type为mop，则owner_id为mopid
        :param includ_id:
        :param function:    settle_task  要执行的  function
        :return:
        """

        self.tyo_task_func.settle_task_request(self.tyo_func_url, "mop", owner_id, include_id, self.sett_date,
                                               function, self.model, self.fileinit)

    def execute_all_mop_function(self, mopid, wopid_list, function_name):
        """
        每次执行所有的wopfunction
        先打印出当前时间，程序结束之后再打印出运行后的时间，然后根据时间去 zabbix平台查看cpu,和相关的内存的使用率
        :param wopid:  wopid
        :param mopid_list:   mopid列表
        :count    每组function的等待时间
        :return:
        """

        print("下面是一组 MOP function-------↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓----------------------------------")
        # count = self.performance_evosettle_db.count("trans", {"mopID": mopid})
        # print("总数是", str(count))
        print("方法名为——", function_name)
        print("exect_before_time", )
        print(self.date_format.format_time(time.time()))
        time1 = time.time()
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, wopid_list, self.sett_date,
                                           function_name, self.model, self.fileinit)
        time2 = time.time()
        print(str(time2 - time1))
        print("exect_after_time", )
        print(self.date_format.format_time(time.time()))
        print("上面是一组 MOP function-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------------------")
        # 休息三分钟，测试function有针对性

    def report_trans_list(self, wopid, mopid, settle_currency, trans_currency):
        # 为了退款计费而造的交易

        mpm_order_number = str(random.randint(10000000000000000000, 90000000000000000000))
        refund_orig_cpm_evonet_order_nuber = str(random.randint(10000000000000000000, 90000000000000000000))
        refund_order_number = str(random.randint(10000000000000000000, 90000000000000000000))

        mpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "MPM Payment", mpm_order_number,
                                                  )
        orig_cpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "CPM Payment",
                                                       refund_orig_cpm_evonet_order_nuber, )
        # CPM退款交易
        refund_cpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "Refund", refund_order_number,
                                                         refund_orig_evonet_order_nuber=refund_orig_cpm_evonet_order_nuber)
        sett_trans_list = [mpm_sett_data, orig_cpm_sett_data, refund_cpm_sett_data]
        order_number_list = [mpm_order_number, refund_orig_cpm_evonet_order_nuber, refund_order_number]

        for i in sett_trans_list:
            i["wopSettleCurrency"] = settle_currency
            i["mopSettleCurrency"] = settle_currency
            i["transCurrency"] = trans_currency
        return (sett_trans_list, order_number_list)

    def execute_tyo_wop_function(self, wopid, mopid_list):
        self.tyo_wop_settle_task(wopid, mopid_list,
                                 [
                                     self.common_name.wop_trans_import,
                                     self.common_name.wop_trans_sync,
                                     self.common_name.wop_trans_calc,
                                     self.common_name.wop_self_sett,
                                     self.common_name.wop_generate_file,
                                 ])

    def execute_tyo_mop_function(self, mopid, wopid_list):
        self.tyo_mop_settle_task(mopid, wopid_list,
                                 [self.common_name.mop_trans_import, self.common_name.mop_trans_calc,
                                  self.common_name.mop_self_sett, self.common_name.mop_generate_file,
                                  ])

    def create_single_config(self, database, wopid, mopid, model, fileinit, date_monthly_type, date_daily_type,
                             brand_id,
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
        database.insert_one("wop", wop_date)

        database.insert_one("mop", mop_date)
        database.insert_one("customizeConfig", custom_date)
        database.insert_one("relation", relation_data)

    def execute_all_wop_function(self, wopid, mopid_list, function_name):
        """
        每次执行所有的wopfunction
        先打印出当前时间，程序结束之后再打印出运行后的时间，然后根据时间去 zabbix平台查看cpu,和相关的内存的使用率
        :param wopid:  wopid
        :param mopid_list:   mopid列表
        :count    每组function的等待时间
        :return:
        """

        print("下面是一个wopfunction-------↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓----------------------------------")
        # count = self.performance_evosettle_db.count("trans", {"wopID": wopid})
        # print("总数是", str(count))
        print("方法名是", function_name)
        print("exect_before_time", )
        print(self.date_format.format_time(time.time()))
        time1 = time.time()
        self.task_func.settle_task_request(self.tyo_func_url, "wop", wopid, mopid_list, self.sett_date,
                                           function_name, self.model, self.fileinit)
        time2 = time.time()
        print(str(time2 - time1))
        print("exect_after_time", )
        print(self.date_format.format_time(time.time()))
        print("上面是一个wopfunction-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------------------")
        # 测试function有针对性

    def insert_trans_data(self, number, settle_currency, wopid, mopid1, mopid2):

        for i in range(number):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.performance_evosettle_db.insert_many("trans",
                                                          self.report_trans_list(wopid,
                                                                                 mopid1,
                                                                                 settle_currency,
                                                                                 trans_currency)[
                                                              0])
                self.performance_evosettle_db.insert_many("trans",
                                                          self.report_trans_list(wopid,
                                                                                 mopid2,
                                                                                 settle_currency,
                                                                                 trans_currency)[
                                                              0])

    def performance_wop_test(self):
        # 测试一个wopid对应两个mopId的交易
        # 这个evonet模式执行时需要三分钟
        wopid = "WOP_aut" + str(random.randint(100000, 900000))
        mopid1 = "MOP_aut" + str(random.randint(100000, 900000))
        mopid2 = "MOP_aut" + str(random.randint(100000, 900000))

        wopid = "WOP_aut" + "intg"
        mopid1 = "MOP_aut" + "skrg"
        mopid2 = "MOP_aut" + "imtg"

        mopid_list = [mopid1, mopid2]
        settle_currency = "CNY"
        # 前置条件删除配置
        self.performance_evoconfig_db.delete_manys("wop", {"baseInfo.wopID": wopid})
        self.performance_evoconfig_db.delete_manys("mop", {"baseInfo.mopID": {"$in": [mopid1, mopid2]}})
        self.performance_evoconfig_db.delete_manys("customizeConfig", {"wopID": wopid})
        self.performance_evoconfig_db.delete_manys("relation", {"wopID": wopid})

        # 创建配置1
        self.create_single_config(self.performance_evoconfig_db, wopid, mopid1, self.model, self.fileinit, "daily",
                                  "daily", str(random.randint(100000, 9900000)), "tyo")
        self.performance_evoconfig_db.delete_manys("wop", {"baseInfo.wopID": wopid})
        # 创建配置 2
        self.create_single_config(self.performance_evoconfig_db, wopid, mopid2, self.model, self.fileinit, "daily",
                                  "daily", str(random.randint(100000, 9900000)), "tyo")
        # 修改币种及计费方式

        self.performance_evoconfig_db.update_one("wop", {"baseInfo.wopID": wopid},
                                                 {"settleInfo.settleCurrency": settle_currency,
                                                  "settleInfo.transProcessingFeeCollectionMethod": "daily",
                                                  "settleInfo.transProcessingFeeCalculatedMethod": "single",
                                                  "settleInfo.fxProcessingFeeCollectionMethod": "daily",
                                                  "settleInfo.fxProcessingFeeCalculatedMethod": "single",
                                                  "settleInfo.fxRebateCollectionMethod": "daily"
                                                  })
        # 数据插入到trans表,造两条交易
        # 修改币种及计费方式
        # 首次删除交易表的数据

        self.performance_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.performance_evosettle_db.delete_manys(self.common_name.trans_summary_wop, {"wopID": wopid})
        # 插入6W数据，并执行测试

        # 插入200000*12 为 240 万条数据 200004
        # self.insert_trans_data(166667, settle_currency, wopid, mopid1, mopid2)
        # self.performance_evosettle_db.update_many("transSettle.wop", {"trans.wopID": "WOP_autintg", "clearFlag": True},
        #                                           {
        #                                               "blendType": "default",
        #                                               "clearFlag": False,
        #                                               "feeFlag": False,
        #                                               "settleFlag": False, })

        function_list = [
            self.common_name.wop_trans_import,
            self.common_name.wop_self_sett,
            self.common_name.wop_trans_calc,
            self.common_name.wop_generate_file,
        ]
        for function_name in function_list:
            self.execute_all_wop_function(wopid, mopid_list, [function_name])
        # _________________________
        # 单独的已下子执行完function
        # self.execute_all_wop_function(wopid, mopid_list, function_list)

    def performance_single_wop_test(self):
        # 测试一个wopid对应两个mopId的交易
        # 这个evonet模式执行时需要三分钟
        wopid = "WOP_aut" + str(random.randint(100000, 900000))
        mopid1 = "MOP_aut" + str(random.randint(100000, 900000))
        mopid2 = "MOP_aut" + str(random.randint(100000, 900000))

        wopid = "WOP_aut" + "intg"
        mopid1 = "MOP_autowwsk"
        mopid2 = "MOP_aut" + "imtg"

        function_list = [
            self.common_name.wop_trans_import,
            self.common_name.wop_self_sett,
            self.common_name.wop_trans_calc,
            self.common_name.wop_generate_file,
        ]
        for function_name in function_list:
            self.execute_all_wop_function(wopid, mopid1, [function_name])
        # _________________________
        # 单独的已下子执行完function
        # self.execute_all_wop_function(wopid, mopid_list, function_list)

    def peformance_wop_system_file_generate(self, wopid, mopid, sett_date, file_name):
        # 生成wop_system 的文件
        trans_data = self.performance_evosettle_db.get_many("transSettle.wop",
                                                            {"settleDate": sett_date, "trans.wopID": wopid,
                                                             "trans.mopID": mopid, "clearFlag": False,
                                                             "feeFlag": False})
        with open(file_name, "w") as file:
            file.write('"Total Count","1"\n')  # 写入第一行,行数
            file.write(
                '"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","EVONET Order Number","WOP Order Number","MOP Order Number","Transaction Type","MOP ID","MOP Name","Transaction Amount","Transaction Currency","Settlement Amount","Settlement Currency","Interchange Fee","Net Settlement Amount","Original EVONET Order Number","Original MOP Order Number","Store ID","Store English Name","Store Local Name","MCC","City","Country","Terminal Number"\n')
            for trans in trans_data:
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

    def model_one_download_resolve_reconcile(self):
        # 流程测试
        # 模式一文件下载，文件解析，文件勾兑
        wopid = "WOP_aut" + str(random.randint(100000, 900000))
        mopid = "MOP_aut" + str(random.randint(100000, 900000))

        settle_currency = "CNY"
        # 333334
        for i in range(1):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.performance_evosettle_db.insert_many("trans",
                                                          self.report_trans_list(wopid,
                                                                                 mopid,
                                                                                 settle_currency,
                                                                                 trans_currency)[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.create_single_config(self.performance_evoconfig_db, wopid, mopid, self.model, self.fileinit, "daily",
                                  "daily", str(random.randint(100000, 9900000)), "tyo")
        # 流水导入和计费，为生wop系统文件做准备

        for function_name in [self.common_name.wop_trans_import, ]:
            self.execute_all_wop_function(wopid, [mopid], [function_name])

        sftp_data = self.case_data.wop_sftp_data(self.performance_tyo_ip, self.performance_tyo_user, wopid,
                                                 self.evosettle_config.get_ini("performance_sftp_data_key"))
        # sftp_info  插入配置
        self.performance_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.peformance_wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("performance_tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.performance_tyo_ip, self.performance_tyo_user, server_cmd)
        # # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.performance_tyo_ip, self.performance_tyo_user,
                                         remote_path + file_name,
                                         file_name)
        # 删除刚上传的文件
        os.remove(file_name)
        # 每次生报表前删除fileInfo的记录
        self.performance_evosettle_db.delete_manys(self.common_name.file_info, {"wopID": wopid})
        self.performance_evosettle_db.delete_manys(self.common_name.trans_file_wop, {"wopID": wopid})

        for function_name in [
            self.common_name.wop_settle_file_download,
            self.common_name.wop_settle_file_resolve,
            self.common_name.wop_trans_reconcile,
            self.common_name.wop_trans_calc,
            self.common_name.wop_generate_file]:
            self.execute_all_wop_function(wopid, [mopid], [function_name])

        # mop侧的相关function
        for function_name in [self.common_name.mop_trans_import,
                              self.common_name.mop_settle_file_resolve,
                              self.common_name.mop_trans_reconcile,
                              self.common_name.mop_trans_calc,
                              self.common_name.mop_generate_file]:
            self.execute_all_mop_function(mopid, [wopid], [function_name])

    def mode_one_wop_mop_reconcile(self):

        wopid = "WOP_aimr343"  # 造 150W条数据并插入到trans表
        mopid = "MOP_ap7w2ef"
        # 模式一 总数据 为  20000004的测试

        # # 模式一文件下载，文件解析，文件勾兑
        # wopid = "WOP_autsoprteu"  # 造 2000004条数据并插入到trans表
        # mopid = "MOP_autproituy"

        self.performance_evosettle_db.delete_manys(self.common_name.file_info, {"firstRole": wopid})
        self.performance_evosettle_db.delete_manys(self.common_name.file_info, {"firstRole": mopid})
        # 删除解析 wop 系统的文件
        # self.performance_evosettle_db.delete_manys(self.common_name.trans_file_wop, {"wopID": wopid})
        # # 删除transSettle.wop transSettle.mop表的数据
        # self.performance_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        #
        # # 删除transSumamry表的数据
        # self.performance_evosettle_db.delete_manys(self.common_name.trans_summary_wop, {"wopID": wopid})
        # self.performance_evosettle_db.delete_manys(self.common_name.trans_summary_mop, {"wopID": wopid})
        # # 删除 transFile.wopNode的数据
        # self.performance_evosettle_db.delete_manys(self.common_name.trans_file_wop_node, {"wopID": wopid})
        self.create_single_config(self.performance_evoconfig_db, wopid, mopid, self.model, self.fileinit, "daily",
                                  "daily", str(random.randint(100000, 9900000)), "tyo")
        settle_currency = "CNY"
        # 333334
        for i in range(3):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.performance_evosettle_db.insert_many("trans",
                                                          self.report_trans_list(wopid,
                                                                                 mopid,
                                                                                 settle_currency,
                                                                                 trans_currency)[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置

        # 流水导入和计费，为生wop系统文件做准备

        for function_name in [self.common_name.wop_trans_import, ]:
            self.execute_all_wop_function(wopid, [mopid], [function_name])

        sftp_data = self.case_data.wop_sftp_data(self.performance_tyo_ip, self.performance_tyo_user, wopid,
                                                 self.evosettle_config.get_ini("performance_sftp_data_key"))
        # sftp_info  插入配置
        self.performance_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.peformance_wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("performance_tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.performance_tyo_ip, self.performance_tyo_user, server_cmd)
        # # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.performance_tyo_ip, self.performance_tyo_user,
                                         remote_path + file_name,
                                         file_name)

        # 删除刚上传的文件
        # os.remove(file_name)
        # 每次生报表前删除fileInfo的记录

        for function_name in [
            self.common_name.wop_settle_file_download,
            self.common_name.wop_settle_file_resolve,
            self.common_name.wop_trans_reconcile,
            self.common_name.wop_trans_calc,
            self.common_name.wop_generate_file]:
            self.execute_all_wop_function(wopid, [mopid], [function_name])

        # mop侧的相关function
        for function_name in [self.common_name.mop_trans_import,
                              self.common_name.mop_settle_file_resolve,
                              self.common_name.mop_trans_reconcile,
                              self.common_name.mop_trans_calc,
                              self.common_name.mop_generate_file]:
            self.execute_all_mop_function(mopid, [wopid], [function_name])


if __name__ == '__main__':
    pass
    common_name = CommonName()

    funciton_test = Performance("test", "20200322", common_name.bilateral,
                                common_name.file_init_wop
                                )
    # import time
    #
    # wopid = "WOP_performnace_one"

    # time1=time.time()
    funciton_test.mode_one_wop_mop_reconcile()
    # funciton_test.performance_single_wop_test()
    # time2=time.time()

    # funciton_test = Performance("test", "20200122", common_name.evonet,
    #                                common_name.evonet,
    #                                )

    # funciton_test.performance_single_wop_test()
    #
    # funciton_test = MopPerformance("test", "20200122", common_name.evonet,
    #                             common_name.evonet, tyo_task_func, sgp_task_func,
    #                             )
    #
    # # 造数据
    # funciton_test.performance_mop_test()

    # MOP 侧----------------------
    # common_name = CommonName()
    # tyo_task_func = TaskFuncs("test", "wop")
    # sgp_task_func = TaskFuncs("test", "mop")
    # funciton_test = MopPerformance("test", "20200122", common_name.evonet,
    #                                common_name.evonet, tyo_task_func, sgp_task_func,
    #                                )
    # import time
    #
    # # 造数据
    # funciton_test.performance_mop_test()

    # count1 = funciton_test.performance_evosettle_db.count("trans", {"wopID": wopid})
    # print(count1)
    # funciton_test.wop_WopPerformance_function()
    # count2 = funciton_test.performance_evosettle_db.count(common_name.trans_settle_wop, {"trans.wopID": wopid})
    # print(count2)

    # funciton_test.performance_evosettle_db.delete_manys(common_name.trans_settle_wop,{"trans.wopID":wopid})
    # count1=funciton_test.performance_evosettle_db.count("trans",{"wopID":wopid})
    # print(count1)
    #
    # time1 = time.time()
    # funciton_test.tyo_wop_settle_task(wopid, ["MOP_performnace_one","MOP_performnace_one",],
    #                              [common_name.wop_trans_import
    #                               ])
    # time2=time.time()
    # print(time2-time1)

    # count2 = funciton_test.performance_evosettle_db.count(common_name.trans_settle_wop, {"trans.wopID": wopid})
    # print(count2)
