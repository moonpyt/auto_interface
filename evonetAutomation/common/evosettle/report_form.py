import requests
import time

tyo_task_url = "https://tyo-testing-api.pre-evonetonline.com/settle/private/doSettleTaskStep"
sgp_task_url = "https://sgp-testing-api.pre-evonetonline.com/settle/private/doSettleTaskStep"


def task_request(url, owner_type, owner_id, sett_date, role, step):
    """
    请求任务
    :param url: tyo或者sgp的url
    :param owner_id:  wopid 或者mopid
    :param owner_type:    wop  或mop
    :param sett_date:     清算日期
    :param role:      wopid或mopid  或者evonet;当是evonet时代表 evonet模式
    :param step:      settTask中的序号
    :return:
    """
    data = {
        "ownerID": owner_id,
        "ownerType": owner_type,
        "settleDate": sett_date,
        "role": role,
        "step": step
    }
    header = {
        'Content-Type': 'application/json'
    }
    uri = "/settle/private/doSettleTaskStep"
    requests.post(url, headers=header, json=data)
    time.sleep(3)


def direct_evonet_single(wopid, mopid, sett_date):
    # 直清模式单节点，evonet出文件
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 1)
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 2)
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 3)
    task_request(tyo_task_url, "mop", mopid, sett_date, wopid, 1)
    task_request(tyo_task_url, "mop", mopid, sett_date, wopid, 2)
    task_request(tyo_task_url, "mop", mopid, sett_date, wopid, 3)


def direct_evonet_dual(wopid, mopid, sett_date):
    # 直清模式双节点，evonet出文件
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 1)
    task_request(sgp_task_url, "mop", mopid, sett_date, wopid, 1)
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 2)
    task_request(sgp_task_url, "mop", mopid, sett_date, wopid, 2)
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 3)
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 4)
    task_request(sgp_task_url, "mop", mopid, sett_date, wopid, 3)
    task_request(sgp_task_url, "mop", mopid, sett_date, wopid, 4)


def model_evoent_single(wopid, mopid, sett_date):
    # evonet模式，单节点
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 1)
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 2)
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 3)
    task_request(tyo_task_url, "mop", mopid, sett_date, "evonet", 1)
    task_request(tyo_task_url, "mop", mopid, sett_date, "evonet", 2)
    task_request(tyo_task_url, "mop", mopid, sett_date, "evonet", 3)


def model_evoent_dual(wopid, mopid, sett_date):
    # evonet模式，单节点
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 1)
    task_request(sgp_task_url, "mop", mopid, sett_date, "evonet", 1)
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 2)
    task_request(sgp_task_url, "mop", mopid, sett_date, "evonet", 2)
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 3)
    task_request(tyo_task_url, "wop", wopid, sett_date, "evonet", 4)
    task_request(sgp_task_url, "mop", mopid, sett_date, "evonet", 3)
    task_request(sgp_task_url, "mop", mopid, sett_date, "evonet", 4)


def direct_evonet_single_report(wopid, mopid):
    # 单节点,月报  sett_date 为  每个月的四号 如  20201004
    sett_date = "20201004"
    task_request(tyo_task_url, "wop", wopid, sett_date, mopid, 3)
    task_request(tyo_task_url, "mop", mopid, sett_date, wopid, 3)


def evonet_model_single_report(owner_type, id, ):
    # 参数 wopid 或mopid
    sett_date = "20201004"
    task_request(tyo_task_url, owner_type, id, sett_date, "evonet", 3)


if __name__ == '__main__':
    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200908")
    direct_evonet_single("WOP_GrabPaySG", "MOP_KTBTH", "20200908")
    direct_evonet_single("WOP_PayboocKR", "MOP_PayPayJP", "20200908")
    direct_evonet_single("WOP_PayboocKR", "MOP_KTBTH", "20200908")
    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200908")

    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200909")
    direct_evonet_single("WOP_GrabPaySG", "MOP_KTBTH", "20200909")
    direct_evonet_single("WOP_PayboocKR", "MOP_PayPayJP", "20200909")
    direct_evonet_single("WOP_PayboocKR", "MOP_KTBTH", "20200909")
    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200909")

    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200910")
    direct_evonet_single("WOP_GrabPaySG", "MOP_KTBTH", "20200910")
    direct_evonet_single("WOP_PayboocKR", "MOP_PayPayJP", "20200910")
    direct_evonet_single("WOP_PayboocKR", "MOP_KTBTH", "20200910")
    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200910")

    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200911")
    direct_evonet_single("WOP_GrabPaySG", "MOP_KTBTH", "20200911")
    direct_evonet_single("WOP_PayboocKR", "MOP_PayPayJP", "20200911")
    direct_evonet_single("WOP_PayboocKR", "MOP_KTBTH", "20200911")
    direct_evonet_single("WOP_GrabPaySG", "MOP_SBPSJP", "20200911")

    # 单节点，evonet模式，月报
    direct_evonet_single_report("WOP_GrabPaySG", "MOP_SBPSJP")
    direct_evonet_single_report("WOP_GrabPaySG", "MOP_KTBTH")
    direct_evonet_single_report("WOP_PayboocKR", "MOP_PayPayJP")
    direct_evonet_single_report("WOP_PayboocKR", "MOP_KTBTH")
    direct_evonet_single_report("WOP_GrabPaySG", "MOP_SBPSJP")

    # evonet模式生月报
    evonet_model_single_report("wop", "WOP_GrabPaySG")
    evonet_model_single_report("wop", "WOP_KTBTH")
    evonet_model_single_report("wop", "WOP_PayPayJP")
    evonet_model_single_report("mop", "MOP_GrabPaySG")
    evonet_model_single_report("mop", "MOP_KTBTH")
    evonet_model_single_report("mop", "MOP_PayboocKR")
    evonet_model_single_report("mop", "MOP_PayPayJP")
    evonet_model_single_report("mop", "MOP_SBPSJP")
