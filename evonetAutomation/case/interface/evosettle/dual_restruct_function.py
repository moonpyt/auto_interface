import random, time
import datetime
from common.evosettle.task_funcs import TaskFuncs
from base.read_config import *
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evosettle.comm_funcs import CommonName
from common.evosettle.parmiko_module import Parmiko_Module
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData


class RestructFunction(object):
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
        self.month_file_sett_date = '20201004'
        self.database_connect = DatabaseConnect(envirs)
        self.tyo_config_db = self.database_connect.tyo_config_db
        self.tyo_evosettle_db = self.database_connect.tyo_evosettle_db
        self.sgp_config_db = self.database_connect.sgp_config_db
        self.sgp_evosettle_db = self.database_connect.sgp_evosettle_db
        self.sftp_func = Parmiko_Module()
        self.tyo_func_url = self.evosettle_config.get_ini("tyo_func_url")  # tyo节点单个任务的url  k8s_tyo_func_url
        self.k8s_tyo_func_url = self.evosettle_config.get_ini("k8s_tyo_func_url")  # tyo节点单个任务的url  k8s_tyo_func_url
        # self.k8s_tyo_func_url = self.evosettle_config.get_ini("k8s_tyo_func_url")
        self.sgp_func_url = self.evosettle_config.get_ini("sgp_func_url")  # sgp节点单个任务的url
        self.tyo_ip = self.evosettle_config.get_ini("tyo_ip")
        self.tyo_user = self.evosettle_config.get_ini("tyo_user")
        self.sgp_ip = self.evosettle_config.get_ini("sgp_ip")
        self.sgp_user = self.evosettle_config.get_ini("sgp_user")
        self.aes_decrypt = Aesecb(self.encrypt.decrypt(self.evosettle_config.get_ini("server_key")))
        self.common_name = CommonName()
        #  删除的查询参数   {"baseInfo.wopID" :{"$regex":"^WOP_Auto"}}

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

    def tyo_sgp_db_init(self):
        # 数据初始化，即删除双节点相关表中的数据;
        # 通过func跑任务不需要有setttask也能执行
        self.task_func.dual_db_init()
        # 造wop,mop，relation,customconfig,的配置
        # 只需要在tyo节点新建就可以，同步应用会同步到 sgp节点

    def refund_trans_list(self, wopid, mopid):
        # 为了退款计费而造的交易;两笔正向，两笔Refund 交易
        refund_orig_mpm_evonet_order_nuber = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_mpm_order_number = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_orig_cpm_evonet_order_nuber = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_cpm_order_number = str(random.randint(100000000000000000000, 900000000000000000000))
        orig_mpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "MPM Payment",
                                                       refund_orig_mpm_evonet_order_nuber, )
        # mPM退款交易
        refund_mpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "Refund",
                                                         refund_mpm_order_number,
                                                         refund_orig_evonet_order_nuber=refund_orig_mpm_evonet_order_nuber)
        # ------------------
        orig_cpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "CPM Payment",
                                                       refund_orig_cpm_evonet_order_nuber, )
        # CPM退款交易
        refund_cpm_sett_data = self.case_data.trans_data(wopid, mopid, self.sett_date, "Refund",
                                                         refund_cpm_order_number,
                                                         refund_orig_evonet_order_nuber=refund_orig_cpm_evonet_order_nuber)
        sett_trans_list = [orig_mpm_sett_data, refund_mpm_sett_data, orig_cpm_sett_data, refund_cpm_sett_data]
        order_number_list = [refund_orig_mpm_evonet_order_nuber, refund_mpm_order_number,
                             refund_orig_cpm_evonet_order_nuber, refund_cpm_order_number]
        return (sett_trans_list, order_number_list)

    def wop_trans_import(self):
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        mopid2 = self.task_func.generate_mopid()
        if self.model == self.common_name.evonet:
            # 如果是evonet模式，可以一个wopid，对应多给mopid

            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            self.tyo_config_db.delete_manys("wop", {"baseInfo.wopID": wopid})
            # 创建配置 2
            self.db_operations.create_single_config(wopid, mopid2, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            evonet_number_list = []
            for mopid in [mopid1, mopid2]:
                data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
                # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
                # 双节点插入到tyo节点trans  表
                self.tyo_evosettle_db.insert_many("trans", data[0])
                evonet_number_list.extend(data[1])
            # 触发交易流水同步
            self.wop_settle_task(wopid, [mopid1, mopid2], [self.common_name.wop_trans_import])
            # 校验数据同步数量一致
            assert self.tyo_evosettle_db.count("trans", {"wopID": wopid,
                                                         "wopSettleDate": self.sett_date}) == self.tyo_evosettle_db.count(
                self.common_name.trans_settle_wop, {"trans.wopID": wopid, "settleDate": self.sett_date})
            # 检验同步的数据字段正确,校验wop侧
            for number in evonet_number_list:
                # 每次查询一条交易进行校验交易流水导入的初始化的值
                self.task_func.trans_import_assert("wop", number)
        if self.model == self.common_name.bilateral:
            # 如果是直清模式则是  一个wopid，对应一个mopid
            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            data = self.case_data.trans_list(wopid, mopid1, self.sett_date, self.model)
            # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
            # 双节点插入到tyo节点trans  表
            self.tyo_evosettle_db.insert_many("trans", data[0])
            # 触发交易流水同步
            self.wop_settle_task(wopid, [mopid1], [self.common_name.wop_trans_import])
            # 校验数据同步数量一致
            assert self.tyo_evosettle_db.count("trans", {"wopID": wopid,
                                                         "wopSettleDate": self.sett_date}) == self.tyo_evosettle_db.count(
                self.common_name.trans_settle_wop, {"trans.wopID": wopid, "settleDate": self.sett_date})
            # 检验同步的数据字段正确,校验wop侧
            for number in data[1]:
                # 每次查询一条交易进行校验交易流水导入的初始化的值
                self.task_func.trans_import_assert("wop", number)

    def mop_trans_import(self):
        # 流水导入，交易从trans表导入到transSettle.wop表
        # 流水导入初始化数据校验
        mopid = self.task_func.generate_mopid()
        wopid1 = self.task_func.generate_wopid()
        wopid2 = self.task_func.generate_wopid()
        if self.model == self.common_name.evonet:
            # 如果是evonet模式，可以一个wopid，对应多给mopid

            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid1, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            # 删除 mop表的信息
            self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
            self.sgp_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
            # 创建配置 2
            self.db_operations.create_single_config(wopid2, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            evonet_number_list = []
            for wopid in [wopid1, wopid2]:
                data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
                # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
                # 双节点插入到tyo节点trans  表
                self.sgp_evosettle_db.insert_many("trans", data[0])
                evonet_number_list.extend(data[1])
            # 触发交易流水同步
            self.mop_settle_task(mopid, [wopid1, wopid2], [self.common_name.mop_trans_import])
            # 校验数据同步数量一致
            assert self.sgp_evosettle_db.count("trans", {"mopID": wopid,
                                                         "mopSettleDate": self.sett_date}) == self.sgp_evosettle_db.count(
                self.common_name.trans_settle_wop, {"trans.mopID": mopid, "settleDate": self.sett_date})
            # 检验同步的数据字段正确,校验wop侧
            for number in evonet_number_list:
                # 每次查询一条交易进行校验交易流水导入的初始化的值
                self.task_func.trans_import_assert("mop", number)
        if self.model == self.common_name.bilateral:
            # 如果是 bilateral模式，一个mopid 对应 一个 wopid
            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid1, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")

            data = self.case_data.trans_list(wopid1, mopid, self.sett_date, self.model)
            # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
            # 双节点插入到tyo节点trans  表
            self.sgp_evosettle_db.insert_many("trans", data[0])
            # 触发交易流水同步
            self.mop_settle_task(mopid, [wopid1, ], [self.common_name.mop_trans_import])
            # 校验数据同步数量一致
            assert self.sgp_evosettle_db.count("trans", {"mopID": mopid,
                                                         "mopSettleDate": self.sett_date}) == self.sgp_evosettle_db.count(
                self.common_name.trans_settle_mop, {"trans.mopID": mopid, "settleDate": self.sett_date})
            # 检验同步的数据字段正确,校验wop侧
            for number in data[1]:
                # 每次查询一条交易进行校验交易流水导入的初始化的值
                self.task_func.trans_import_assert("mop", number)

    def wop_file_download_resolve_reconcile(self):
        # 校验勾兑平
        # 只存在模式一中:文件下载，文件解析，文件勾兑
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        # 流水导入和计费，为生wop系统文件做准备
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        sftp_data = self.case_data.wop_sftp_data(self.tyo_ip, self.tyo_user, wopid,
                                                 self.evosettle_config.get_ini("wop_sftp_data_key"))
        # sftp_info  插入配置
        self.tyo_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.task_func.wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.tyo_ip, self.tyo_user, server_cmd)
        # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path + file_name,
                                         file_name)
        self.wop_settle_task(wopid, [mopid], [
            self.common_name.wop_settle_file_download,
            self.common_name.wop_settle_file_resolve])
        resolve_result = self.tyo_evosettle_db.get_one("fileInfo", {"firstRole": mopid})["resolveFlag"]
        assert resolve_result == True
        # # 校验解析进入数据库的信息
        interchange_fee = 3.0
        self.task_func.wop_system_filerecon_assert(file_name, wopid, mopid, self.sett_date)
        # 删除刚上传的文件
        os.remove(file_name)
        self.tyo_evosettle_db.update_many(self.common_name.trans_file_wop, {"wopID": wopid},
                                          {"trans.interchangeFee": interchange_fee})
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"settleInfo.settleAmount": 33333,
                                           "settleInfo.settleCurrency": "evonet_test",
                                           "settleInfo.interchangeFee": 333333, })
        # 触发勾兑
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile])
        # 校验勾兑后的状态blendType,settleFlag
        for evonet_number in data[1]:
            self.task_func.chec_recon_result(self.common_name.file_init_wop, evonet_number)
        # 这下面这一步是为了测试 计费时候 不影响勾兑时候时赋值的 interchangeFee
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_sett_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        for fee_data in trans_sett_data:
            assert fee_data["settleInfo"]["interchangeFee"] == interchange_fee

    def wop_file_full_extra_resolve_reconcile(self):
        # 模式一文件下载，文件解析，文件勾兑,勾兑时 为多清,且勾兑时，trans表和transSett表根据
        # transFile中的 evonetOrderNumber订单号都找不到对应的交易
        # 只存在模式一中:文件下载，文件解析，文件勾兑
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        # 流水导入和计费，为生wop系统文件做准备
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])
        sftp_data = self.case_data.wop_sftp_data(self.tyo_ip, self.tyo_user, wopid,
                                                 self.evosettle_config.get_ini("wop_sftp_data_key"))
        # sftp_info  插入配置
        self.tyo_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.task_func.wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.tyo_ip, self.tyo_user, server_cmd)
        # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path + file_name,
                                         file_name)
        self.wop_settle_task(wopid, [mopid], [
            self.common_name.wop_settle_file_download,
            self.common_name.wop_settle_file_resolve])
        # # 校验解析进入数据库的信息
        interchange_fee = 3.0
        self.task_func.wop_system_filerecon_assert(file_name, wopid, mopid, self.sett_date)
        # 删除刚上传的文件
        os.remove(file_name)
        self.tyo_evosettle_db.update_many(self.common_name.trans_file_wop, {"wopID": wopid},
                                          {"trans.interchangeFee": interchange_fee})
        # 删除transSettle.wop数据并触发勾兑
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.tyo_evosettle_db.delete_manys(self.common_name.trans, {"wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile])
        # 根据订单号查询并校验
        for evonet_number in data[1]:
            self.task_func.full_extra_sett(self.common_name.file_init_wop, evonet_number)

    def wop_file_extra_trans_resolve_reconcile(self):
        # 模式一文件下载，文件解析，文件勾兑,勾兑时 为多清,且勾兑时，trans表可以找到交易的多清
        # 只存在模式一中:文件下载，文件解析，文件勾兑
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        # 流水导入和计费，为生wop系统文件做准备
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])
        sftp_data = self.case_data.wop_sftp_data(self.tyo_ip, self.tyo_user, wopid,
                                                 self.evosettle_config.get_ini("wop_sftp_data_key"))
        # sftp_info  插入配置
        self.tyo_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.task_func.wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.tyo_ip, self.tyo_user, server_cmd)
        # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path + file_name,
                                         file_name)
        self.wop_settle_task(wopid, [mopid], [
            self.common_name.wop_settle_file_download,
            self.common_name.wop_settle_file_resolve])
        # # 校验解析进入数据库的信息
        interchange_fee = 3.0
        self.task_func.wop_system_filerecon_assert(file_name, wopid, mopid, self.sett_date)
        # 删除刚上传的文件
        os.remove(file_name)
        self.tyo_evosettle_db.update_many(self.common_name.trans_file_wop, {"wopID": wopid},
                                          {"trans.interchangeFee": interchange_fee})
        # 删除transSettle.wop数据并触发勾兑
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile])
        # 根据订单号查询并校验
        for evonet_number in data[1]:
            self.task_func.assert_extra_trans_sett(self.common_name.file_init_wop, evonet_number)

    def wop_file_lack_reconcile(self):
        # 少清状态校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, self.common_name.wop_trans_reconcile])
        # 校验勾兑后的状态blendType,settleFlag
        trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        # 校验勾兑后的状态
        count = 0
        # 校验勾兑成功的标志，
        for i in trans_data:
            assert i["settleFlag"] == False
            assert i["blendType"] == "Lack"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
            count += 1
        # 校验勾兑的数量
        assert count == 4

    def wop_file_reconcile_status_assert(self):
        # 勾对时，查询transSettle.wop表交易的条件的校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        # -----------------------
        # blendType 为default,settleFlag为 True
        self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"blendType": "default", "settleFlag": False})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile, ])
        trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                           "function": self.common_name.wop_trans_reconcile})[
            "result"]
        count = 0

        for i in trans_data:
            assert i["settleFlag"] == False
            assert i["blendType"] == "Lack"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
            count += 1
        assert func_result_flag == "success"
        # 校验勾兑的数量
        assert count == 4
        # --------------------
        # blendType 为not_default,settleFlag为 test_flag
        blend_type = "not_default"
        self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"blendType": blend_type, "settleFlag": False})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile, ])
        trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                           "function": self.common_name.wop_trans_reconcile})[
            "result"]
        count = 0
        for i in trans_data:
            assert i["settleFlag"] == False
            assert i["blendType"] == blend_type
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
            count += 1
        # 校验勾兑的数量
        assert count == 4
        assert func_result_flag == "success"
        # ---------------------------------
        # blendType 为default,settleFlag为 test_flag
        self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"blendType": "default", "settleFlag": "test_flag"})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile, ])
        trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
        func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                           "function": self.common_name.wop_trans_reconcile})[
            "result"]
        count = 0
        for i in trans_data:
            assert i["settleFlag"] == "test_flag"
            assert i["blendType"] == "default"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
            count += 1
        # 校验勾兑的数量
        assert count == 4
        assert func_result_flag == "success"

        # --------------------
        # 交易状态校验
        for status in ["succeeded", "partially refunded", "fully refunded", "not_succeeded"]:
            self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.status": status})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile, ])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
            func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.wop_trans_reconcile})[
                "result"]
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == False
                if status != "not_succeeded":
                    assert i["blendType"] == "Lack"
                else:
                    assert i["blendType"] == "default"
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                assert i["settleInfo"]["interchangeFee"] == 0.0
                count += 1
            # 校验勾兑的数量
            assert count == 4
            assert func_result_flag == "success"
        # -----------------------
        # 交易类型校验
        for trans_type in ["CPM Payment", "MPM Payment", "Account Debit", "Account Credit", "Refund", "not_transtype"]:

            self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.transType": trans_type, "trans.status": "succeeded"})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_reconcile, ])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
            func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.wop_trans_reconcile})[
                "result"]
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == False
                if trans_type != "not_transtype":
                    assert i["blendType"] == "Lack"

                else:
                    assert i["blendType"] == "default"
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                assert i["settleInfo"]["interchangeFee"] == 0.0
                count += 1
            # 校验勾兑的数量
            assert count == 4
            assert func_result_flag == "success"

    def mop_file_download_resolve_reconcile(self):
        # 校验勾兑平
        # 只存在模式一中:文件下载，文件解析，文件勾兑
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        # 流水导入和计费，为生wop系统文件做准备
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])
        # 修改状态，为生文件任务做准备
        interchange_fee = 3
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"settleInfo.interchangeFee": interchange_fee, "settleFlag": True,
                                           "blendType": "success",
                                           "clearFlag": True, "feeFlag": True
                                           })
        # transFile.wopNode的校验
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_generate_file])
        self.mop_settle_task(mopid, [wopid],
                             [self.common_name.mop_trans_import,
                              self.common_name.mop_settle_file_download, self.common_name.mop_settle_file_resolve,
                              ])
        # 校验解析到 transFile.wopNode的数据，对比 sgp 的 transSettle.mop和sgp的transFile.wopNode的数据
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                          {"settleInfo.settleAmount": 33333,
                                           "settleInfo.settleCurrency": "evonet_test",
                                           "settleInfo.interchangeFee": 333333, })
        self.mop_settle_task(mopid, [wopid],
                             [self.common_name.mop_trans_reconcile])
        # 触发勾兑
        for evonet_number in data[1]:
            self.task_func.chec_recon_result("mop", evonet_number)
        trans_sett_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid})
        for fee_data in trans_sett_data:
            assert fee_data["settleInfo"]["interchangeFee"] == interchange_fee

    def mop_file_full_extra_resolve_reconcile(self):
        # mop侧完全多清即，mop侧 trans表和transSettle.wop表多不存对应的数据
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 customizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        # 流水导入和计费，为生wop系统文件做准备
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])
        # 修改状态，为生文件任务做准备
        interchange_fee = 3
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"settleInfo.interchangeFee": interchange_fee, "settleFlag": True,
                                           "blendType": "success",
                                           "clearFlag": True, "feeFlag": True
                                           })
        # transFile.wopNode的校验
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_generate_file])
        self.mop_settle_task(mopid, [wopid],
                             [self.common_name.mop_trans_import,
                              self.common_name.mop_settle_file_download, self.common_name.mop_settle_file_resolve,
                              ])
        self.mop_settle_task(mopid, [wopid],
                             [self.common_name.mop_trans_reconcile])
        # 根据订单号查询并校验
        for evonet_number in data[1]:
            self.task_func.full_extra_sett("mop", evonet_number)

    def mop_file_extra_trans_resolve_reconcile(self):
        # 模式一文件下载，文件解析，文件勾兑,勾兑时 为多清,且勾兑时，trans表可以找到交易的多清
        # 只存在模式一中:文件下载，文件解析，文件勾兑
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        # 流水导入和计费，为生wop系统文件做准备
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])
        # 修改状态，为生文件任务做准备
        interchange_fee = 3
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"settleInfo.interchangeFee": interchange_fee, "settleFlag": True,
                                           "blendType": "success",
                                           "clearFlag": True, "feeFlag": True
                                           })
        # transFile.wopNode的校验
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_generate_file])
        self.mop_settle_task(mopid, [wopid],
                             [self.common_name.mop_settle_file_download, self.common_name.mop_settle_file_resolve,
                              self.common_name.mop_trans_reconcile])

        # 根据订单号查询并校验
        for evonet_number in data[1]:
            self.task_func.assert_extra_trans_sett("mop", evonet_number)

    def mop_file_lack_reconcile(self):
        # 少清状态校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        self.mop_settle_task(wopid, [mopid], [self.common_name.mop_trans_import, self.common_name.mop_trans_reconcile])
        # 校验勾兑后的状态blendType,settleFlag
        trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
        # 校验勾兑后的状态
        # 校验勾兑成功的标志，
        for i in trans_data:
            assert i["settleFlag"] == False
            assert i["blendType"] == "Lack"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
        # 校验勾兑的数量

    def mop_file_reconcile_status_assert(self):
        # 勾对时，查询transSettle.wop表交易的条件的校验
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        # -----------------------
        # blendType 为default,settleFlag为 True
        blend_type = "default"
        settle_flag = False
        self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, ])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                          {"blendType": blend_type, "settleFlag": settle_flag})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_reconcile, ])
        trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
        func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"mopID": mopid,
                                                                                           "function": self.common_name.mop_trans_reconcile})[
            "result"]
        count = 0
        for i in trans_data:
            assert i["settleFlag"] == False
            assert i["blendType"] == "Lack"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
            count += 1
        assert func_result_flag == "success"
        # 校验勾兑的数量
        assert count == 4
        # --------------------
        blend_type = "notdefault"
        settle_flag = False
        # blendType 为notdefault,settleFlag为 False
        self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, ])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                          {"blendType": blend_type, "settleFlag": False})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_reconcile, ])
        trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
        func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                           "function": self.common_name.mop_trans_reconcile})[
            "result"]
        count = 0
        for i in trans_data:
            assert i["settleFlag"] == False
            assert i["blendType"] == "notdefault"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
            count += 1
        assert func_result_flag == "success"
        # 校验勾兑的数量
        assert count == 4
        # ---------------------------------
        blend_type = "default"
        settle_flag = "test_flag"
        # blendType 为notdefault,settleFlag为 False
        self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, ])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                          {"blendType": blend_type, "settleFlag": settle_flag})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_reconcile, ])
        trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
        func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                           "function": self.common_name.mop_trans_reconcile})[
            "result"]
        for i in trans_data:
            assert i["settleFlag"] == "test_flag"
            assert i["blendType"] == "default"
            assert i["feeFlag"] == False
            assert i["clearFlag"] == False
            assert i["settleInfo"]["interchangeFee"] == 0.0
        # 校验勾兑的数量
        assert count == 4
        assert func_result_flag == "success"

        # ------------------
        # 交易状态校验
        for status in ["succeeded", "partially refunded", "fully refunded", "not_succeeded"]:
            self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, ])

            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.status": status})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_reconcile, ])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
            func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.mop_trans_reconcile})[
                "result"]
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == False
                if status != "not_succeeded":
                    assert i["blendType"] == "Lack"
                else:
                    assert i["blendType"] == "default"
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                assert i["settleInfo"]["interchangeFee"] == 0.0
                count += 1
            # 校验勾兑的数量
            assert count == 4
            assert func_result_flag == "success"
        # -----------------------
        # 交易类型校验
        for trans_type in ["CPM Payment", "MPM Payment", "Account Debit", "Account Credit", "Refund", "not_transtype"]:

            self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, ])

            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.transType": trans_type, "trans.status": "succeeded"})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_reconcile, ])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
            func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.mop_trans_reconcile})[
                "result"]
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == False
                if trans_type != "not_transtype":
                    assert i["blendType"] == "Lack"

                else:
                    assert i["blendType"] == "default"
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                assert i["settleInfo"]["interchangeFee"] == 0.0
                count += 1
            # 校验勾兑的数量
            assert count == 4
            assert func_result_flag == "success"

    def wop_self_settle(self):
        wopid = self.task_func.generate_wopid()
        mopid1 = self.task_func.generate_mopid()
        mopid2 = self.task_func.generate_mopid()
        if self.model == self.common_name.evonet:
            # 如果是evonet模式，可以一个wopid，对应多给mopid
            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            self.tyo_config_db.delete_manys("wop", {"baseInfo.wopID": wopid})
            # 创建配置 2
            self.db_operations.create_single_config(wopid, mopid2, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            mopid_list = [mopid1, mopid2]
            for mopid in mopid_list:
                data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
                # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
                # 双节点插入到tyo节点trans  表
                self.tyo_evosettle_db.insert_many("trans", data[0])
            # ------------------
            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_trans_import])
            blend_type = "default"
            flag = False
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_self_sett])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                        {"trans.wopID": wopid})

            # 校验勾兑后的状态
            count = 0
            # 校验勾兑成功的标志，
            for i in trans_data:
                assert i["settleFlag"] == True
                assert i["blendType"] == "selfSettle"
                assert i["clearFlag"] == False
                assert i["feeFlag"] == False
                count += 1
            # 校验勾兑的数量
            assert count == 8
            # ------------------------
            # 自主清算标识校验，即 只有 settleFlag为False,blendType为default才会进行自主清算
            blend_type = "notdefault"
            flag = False
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_self_sett])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                        {"trans.wopID": wopid})
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == flag
                assert i["blendType"] == blend_type
                count += 1
            # 校验勾兑的数量
            assert count == 8
            # ---------------------
            # 自主清算标识校验，即 只有 settleFlag为False,blendType为default才会进行自主清算
            blend_type = "default"
            flag = "notFalse"
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_self_sett])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                        {"trans.wopID": wopid})
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == flag
                assert i["blendType"] == blend_type
                count += 1
            # 校验勾兑的数量
            assert count == 8
            # ---------------------
            # 自主清算标识校验，即 只有 settleFlag为False,blendType为default才会进行自主清算
            blend_type = "notdefault"
            flag = "notFalse"
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_self_sett])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                        {"trans.wopID": wopid})
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == flag
                assert i["blendType"] == blend_type
                count += 1
            # 校验勾兑的数量
            assert count == 8

        if self.model == self.common_name.bilateral:
            # 如果是evonet模式，可以一个wopid，对应多给mopid

            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid, mopid1, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")

            mopid_list = [mopid1]
            for mopid in mopid_list:
                data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
                # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
                # 双节点插入到tyo节点trans  表
                self.tyo_evosettle_db.insert_many("trans", data[0])
            # ------------------
            blend_type = "default"
            flag = False
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_trans_import])

            self.wop_settle_task(wopid, mopid_list, [self.common_name.wop_self_sett])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                        {"trans.wopID": wopid})

            # 校验勾兑后的状态
            count = 0
            # 校验勾兑成功的标志，
            for i in trans_data:
                assert i["settleFlag"] == True
                assert i["blendType"] == "selfSettle"
                assert i["clearFlag"] == False
                assert i["feeFlag"] == False
                count += 1
            # 校验勾兑的数量
            assert count == 4

    def mop_self_settle_abnormal(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        # -----------------------
        # blendType 为default,settleFlag为 True
        self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import, ])
        # 自主清算异常测试
        # 交易状态校验
        for status in ["succeeded", "partially refunded", "fully refunded", "not_succeeded"]:

            self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})

            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.status": status})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_self_sett, ])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
            func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.mop_self_sett})[
                "result"]
            count = 0
            for i in trans_data:
                if status != "not_succeeded":
                    assert i["blendType"] == "selfSettle"
                    assert i["settleFlag"] == True
                else:
                    assert i["blendType"] == "default"
                    assert i["settleFlag"] == False
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                count += 1
            # 校验勾兑的数量

            assert count == 4
            assert func_result_flag == "success"
        # -----------------------
        # 交易类型校验
        for trans_type in ["CPM Payment", "MPM Payment", "Refund", "not_transtype"]:
            self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})

            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.transType": trans_type, "trans.status": "succeeded"})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_self_sett, ])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop, {"trans.wopID": wopid})
            func_result_flag = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.mop_self_sett})[
                "result"]
            count = 0
            for i in trans_data:
                if trans_type != "not_transtype":
                    assert i["blendType"] == "selfSettle"
                    assert i["settleFlag"] == True

                else:
                    assert i["blendType"] == "default"
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                count += 1
            # 校验勾兑的数量
            assert count == 4
            assert func_result_flag == "success"

    def wop_self_settle_abnormal(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        # -----------------------
        # blendType 为default,settleFlag为 True
        self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])
        # 自主清算异常测试
        # 交易状态校验
        for status in ["succeeded", "partially refunded", "fully refunded", "not_succeeded"]:
            self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.status": status})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_self_sett, ])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
            func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.wop_self_sett})[
                "result"]
            count = 0
            for i in trans_data:
                if status != "not_succeeded":
                    assert i["blendType"] == "selfSettle"
                    assert i["settleFlag"] == True
                else:
                    assert i["blendType"] == "default"
                    assert i["settleFlag"] == False
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                count += 1
            # 校验勾兑的数量

            assert count == 4
            assert func_result_flag == "success"
        # -----------------------
        # 交易类型校验
        for trans_type in ["CPM Payment", "MPM Payment", "Refund", "not_transtype"]:

            self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import, ])

            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": "default", "settleFlag": False,
                                               "trans.transType": trans_type, "trans.status": "succeeded"})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_self_sett, ])
            trans_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid})
            func_result_flag = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                               "function": self.common_name.wop_self_sett})[
                "result"]
            count = 0
            for i in trans_data:
                if trans_type != "not_transtype":
                    assert i["blendType"] == "selfSettle"
                    assert i["settleFlag"] == True

                else:
                    assert i["blendType"] == "default"
                assert i["feeFlag"] == False
                assert i["clearFlag"] == False
                count += 1
            # 校验勾兑的数量
            assert count == 4
            assert func_result_flag == "success"

    def mop_self_settle(self):
        # mop侧一个mopid对应两个wopID
        mopid = self.task_func.generate_mopid()
        wopid1 = self.task_func.generate_wopid()
        wopid2 = self.task_func.generate_wopid()
        if self.model == self.common_name.evonet:
            # 如果是evonet模式，可以一个wopid，对应多给mopid
            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid1, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
            self.sgp_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
            # 创建配置 2
            self.db_operations.create_single_config(wopid2, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            wopid_list = [wopid1, wopid2]
            for wopid in wopid_list:
                data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
                # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
                # 双节点插入到tyo节点trans  表
                self.sgp_evosettle_db.insert_many("trans", data[0])
            # ------------------
            blend_type = "default"
            flag = False

            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_trans_import])
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_self_sett])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                        {"trans.mopID": mopid})

            # 校验勾兑后的状态
            count = 0
            # 校验勾兑成功的标志，
            for i in trans_data:
                assert i["settleFlag"] == True
                assert i["blendType"] == "selfSettle"
                assert i["clearFlag"] == False
                assert i["feeFlag"] == False
                count += 1
            # 校验勾兑的数量
            assert count == 8
            # ------------------------
            # 自主清算标识校验，即 只有 settleFlag为False,blendType为default才会进行自主清算
            blend_type = "notdefault"
            flag = False
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_self_sett])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                        {"trans.mopID": mopid})
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == flag
                assert i["blendType"] == blend_type
                count += 1
            # 校验勾兑的数量
            assert count == 8
            # ---------------------
            # 自主清算标识校验，即 只有 settleFlag为False,blendType为default才会进行自主清算
            blend_type = "default"
            flag = "notFalse"
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_self_sett])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                        {"trans.mopID": mopid})
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == flag
                assert i["blendType"] == blend_type
                count += 1
            # 校验勾兑的数量
            assert count == 8
            # ---------------------
            # 自主清算标识校验，即 只有 settleFlag为False,blendType为default才会进行自主清算
            blend_type = "notdefault"
            flag = "notFalse"
            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_self_sett])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                        {"trans.mopID": mopid})
            count = 0
            for i in trans_data:
                assert i["settleFlag"] == flag
                assert i["blendType"] == blend_type
                count += 1
            # 校验勾兑的数量
            assert count == 8
        if self.model == self.common_name.bilateral:
            # 如果是 bilateral 模式，一个mopid对应一个wopid
            # 创建wop mop信息，且mop的 nodeid为sgp
            # 创建配置1
            self.db_operations.create_single_config(wopid1, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
            self.sgp_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
            # 创建配置 2
            self.db_operations.create_single_config(wopid2, mopid, self.model, self.fileinit, "daily",
                                                    "daily", str(random.randint(100000, 9900000)), "sgp")
            wopid_list = [wopid1]
            for wopid in wopid_list:
                data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
                # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
                # 双节点插入到tyo节点trans  表
                self.sgp_evosettle_db.insert_many("trans", data[0])
            # ------------------
            blend_type = "default"
            flag = False
            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_trans_import])

            # 修改 clearFlag状态为 False，再次触发校验 blendType  settleFlag 的状态
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                              {"blendType": blend_type, "settleFlag": flag, })
            self.mop_settle_task(mopid, wopid_list, [self.common_name.mop_self_sett])
            trans_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                        {"trans.mopID": mopid})

            # 校验勾兑后的状态
            count = 0
            # 校验勾兑成功的标志，
            for i in trans_data:
                assert i["settleFlag"] == True
                assert i["blendType"] == "selfSettle"
                assert i["clearFlag"] == False
                assert i["feeFlag"] == False
                count += 1
            # 校验勾兑的数量
            assert count == 8

    def wop_calc_custom_config(self):
        # 将计费的逻辑全部assert;计费时取的参数为 customizeconfig
        # 直清模式一 wop侧计费
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费1
        # 修改交易状态,计费为日元到日元,且settleinfo.settlecurrency等于customizeconfig的settlecurrency
        self.db_operations.update_clear_fee_flag("wop", wopid, mopid, )
        # 修改wop 表中的币种和transSettle.wop表中的币种；
        # 每笔交易都计算 fxProcessFee
        sett_currency = "JPY"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": sett_currency,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.tyo_evosettle_db.update_many("transSettle.wop",
                                          {"trans.wopID": wopid},
                                          {"trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"})
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        # wop侧计费校验
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit, )
        # ______________________
        # 计费2;测试小数位,人民币到人民币，wop表的settlecurrency和customizeconfig 的settlecurrency 一致都是CNY
        # 修改交易状态,计费为人民币到人民币,且清算表 wop表settlecurrency 等于customizeconfig的settlecurrency等于CNY
        # 修改wop 表中的币种和transSettle.wop表中的币种；
        # 每笔交易都计算 fxProcessFee
        sett_currency = "CNY"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": sett_currency,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {
                                              "trans.wopSettleCurrency": sett_currency,
                                              "settleInfo.settleCurrency": sett_currency,
                                              "trans.wopConverterCurrencyFlag": True,
                                              "settleFlag": True,
                                              "blendType": "success"
                                          })
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit, )
        # _______________________
        # 计费3,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,但是交易币种和清算币种一致，
        # 用交易币CNY>>和清算币种一致
        sett_currency = "CNY"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": "JPY",
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit, )

    def wop_calc_three_currency(self):
        # 三种币种都不一致的情况
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop 侧和mop侧 的 wopsettleamount 和 wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费4,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 JPY  转换到CNY，需要乘以（1+mccr）  才能算出手续费
        trans_currency = "JPY"
        sett_currency = "USD"
        wop_settle_curreny = "CNY"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": wop_settle_curreny,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("wop", trans_currency, wop_settle_curreny)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # --------------------------
        # 三种币种都不一致的情况
        # 计费5,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 CNY  转换到 JPY，需要乘以（1+mccr）  才能算出手续费
        sett_currency = "USD"
        trans_currency = "CNY"
        wop_settle_curreny = 'JPY'
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("wop", trans_currency, wop_settle_curreny)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

    def wop_calc_fee_type_single_accumulation(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费6 收费方式为 transProcessingFeeCalculatedMethod": "accumulation",fxProcessingFeeCollectionMethod：“accumulation”
        # transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 CNY  转换到JPY，需要乘以（1+mccr）  才能算出手续费
        sett_currency = "USD"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "accumulation",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "accumulation"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        trans_currency = "CNY"
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # -----------------
        # 计费7 收费方式为 transProcessingFeeCalculatedMethod": "single",fxProcessingFeeCollectionMethod：“accumulation”
        sett_currency = "USD"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "accumulation"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        trans_currency = "CNY"
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)
        # -----------------
        # 计费8 收费方式为 transProcessingFeeCalculatedMethod": "accumulation",fxProcessingFeeCollectionMethod：“single”
        sett_currency = "USD"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "accumulation",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        trans_currency = "CNY"
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # 计费9 mccr测试，通用mccr;现在cutomizeconfig的交易币种只有 CNY和JPY ,造交易币种不是CNY，为USD就可以测试通用mccr 了
        sett_currency = "CNY"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": sett_currency,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        trans_currency = "USD"
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

    def wop_evonet_mode_calc(self):
        # evonet模式计费，计费时，不存在 customizecongig也可以进行清分计费
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        self.tyo_config_db.delete_manys(self.common_name.custom_config, {"wopID": wopid})
        # ------------------------
        for fee_collect_method in ["daily", "monthly"]:
            if fee_collect_method == "mothly":
                fee_calculate_method = ["single", "accumulation"]
            if fee_collect_method == "daily":
                fee_calculate_method = "single"
            # 先删除数据，再出发流水导入
            for sett_currency in ["CNY", "JPY"]:
                for wop_covert_flag in [True, False]:
                    self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                                  {"settleInfo.settleCurrency": sett_currency,
                                                   "settleInfo.transProcessingFeeCollectionMethod": fee_collect_method,
                                                   "settleInfo.transProcessingFeeCalculatedMethod": fee_calculate_method,
                                                   "settleInfo.fxProcessingFeeCollectionMethod": fee_collect_method,
                                                   "settleInfo.fxProcessingFeeCalculatedMethod": fee_calculate_method
                                                   })
                    # 删除数据之后，再触发流水导入并计费
                    self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                                       {"trans.wopID": wopid})
                    self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
                    trans_currency = "CNY"
                    self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                                      {"trans.wopID": wopid},
                                                      {"trans.transCurrency": trans_currency,
                                                       "trans.wopSettleCurrency": sett_currency,
                                                       "settleInfo.settleCurrency": sett_currency,
                                                       "trans.wopConverterCurrencyFlag": wop_covert_flag,
                                                       "settleFlag": True,
                                                       "blendType": "selfSettle"
                                                       })
                    # 触发计费交易计费
                    self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
                    self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                                           trans_currency)

    # -----------------------------------

    def mop_evonet_mode_calc(self):
        # evonet模式计费，计费时，不存在 customizecongig也可以进行清分计费
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 删除customizeconfig
        self.tyo_config_db.delete_manys(self.common_name.custom_config, {"wopID": wopid})
        self.sgp_config_db.delete_manys(self.common_name.custom_config, {"wopID": wopid})

        # ------------------------
        for fee_collect_method in ["daily", "monthly"]:
            if fee_collect_method == "mothly":
                fee_calculate_method = ["single", "accumulation"]
            if fee_collect_method == "daily":
                fee_calculate_method = "single"
            # 先删除数据，再出发流水导入
            for sett_currency in ["CNY", "JPY"]:
                for wop_covert_flag in [True, False]:
                    self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                                  {"settleInfo.settleCurrency": sett_currency,
                                                   "settleInfo.transProcessingFeeCollectionMethod": fee_collect_method,
                                                   "settleInfo.transProcessingFeeCalculatedMethod": fee_calculate_method,
                                                   "settleInfo.fxProcessingFeeCollectionMethod": fee_collect_method,
                                                   "settleInfo.fxProcessingFeeCalculatedMethod": fee_calculate_method
                                                   })
                    # 删除数据之后，再触发流水导入并计费
                    self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                                       {"trans.mopID": mopid})
                    self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
                    trans_currency = "CNY"
                    self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                                      {"trans.mopID": mopid},
                                                      {"trans.transCurrency": trans_currency,
                                                       "trans.mopSettleCurrency": sett_currency,
                                                       "settleInfo.settleCurrency": sett_currency,
                                                       "trans.mopConverterCurrencyFlag": wop_covert_flag,
                                                       "settleFlag": True,
                                                       "blendType": "selfSettle"
                                                       })
                    # 触发计费交易计费
                    self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
                    self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                                           trans_currency)

    def wop_calc_daily_single(self):
        # 这个只有 模式四 evonet模式有
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费10测试 wopConverterCurrencyFlag为False
        # -----------------
        trans_currency = "USD"
        settle_currency = "SGD"
        wop_settle_currency = "CNY"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": wop_settle_currency,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.wopConverterCurrencyFlag": False,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("wop", trans_currency, wop_settle_currency)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)
        # --------------------------
        # 计费12测试 测试计费方式都为daily,
        # -----------------
        settle_currency = "SGD"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "CNY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "daily",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "daily",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        trans_currency = "USD"
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.wopConverterCurrencyFlag": False,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("wop", trans_currency, settle_currency)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)
        # 计费13测试 测试计费方式都为processing为 daily和 fxFee为 monthly,
        # -----------------
        settle_currency = "SGD"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": "CNY",
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "daily",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "accumulation"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        trans_currency = "USD"
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("wop", trans_currency, settle_currency)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # ------------
        # 计费13测试 测试计费方式都为processing为 monthly fxFee为 daily,
        # -----------------
        trans_currency = "CNY"
        settle_currency = "SGD"
        wop_settle_currency = "USD"
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": wop_settle_currency,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "daily",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.wopSettleCurrency": "SGD",
                                           "settleInfo.settleCurrency": "SGD",
                                           "trans.wopConverterCurrencyFlag": True,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("wop", trans_currency, wop_settle_currency)
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.wop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

    def wop_evonet_fileinit_calc_refund_calc(self):
        # wop侧 且是evonet出文件时的 退款的计费
        # 退款类的计费，包含当日和隔日
        # 当天部分退款的interchangfee的计算
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.refund_trans_list(wopid, mopid)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        # 退款计费1
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 触发流水导入
        settle_currency = "CNY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.tyo_evosettle_db.update_many("transSettle.wop",
                                          {"trans.wopID": wopid},
                                          {"trans.wopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "settleFlag": True,
                                           "blendType": "success",
                                           })
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        # 退款一半的interchageFee的校验
        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid, )
        # ----------------------------
        # 退款计费2 interchangFee #全款退款
        # 触发流水导入
        settle_currency = "JPY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        self.tyo_evosettle_db.update_many("transSettle.wop",
                                          {"trans.wopID": wopid},
                                          {"trans.transAmount": 2233.33,
                                           "trans.wopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "settleFlag": True,
                                           "blendType": "success"
                                           })
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid, )
        # ----------------------------------
        # 退款计费3     隔日部分退款 interchangfee的计费
        settle_currency = "CNY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 直接将cpm,mpm的交易的日期切换为当天，Refund交易切换为第二天，然后触发计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency, })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        interchange_amount = 33.33
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment", ]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "settleFlag": True, "clearFlag": True, "blendType": "success",
                                           "feeFlag": True,
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           })
        #
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": "Refund"},
                                          {"settleFlag": True, "blendType": "success", })
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid, )
        # -----------------------------------
        # 退款计费3     隔日全款退款 interchangfee的计费
        settle_currency = "CNY"

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 直接将cpm,mpm的交易的日期切换为当天，Refund交易切换为第二天，然后触发计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency, })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        interchange_amount = 33.33
        trans_amount = 233.33

        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment", ]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "settleFlag": True, "clearFlag": True, "blendType": "success",
                                           "feeFlag": True,
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           "trans.transAmount": trans_amount
                                           })
        #
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": "Refund"},
                                          {"settleFlag": True, "blendType": "success",
                                           "trans.transAmount": trans_amount})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid, )

    def wop_wop_fileinit_calc_refund_calc(self):
        # wop侧 且是wop出文件时的 退款的计费
        # 退款类的计费，包含当日和隔日
        # 当天部分退款的interchangfee的计算
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.refund_trans_list(wopid, mopid)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        # 退款计费1;部分退款
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 触发流水导入
        settle_currency = "CNY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        interchange_amount = 33.33
        self.tyo_evosettle_db.update_many("transSettle.wop",
                                          {"trans.wopID": wopid},
                                          {"trans.wopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "settleFlag": True,
                                           "blendType": "success",
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           })
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {"trans.wopID": wopid})
        for service in trans_settle_data:
            assert service["settleInfo"]["interchangeFee"] == interchange_amount
        # ----------------------------------
        # 退款计费2     隔日部分退款 interchangfee的计费，勾兑是什么值，计费时，intechangeFee就是什么值
        settle_currency = "CNY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 直接将cpm,mpm的交易的日期切换为当天，Refund交易切换为第二天，然后触发计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency, })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        interchange_amount = 33.33
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment", ]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "settleFlag": True, "clearFlag": True, "blendType": "success",
                                           "feeFlag": True,
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           })
        #
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": "Refund"},
                                          {"settleFlag": True, "blendType": "success",
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           })
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {"trans.wopID": wopid})
        for service in trans_settle_data:
            assert service["settleInfo"]["interchangeFee"] == interchange_amount

    def wop_calc_assert_lack_settlement_settle_currency(self):
        # 模式二和模式四，模式一用不到,；直清模式用不到
        # 校验 settlement或者settlecurrency不存在时的计费或者都不存在的时候的计费
        for delete_data in ["wopSettleAmount", ]:  # "wopSettleCurrency"
            wopid = self.task_func.generate_wopid()
            mopid = self.task_func.generate_mopid()
            data = self.refund_trans_list(wopid, mopid)
            for i in data[0]:
                i.pop(delete_data)
            # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
            # 数据插入到trans  表
            self.tyo_evosettle_db.insert_many("trans", data[0])

            # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
            # 退款计费1
            self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                    "monthly", str(random.randint(100000, 9900000)), "sgp")
            # 触发流水导入
            settle_currency = "CNY"
            self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                          {"settleCurrency": settle_currency,
                                           "transProcessingFeeCollectionMethod": "monthly",
                                           "transProcessingFeeCalculatedMethod": "single",
                                           "fxProcessingFeeCollectionMethod": "monthly",
                                           "fxProcessingFeeCalculatedMethod": "single"
                                           })

            self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                          {"settleInfo.settleCurrency": settle_currency,
                                           })
            self.tyo_evosettle_db.update_many('trans', {'wopID': wopid}, {'wopSettleCurrency': settle_currency})
            # 流水导入,
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                              {"blendType": "success", "settleFlag": True})
            # 这时cpm,mpm,refund 已经计费结束，退款的是以交易金额计算也是0
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
            # 校验字段状态
            trans_sett_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                             {"trans.wopID": wopid, })
            # 校验正向交易缺少wopsettleamtount或者wopsettlecurrency;及反向交易找不到正向交易时的feeFlag 和 clearFlag 的判断
            for data in trans_sett_data:
                assert data["feeFlag"] == True
                assert data["clearFlag"] == False
            # 校验  settleFuncLog  的状态
            assert self.tyo_evosettle_db.get_one("settleFuncLog", {"wopID": wopid,
                                                                   "function": self.common_name.wop_trans_calc})[
                       "result"] == "success"
            # ----------------------------------------

            # 找的到原交易，但是反向交易缺少wopSettleamount和wopsettlecurrency字段时，feeFlag的判断
            self.tyo_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"wopID": wopid})
            self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                              {"trans.wopID": wopid, "trans.transType": {
                                                  "$in": ["MPM Payment", "CPM Payment"]}},
                                              {"feeFlag": True, "clearFlag": True, "settleFlag": True,
                                               "settleDate": str(int(self.sett_date) - 1)})
            self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
            trans_sett_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                             {"trans.wopID": wopid, "trans.transType": "Refund"})
            # 校验正向交易缺少 wopsettleamtount或者 wopsettlecurrency;及反向交易找不到正向交易时的feeFlag判断
            for data in trans_sett_data:
                assert data["feeFlag"] == True
                assert data["clearFlag"] == False
            # 校验  settleFuncLog  的状态
            assert self.tyo_evosettle_db.get_one("settleFuncLog", {"wopID": wopid,
                                                                   "function": self.common_name.wop_trans_calc})[
                       "result"] == "success"

    def wop_evonet_mode_calc_evonet_rebate(self):
        # 只有模式四；即model为evonet，fileinit为evonet才会计算 rebate
        # 正向rebate和负向rebate计费，包含当日和隔日
        # 当天部分退款的interchangfee的计算
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.refund_trans_list(wopid, mopid)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount 和 wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        # 退款计费1
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 触发流水导入
        settle_currency = "CNY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency,
                                           })
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"blendType": "success", "settleFlag": True})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])

        # 退款一半的interchageFee的校验
        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid)
        # 正向交易额rebate 校验
        self.task_func.cpm_mpm_rebate_fee_assert(wopid, mopid)
        # refund交易   rebate的校验
        self.task_func.refund_rebate_fee_assert(wopid, )
        # refund交易的rebate
        # ----------------------------
        # 退款计费2 interchangFee #全款退款
        # 触发流水导入

        settle_currency = "JPY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"transAmount": 2300,
                                           "wopSettleCurrency": settle_currency,
                                           })
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop, {"trans.wopID": wopid},
                                          {"blendType": "success", "settleFlag": True})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])

        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid)
        # 正向交易额rebate 校验
        self.task_func.cpm_mpm_rebate_fee_assert(wopid, mopid)
        # refund交易   rebate的校验
        self.task_func.refund_rebate_fee_assert(wopid, )

        # ----------------------------------
        # 退款计费3     隔日退款 interchangfee的计费
        settle_currency = "CNY"
        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency, })
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        # 流水导入
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        interchange_amount = 33.33
        rebate_amount = 33.33
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment"]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "blendType": "success", "settleFlag": True,
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           "settleInfo.rebate": rebate_amount,
                                           "settleInfo.rebateRefund": rebate_amount, "feeFlag": True,
                                           "clearFlag": True})

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_wop,
                                          {"trans.wopID": wopid, "trans.transType": "Refund"},
                                          {"blendType": "success", "settleFlag": True})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        self.task_func.refund_interchange_fee_assert("wop", wopid, mopid)

        # refund交易   rebate的校验
        self.task_func.refund_rebate_fee_assert(wopid, )

    def mop_calc_custom_config(self):
        # 将计费的逻辑全部 assert
        # 直清模式一 wop侧计费
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费1
        # 修改交易状态,计费为日元到日元,且settleinfo.settlecurrency等于customizeconfig的settlecurrency
        # 修改wop 表中的币种和transSettle.wop表中的币种；
        # 每笔交易都计算 fxProcessFee
        sett_currency = "JPY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": sett_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        self.sgp_evosettle_db.update_many("transSettle.mop",
                                          {"trans.mopID": mopid},
                                          {"trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True,
                                           "blendType": "success", "settleFlag": True})
        # 交易流水导入和交易计费
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit, )
        # ______________________
        # 计费2;测试小数位,人民币到人民币，wop表的settlecurrency和customizeconfig 的settlecurrency 一致都是CNY
        # 修改交易状态,计费为人民币到人民币,且清算表 wop表settlecurrency 等于customizeconfig的settlecurrency等于CNY
        # 修改wop 表中的币种和transSettle.wop表中的币种；
        # 每笔交易都计算 fxProcessFee
        sett_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": sett_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {
                                              "trans.mopSettleCurrency": sett_currency,
                                              "settleInfo.settleCurrency": sett_currency,
                                              "trans.mopConverterCurrencyFlag": True,
                                              "blendType": "success", "settleFlag": True})
        # 交易流水导入和交易计费
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit, )
        # _______________________
        # 计费3,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,但是交易币种和清算币种一致，
        # 用交易币CNY>>和清算币种一致
        sett_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": "JPY",
                                           "trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit, )

    def mop_calc_three_currency(self):
        # 三种币种都不一致的情况
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费4,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 JPY  转换到CNY，需要乘以（1+mccr）  才能算出手续费
        trans_currency = "JPY"
        sett_currency = "USD"
        mop_settle_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_currency,
                                       })
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.sgp_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"mopSettleCurrency": sett_currency, })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("mop", trans_currency, mop_settle_currency)
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

    def mop_calc_fee_type_single_accumulation(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费6 收费方式为 transProcessingFeeCalculatedMethod": "accumulation",fxProcessingFeeCollectionMethod：“accumulation”
        # transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 CNY  转换到JPY，需要乘以（1+mccr）  才能算出手续费
        sett_currency = "USD"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "accumulation",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "accumulation"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        trans_currency = "CNY"
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # -----------------
        # 计费7 收费方式为 transProcessingFeeCalculatedMethod": "single",fxProcessingFeeCollectionMethod：“accumulation”
        trans_currency = "CNY"
        sett_currency = "USD"
        mop_settle_currency = "JPY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "accumulation"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("mop", trans_currency, mop_settle_currency)
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)
        # ---------------------------------------
        # 计费8 收费方式为 transProcessingFeeCalculatedMethod": "accumulation",fxProcessingFeeCollectionMethod：“single”
        sett_currency = "USD"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": "JPY",
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "accumulation",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        trans_currency = "CNY"
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # 计费9 mccr测试，通用mccr;现在cutomizeconfig的交易币种只有 CNY和JPY ,造交易币种不是CNY，为USD就可以测试通用mccr 了
        sett_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": sett_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        trans_currency = "USD"
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": sett_currency,
                                           "settleInfo.settleCurrency": sett_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

    def mop_calc_daily_single(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费10测试 wopConverterCurrencyFlag为False
        # -----------------
        trans_currency = "USD"
        settle_currency = "SGD"
        mop_settle_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.mopConverterCurrencyFlag": False, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("mop", trans_currency, mop_settle_currency)
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)
        # --------------------------
        # 计费12测试 测试计费方式都为daily,
        # -----------------
        trans_currency = "USD"
        settle_currency = "SGD"
        mop_settle_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "daily",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "daily",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.mopConverterCurrencyFlag": False, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("mop", trans_currency, mop_settle_currency)
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)
        # 计费13测试 测试计费方式都为processing为 daily和 fxFee为 monthly,
        # -----------------
        settle_currency = "SGD"
        trans_currency = "USD"
        mop_settle_currency = "CNY"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "daily",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "accumulation"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("mop", trans_currency, mop_settle_currency)
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

        # ------------
        # 计费13测试 测试计费方式都为processing为 monthly fxFee为 daily,
        # -----------------
        trans_currency = "CNY"
        settle_currency = "SGD"
        mop_settle_currency = "USD"
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_currency,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "daily",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid},
                                          {"trans.transCurrency": trans_currency,
                                           "trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "trans.mopConverterCurrencyFlag": True, "blendType": "success",
                                           "settleFlag": True})
        # 交易流水导入和交易计费
        self.task_func.fx_rate_set("mop", trans_currency, mop_settle_currency)
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.mop_get_calc_fee_assert(wopid, mopid, self.sett_date, self.model, self.fileinit,
                                               trans_currency)

    def mop_evonet_fileinit_calc_refund_calc(self):
        # 退款类的计费，包含当日和隔日
        # 当天部分退款的interchangfee的计算
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.refund_trans_list(wopid, mopid)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        # 退款计费1
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 触发流水导入
        settle_currency = "CNY"
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many("transSettle.mop",
                                          {"trans.mopID": mopid},
                                          {"trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "blendType": "success",
                                           "settleFlag": True
                                           })
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        # 退款一半的interchageFee的校验
        self.task_func.refund_interchange_fee_assert("mop", wopid, mopid, )
        # ----------------------------
        # 退款计费2 interchangFee #全款退款
        # 触发流水导入

        settle_currency = "JPY"
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        self.sgp_evosettle_db.update_many("transSettle.mop",
                                          {"trans.mopID": mopid},
                                          {"trans.transAmount": 2233.33,
                                           "trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "blendType": "success",
                                           "settleFlag": True
                                           })
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.refund_interchange_fee_assert("mop", wopid, mopid, )
        # ----------------------------------
        # 退款计费3     隔日部分退款 interchangfee的计费
        settle_currency = "CNY"
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.sgp_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency, })
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment"]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "settleFlag": True, "blendType": "success",
                                           "settleInfo.interchangeFee": 33.33,
                                           "settleInfo.interchangeFeeRefund": 33.33})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.refund_interchange_fee_assert("mop", wopid, mopid, )
        # -----------------------------
        # 退款计费4 隔日全款退款 interchangfee的计费
        settle_currency = "CNY"
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.sgp_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency,
                                           "transAmount": 2233.33})
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment"]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "settleFlag": True, "blendType": "success",
                                           "settleInfo.interchangeFee": 33.33,
                                           "settleInfo.interchangeFeeRefund": 33.33})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        self.task_func.refund_interchange_fee_assert("mop", wopid, mopid, )

    def mop_wop_fileinit_calc_refund_calc(self):
        # wop出文件退款类的计费，包含当日和隔日
        # 当天部分退款的interchangfee的计算
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.refund_trans_list(wopid, mopid)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        # 退款计费1
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 触发流水导入
        settle_currency = "CNY"
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        interchange_amount = 33.33
        self.sgp_evosettle_db.update_many("transSettle.mop",
                                          {"trans.mopID": mopid},
                                          {"trans.mopSettleCurrency": settle_currency,
                                           "settleInfo.settleCurrency": settle_currency,
                                           "blendType": "success",
                                           "settleFlag": True,
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount
                                           })
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {"trans.wopID": wopid})
        for service in trans_settle_data:
            assert service["settleInfo"]["interchangeFee"] == interchange_amount
        # ----------------------------------
        # 退款计费2     隔日退款 interchangfee的计费
        settle_currency = "CNY"
        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": settle_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single"
                                       })
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.mopID": mopid})
        self.sgp_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"wopSettleCurrency": settle_currency,
                                           "transAmount": 2233.33})
        interchange_amount = 33.33
        # 流水导入
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])
        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid,
                                           "trans.transType": {"$in": ["CPM Payment", "MPM Payment"]}},
                                          {"settleDate": str(int(self.sett_date) - 1),
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount,
                                           "settleFlag": True, "blendType": "success", "clearFlag": True,
                                           "feeFlag": True})

        self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.mopID": mopid,
                                           "trans.transType": "Refund"},
                                          {"settleFlag": True, "blendType": "success",
                                           "settleInfo.interchangeFee": interchange_amount,
                                           "settleInfo.interchangeFeeRefund": interchange_amount})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {"trans.wopID": wopid})
        for service in trans_settle_data:
            assert service["settleInfo"]["interchangeFee"] == interchange_amount

    def mop_calc_assert_lack_settlement_settle_currency(self):
        # 模式二和模式四，模式一用不到
        # 校验 settlement或者settlecurrency不存在时的计费或者都不存在的时候的计费
        # 当天部分退款的interchangfee的计算
        for delete_data in ["mopSettleCurrency", "mopSettleAmount"]:
            wopid = self.task_func.generate_wopid()
            mopid = self.task_func.generate_mopid()
            data = self.refund_trans_list(wopid, mopid)
            for i in data[0]:
                i.pop(delete_data)
            # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
            # 数据插入到trans  表
            self.sgp_evosettle_db.insert_many("trans", data[0])

            # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
            self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                    "monthly", str(random.randint(100000, 9900000)), "sgp")
            # 触发流水导入
            settle_currency = "CNY"
            self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                          {"settleCurrency": settle_currency,
                                           "transProcessingFeeCollectionMethod": "monthly",
                                           "transProcessingFeeCalculatedMethod": "single",
                                           "fxProcessingFeeCollectionMethod": "monthly",
                                           "fxProcessingFeeCalculatedMethod": "single"
                                           })

            self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                          {"settleInfo.settleCurrency": settle_currency,
                                           })

            self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                               {"trans.mopID": mopid})
            # 流水导入,
            self.mop_settle_task(mopid, [wopid],
                                 [self.common_name.mop_trans_import])

            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop, {"trans.mopID": mopid},
                                              {"blendType": "success", "settleFlag": True})

            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])

            # ------------------值得判断
            # 校验字段状态
            trans_sett_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                             {"trans.mopID": mopid, })
            # 校验正向交易缺少wopsettleamtount或者wopsettlecurrency;及反向交易找不到正向交易时的feeFlag和 clearFlag 的判断
            for data in trans_sett_data:
                assert data["feeFlag"] == True
                assert data["clearFlag"] == False
            # 校验  settleFuncLog  的状态
            assert self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"mopID": mopid,
                                                                                   "function": self.common_name.mop_trans_calc})[
                       "result"] == "success"
            # ----------------------------------------
            # 找的到原交易，但是反向交易缺少wopSettleamount和wopsettlecurrency字段时，feeFlag的判断
            self.sgp_evosettle_db.delete_manys(self.common_name.settle_funcLog, {"mopID": mopid})
            self.sgp_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                              {"trans.mopID": mopid, "trans.transType": {
                                                  "$in": ["MPM Payment", "CPM Payment"]}},
                                              {"feeFlag": True, "clearFlag": True, "settleFlag": True,
                                               "settleDate": str(
                                                   int(self.sett_date) - 1)})
            self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
            trans_sett_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                             {"trans.mopID": mopid, "trans.transType": "Refund"})
            # 校验正向交易缺少wopsettleamtount或者wopsettlecurrency;及反向交易找不到正向交易时的feeFlag判断
            for data in trans_sett_data:
                assert data["feeFlag"] == True
                assert data["clearFlag"] == False
            # 校验  settleFuncLog  的状态
            assert self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"mopID": mopid,
                                                                                   "function": self.common_name.mop_trans_calc})[
                       "result"] == "success"

    def wop_settle_dual_task_assert(self):
        # 清分任务生成的校验及cutofftime的校验
        for model in [self.common_name.bilateral, self.common_name.evonet]:
            if model == self.common_name.bilateral:
                fileinits = ["wop", 'evonet', "mop"]
            if model == "evonet":
                fileinits = ["evonet"]
            for fileinit in fileinits:
                wopid = self.task_func.generate_wopid()
                mopid1 = self.task_func.generate_mopid()
                mopid2 = self.task_func.generate_mopid()
                self.tyo_evosettle_db.delete_manys(self.common_name.base_task,
                                                   {"taskName": "RegisterSettleTask"}),
                self.tyo_evosettle_db.insert_one(self.common_name.base_task,
                                                 {"taskName": "RegisterSettleTask",
                                                  "taskCron": "@every 2s",
                                                  "lockType": "0",
                                                  "function": "RegisterSettleTask",
                                                  "preferHost": "jp3evonet-Testing",
                                                  "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                                      days=-10),
                                                  })

                time.sleep(2)
                # 修改baseTsk中的配置
                if model == self.common_name.bilateral:
                    self.db_operations.create_single_config(wopid, mopid1, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    self.tyo_config_db.delete_manys("wop", {"baseInfo.wopID": wopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid, mopid2, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    cutoff_time = "02:00+0800"
                    self.tyo_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                                                   {"cutoffTime": cutoff_time})

                    time.sleep(12)
                    # 如果是evonet模式
                    for mopid in [mopid1, mopid2]:
                        # 默认fileinit为 wop
                        steps = [int(1), int(2), int(3), int(4)]
                    if fileinit == "evonet":
                        steps = [int(1), int(2)]
                    if fileinit == "mop":
                        steps = [int(1), int(2), int(3)]
                    for step in steps:
                        custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                    {"ownerID": wopid, "partnerID": mopid,
                                                                     "step": step})
                    assert custom_data["ownerID"] == wopid
                    assert custom_data["ownerType"] == "wop"
                    assert custom_data["partnerType"] == "mop"
                    assert custom_data["partnerID"] == mopid
                    assert custom_data["parameters"]["model"] == model
                    assert custom_data["parameters"]["fileInitiator"] == fileinit
                    assert custom_data["parameters"]["nodeType"] == "dual"
                    assert custom_data["parameters"]["cutoffTime"] == cutoff_time
                    assert custom_data["parameters"]["includeMOPIDs"] == [mopid]
                    if fileinit == "evonet":
                        if step == int(1):
                            assert custom_data["parameters"]["functions"] == ["WopTransImport",
                                                                              "WopSelfSettle",
                                                                              "WopTransFeeCalculate",
                                                                              "WopSettleFileGenerate"]
                        if step == int(2):
                            assert custom_data["parameters"]["functions"] == ["WopFeeFileGenerate"]
                    # 模式二没有生月报

                    if fileinit == "wop":
                        if step == int(1):
                            assert custom_data["parameters"]["functions"] == ["WopTransImport"]
                        if step == int(2):
                            assert custom_data["parameters"]["functions"] == ["WopSettleFileDownload",
                                                                              "WopSettleFileDistribute",
                                                                              "WopSettleFileResolve"]
                        if step == int(3):
                            assert custom_data["parameters"]["functions"] == ["WopTransReconcile",
                                                                              "WopTransFeeCalculate",
                                                                              "WopSettleFileGenerate"]
                        if step == int(4):
                            assert custom_data["parameters"]["functions"] == ["WopFeeFileGenerate"]

                    if fileinit == "mop":
                        if step == int(1):
                            assert custom_data["parameters"]["functions"] == ["WopTransImport"]
                        if step == int(2):
                            assert custom_data["parameters"]["functions"] == ["WopSettleFileDownload",
                                                                              "WopSettleFileResolve",
                                                                              "WopTransReconcile",
                                                                              "WopTransFeeCalculate",
                                                                              "WopSettleFileGenerate"]
                        if step == int(3):
                            assert custom_data["parameters"]["functions"] == ["WopFeeFileGenerate"]

                if model == self.common_name.evonet:
                    time.sleep(2)
                    self.db_operations.create_single_config(wopid, mopid1, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")

                    self.tyo_config_db.delete_manys("wop", {"baseInfo.wopID": wopid})
                    self.tyo_evosettle_db.delete_manys("wop", {"baseInfo.wopID": wopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid, mopid2, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    wop_cutoff_time = "07:00+0800"
                    self.tyo_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                                   {"settleInfo.cutoffTime": wop_cutoff_time})

                    time.sleep(10)
                    steps = [int(1), int(2)]
                    for step in steps:
                        custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                    {"ownerID": wopid, "step": step})
                    assert custom_data["ownerID"] == wopid
                    assert custom_data["ownerType"] == "wop"
                    assert custom_data["partnerType"] == "evonet"
                    assert custom_data["partnerID"] == "EVONET"

                    assert custom_data["parameters"]["model"] == model
                    assert custom_data["parameters"]["fileInitiator"] == fileinit
                    assert custom_data["parameters"]["nodeType"] == "dual"
                    assert custom_data["parameters"]["cutoffTime"] == wop_cutoff_time
                    assert mopid1 in custom_data["parameters"]["includeMOPIDs"]
                    assert mopid2 in custom_data["parameters"]["includeMOPIDs"]
                    if fileinit == "evonet":
                        if step == int(1):
                            assert custom_data["parameters"]["functions"] == ["WopTransImport",
                                                                              "WopSelfSettle",
                                                                              "WopTransFeeCalculate",
                                                                              "WopSettleFileGenerate"]
                    if step == int(2):
                        assert custom_data["parameters"]["functions"] == [self.common_name.wop_fee_file]
                self.tyo_evosettle_db.update_many(self.common_name.base_task,
                                                  {"taskName": "RegisterSettleTask"},
                                                  {"lockType": "222", "taskCron": "@every 1s"})

    def mop_settle_dual_task_assert(self):
        # 清分任务生成的校验及cutofftime的校验
        for model in [self.common_name.bilateral, self.common_name.evonet]:
            if model == self.common_name.bilateral:
                fileinits = ["wop", 'evonet', "mop"]
            if model == "evonet":
                fileinits = ["evonet"]
            for fileinit in fileinits:
                mopid = self.task_func.generate_mopid()
                wopid1 = self.task_func.generate_wopid()
                wopid2 = self.task_func.generate_wopid()
                # 修改baseTsk中的配置
                self.sgp_evosettle_db.delete_manys(self.common_name.base_task,
                                                   {"taskName": "RegisterSettleTask"}),
                self.sgp_evosettle_db.insert_one(self.common_name.base_task,
                                                 {"taskName": "RegisterSettleTask",
                                                  "taskCron": "@every 2s",
                                                  "lockType": "0",
                                                  "function": "RegisterSettleTask",
                                                  "preferHost": "sg1evonet-Testing",
                                                  "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                                      days=-10),
                                                  })
                time.sleep(2)
                if model == self.common_name.bilateral:

                    self.db_operations.create_single_config(wopid1, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    self.sgp_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid2, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    cutoff_time = "02:00+0800"
                    self.sgp_config_db.update_many(self.common_name.custom_config, {"mopID": mopid},
                                                   {"cutoffTime": cutoff_time})
                    time.sleep(10)
                    # 如果是evonet模式
                    for wopid in [wopid1, wopid2]:
                        # 模式模式一的step
                        steps = [int(1), int(2), int(3)]
                        if fileinit == "evonet":
                            steps = [int(1), int(2), int(3)]
                        if fileinit == "mop":
                            steps = [int(1)]
                        for step in steps:
                            custom_data = self.sgp_evosettle_db.get_one(self.common_name.settle_task,
                                                                        {"ownerID": mopid, "partnerID": wopid,
                                                                         "step": step})
                            assert custom_data["ownerID"] == mopid
                            assert custom_data["ownerType"] == "mop"
                            assert custom_data["partnerType"] == "wop"
                            assert custom_data["partnerID"] == wopid
                            assert custom_data["parameters"]["model"] == model
                            assert custom_data["parameters"]["fileInitiator"] == fileinit
                            assert custom_data["parameters"]["nodeType"] == "dual"
                            assert custom_data["parameters"]["cutoffTime"] == cutoff_time
                            assert custom_data["parameters"]["includeWOPIDs"] == [wopid]
                            if fileinit == "evonet":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == [self.common_name.mop_trans_import]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == ["MopSettleFileDownload",
                                                                                      "MopSettleFileResolve",
                                                                                      "MopTransReconcile",
                                                                                      "MopTransFeeCalculate",
                                                                                      "MopSettleFileGenerate"]
                                if step == int(3):
                                    assert custom_data["parameters"]["functions"] == [self.common_name.mop_fee_file]
                            # 模式二没有生月报

                            if fileinit == "wop":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["MopTransImport"]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == ["MopSettleFileDownload",
                                                                                      "MopSettleFileResolve",
                                                                                      "MopTransReconcile",
                                                                                      "MopTransFeeCalculate",
                                                                                      "MopSettleFileGenerate"]
                                if step == int(3):
                                    assert custom_data["parameters"]["functions"] == ["MopFeeFileGenerate"]

                            if fileinit == "mop":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["MopSettleFileDownload"]

                if model == self.common_name.evonet:
                    self.db_operations.create_single_config(wopid1, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    self.sgp_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid2, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    mop_cutoff_time = "07:00+0800"
                    time.sleep(1)
                    self.sgp_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                                   {"settleInfo.cutoffTime": mop_cutoff_time})
                    # 这个时间6s比较合适，5s会出现任务未生成的情况
                    time.sleep(12)
                    steps = [int(1), int(2), int(3)]
                    for step in steps:
                        custom_data = self.sgp_evosettle_db.get_one(self.common_name.settle_task,
                                                                    {"ownerID": mopid, "step": step})
                        if step == int(3):
                            custom_data = self.sgp_evosettle_db.get_one(self.common_name.settle_task,
                                                                        {"ownerID": mopid, "taskCron": "@hourly"})

                        assert custom_data["ownerID"] == mopid
                        assert custom_data["ownerType"] == "mop"
                        assert custom_data["partnerType"] == "evonet"
                        assert custom_data["partnerID"] == "EVONET"
                        if step == int(3):
                            assert custom_data["parameters"]["cutoffTime"] == "00:00+0800"
                        else:
                            assert custom_data["parameters"]["model"] == model
                            assert custom_data["parameters"]["fileInitiator"] == fileinit
                            assert custom_data["parameters"]["nodeType"] == "dual"
                            assert custom_data["parameters"]["cutoffTime"] == mop_cutoff_time
                        assert wopid1 in custom_data["parameters"]["includeWOPIDs"]
                        assert wopid2 in custom_data["parameters"]["includeWOPIDs"]
                        if fileinit == "evonet":
                            if step == int(1):
                                assert custom_data["parameters"]["functions"] == ["MopTransImport",
                                                                                  "MopSelfSettle",
                                                                                  "MopTransFeeCalculate",
                                                                                  "MopSettleFileGenerate"]
                            if step == int(2):
                                assert custom_data["parameters"]["functions"] == [self.common_name.mop_fee_file]

                            if step == int(3):
                                assert custom_data["parameters"]["functions"] == [self.common_name.mop_file_resolve,
                                                                                  self.common_name.mop_refund_trans_send,
                                                                                  self.common_name.mop_refund_file_generate]
                self.sgp_evosettle_db.update_many(self.common_name.base_task,
                                                  {"taskName": "RegisterSettleTask"},
                                                  {"lockType": "222", "taskCron": "@every 1s"})

    def wop_settle_single_task_assert(self):
        # 单节点任务的校验
        # 清分任务生成的校验及cutofftime的校验
        for model in [self.common_name.bilateral, self.common_name.evonet]:
            if model == self.common_name.bilateral:
                fileinits = ["wop", 'evonet', "mop"]
            if model == "evonet":
                fileinits = ["evonet"]
            for fileinit in fileinits:
                wopid = self.task_func.generate_wopid()
                mopid1 = self.task_func.generate_mopid()
                mopid2 = self.task_func.generate_mopid()
                self.tyo_evosettle_db.delete_manys(self.common_name.base_task,
                                                   {"taskName": "RegisterSettleTask"})
                self.tyo_evosettle_db.insert_one(self.common_name.base_task,
                                                 {"taskName": "RegisterSettleTask",
                                                  "taskCron": "@every 2s",
                                                  "lockType": "0",
                                                  "function": "RegisterSettleTask",
                                                  "preferHost": "jp3evonet-Testing",
                                                  "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                                      days=-10),
                                                  })
                time.sleep(2)
                # 修改baseTsk中的配置
                if model == self.common_name.bilateral:
                    self.db_operations.create_single_config(wopid, mopid1, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    self.tyo_config_db.delete_manys("wop", {"baseInfo.wopID": wopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid, mopid2, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")

                    # 修改 cutoff_time
                    cutoff_time = "02:00+0800"
                    self.tyo_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                                                   {"cutoffTime": cutoff_time})

                    # 修改为单节点
                    self.tyo_config_db.update_many("mop", {"baseInfo.mopID": {"$in": [mopid1, mopid2]}},
                                                   {"baseInfo.nodeID": "tyo"})

                    time.sleep(12)
                    # 如果是evonet模式
                    for mopid in [mopid1, mopid2]:
                        # 默认fileinit为 wop
                        steps = [int(1), int(2), int(3), int(4)]
                        if fileinit == "evonet":
                            steps = [int(1), int(2)]
                        if fileinit == "mop":
                            steps = [int(1), int(2), int(3)]
                        for step in steps:
                            custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                        {"ownerID": wopid, "partnerID": mopid,
                                                                         "step": step})
                            assert custom_data["ownerID"] == wopid
                            assert custom_data["ownerType"] == "wop"
                            assert custom_data["partnerType"] == "mop"
                            assert custom_data["partnerID"] == mopid
                            assert custom_data["parameters"]["model"] == model
                            assert custom_data["parameters"]["fileInitiator"] == fileinit
                            assert custom_data["parameters"]["nodeType"] == "single"
                            assert custom_data["parameters"]["cutoffTime"] == cutoff_time
                            assert custom_data["parameters"]["includeMOPIDs"] == [mopid]
                            if fileinit == "evonet":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["WopTransImport",
                                                                                      "WopSelfSettle",
                                                                                      "WopTransFeeCalculate",
                                                                                      "WopSettleFileGenerate"]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == ["WopFeeFileGenerate"]
                            # 模式二没有生月报

                            if fileinit == "wop":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["WopTransImport"]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == ["WopSettleFileDownload",
                                                                                      "WopSettleFileDistribute",
                                                                                      "WopSettleFileResolve"]
                                if step == int(3):
                                    assert custom_data["parameters"]["functions"] == ["WopTransReconcile",
                                                                                      "WopTransFeeCalculate",
                                                                                      "WopSettleFileGenerate"]
                                if step == int(4):
                                    assert custom_data["parameters"]["functions"] == ["WopFeeFileGenerate"]
                            if fileinit == "mop":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["WopTransImport"]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == [
                                        "WopSettleFileResolve",
                                        "WopTransReconcile",
                                        "WopTransFeeCalculate",
                                        "WopSettleFileGenerate"]
                                if step == int(3):
                                    assert custom_data["parameters"]["functions"] == ["WopFeeFileGenerate"]

                if model == self.common_name.evonet:

                    time.sleep(2)
                    self.db_operations.create_single_config(wopid, mopid1, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")

                    self.tyo_config_db.delete_manys("wop", {"baseInfo.wopID": wopid})
                    self.tyo_evosettle_db.delete_manys("wop", {"baseInfo.wopID": wopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid, mopid2, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    wop_cutoff_time = "07:00+0800"
                    self.tyo_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                                   {"settleInfo.cutoffTime": wop_cutoff_time})
                    self.tyo_config_db.update_many("mop", {"baseInfo.mopID": {"$in": [mopid1, mopid2]}},
                                                   {"baseInfo.nodeID": "tyo"})

                    time.sleep(12)
                    steps = [int(1), int(2)]
                    for step in steps:
                        custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                    {"ownerID": wopid, "step": step})
                        assert custom_data["ownerID"] == wopid
                        assert custom_data["ownerType"] == "wop"
                        assert custom_data["partnerType"] == "evonet"
                        assert custom_data["partnerID"] == "EVONET"

                        assert custom_data["parameters"]["model"] == model
                        assert custom_data["parameters"]["fileInitiator"] == fileinit
                        assert custom_data["parameters"]["nodeType"] == "single"
                        assert custom_data["parameters"]["cutoffTime"] == wop_cutoff_time
                        assert mopid1 in custom_data["parameters"]["includeMOPIDs"]
                        assert mopid2 in custom_data["parameters"]["includeMOPIDs"]
                        if fileinit == "evonet":
                            if step == int(1):
                                assert custom_data["parameters"]["functions"] == ["WopTransImport",
                                                                                  "WopSelfSettle",
                                                                                  "WopTransFeeCalculate",
                                                                                  "WopSettleFileGenerate"]
                            if step == int(2):
                                assert custom_data["parameters"]["functions"] == [self.common_name.wop_fee_file]
                self.tyo_evosettle_db.update_many(self.common_name.base_task,
                                                  {"taskName": "RegisterSettleTask"},
                                                  {"lockType": "222", "taskCron": "@every 1s"})

    def mop_settle_single_task_assert(self):
        # 清分任务生成的校验及cutofftime的校验
        for model in [self.common_name.bilateral, self.common_name.evonet]:
            if model == self.common_name.bilateral:
                fileinits = ["wop", 'evonet', "mop"]
            if model == "evonet":
                fileinits = ["evonet"]
            for fileinit in fileinits:
                mopid = self.task_func.generate_mopid()
                wopid1 = self.task_func.generate_wopid()
                wopid2 = self.task_func.generate_wopid()
                # 修改baseTsk中的配置
                self.tyo_evosettle_db.delete_manys(self.common_name.base_task,
                                                   {"taskName": "RegisterSettleTask"}),
                self.tyo_evosettle_db.insert_one(self.common_name.base_task,
                                                 {"taskName": "RegisterSettleTask",
                                                  "taskCron": "@every 2s",
                                                  "lockType": "0",
                                                  "function": "RegisterSettleTask",
                                                  "preferHost": "jp3evonet-Testing",
                                                  "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                                      days=-10),
                                                  })
                time.sleep(2)
                if model == self.common_name.bilateral:

                    self.db_operations.create_single_config(wopid1, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid2, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    cutoff_time = "02:00+0800"
                    self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                                   {"baseInfo.nodeID": "tyo"})
                    self.tyo_config_db.update_many(self.common_name.custom_config, {"mopID": mopid},
                                                   {"cutoffTime": cutoff_time})

                    time.sleep(10)
                    # 如果是evonet模式
                    for wopid in [wopid1, wopid2]:
                        # 模式模式一的step
                        steps = [int(1), int(2), int(3)]
                        if fileinit == "evonet":
                            steps = [int(1), int(2), int(3)]
                        if fileinit == "mop":
                            steps = [int(1)]
                        for step in steps:
                            custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                        {"ownerID": mopid, "partnerID": wopid,
                                                                         "step": step})
                            assert custom_data["ownerID"] == mopid
                            assert custom_data["ownerType"] == "mop"
                            assert custom_data["partnerType"] == "wop"
                            assert custom_data["partnerID"] == wopid
                            assert custom_data["parameters"]["model"] == model
                            assert custom_data["parameters"]["fileInitiator"] == fileinit
                            assert custom_data["parameters"]["nodeType"] == "single"
                            assert custom_data["parameters"]["cutoffTime"] == cutoff_time
                            assert custom_data["parameters"]["includeWOPIDs"] == [wopid]
                            if fileinit == "evonet":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == [self.common_name.mop_trans_import]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == ["MopSettleFileResolve",
                                                                                      "MopTransReconcile",
                                                                                      "MopTransFeeCalculate",
                                                                                      "MopSettleFileGenerate"]

                                if step == int(3):
                                    assert custom_data["parameters"]["functions"] == [self.common_name.mop_fee_file]
                            # 模式二没有生月报

                            if fileinit == "wop":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["MopTransImport"]
                                if step == int(2):
                                    assert custom_data["parameters"]["functions"] == ["MopSettleFileResolve",
                                                                                      "MopTransReconcile",
                                                                                      "MopTransFeeCalculate",
                                                                                      "MopSettleFileGenerate"]

                                if step == int(3):
                                    assert custom_data["parameters"]["functions"] == ["MopFeeFileGenerate"]

                            if fileinit == "mop":
                                if step == int(1):
                                    assert custom_data["parameters"]["functions"] == ["MopSettleFileDownload"]
                if model == self.common_name.evonet:
                    self.db_operations.create_single_config(wopid1, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    self.tyo_config_db.delete_manys("mop", {"baseInfo.mopID": mopid})
                    # 创建配置 2
                    self.db_operations.create_single_config(wopid2, mopid, model, fileinit, "daily",
                                                            "daily", str(random.randint(100000, 9900000)), "sgp")
                    # 修改 cutoff_time
                    mop_cutoff_time = "07:00+0800"
                    time.sleep(1)
                    self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                                   {"settleInfo.cutoffTime": mop_cutoff_time})
                    self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                                   {"baseInfo.nodeID": "tyo"})

                    # 这个时间6s比较合适，5s会出现任务未生成的情况
                    time.sleep(12)

                    steps = [int(1), int(2), int(3)]
                    for step in steps:
                        custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                    {"ownerID": mopid, "step": step})
                        if step == int(3):
                            custom_data = self.tyo_evosettle_db.get_one(self.common_name.settle_task,
                                                                        {"ownerID": mopid, "taskCron": "@hourly"})
                        assert custom_data["ownerID"] == mopid
                        assert custom_data["ownerType"] == "mop"
                        assert custom_data["partnerType"] == "evonet"
                        assert custom_data["partnerID"] == "EVONET"
                        if step == int(3):
                            assert custom_data["parameters"]["cutoffTime"] == "00:00+0800"
                        else:
                            assert custom_data["parameters"]["model"] == model
                            assert custom_data["parameters"]["fileInitiator"] == fileinit
                            assert custom_data["parameters"]["nodeType"] == "single"
                            assert custom_data["parameters"]["cutoffTime"] == mop_cutoff_time
                        assert wopid1 in custom_data["parameters"]["includeWOPIDs"]
                        assert wopid2 in custom_data["parameters"]["includeWOPIDs"]
                        if fileinit == "evonet":
                            if step == int(1):
                                assert custom_data["parameters"]["functions"] == ["MopTransImport",
                                                                                  "MopSelfSettle",
                                                                                  "MopTransFeeCalculate",
                                                                                  "MopSettleFileGenerate"]
                            if step == int(2):
                                assert custom_data["parameters"]["functions"] == [self.common_name.mop_fee_file]
                            if step == int(3):
                                assert custom_data["parameters"]["functions"] == [self.common_name.mop_file_resolve,
                                                                                  self.common_name.mop_refund_trans_send,
                                                                                  self.common_name.mop_refund_file_generate]

                self.tyo_evosettle_db.update_many(self.common_name.base_task,
                                                  {"taskName": "RegisterSettleTask"},
                                                  {"lockType": "222", "taskCron": "@every 1s"})

    def settletask_update_assert(self):
        # 清分任务的cutoffTime的修改，并校验修改后的任务

        for model in [self.common_name.bilateral, self.common_name.evonet]:
            if model == self.common_name.bilateral:
                fileinits = ["wop", "evonet", "mop"]
            if model == "evonet":
                fileinits = ["evonet"]
            for fileinit in fileinits:
                wopid = self.task_func.generate_wopid()
                mopid = self.task_func.generate_mopid()
                self.tyo_evosettle_db.delete_manys(self.common_name.base_task,
                                                   {"taskName": "RegisterSettleTask"})
                self.tyo_evosettle_db.insert_one(self.common_name.base_task,
                                                 {"taskName": "RegisterSettleTask",
                                                  "taskCron": "@every 2s",
                                                  "lockType": "0",
                                                  "function": "RegisterSettleTask",
                                                  "preferHost": "jp3evonet-Testing",
                                                  "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                                      days=-10),
                                                  })
                self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                        "daily", str(random.randint(100000, 9900000)), "sgp")
                time.sleep(10)
                if model == self.common_name.bilateral:
                    cutoff_time = "11:11+0800"
                    self.tyo_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                                                   {"cutoffTime": cutoff_time, "version": int(2)})
                    time.sleep(10)
                    wop_settletask_data = self.tyo_evosettle_db.get_many(self.common_name.settle_task,
                                                                         {"ownerID": wopid})
                    mop_settletask_data = self.tyo_evosettle_db.get_many(self.common_name.settle_task,
                                                                         {"ownerID": mopid})
                    for data in wop_settletask_data:
                        assert data["parameters"]["cutoffTime"] == cutoff_time

                    for data in mop_settletask_data:
                        assert data["parameters"]["cutoffTime"] == cutoff_time
                if model == self.common_name.evonet:
                    wop_cutoff_time = "06:06+0800"
                    mop_cutoff_time = "07:07+0800"
                    # self.tyo_config_db.update_many(self.common_name.custom_config, {"wopID": wopid},
                    #                                {"cutoffTime": "09:09+0800", "version": int(2)})
                    self.tyo_config_db.update_many("wop", {"baseInfo.wopID": wopid},
                                                   {"settleInfo.cutoffTime": wop_cutoff_time, "version": int(2)})
                    self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid},
                                                   {"settleInfo.cutoffTime": mop_cutoff_time, "version": int(2)})
                    time.sleep(10)
                    wop_settletask_data = self.tyo_evosettle_db.get_many(self.common_name.settle_task,
                                                                         {"ownerID": wopid})
                    mop_settletask_data = self.tyo_evosettle_db.get_many(self.common_name.settle_task,
                                                                         {"ownerID": mopid})
                    for data in wop_settletask_data:
                        assert data["parameters"]["cutoffTime"] == wop_cutoff_time

                    for data in mop_settletask_data:
                        assert data["parameters"]["cutoffTime"] == mop_cutoff_time

    def evonet_model_evonet_fileinit_process(self):
        # k8s，加settleFunclog测试
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        model = "evonet"
        fileinit = "evonet"
        # 创建配置1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        data = self.case_data.trans_list(wopid, mopid, self.sett_date, "evonet")
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 双节点插入到tyo节点trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 双节点
        functions = [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                     self.common_name.wop_trans_calc, self.common_name.wop_generate_file]
        for function in functions:
            self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                               [function],
                                               model, fileinit)
            result = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                     "function": function})["result"]

            assert result == "success"
        functions = [self.common_name.mop_trans_import, self.common_name.mop_self_sett,
                     self.common_name.mop_trans_calc, self.common_name.mop_generate_file]
        for function in functions:
            self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], self.sett_date,
                                               [function],
                                               model, fileinit)
            result = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                     "function": function})["result"]

            assert result == "success"

        # --单节点
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        # 创建配置1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        data = self.case_data.trans_list(wopid, mopid, self.sett_date, "evonet")
        self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid}, {"baseInfo.nodeID": "tyo", "version": int(2)})
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                                            self.common_name.wop_trans_calc, self.common_name.wop_generate_file],
                                           model, fileinit)
        # 单节点mop侧
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "mop", mopid, [wopid], self.sett_date,
                                           [self.common_name.mop_trans_import, self.common_name.mop_self_sett,
                                            self.common_name.mop_trans_calc, self.common_name.mop_generate_file],
                                           model, fileinit)

    def bilateral_model_evonet_fileinit_process(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        model = "bilateral"
        fileinit = "evonet"
        # 创建配置1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        data = self.case_data.trans_list(wopid, mopid, self.sett_date, model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 双节点插入到tyo节点trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 双节点
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                                            self.common_name.wop_trans_calc, self.common_name.wop_generate_file],
                                           model, fileinit)
        functions = [self.common_name.mop_trans_import,
                     self.common_name.mop_settle_file_download,
                     self.common_name.mop_settle_file_resolve,
                     self.common_name.mop_trans_reconcile,
                     self.common_name.mop_trans_calc, self.common_name.mop_generate_file]
        for function in functions:
            self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], self.sett_date,
                                               [function],
                                               model, fileinit)
            result = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                     "function": function})["result"]

            assert result == "success"

        # ---------------单节点
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        # 创建配置1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        data = self.case_data.trans_list(wopid, mopid, self.sett_date, model)
        self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid}, {"baseInfo.nodeID": "tyo", "version": int(2)})
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_trans_import, self.common_name.wop_self_sett,
                                            self.common_name.wop_trans_calc, self.common_name.wop_generate_file],
                                           model, fileinit)
        # 单节点mop侧
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "mop", mopid, [wopid], self.sett_date,
                                           [self.common_name.mop_trans_import, self.common_name.mop_settle_file_resolve,
                                            self.common_name.mop_trans_reconcile,
                                            self.common_name.mop_trans_calc, self.common_name.mop_generate_file],
                                           model, fileinit)

    def bilateral_model_wop_fileinit_process(self):
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        model = "bilateral"
        fileinit = "wop"
        # 创建配置1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")

        data = self.case_data.trans_list(wopid, mopid, self.sett_date, model)
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        # 双节点插入到tyo节点trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.sgp_evosettle_db.insert_many("trans", data[0])
        # 双节点
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_trans_import],
                                           model, fileinit)

        sftp_data = self.case_data.wop_sftp_data(self.tyo_ip, self.tyo_user, wopid,
                                                 self.evosettle_config.get_ini("wop_sftp_data_key"))
        # sftp_info  插入配置
        self.tyo_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.task_func.wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.tyo_ip, self.tyo_user, server_cmd)
        # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path + file_name,
                                         file_name)
        functions = [self.common_name.wop_settle_file_download,
                     self.common_name.wop_settle_file_resolve,
                     self.common_name.wop_trans_reconcile,
                     self.common_name.wop_trans_calc, self.common_name.wop_generate_file]
        for function in functions:
            self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                               [function],
                                               model, fileinit)
            result = self.tyo_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                     "function": function})["result"]

            assert result == "success"
        functions = [self.common_name.mop_trans_import,
                     self.common_name.mop_settle_file_download,
                     self.common_name.mop_settle_file_resolve,
                     self.common_name.mop_trans_reconcile,
                     self.common_name.mop_trans_calc, self.common_name.mop_generate_file]
        for function in functions:
            self.task_func.settle_task_request(self.sgp_func_url, "mop", mopid, [wopid], self.sett_date,
                                               [function],
                                               model, fileinit)
            result = self.sgp_evosettle_db.get_one(self.common_name.settle_funcLog, {"wopID": wopid,
                                                                                     "function": function})["result"]

            assert result == "success"

        # ---------------单节点
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        # 创建配置1
        self.db_operations.create_single_config(wopid, mopid, model, fileinit, "daily",
                                                "daily", str(random.randint(100000, 9900000)), "sgp")
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, model)
        self.tyo_config_db.update_many("mop", {"baseInfo.mopID": mopid}, {"baseInfo.nodeID": "tyo", "version": int(2)})
        # 插入数据，插入数据的时候，造了，wop侧和mop侧 的 wopsettleamount和wopsettlecurrency 不一致的情况
        self.tyo_evosettle_db.insert_many("trans", data[0])
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_trans_import],
                                           model, fileinit)

        sftp_data = self.case_data.wop_sftp_data(self.tyo_ip, self.tyo_user, wopid,
                                                 self.evosettle_config.get_ini("wop_sftp_data_key"))
        # sftp_info  插入配置
        self.tyo_evosettle_db.insert_one("sftpInfo", sftp_data)
        # wop系统文件下载;这个文件是自己造的，单独写一个方法生文件并将文件上传至服务器
        file_name = mopid + "-WOPFile-Details-" + wopid + "-" + self.sett_date + "-001.csv"
        self.task_func.wop_system_file_generate(wopid, mopid, self.sett_date, file_name)
        remote_path = "/home/webapp/test/" + wopid + "/" + self.sett_date + "/"
        private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("tyo_key"))
        server_cmd = "mkdir -p " + remote_path
        self.sftp_func.run_cmd(private_key, self.tyo_ip, self.tyo_user, server_cmd)
        # 上传文件
        self.sftp_func.ssh_download_file("put", private_key, self.tyo_ip, self.tyo_user, remote_path + file_name,
                                         file_name)

        self.task_func.settle_task_request(self.k8s_tyo_func_url, "wop", wopid, [mopid], self.sett_date,
                                           [self.common_name.wop_settle_file_download,
                                            self.common_name.wop_settle_file_resolve,
                                            self.common_name.wop_trans_reconcile,
                                            self.common_name.wop_trans_calc, self.common_name.wop_generate_file],
                                           model, fileinit)
        # 单节点mop侧
        self.task_func.settle_task_request(self.k8s_tyo_func_url, "mop", mopid, [wopid], self.sett_date,
                                           [self.common_name.mop_trans_import, self.common_name.mop_settle_file_resolve,
                                            self.common_name.mop_trans_reconcile,
                                            self.common_name.mop_trans_calc, self.common_name.mop_generate_file],
                                           model, fileinit)

    def all_sett_task_assert(self):
        # settleTask任务的校验
        # 模式一，二，四，银联模式四种模式的单双节点生成的settletask的校验
        self.wop_settle_single_task_assert()
        self.mop_settle_single_task_assert()
        self.mop_settle_dual_task_assert()
        self.wop_settle_dual_task_assert()
        self.settletask_update_assert()

    def bilateral_mode_wop_calc_three_currency(self):
        # 优化的后 fx_rate 的测试
        # 三种币种都不一致的情况
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop 侧和mop侧 的 wopsettleamount 和 wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.tyo_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig  表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费4,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 JPY  转换到CNY，需要乘以（1+mccr）  才能算出手续费
        trans_currency = "SGD"
        sett_currency = "USD"
        wop_settle_curreny = "JPY"
        fee_rate = 0.0595173  # 不要改
        trans_amount = 2333.0
        mccr = 0.0725964  # 不要改
        # 未乘以  fx_rate 的 清算金额为 148.9341513274408
        # jpy--cny
        self.tyo_config_db.update_one("wop", {"baseInfo.wopID": wopid},
                                      {"settleInfo.settleCurrency": wop_settle_curreny,
                                       })

        self.tyo_config_db.update_one("customizeConfig", {"wopID": wopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single",
                                       "transactionProcessingFeeRate": fee_rate,
                                       "fxProcessingFeeRate": fee_rate,
                                       'mccr': mccr
                                       })

        self.tyo_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"transCurrency": trans_currency,
                                           "wopSettleCurrency": sett_currency,
                                           "wopConverterCurrencyFlag": True,
                                           'transAmount': trans_amount

                                           })
        # 删除数据，再次触发流水导入并计费
        self.tyo_evosettle_db.delete_manys(self.common_name.trans_settle_wop,
                                           {"trans.wopID": wopid})
        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_import])

        # ----------------------------------
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('wop', [(trans_currency, wop_settle_curreny)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", trans_currency, wop_settle_curreny, wopid)

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid, 'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*fxrate*fee_rate
            self.task_func.assert_fee(trans, 12335.0)

        # ---------------------
        # 2查找直接反向汇率antiFxRate[JPY->SGD], 如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('wop', [(trans_currency, wop_settle_curreny)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", wop_settle_curreny, trans_currency, wopid)

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 14746.0)
        # ---------------------
        # 3 查找两个间接汇率indirectFxRate1[SGD->USD]，indirectFxRate2[USD->JPY]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('wop', [(wop_settle_curreny, trans_currency)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", trans_currency, 'USD', wopid)
        self.task_func.evonet_rate_set("wop", 'USD', wop_settle_curreny, wopid)

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            self.task_func.assert_fee(trans, 12240.0)  # 64.87
        # ---------------------
        # 4 查找两个间接汇率indirectFxRate1[SGD->USD]，indirectFxRate2[JPY->USD]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('wop', [(trans_currency, 'USD'), ('USD', wop_settle_curreny)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", trans_currency, 'USD', wopid)
        self.task_func.evonet_rate_set("wop", wop_settle_curreny, 'USD', wopid)

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 12477.0)  # 446.8

        # ---------------------
        # 5 查找两个间接汇率indirectFxRate1[USD->SGD]，indirectFxRate2[JPY->USD]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('wop', [(trans_currency, 'USD'), (wop_settle_curreny, 'USD')])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", 'USD', trans_currency, wopid)
        self.task_func.evonet_rate_set("wop", wop_settle_curreny, 'USD', wopid)

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 12537.0)  # 3077.21

        # ---------------------
        # 6 查找两个间接汇率indirectFxRate1[USD->SGD]，indirectFxRate2[USD->JPY]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('wop', [('USD', trans_currency), (wop_settle_curreny, 'USD')])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", 'USD', trans_currency, wopid)
        self.task_func.evonet_rate_set("wop", 'USD', wop_settle_curreny, wopid)

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 12298.0)  #
        # -------------
        # 7 假如最后的汇率也不存在；则计费失败，计费的feeFlag,clearFlag应该为 False
        # 查找两个间接汇率indirectFxRate1[USD->SGD]，indirectFxRate2[USD->JPY]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("wop", 'USD', trans_currency, wopid)
        self.task_func.evonet_rate_set("wop", 'USD', wop_settle_curreny, wopid)
        self.task_func.delete_fx_rate('wop', [('USD', trans_currency), ('USD', wop_settle_curreny),
                                              (wop_settle_curreny, 'USD')])

        self.wop_settle_task(wopid, [mopid], [self.common_name.wop_trans_calc])
        trans_settle_data = self.tyo_evosettle_db.get_many(self.common_name.trans_settle_wop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            assert trans["feeFlag"] == False
            assert trans["clearFlag"] == False

    def bilateral_mode_mop_calc_three_currency(self):
        # 优化的后 fx_rate 的测试
        # 三种币种都不一致的情况
        wopid = self.task_func.generate_wopid()
        mopid = self.task_func.generate_mopid()
        data = self.case_data.trans_list(wopid, mopid, self.sett_date, self.model)
        # 插入数据，插入数据的时候，造了，wop 侧和mop侧 的 wopsettleamount 和 wopsettlecurrency 不一致的情况
        # 数据插入到trans  表
        self.sgp_evosettle_db.insert_many("trans", data[0])

        # 创建配置; customizeconfig存在所有手续费的配置，计费时优先选择 cutomizeconfig表的配置
        self.db_operations.create_single_config(wopid, mopid, self.model, self.fileinit, "monthly",
                                                "monthly", str(random.randint(100000, 9900000)), "sgp")
        # 计费4,transSett.wop表的 settleinfo.settlecurrency和wop表cusomizeconfig表的settlecurrency不一致,且交易币种和清算币种不一致，
        # 用交易币 JPY  转换到CNY，需要乘以（1+mccr）  才能算出手续费
        trans_currency = "SGD"
        sett_currency = "USD"
        mop_settle_curreny = "JPY"
        fee_rate = 0.0595173  # 不要改
        trans_amount = 2333.0
        mccr = 0.0725964  # 不要改
        # 未乘以  fx_rate 的 清算金额为 148.9341513274408
        # jpy--cny
        self.sgp_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {"settleInfo.settleCurrency": mop_settle_curreny,
                                       })

        self.sgp_config_db.update_one("customizeConfig", {"mopID": mopid},
                                      {"settleCurrency": sett_currency,
                                       "transProcessingFeeCollectionMethod": "monthly",
                                       "transProcessingFeeCalculatedMethod": "single",
                                       "fxProcessingFeeCollectionMethod": "monthly",
                                       "fxProcessingFeeCalculatedMethod": "single",
                                       "transactionProcessingFeeRate": fee_rate,
                                       "fxProcessingFeeRate": fee_rate,
                                       'mccr': mccr
                                       })

        self.sgp_evosettle_db.update_many("trans",
                                          {"wopID": wopid},
                                          {"transCurrency": trans_currency,
                                           "wopSettleCurrency": sett_currency,
                                           "wopConverterCurrencyFlag": True,
                                           'transAmount': trans_amount

                                           })
        # 删除数据，再次触发流水导入并计费
        self.sgp_evosettle_db.delete_manys(self.common_name.trans_settle_mop,
                                           {"trans.wopID": wopid})
        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_import])

        # ----------------------------------
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('mop', [(trans_currency, mop_settle_curreny)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", trans_currency, mop_settle_curreny, wopid)

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid, 'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*fxrate*fee_rate
            self.task_func.assert_fee(trans, 12335.0)

        # ---------------------
        # 2查找直接反向汇率antiFxRate[JPY->SGD], 如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('mop', [(trans_currency, mop_settle_curreny)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", mop_settle_curreny, trans_currency, wopid)

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 14746.0)
        # ---------------------
        # 3 查找两个间接汇率indirectFxRate1[SGD->USD]，indirectFxRate2[USD->JPY]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('mop', [(mop_settle_curreny, trans_currency)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", trans_currency, 'USD', wopid)
        self.task_func.evonet_rate_set("mop", 'USD', mop_settle_curreny, wopid)

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            self.task_func.assert_fee(trans, 12240.0)  # 64.87
        # ---------------------
        # 4 查找两个间接汇率indirectFxRate1[SGD->USD]，indirectFxRate2[JPY->USD]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('mop', [(trans_currency, 'USD'), ('USD', mop_settle_curreny)])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", trans_currency, 'USD', wopid)
        self.task_func.evonet_rate_set("mop", mop_settle_curreny, 'USD', wopid)

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 12477.0)  # 446.8

        # ---------------------
        # 5 查找两个间接汇率indirectFxRate1[USD->SGD]，indirectFxRate2[JPY->USD]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('mop', [(trans_currency, 'USD'), (mop_settle_curreny, 'USD')])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", 'USD', trans_currency, wopid)
        self.task_func.evonet_rate_set("mop", mop_settle_curreny, 'USD', wopid)

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 12537.0)  # 3077.21

        # ---------------------
        # 6 查找两个间接汇率indirectFxRate1[USD->SGD]，indirectFxRate2[USD->JPY]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        self.task_func.delete_fx_rate('mop', [('USD', trans_currency), (mop_settle_curreny, 'USD')])
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", 'USD', trans_currency, wopid)
        self.task_func.evonet_rate_set("mop", 'USD', mop_settle_curreny, wopid)

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            # tansamount*(1+mccr)*1/fxrate*fee_rate
            self.task_func.assert_fee(trans, 12298.0)  #
        # ---------------------
        # 7 假如最后的汇率也不存在；则计费失败，计费的feeFlag,clearFlag应该为 False
        # 查找两个间接汇率indirectFxRate1[USD->SGD]，indirectFxRate2[USD->JPY]，如果存在
        # 设置 fx_rate 表 "bid": 0.22, "ask": 0.44, "mid": 0.66,
        # 修改transSettle.wop的blendType和 fx_rate  的费率
        self.task_func.evonet_rate_set("mop", 'USD', trans_currency, wopid)
        self.task_func.evonet_rate_set("mop", 'USD', mop_settle_curreny, wopid)
        self.task_func.delete_fx_rate('mop', [('USD', trans_currency), ('USD', mop_settle_curreny),
                                              (mop_settle_curreny, 'USD')])

        self.mop_settle_task(mopid, [wopid], [self.common_name.mop_trans_calc])
        trans_settle_data = self.sgp_evosettle_db.get_many(self.common_name.trans_settle_mop,
                                                           {'trans.wopID': wopid,
                                                            'trans.transType': {'$ne': 'Refund'}})
        # 手续费校验
        for trans in trans_settle_data:
            assert trans["feeFlag"] == False
            assert trans["clearFlag"] == False


