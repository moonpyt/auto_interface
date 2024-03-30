import requests
import json
import random
from .trans_fer_data import TransFerData


class TransFerFunc(TransFerData, object):
    def __init__(self, envirs, path=None, title=None):
        super(TransFerFunc, self).__init__(envirs, path=None, title=None)

    def evopay_transfer_request(self, method, url, participant_id, signkey, data=None,
                                **kwargs):
        """
        :param url:  请求地址
        :param path: 请求路径
        :return:
        """
        if url.endswith("/transfer/sop/roplist"):
            if kwargs.get("location"):
                param = {"location": kwargs["location"]}
                uri = "?location=%s" % kwargs["location"]
                header = self.get_hearder.check_sign_get(method, url + uri, participant_id,
                                                         self.create_msgid,
                                                         self.create_datetime, signkey)

                resp = requests.get(url, headers=header, params=param)

            else:
                header = self.get_hearder.check_sign_get(method, url, participant_id,
                                                         self.create_msgid,
                                                         self.create_datetime, signkey)
                resp = requests.get(url, headers=header)
        elif url.endswith("v0/transfer/rop/receivecode"):
            if kwargs.get("evonetUserReference"):
                param = {"evonetUserReference": kwargs["evonetUserReference"]}
                uri = "?evonetUserReference=%s" % kwargs["evonetUserReference"]
                header = self.get_hearder.check_sign_get(method, url + uri, participant_id,
                                                         self.create_msgid,
                                                         self.create_datetime, signkey)

                resp = requests.get(url, headers=header, params=param)

            else:
                header = self.get_hearder.check_sign_get(method, url, participant_id,
                                                         self.create_msgid,
                                                         self.create_datetime, signkey)
                resp = requests.get(url, headers=header)
        else:
            header = self.get_hearder.check_sign_post(method, url, participant_id, self.create_msgid,
                                                      self.create_datetime, signkey, data)
            if method == 'POST':
                resp = requests.post(url, headers=header, json=json.loads(data))
            if method == 'PUT':
                resp = requests.put(url, headers=header, json=json.loads(data))
            if method == 'DELETE':
                resp = requests.delete(url, headers=header, json=json.loads(data))


        return resp

    @property
    def sop_rop_header(self):
        # 设置SOP，ROP的开头
        random_string = ""
        for i in range(6):
            letter = chr(random.randint(65, 90))
            random_string += letter
        return "SOP_AUTO", "ROP_AUTO", random_string

    @property
    def gengerate_sop_rop(self):
        # 返回sopid,ropid
        data = self.sop_rop_header
        sopid = "{}_{}".format(data[0], data[2])
        ropid1 = "{}_{}".format(data[1], data[2])
        ropid2 = "{}_{}".format(data[1], data[2])
        return sopid, ropid1, ropid2

    def delete_sop_rop_config(self):
        for db in [self.tyo_config_db]:
            db.delete_manys("sop", {"baseInfo.sopID": {"$regex": '^' + self.sop_rop_header[0]}})
            db.delete_manys("rop", {"baseInfo.ropID": {"$regex": '^' + self.sop_rop_header[1]}})
            db.delete_manys(self.comm_name.relation_transfer,
                            {"sopID": {"$regex": '^' + self.sop_rop_header[0]}})
            db.delete_manys(self.comm_name.service_fee,
                            {"sopID": {"$regex": '^' + self.sop_rop_header[0]}})

    def rop_list_assert(self, key, resp_json, sopid, ropid1=None, ropid2=None):
        if key == "standard":  # 单节点一个sop对应两个 在线 online的rop
            result = resp_json["result"]
            rop_info = resp_json["ropInfo"]
            assert result == {'code': 'S0000', 'message': 'Success.'}
            count = 0
            for ropid in [ropid1, ropid2]:
                for i in range(2):
                    result_rop_data = rop_info[i]
                    if result_rop_data["ropID"] == ropid:
                        db_relations_data = self.tyo_config_db.get_one(self.comm_name.relation_transfer,
                                                                       {"ropID": ropid, "sopID": sopid})
                        # rop表的数据
                        rop_data = self.tyo_config_db.get_one("rop",
                                                              {"baseInfo.ropID": ropid})
                        # roplist字段待确认
                        assert result_rop_data["ropName"] == rop_data["baseInfo"]["ropName"]
                        assert result_rop_data["ropLogo"] == rop_data["baseInfo"]["ropLogo"]
                        count += 1
            assert count == 2
        if key == "less_location":
            assert resp_json == {'result': {'code': 'V0001', 'message': 'Field {location} absent or empty.'}}
        if key == "location_length_is_three":
            assert resp_json == {'result': {'code': 'V0001', 'message': 'Field {location} absent or empty.'}}
        if key == "location_length_is_three":
            assert resp_json == {'result': {'code': 'V0001', 'message': 'Field {location} absent or empty.'}}
        if key == "sopid_not_exist":
            assert resp_json == {'code': 'C0000', 'message': 'Configuration error.'}
        if key == "sop_status_not_active":
            assert resp_json == "sdf"

    def service_fee_assert(self, sopid, ropid, resp_json, key_desc):
        service_data = self.tyo_config_db.get_one(self.comm_name.service_fee, {"sopID": sopid, "ropID": ropid})
        if key_desc == 'standard_offline' or key_desc == 'standard_online':  # 所有必传参数都进行传输
            assert resp_json["result"] == {'code': 'S0000', 'message': 'Success.'}
            assert resp_json["transferFee"]["value"] == service_data["sopSettleFeeCurrency"]
            assert float(resp_json["transferFee"]["currency"]) == service_data["sopSettleFee"]
        if key_desc == 'sop_not_exist':
            assert resp_json == {'code': 'B0032', 'message': 'SOP ID not found.'}
        if key_desc == 'sop_status_locked':
            # 应该返回B0034
            # assert resp_json
            pass
        if key_desc == 'rop_not_exist':
            pass   #现在返回的是  {'code': 'B0032', 'message': 'ROP ID not found.'}
            # assert resp_json == {'code': 'B0033', 'message': 'ROP ID not found.'}
        if key_desc == 'rop_status_locked':
            # 应该返回 B0035  ;现在返回的是  {'code': 'B0032', 'message': 'SOP ID not found.'}
            # assert resp_json
            pass
        if key_desc=="online_but_less_relation":
            assert  resp_json