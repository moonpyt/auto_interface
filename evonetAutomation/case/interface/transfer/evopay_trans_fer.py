import random, time, json
import datetime
from common.evosettle.task_funcs import TaskFuncs
from base.read_config import *
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evopay_transfer.trans_fer_func import TransFerFunc, TransFerData
from common.evosettle.comm_funcs import CommonName
from common.evosettle.parmiko_module import Parmiko_Module
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData


class EvopayTransFer(DatabaseConnect):
    def __init__(self, envirs, path=None, title=None):
        super(EvopayTransFer, self).__init__(envirs, path=None, title=None)
        self.transfer_func = TransFerFunc(envirs)
        self.signkey = "9fce499557bd463271b758389981692c"
        self.trans_fer_data = TransFerData(envirs)

    def solve_result(self, result_json):
        code = result_json['result']['code']
        message = result_json['result']['message']
        return code, message

    def standad_rop_list(self, sopid, ropid_one, ropid_two, key_desc):
        # 一个正常的roplist请求,即所必传参数非必传参数都给进行传参
        # 一个sop可以对应多个ropid
        # 根据nodeid来新建sopid，ropid
        roplist_url = self.evosettle_config.get_ini("transfer_tyo_roplist")
        if key_desc == "standard":
            location = {"location": "CHN"}
            self.trans_fer_data.sop_data(sopid, location["location"])
            # 修改rop表的
            for ropid in [ropid_one, ropid_two]:
                self.transfer_func.transfer_config_data(sopid, ropid, location=location["location"], nodeid='tyo')
            resp_json = self.transfer_func.evopay_transfer_request("GET", roplist_url, sopid,
                                                                   self.signkey, data=None, **location).json()
            print(resp_json)
            self.transfer_func.rop_list_assert(key_desc, resp_json, sopid, ropid_one, ropid2=ropid_two)
        if key_desc == "less_location":  # 未传location
            location = {"location": "CHN"}
            self.trans_fer_data.sop_data(sopid, location["location"])
            # 修改rop表的
            for ropid in [ropid_one, ropid_two]:
                self.transfer_func.transfer_config_data(sopid, ropid, location=location["location"], nodeid='tyo')
            resp_json = self.transfer_func.evopay_transfer_request("GET", roplist_url, sopid,
                                                                   self.signkey, data=None).json()
            print(resp_json)
            self.transfer_func.rop_list_assert(key_desc, resp_json, sopid)
        if key_desc == "location_length_is_three":  # location长度
            for location in ["CHNN", "CH"]:
                location = {"location": location}
                self.trans_fer_data.sop_data(sopid, location["location"])
                # 修改rop表的
                for ropid in [ropid_one, ropid_two]:
                    self.transfer_func.transfer_config_data(sopid, ropid, location=location["location"], nodeid='tyo')
                resp_json = self.transfer_func.evopay_transfer_request("GET", roplist_url, sopid,
                                                                       self.signkey, data=None, **location).json()
                print(resp_json)
                self.transfer_func.rop_list_assert(key_desc, resp_json, sopid)
        if key_desc == "less_relation":  # 缺少relation case
            location = {"location": "CHN"}
            self.trans_fer_data.sop_data(sopid, location["location"])
            # 修改rop表的
            for ropid in [ropid_one, ropid_two]:
                self.transfer_func.transfer_config_data(sopid, ropid, location=location["location"], nodeid='tyo')
            self.tyo_config_db.delete_manys(self.comm_name.relation_transfer, {"sopID": sopid})
            resp_json = self.transfer_func.evopay_transfer_request("GET", roplist_url, sopid,
                                                                   self.signkey, data=None, **location).json()
            print(resp_json)
            self.transfer_func.rop_list_assert(key_desc, resp_json, sopid)
        if key_desc == "sopid_not_exist":  # 缺少relation case
            location = {"location": "CHN"}
            self.trans_fer_data.sop_data(sopid, location["location"])
            resp_json = self.transfer_func.evopay_transfer_request("GET", roplist_url,
                                                                   str(random.randint(222222222, 922222222)),
                                                                   self.signkey, data=None, **location).json()
            print(resp_json)
            self.transfer_func.rop_list_assert(key_desc, resp_json, sopid)
        if key_desc == "sop_status_not_active":  # 缺少relation case
            location = {"location": "CHN"}
            self.trans_fer_data.sop_data(sopid, location["location"])
            # 修改rop表的
            for ropid in [ropid_one, ropid_two]:
                self.transfer_func.transfer_config_data(sopid, ropid, location=location["location"], nodeid='tyo')
            self.tyo_config_db.update_many("sop", {"baseInfo.sopID": sopid}, {"status": "not_active"})
            self.tyo_config_db.delete_manys(self.comm_name.relation_transfer, {"sopID": sopid})
            resp_json = self.transfer_func.evopay_transfer_request("GET", roplist_url,
                                                                   sopid,
                                                                   self.signkey, data=None, **location).json()
            print(resp_json)
            self.transfer_func.rop_list_assert(key_desc, resp_json, sopid)

    def standad_service_fee(self, sopid, ropid, sign):
        service_fee_url = self.evosettle_config.get_ini("transfer_tyo_service_fee")
        if sign == "standard_online" or sign == 'standard_offline':  # 一个sop对应两个rop
            location = 'CHN'
            for type in ["Online", 'Offline']:
                self.transfer_func.transfer_config_data(sopid, ropid, location, nodeid='tyo', type=type)
                self.tyo_config_db.update_one(self.comm_name.service_fee, {"sopID": sopid}, {"sopFee": 12.0,
                                                                                             # sender出的交易总手续费
                                                                                             "sopFeeCurrency": "JPY",
                                                                                             # sender的交易trans_currency
                                                                                             "sopSettleFee": 13.00,
                                                                                             # sop 要收的手续费
                                                                                             "sopSettleFeeCurrency": "SGD",
                                                                                             # sop收的手续费的币种
                                                                                             "ropFee": 14.00,
                                                                                             "ropFeeCurrency": "HKD",
                                                                                             "ropSettleFee": 15.0,
                                                                                             "ropSettleFeeCurrency": "USD",
                                                                                             })
                request_data = {"location": location, "ropID": ropid, "type": type,
                                'sendAmount': {'currency': 'CNY', 'value': "100"}}

                if type == 'Online':
                    request_data['location'] == 'USA'
                resp_json = self.transfer_func.evopay_transfer_request("POST", service_fee_url, sopid,
                                                                       self.signkey,
                                                                       data=json.dumps(request_data)).json()
                print(resp_json)
                self.transfer_func.service_fee_assert(sopid, ropid, resp_json, "standard_online")
        if sign in ["sop_not_exist", "sop_status_locked", "rop_not_exist", "rop_status_locked",
                    "online_but_less_relation"]:  # 一个sop对应两个rop
            location = 'CHN'
            type = 'Online'
            self.transfer_func.transfer_config_data(sopid, ropid, location, nodeid='tyo', type=type)
            self.tyo_config_db.update_one(self.comm_name.service_fee, {"sopID": sopid}, {"sopFee": 12.0,
                                                                                         # sender出的交易总手续费
                                                                                         "sopFeeCurrency": "JPY",
                                                                                         # sender的交易trans_currency
                                                                                         "sopSettleFee": 13.00,
                                                                                         # sop 要收的手续费
                                                                                         "sopSettleFeeCurrency": "SGD",
                                                                                         # sop收的手续费的币种
                                                                                         "ropFee": 14.00,
                                                                                         "ropFeeCurrency": "HKD",
                                                                                         "ropSettleFee": 15.0,
                                                                                         "ropSettleFeeCurrency": "USD",
                                                                                         })
            request_data = {"location": location, "ropID": ropid, "type": type,
                            'sendAmount': {'currency': 'CNY', 'value': "100"}}
            if sign == 'sop_not_exist':
                self.tyo_config_db.delete_manys('sop', {'baseInfo.sopID': sopid})
            if sign == 'sop_status_locked':
                self.tyo_config_db.update_one('sop', {'baseInfo.sopID': sopid}, {'status': 'locked'})

            if sign == 'rop_not_exist':
                self.tyo_config_db.delete_manys('rop', {'baseInfo.ropID': ropid})
            if sign == 'rop_status_locked':
                self.tyo_config_db.update_one('rop', {'baseInfo.ropID': ropid}, {'status': 'locked'})
            if sign == "online_but_less_relation":
                self.tyo_config_db.delete_manys(self.comm_name.relation_transfer, {"sopID": sopid})

            resp_json = self.transfer_func.evopay_transfer_request("POST", service_fee_url, sopid,
                                                                   self.signkey,
                                                                   data=json.dumps(request_data)).json()
            print(resp_json)
            self.transfer_func.service_fee_assert(sopid, ropid, resp_json, sign)

    def standad_account_create(self):
        sopid = "sop_evopay_walker"
        ropid = "rop_evopay_walker"
        create_account_url = self.evosettle_config.get_ini("transfer_tyo_sop_create_account")

        location = 'CHN'
        type = "Online"
        self.transfer_func.transfer_config_data(sopid, ropid, location, nodeid='tyo', type=type)
        request_data = self.trans_fer_data.request_account_data(sopid, sopid)

        self.tyo_evopay_db.delete_manys(self.comm_name.trans_account, {"ownerID": sopid})
        resp = self.transfer_func.evopay_transfer_request("POST", create_account_url, sopid,
                                                          self.signkey, data=json.dumps(request_data))

    def standad_account_update(self):
        sopid = "sop_evopay_walker"
        ropid = "rop_evopay_walker"
        create_account_url = self.evosettle_config.get_ini("transfer_tyo_sop_create_account")
        update_account_url = self.evosettle_config.get_ini("transfer_tyo_sop_update_account")
        location = 'CHN'
        type = "Online"
        self.transfer_func.transfer_config_data(sopid, ropid, location, nodeid='tyo', type=type)
        request_data = self.trans_fer_data.request_account_data(sopid, sopid)

        print(request_data)
        self.tyo_evopay_db.delete_manys(self.comm_name.trans_account, {"ownerID": sopid})
        # 新建account
        resp = self.transfer_func.evopay_transfer_request("POST", create_account_url, sopid,
                                                          self.signkey, data=json.dumps(request_data))
        print(resp.json())
        evonet_refernece = resp.json()["userInfo"]["evonetUserReference"]
        print(resp.json()["userInfo"]["evonetUserReference"])
        del request_data["userInfo"]["userReference"]
        request_data["userInfo"]["evonetUserReference"] = evonet_refernece
        # # 修改account
        resp = self.transfer_func.evopay_transfer_request("PUT", update_account_url, sopid,
                                                          self.signkey, data=json.dumps(request_data))
        print(resp.json())

    def standad_account_delete(self):
        sopid = "sop_evopay_walker"
        ropid = "rop_evopay_walker"
        create_account_url = self.evosettle_config.get_ini("transfer_tyo_sop_create_account")
        delete_account_url = self.evosettle_config.get_ini("transfer_tyo_sop_delete_account")
        location = 'CHN'
        type = "Online"
        self.transfer_func.transfer_config_data(sopid, ropid, location, nodeid='tyo', type=type)
        request_data = self.trans_fer_data.request_account_data(sopid, sopid)

        print(request_data)
        self.tyo_evopay_db.delete_manys(self.comm_name.trans_account, {"ownerID": sopid})
        # 新建account
        resp = self.transfer_func.evopay_transfer_request("POST", create_account_url, sopid,
                                                          self.signkey, data=json.dumps(request_data))
        request_data = {"userInfo": {"evonetUserReference": resp.json()["userInfo"]["evonetUserReference"]}}

        # # 修改account
        resp = self.transfer_func.evopay_transfer_request("DELETE", delete_account_url, sopid,
                                                          self.signkey, data=json.dumps(request_data))
        print(resp.json())

    def standad_rop_recive_code(self):
        sopid = "sop_evopay_walker"
        ropid = "rop_evopay_walker"
        # rop测新建url
        create_account_url = self.evosettle_config.get_ini("transfer_tyo_rop_create_account")
        rop_receive_code_url = self.evosettle_config.get_ini("transfer_tyo_rop_receive_code")
        location = 'CHN'
        type = "Online"
        self.transfer_func.transfer_config_data(sopid, ropid, location, nodeid='tyo', type=type)
        # 造请求数据
        request_data = self.trans_fer_data.request_account_data(ropid, ropid)
        print(request_data)
        self.tyo_evopay_db.delete_manys(self.comm_name.trans_account, {"ownerID": sopid})
        # 新建account
        resp = self.transfer_func.evopay_transfer_request("POST", create_account_url, ropid,
                                                          self.signkey, data=json.dumps(request_data))

        request_data = {"evonetUserReference": resp.json()["userInfo"]["evonetUserReference"]}

        resp = self.transfer_func.evopay_transfer_request("GET", rop_receive_code_url, ropid,
                                                          self.signkey, **request_data)
        print(resp.json())