if __name__ == '__main__':
    # 双节点测试
    common_name = CommonName()
    funciton_test = RestructFunction("test", "20200922", common_name.bilateral,
                                     common_name.evonet
                                     )
    # funciton_test.bilateral_mode_wop_calc_three_currency()
    # funciton_test.bilateral_mode_mop_calc_three_currency()
    # funciton_test.tyo_sgp_db_init()
    # funciton_test.wop_trans_import()
    # funciton_test.mop_trans_import()
    # funciton_test.evonet_model_evonet_fileinit_process()
    # funciton_test.bilateral_model_evonet_fileinit_process()
    # funciton_test.bilateral_model_wop_fileinit_process()

    # funciton_test.tyo_sgp_db_init()
    # funciton_test.all_sett_task_assert()

    # funciton_test.wop_evonet_mode_calc()
    # funciton_test.wop_evonet_mode_calc()
    # funciton_test.wop_trans_import()
    # funciton_test.mop_trans_import()
    # funciton_test.wop_self_settle()
    # #
    # funciton_test.wop_self_settle_abnormal()
    # funciton_test.mop_self_settle_abnormal()
    # funciton_test.wop_file_download_resolve_reconcile()
    # funciton_test.wop_file_full_extra_resolve_reconcile()
    # funciton_test.wop_file_extra_trans_resolve_reconcile()
    # funciton_test.wop_file_lack_reconcile()
    # funciton_test.wop_file_reconcile_status_assert()
    # funciton_test.mop_file_download_resolve_reconcile()

    # funciton_test.mop_file_full_extra_resolve_reconcile()
    # funciton_test.mop_file_extra_trans_resolve_reconcile()
    # funciton_test.mop_file_lack_reconcile()
    # funciton_test.mop_file_reconcile_status_assert()

    # funciton_test.wop_calc_custom_config()
    # funciton_test.wop_calc_three_currency()
    # funciton_test.wop_calc_fee_type_single_accumulation()
    # funciton_test.wop_calc_daily_single()
    # funciton_test.wop_evonet_fileinit_calc_refund_calc()
    # funciton_test.wop_evonet_mode_calc_evonet_rebate()
    # funciton_test.wop_wop_fileinit_calc_refund_calc()
    # funciton_test.wop_calc_assert_lack_settlement_settle_currency()  #evonet模式特有

    # funciton_test.mop_evonet_mode_calc()
    # funciton_test.mop_calc_custom_config()
    # funciton_test.mop_calc_three_currency()
    # funciton_test.mop_calc_fee_type_single_accumulation()
    # funciton_test.mop_calc_daily_single()
    # funciton_test.mop_evonet_fileinit_calc_refund_calc()
    # funciton_test.mop_wop_fileinit_calc_refund_calc()
    # funciton_test.mop_calc_assert_lack_settlement_settle_currency()

    #
    # ---------------
    # evonet模式
    # db_poerations = DatabaseOperations("test", )
    # funciton_test = RestructFunction("test", "20200922", common_name.evonet,
    #                                  common_name.evonet,
    #                                                                   )
    # funciton_test.wop_trans_import()
    # funciton_test.mop_trans_import()
    # funciton_test.wop_self_settle()
    # funciton_test.mop_self_settle()
