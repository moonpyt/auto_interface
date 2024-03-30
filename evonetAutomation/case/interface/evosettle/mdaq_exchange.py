import random, time
from decimal import Decimal
import datetime
from common.evosettle.task_funcs import TaskFuncs
from base.read_config import *
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evosettle.comm_funcs import CommonName
from common.evosettle.create_report_data import CreateReportData
from common.evosettle.parmiko_module import Parmiko_Module
from common.evosettle.task_funcs import TaskFuncs
from common.evosettle.case_data import CaseData


class MdaqExchange(DatabaseConnect):
    def __init__(self, envirs):
        super().__init__(envirs)
        self.db_operations = DatabaseOperations(envirs)
        self.common_name = CommonName()
        self.create_report = CreateReportData()
        self.settle_date = "20210406"
        self.sftp_func = Parmiko_Module()
        self.private_key = self.aes_decrypt.decrypt(self.evosettle_config.get_ini("sgp_key"))
        self.tyo_ip = self.evosettle_config.get_ini("tyo_ip")
        self.tyo_user = self.evosettle_config.get_ini("tyo_user")
        self.task_func = TaskFuncs(envirs)
        self.case_data = CaseData()
        self.tyo_func_url = self.evosettle_config.get_ini("tyo_func_url")  # tyo节点单个任务的url
        self.sgp_func_url = self.evosettle_config.get_ini("sgp_func_url")  # spg节点单个任务的url

    def mdaq_file(self):
        # 文件下载测试
        pass

    def mdaq_task_resolve_one_record(self):
        # mdaq文件解析，1 先造文件上传至服务器，并在fileInfo插入记录，触发解析，2 校验 evosettle库中每个字段的的值是否和文件中的一致
        self.tyo_evosettle_db.delete_manys(self.common_name.advice_file, {"expectValueDate": self.settle_date})
        file_name_one = "evonet_ExecRpt_" + self.settle_date + "_" + self.settle_date + "0" + str(
            random.randint(10000, 90000)) + "_021.csv"

        file_path = "/home/webapp/evofile/rawData/" + self.settle_date + "/"
        # 造文件出来
        for file_name in [file_name_one]:
            self.create_report.mdaq_execrpt_file(file_name, self.settle_date)
            # 上传文件至远程服务器 file_path
            self.sftp_func.ssh_download_file("put", self.private_key, self.tyo_ip, self.tyo_user,
                                             remote_path=file_path + file_name,
                                             local_path=file_name
                                             )
        # 删除fileInfo记录
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {"settleDate": self.settle_date})
        # 将其它的fileInfo记录 resolveFlag变为True
        self.tyo_evosettle_db.update_many(self.common_name.file_info, {"fileSubType": "ExecRpt"},
                                          {"resolveFlag": True})

        # 删除task 任务
        self.tyo_config_db.delete_manys("task", {"taskName": self.common_name.mdaq_resolve})

        # 插入记录
        for file_name in [file_name_one, ]:
            file_record = {"firstRole": "MDAQ",
                           "secondRole": "EVONET",
                           "settleDate": self.settle_date,
                           "fileName": file_name,
                           "filePath": file_path,
                           "fileType": "Other",
                           "fileSubType": "ExecRpt",
                           "resolveFlag": False}
            self.tyo_evosettle_db.insert_one(self.common_name.file_info, file_record)
        task_resolve = {"taskName": self.common_name.mdaq_resolve,
                        "taskCron": "00 35 08 * * *",
                        "taskType": "loop",
                        "lockType": "0",
                        "handler": self.common_name.mdaq_resolve,
                        "timeout": int(30),
                        "lastExecuteTime": datetime.datetime.now() + datetime.timedelta(days=-10),
                        "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                            days=-10)}
        # 删除日志
        self.tyo_config_db.delete_manys("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 插入task马上就能解析
        self.tyo_config_db.insert_one("task", task_resolve)
        time.sleep(5)
        for file_name in [file_name_one]:
            self.task_func.mdaq_resolve_assert(file_name)
            os.remove(file_name)
        reslove_log = self.tyo_config_db.get_one("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 根据file_name 取fileinfo查找数据，并校验 resolveFlag为True
        for file_name in [file_name_one]:
            data = self.tyo_evosettle_db.get_one(self.common_name.file_info, {"fileName": file_name})
            assert data["resolveFlag"] == True
        assert reslove_log["taskresult"]["result"] == int(0)
        resolve_flag = self.tyo_evosettle_db.get_one(self.common_name.file_info, {'fileName': file_name_one})[
            'resolveFlag']
        assert resolve_flag == True
        # 解析完的再解析一次
        self.tyo_evosettle_db.delete_manys(self.common_name.advice_file, {"expectValueDate": self.settle_date})
        self.tyo_evosettle_db.update_many(self.common_name.file_info, {"taskName": self.common_name.mdaq_resolve},
                                          {"nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                              days=-10)})
        time.sleep(3)
        count = self.tyo_evosettle_db.count(self.common_name.advice_file, {"expectValueDate": self.settle_date})
        assert count == 0

    def mdaq_task_resolve_two_record(self):
        # mdaq文件解析，1 先造文件上传至服务器，并在fileInfo插入记录，触发解析，2 校验 evosettle库中每个字段的的值是否和文件中的一致
        file_name_one = "evonet_ExecRpt_" + self.settle_date + "_" + self.settle_date + "0" + str(
            random.randint(10000, 90000)) + "_021.csv"
        file_name_two = "evonet_ExecRpt_" + str(int(self.settle_date) - 1) + "_" + self.settle_date + "0" + str(
            random.randint(10000, 90000)) + "_021.csv"
        file_path = "/home/webapp/evofile/rawData/" + self.settle_date + "/"
        # 造文件出来
        for file_name in [file_name_one, file_name_two]:
            self.create_report.mdaq_execrpt_file(file_name, self.settle_date)
            # 上传文件至远程服务器 file_path
            self.sftp_func.ssh_download_file("put", self.private_key, self.tyo_ip, self.tyo_user,
                                             remote_path=file_path + file_name,
                                             local_path=file_name
                                             )
        # 删除fileInfo记录
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {"settleDate": self.settle_date})
        # 将其它的fileInfo记录 resolveFlag变为True
        self.tyo_evosettle_db.update_many(self.common_name.file_info, {"fileSubType": "ExecRpt"},
                                          {"resolveFlag": True})

        # 删除task 任务
        self.tyo_config_db.delete_manys("task", {"taskName": self.common_name.mdaq_resolve})

        # 插入记录
        for file_name in [file_name_one, file_name_two]:
            file_record = {"firstRole": "MDAQ",
                           "secondRole": "EVONET",
                           "settleDate": self.settle_date,
                           "fileName": file_name,
                           "filePath": file_path,
                           "fileType": "Other",
                           "fileSubType": "ExecRpt",
                           "resolveFlag": False}
            self.tyo_evosettle_db.insert_one(self.common_name.file_info, file_record)
        task_resolve = {"taskName": self.common_name.mdaq_resolve,
                        "taskCron": "00 35 08 * * *",
                        "taskType": "loop",
                        "lockType": "0",
                        "handler": self.common_name.mdaq_resolve,
                        "timeout": int(30),
                        "lastExecuteTime": datetime.datetime.now() + datetime.timedelta(days=-10)
            ,
                        "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                            days=-10)}
        # 删除日志
        self.tyo_config_db.delete_manys("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 插入task马上就能解析
        self.tyo_config_db.insert_one("task", task_resolve)
        time.sleep(5)
        for file_name in [file_name_one, file_name_two]:
            self.task_func.mdaq_resolve_assert(file_name)
            os.remove(file_name)
        reslove_log = self.tyo_config_db.get_one("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 根据file_name 取fileinfo查找数据，并校验 resolveFlag为True
        for file_name in [file_name_one, file_name_two]:
            data = self.tyo_evosettle_db.get_one(self.common_name.file_info, {"fileName": file_name})
            assert data["resolveFlag"] == True
        assert reslove_log["taskresult"]["result"] == int(0)

    def mdaq_task_resolve_file_not_exist(self):
        # mdaq文件解析，fileInfo不存在需要解析的文件的记录
        file_name_one = "evonet_ExecRpt_" + self.settle_date + "_" + self.settle_date + "0" + str(
            random.randint(10000, 90000)) + "_021.csv"
        file_name_two = "evonet_ExecRpt_" + str(int(self.settle_date) - 1) + "_" + self.settle_date + "0" + str(
            random.randint(10000, 90000)) + "_021.csv"
        file_path = "/home/webapp/evofile/rawData/" + self.settle_date + "/"
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {"settleDate": self.settle_date})
        # 将其它的fileInfo记录 resolveFlag变为True
        self.tyo_evosettle_db.update_many(self.common_name.file_info, {"fileSubType": "ExecRpt"},
                                          {"resolveFlag": True})
        # 删除task 任务
        self.tyo_config_db.delete_manys("task", {"taskName": self.common_name.mdaq_resolve})

        # 插入记录
        for file_name in [file_name_one, file_name_two]:
            file_record = {"firstRole": "MDAQ",
                           "secondRole": "EVONET",
                           "settleDate": self.settle_date,
                           "fileName": file_name,
                           "filePath": file_path,
                           "fileType": "Other",
                           "fileSubType": "ExecRpt",
                           "resolveFlag": False}
            self.tyo_evosettle_db.insert_one(self.common_name.file_info, file_record)
        task_resolve = {"taskName": self.common_name.mdaq_resolve,
                        "taskCron": "00 35 08 * * *",
                        "taskType": "loop",
                        "lockType": "0",
                        "handler": self.common_name.mdaq_resolve,
                        "timeout": int(30),
                        "lastExecuteTime": datetime.datetime.now() + datetime.timedelta(days=-10),
                        "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                            days=-10)}
        # 删除日志
        self.tyo_config_db.delete_manys("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 插入task马上就能解析
        self.tyo_config_db.insert_one("task", task_resolve)
        time.sleep(5)
        reslove_log = self.tyo_config_db.get_one("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 根据file_name 取fileinfo查找数据，并校验 resolveFlag为True
        for file_name in [file_name_one, file_name_two]:
            data = self.tyo_evosettle_db.get_one(self.common_name.file_info, {"fileName": file_name})
            assert data["resolveFlag"] == True  # 这个是服务器不存在文件，但是fileInfo存在记录，记为True也没事
        assert reslove_log["taskresult"]["result"] == int(0)

    def mdaq_task_resolve_fileinfo_not_exist(self):
        # mdaq文件解析，fileInfo有记录，但是服务器文件不存在

        # 将fileInfo记录 resolveFlag变为True
        self.tyo_evosettle_db.update_many(self.common_name.file_info, {"fileSubType": "ExecRpt"},
                                          {"resolveFlag": True})
        # 删除task 任务
        self.tyo_config_db.delete_manys("task", {"taskName": self.common_name.mdaq_resolve})
        # 插入解析任务记录
        task_resolve = {"taskName": self.common_name.mdaq_resolve,
                        "taskCron": "00 35 08 * * *",
                        "taskType": "loop",
                        "lockType": "0",
                        "handler": self.common_name.mdaq_resolve,
                        "timeout": int(30),
                        "lastExecuteTime": datetime.datetime.now() + datetime.timedelta(days=-10),
                        "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                            days=-10)}
        # 删除日志
        self.tyo_config_db.delete_manys("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 插入task马上就能解析
        self.tyo_config_db.insert_one("task", task_resolve)
        time.sleep(5)
        reslove_log = self.tyo_config_db.get_one("task_log", {"taskName": self.common_name.mdaq_resolve})
        # 根据file_name 取fileinfo查找数据，并校验 resolveFlag为True
        assert reslove_log["taskresult"]["result"] == int(0)

    def mdaq_task_recon(self):
        # maqp，勾兑，需要传参，settleDate
        self.tyo_evosettle_db.delete_manys(self.common_name.advice, {"expectValueDate": self.settle_date})
        self.tyo_evosettle_db.delete_manys(self.common_name.advice_file, {"expectValueDate": self.settle_date})
        transformation_settle_date = "transformation_settle_date"
        self.tyo_evosettle_db.delete_manys(self.common_name.advice, {"expectValueDate": "transformation_settle_date"})
        self.tyo_evosettle_db.delete_manys(self.common_name.advice_file,
                                           {"expectValueDate": "transformation_settle_date"})
        file_name = "evonet_ExecRpt_" + self.settle_date + "_" + self.settle_date + "0" + str(
            random.randint(10000, 90000)) + "_021.csv"
        file_path = "/home/webapp/evofile/rawData/" + self.settle_date + "/"

        # 造文件出来
        self.create_report.mdaq_execrpt_file(file_name, self.settle_date)
        # 上传文件至远程服务器 file_path
        self.sftp_func.ssh_download_file("put", self.private_key, self.tyo_ip, self.tyo_user,
                                         remote_path=file_path + file_name,
                                         local_path=file_name
                                         )
        # 根据日期删除fileInfo记录
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info, {"settleDate": self.settle_date})
        # 将其它的fileInfo记录 resolveFlag变为True
        self.tyo_evosettle_db.update_many(self.common_name.file_info, {"fileSubType": "ExecRpt"},
                                          {"resolveFlag": True})
        # 删除task 任务
        self.tyo_config_db.delete_manys("task", {"taskName": self.common_name.mdaq_resolve})
        # 插入记录
        file_record = {"firstRole": "MDAQ",
                       "secondRole": "EVONET",
                       "settleDate": self.settle_date,
                       "fileName": file_name,
                       "filePath": file_path,
                       "fileType": "Other",
                       "fileSubType": "ExecRpt",
                       "resolveFlag": False}
        self.tyo_evosettle_db.insert_one(self.common_name.file_info, file_record)
        task_resolve = {"taskName": self.common_name.mdaq_resolve,
                        "taskCron": "00 35 08 * * *",
                        "taskType": "loop",
                        "lockType": "0",
                        "handler": self.common_name.mdaq_resolve,
                        "timeout": int(30),
                        "lastExecuteTime": datetime.datetime.now() + datetime.timedelta(days=-10)
            ,
                        "nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                            days=-10)}
        # 删除日志
        # 插入task马上就能解析
        self.tyo_config_db.insert_one("task", task_resolve)
        time.sleep(5)  # 等待数据进入到 advice_file表，
        # 触发post 勾兑请求
        # 全是多清
        self.task_func.mdaq_request("MDaqRecon", "MDaqRecon", self.settle_date)

        # 获取 advice_file表的数据
        data = self.tyo_evosettle_db.get_many(self.common_name.advice_file, {'expectValueDate': self.settle_date})
        # 获取所有的key，并组成列表
        keys = []
        for advice_data in data:
            keys.append(advice_data['adviceId'])
        assert len(keys) == 6  # 这个是在前置条件文件解析中做了六条交易
        # 全部多清校验
        for key in keys:
            advice_file_data = self.tyo_evosettle_db.get_one(self.common_name.advice_file,
                                                             {'adviceId': key})
            advice_data = self.tyo_evosettle_db.get_one(self.common_name.advice,
                                                        {'adviceId': key})
            assert advice_data == advice_file_data
            assert advice_data['reconFlag'] == int(2)
        # 全部勾兑平
        self.tyo_evosettle_db.update_many(self.common_name.advice, {'expectValueDate': self.settle_date},
                                          {"reconFlag": int(0)})
        # 删除fileInfo recon记录
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info,
                                           {"settleDate": self.settle_date, "fileSubType": "Recon"})
        # 触发勾兑请求
        self.task_func.mdaq_request("MDaqRecon", "MDaqRecon", self.settle_date)
        for key in keys:
            advice_data = self.tyo_evosettle_db.get_one(self.common_name.advice,
                                                        {'adviceId': key})
            assert advice_data['reconFlag'] == int(1)  # 勾兑平
        # 全部少清
        self.tyo_evosettle_db.update_many(self.common_name.advice_file, {'expectValueDate': self.settle_date},
                                          {'expectValueDate': transformation_settle_date})
        self.tyo_evosettle_db.update_many(self.common_name.advice, {'expectValueDate': self.settle_date},
                                          {"reconFlag": int(0)})
        # 修改advice_file表的数据 为生勾兑文件做准备，因为这几个值在 mdaq给的文件中不存在
        # [advice_time], [settle_date], [beneficiary], [fxg_adj_client_profit],
        # [original_batch_id], [evonet_order_number], [orig_evonet_order_number], [mdaq_rate],
        # 修改advice表的数据
        self.tyo_evosettle_db.update_many(self.common_name.advice, {"expectValueDate": self.settle_date},
                                          {
                                              'origEvonetOrderNumber': str(
                                                  random.randint(10000000000000000000000, 90000000000000000000000)),
                                              "settleDate": self.settle_date,
                                              "beneficiary": str(random.randint(100000, 900000)),
                                              "fxgAdjClientProfit": random.randint(100, 999) * 0.1,
                                              "originalBatchId": str(
                                                  random.randint(10000000000000000000000, 90000000000000000000000)),
                                              "evonetOrderNumber": str(
                                                  random.randint(10000000000000000000000, 90000000000000000000000)),
                                              "mdaqRate": random.randint(100, 999) * 0.01,
                                              'adviceTime': datetime.datetime.now()
                                          })

        # 删除fileInfo recon记录
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info,
                                           {"settleDate": self.settle_date, "fileSubType": "Recon"})
        self.task_func.mdaq_request("MDaqRecon", "MDaqRecon", self.settle_date)
        for key in keys:
            advice_data = self.tyo_evosettle_db.get_one(self.common_name.advice,
                                                        {'adviceId': key})
            assert advice_data['reconFlag'] == int(0)  #
        # ----------
        # 多清，少清，勾兑平都有
        self.tyo_evosettle_db.update_many(self.common_name.advice_file, {'expectValueDate': transformation_settle_date},
                                          {'expectValueDate': self.settle_date})
        self.tyo_evosettle_db.update_many(self.common_name.advice, {'expectValueDate': self.settle_date},
                                          {"reconFlag": int(0)})
        # 造多清
        self.tyo_evosettle_db.delete_one(self.common_name.advice, {"adviceId": keys[0]})
        # 造少清
        self.tyo_evosettle_db.delete_one(self.common_name.advice_file, {"adviceId": keys[-1]})
        # 四条，勾兑平，一条多清，一条少清
        # 删除fileInfo recon记录
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info,
                                           {"settleDate": self.settle_date, "fileSubType": "Recon"})
        self.task_func.mdaq_request("MDaqRecon", "MDaqRecon", self.settle_date)
        for key in keys[1:5]:
            advice_data = self.tyo_evosettle_db.get_one(self.common_name.advice,
                                                        {'adviceId': key})
            assert advice_data['reconFlag'] == int(1)  # 勾兑平
        # 少清校验
        assert self.tyo_evosettle_db.get_one(self.common_name.advice, {"adviceId": keys[-1]})["reconFlag"] == int(0)
        # 多清校验
        assert self.tyo_evosettle_db.get_one(self.common_name.advice, {"adviceId": keys[0]})["reconFlag"] == int(2)
        os.remove(file_name)
        # 校验log状态
        self.tyo_config_db.delete_manys("task_log", {"taskName": self.common_name.mdaq_recon})
        # 修改时间为10天前
        self.tyo_config_db.update_one("task", {"taskName": self.common_name.mdaq_recon},
                                      {"nextExecuteTime": datetime.datetime.now() + datetime.timedelta(
                                          days=-10)})
        time.sleep(5)
        assert self.tyo_config_db.get_one("task_log", {"taskName": self.common_name.mdaq_recon})["taskresult"][
                   "result"] == int(0)
        # 生出的勾兑的文件校验，1 从服务器下载，然后校验，这个是完全从数据库获取出来的值，
        recon_file_name = "MDAQ_Advice_Recon_{}.csv".format(self.settle_date)
        self.sftp_func.ssh_download_file("get", self.private_key, self.tyo_ip, self.tyo_user,
                                         remote_path=file_path + recon_file_name,
                                         local_path=recon_file_name
                                         )
        self.task_func.mdaq_recon_file_assert("MDAQ_Advice_Recon_{}.csv".format(self.settle_date))
        # 勾兑之后查看fileInfo记录，服务器文件内容
        #删除够对的文件
        os.remove(recon_file_name)
    def mdaq_empty_recon(self):
        # 当adviceFile表和adviceFile表没有符合勾兑条件的数据时
        # 删除 advicefile和advice表的数据
        self.tyo_evosettle_db.delete_manys(self.common_name.advice, {"expectValueDate": self.settle_date})
        self.tyo_evosettle_db.delete_manys(self.common_name.advice_file, {"expectValueDate": self.settle_date})
        self.tyo_evosettle_db.delete_manys(self.common_name.file_info,
                                           {"settleDate": self.settle_date, "fileSubType": "Recon"})

        self.task_func.mdaq_request("MDaqRecon", "MDaqRecon", self.settle_date)
        time.sleep(3)
        # 校验fileInfo记录，校验空文件

    def report_trans_list(self, wopid, mopid, settle_currency, trans_currency, every_date=None):
        # 为了退款计费而造的交易
        if every_date:
            report_date = every_date
        else:
            report_date = self.settle_date
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

    def mdaq_task_request(self, mopid, wopid_list, function_list):
        self.task_func.settle_task_request(self.tyo_func_url, "mop", mopid, wopid_list, self.settle_date,
                                           function_list
                                           , "evonet", "evonet")

    def mdaq_evonet_advice(self):
        # 每日报表mop插入到 advice表,一个mopid对应wopid

        mopid = "bccardnacfusd"
        wopid1 = self.task_func.generate_wopid()
        wopid2 = self.task_func.generate_wopid()
        wopid3 = self.task_func.generate_wopid()
        settle_currency = "SGD"  # 修改币种及计费方式
        wop_settlecurrency = 'JPY'
        model_file_init = "evonet"
        # 创建配置 1
        self.tyo_config_db.update_many('task',{"taskName" : "TransMessage"},{"lockType" : "0"})
        self.db_operations.mdaq_create_single_config(wopid1, mopid, model_file_init, model_file_init,
                                                     "monthly", "monthly",
                                                     str(random.randint(100000, 9900000)),
                                                     "tyo")
        # 删除配置wop表的配置
        # ----------------------
        # 创建配置 2
        self.db_operations.mdaq_create_single_config(wopid2, mopid, model_file_init, model_file_init,
                                                     "monthly",
                                                     "monthly",
                                                     str(random.randint(100000, 9900000)),
                                                     "tyo")
        # 创建配置3
        self.db_operations.mdaq_create_single_config(wopid3, mopid, model_file_init, model_file_init,
                                                     "monthly",
                                                     "monthly",
                                                     str(random.randint(100000, 9900000)),
                                                     "tyo")
        # 触发流水导入
        # 数据插入到trans表,造两条交易
        self.tyo_config_db.update_one("mop", {"baseInfo.mopID": mopid},
                                      {
                                          "settleInfo.settleCurrency": settle_currency,
                                          "settleInfo.beneficiary":"bccardnacf"+settle_currency.lower(),
                                            "settleInfo.transProcessingFeeCollectionMethod": "daily",
                                            "settleInfo.transProcessingFeeCalculatedMethod": "single",
                                            "settleInfo.fxProcessingFeeCollectionMethod": "daily",
                                            "settleInfo.fxProcessingFeeCalculatedMethod": "single",
                                            "settleInfo.cpmInterchangeFeeRate": 0.0632658,  # 不要改
                                            "settleInfo.mpmInterchangeFeeRate": 0.08328446, }) # 不要改

        self.tyo_config_db.update_one(self.common_name.custom_config, {"mopID": mopid},
                                      {
                                          "transactionProcessingFeeRate": 0.0595173,  # 不要改
                                          "fxProcessingFeeRate": 0.0852973,  # 不要改
                                      })

        for i in range(2):  # 造一个wopid对应两个mopid的交易，且wopid和mopid包含两个交易币种
            for trans_currency in ["CNY", "JPY"]:
                for wopid in [wopid1, wopid2, wopid3]:
                    self.tyo_evosettle_db.insert_many("trans",
                                                      self.report_trans_list(wopid, mopid,
                                                                             settle_currency,
                                                                             trans_currency)[0])
        self.tyo_evosettle_db.update_many('trans',
                                          {"wopID": {"$in": [wopid1, wopid2, wopid3]}},
                                          {'wopSettleCurrency': wop_settlecurrency})
        self.tyo_evosettle_db.update_many('wop', {"baseInfo.wopID": {"$in": [wopid1, wopid2, wopid3]}},
                                          {"settleInfo.settleCurrency": wop_settlecurrency})
        # evonet模式执行正常function,生每日报表，
        self.mdaq_task_request(mopid, [wopid1, wopid2, wopid3],
                               [self.common_name.mop_trans_import, self.common_name.mop_self_sett,
                                self.common_name.mop_trans_calc, self.common_name.mop_generate_file,
                                ])
        # 当，advice表的手续费为负时，数据进入到trans_message和advice 表字段的校验
        self.task_func.trans_message_assert(mopid, wopid1, wopid2, wopid3, wop_settlecurrency, settle_currency,
                                            self.settle_date)
        # ---------------------
        # 做手续费大于0时进入到 trans_message 和 advice 表时的各个字段的校验，实际和上面校验只有两个字段不一致
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_mop,
                                          {"trans.wopID": {"$in": [wopid1, wopid2, wopid3]},
                                           "trans.transType": "Refund"},
                                          {"settleInfo.interchangeFee": 1111.11})  # 修改interchangeFee，使总手续费大于0
        # 触发生每日报表
        self.mdaq_task_request(mopid, [wopid1, wopid2, wopid3],
                               [self.common_name.mop_generate_file,
                                ])
        self.task_func.trans_message_assert(mopid, wopid1, wopid2, wopid3, wop_settlecurrency, settle_currency,
                                            self.settle_date)
        # 当  # 其中一组 wopid1，手续费和为 0 时，
        self.tyo_evosettle_db.update_many(self.common_name.trans_settle_mop,  # 只修改一个wopId的手续费为0
                                          {"trans.wopID": {"$in": [wopid1]},
                                           "trans.transType": "Refund"},
                                          {
                                              "settleInfo.interchangeFee": 523.42})  # 这个值不要改，为了，验证手续费之和为0时，校验数据不进入到trans_message表
        # 触发生每日报表
        self.mdaq_task_request(mopid, [wopid1, wopid2, wopid3],
                               [self.common_name.mop_generate_file,
                                ])
        self.task_func.trans_message_assert(mopid, wopid1, wopid2, wopid3, wop_settlecurrency, settle_currency,
                                            self.settle_date)


m = MdaqExchange("test")
for i in range(1):
    # m.mdaq_task_resolve_one_record()
    # m.mdaq_task_resolve_two_record()
    # m.mdaq_task_resolve_file_not_exist()
    # m.mdaq_task_resolve_fileinfo_not_exist()
    # m.mdaq_task_recon()
    m.mdaq_evonet_advice()
    # m.mdaq_empty_recon()
    # # pass