if __name__ == '__main__':
    sk = EvopayTransFer("test")
    # sopid = "sop_evopay_walker"
    # rop1 = "rop_evopay_walker"
    # rop2 = "rop_evopay_walker"
    sopid = sk.transfer_func.gengerate_sop_rop[0]

    rop1 = sk.transfer_func.gengerate_sop_rop[1]

    rop2 = sk.transfer_func.gengerate_sop_rop[2]
    # print(s)
    # print(rop1)
    # sk.standad_rop_list(sopid, ropid,
    #                     rop2, "sop_status_not_active")
    # --------------
    # sk.standad_service_fee(sopid, rop1, 'standard_offline')
    # sk.standad_service_fee(sopid, rop1, 'standard_oline')
    # sk.standad_service_fee(sopid, rop1, 'sop_not_exist')
    # sk.standad_service_fee(sopid, rop1, 'sop_status_locked')

    # sk.standad_service_fee(sopid, rop1, 'rop_not_exist')
    # sk.standad_service_fee(sopid, rop1, 'rop_status_locked')

    sk.standad_service_fee(sopid, rop1, 'online_but_less_relation')

    # sk.transfer_func.delete_sop_rop_config()
    # sk.standad_account_create()
    # sk.standad_account_update()
    # sk.standad_account_delete()
    # sk.standad_rop_recive_code()
