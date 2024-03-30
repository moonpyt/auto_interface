import random
from base.db import MongoDB
from base.date_format import DateUtil
from base.read_config import *
from common.evosettle.task_funcs import TaskFuncs
from common.evosettle.comm_funcs import CommonName
from common.evosettle.parmiko_module import Parmiko_Module
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData
from common.evosettle.mongo_data import CreateConfig


class MopPerformance(object):
    # 统一以 tyo  为wop节点;sgp  为mop节点
    # 重构之后其它模式只需要调用对应的方法并传入对应的参数就执对应的方法了，不需要每个模式都再写一遍，有需要的话，只需要在这里修改了，还可以通过多线程的方式调用case
    def __init__(self, envirs, sett_date, model, fileinit, tyo_task_func, sgp_task_func,
                 path=None, title=None, ):
        if path == None:
            path = abspath(__file__, '../../../config/evosettle/evosettle_' + envirs + '.ini')
        if title == None:
            title = 'trans_data'
        self.date_format = DateUtil()
        # 获取配置参数
        self.evosettle_config = ConfigIni(path, title)
        # config 和settle数据库的对象
        self.performance_evoconfig_db = MongoDB(self.evosettle_config.get_ini("performance_evoconfig_url"),
                                                "evoconfig")
        self.performance_evosettle_db = MongoDB(self.evosettle_config.get_ini("performance_evosetltle_url"),
                                                "evosettle")
        self.tyo_func_url = self.evosettle_config.get_ini("tyo_performance_request_url")  # tyo节点单个任务的url
        self.create_config = CreateConfig()
        self.encrypt = Encrypt()
        self.tyo_task_func = tyo_task_func
        self.sgp_task_func = sgp_task_func
        self.model = model
        self.fileinit = fileinit
        self.case_data = CaseData()
        self.trans_type_list = ["CPM Payment", "MPM Payment", "Refund"]
        self.sett_date = sett_date
        # 月报日期，每月四号生月报
        self.monthly_sett_date = '20201004'
        self.sftp_func = Parmiko_Module()

        self.sgp_func_url = self.evosettle_config.get_ini("sgp_func_url")  # spg节点单个任务的url
        # self.tyo_ip = self.evosettle_config.get_ini("tyo_ip")
        # self.tyo_user = self.evosettle_config.get_ini("tyo_user")
        # self.sgp_ip = self.evosettle_config.get_ini("sgp_ip")
        # self.sgp_user = self.evosettle_config.get_ini("sgp_user")
        self.aes_decrypt = Aesecb(self.encrypt.decrypt(self.evosettle_config.get_ini("server_key")))
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
                                 [self.common_name.mop_trans_import,
                                  self.common_name.mop_trans_sync,
                                  self.common_name.mop_trans_calc,
                                  self.common_name.mop_self_sett,
                                  self.common_name.mop_generate_file,
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
        self.tyo_task_func.settle_task_request(self.tyo_func_url, "mop", mopid, wopid_list, self.sett_date,
                                               function_name, self.model, self.fileinit)
        time2 = time.time()
        print(str(time2 - time1))
        print("exect_after_time", )
        print(self.date_format.format_time(time.time()))
        print("上面是一组 MOP function-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------------------")
        # 休息三分钟，测试function有针对性

    def insert_trans_data(self, number, settle_currency, mopid, wopid1, wopid2):

        for i in range(number):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                self.performance_evosettle_db.insert_many("trans",
                                                          self.report_trans_list(wopid1,
                                                                                 mopid,
                                                                                 settle_currency,
                                                                                 trans_currency)[
                                                              0])
                self.performance_evosettle_db.insert_many("trans",
                                                          self.report_trans_list(wopid2,
                                                                                 mopid,
                                                                                 settle_currency,
                                                                                 trans_currency)[
                                                              0])

    def performance_mop_test(self):
        # 测试一个wopid对应两个mopId的交易
        # 这个evonet模式执行时需要三分钟
        mopid = "MOP_auto" + str(random.randint(10000, 999999))
        wopid1 = "WOP_auto" + str(random.randint(10000, 999999))
        wopid2 = "WOP_auto" + str(random.randint(10000, 999999))

        mopid = "MOP_auto" + "wwsk"
        wopid1 = "WOP_auto" + "mkyg"
        wopid2 = "WOP_auto" + "linu"

        wopid_list = [wopid1, wopid2]
        settle_currency = "CNY"
        # 删除配置2

        self.performance_evoconfig_db.delete_manys("mop", {"baseInfo.mopID": mopid})
        self.performance_evoconfig_db.delete_manys("wop", {"baseInfo.wopID": {"$in": [wopid1, wopid2]}})
        self.performance_evoconfig_db.delete_manys("customizeConfig", {"mopID": mopid})
        self.performance_evoconfig_db.delete_manys("relation", {"mopID": mopid})

        # 创建配置1
        self.create_single_config(self.performance_evoconfig_db, wopid1, mopid, self.model, self.fileinit, "daily",
                                  "daily", str(random.randint(100000, 9900000)), "tyo")
        self.performance_evoconfig_db.delete_manys("mop", {"baseInfo.mopID": mopid})
        # 创建配置 2
        self.create_single_config(self.performance_evoconfig_db, wopid2, mopid, self.model, self.fileinit, "daily",
                                  "daily", str(random.randint(100000, 9900000)), "tyo")
        # 修改币种及计费方式

        self.performance_evoconfig_db.update_one("mop", {"baseInfo.mopID": mopid},
                                                 {"settleInfo.settleCurrency": settle_currency,
                                                  "settleInfo.transProcessingFeeCollectionMethod": "daily",
                                                  "settleInfo.transProcessingFeeCalculatedMethod": "single",
                                                  "settleInfo.fxProcessingFeeCollectionMethod": "daily",
                                                  "settleInfo.fxProcessingFeeCalculatedMethod": "single",
                                                  "settleInfo.fxRebateCollectionMethod": "daily"
                                                  })
        # 数据插入到trans表,造两条交易
        # 修改币种及计费方式
        # # 首次删除交易表的数据
        self.performance_evosettle_db.delete_manys(self.common_name.trans_settle_mop, {"trans.mopID": mopid})
        self.performance_evosettle_db.delete_manys(self.common_name.trans_summary_mop, {"trans.mopID": mopid})

        # self.performance_evosettle_db.update_many("transSettle.mop", {"trans.mopID": "MOP_autowwsk", "clearFlag": True},
        #                                           {
        #                                               "blendType": "default",
        #                                               "clearFlag": False,
        #                                               "feeFlag": False,
        #                                               "settleFlag": False, })
        #
        # # 插入2000000* 为 240 万条数据
        # # self.insert_trans_data(166667, settle_currency, mopid, wopid1, wopid2)
        #
        function_list = [
            self.common_name.mop_trans_import,
            self.common_name.mop_self_sett,
            self.common_name.mop_trans_calc,
            self.common_name.mop_generate_file,
        ]
        # --------------
        for function_name in function_list:
            self.execute_all_mop_function(mopid, wopid_list, [function_name])
        # _____________________________
        #单独执行functionlist
        # self.execute_all_mop_function(mopid, wopid_list, function_list)

if __name__ == '__main__':
    common_name = CommonName()
    tyo_task_func = TaskFuncs("test", "wop")
    sgp_task_func = TaskFuncs("test", "mop")
    funciton_test = MopPerformance("test", "20200122", common_name.evonet,
                                   common_name.evonet, tyo_task_func, sgp_task_func,
                                   )
    import time


    # 造数据
    funciton_test.performance_mop_test()
