import random, time, requests, json
import datetime
from common.evosettle.task_funcs import TaskFuncs
from base.read_config import *
from common.evosettle.database_operation import DatabaseOperations, DatabaseConnect
from common.evosettle.comm_funcs import CommonName
from common.evosettle.parmiko_module import Parmiko_Module
from base.encrypt import Aesecb, Encrypt
from common.evosettle.case_data import CaseData
from common.evopay.check_sign import CheckSign
from common.evopay.moudle import Moudle
from common.evopay.conf_init import db_tyo_evoconfig, db_sgp_evoconfig, evopay_conf, db_tyo_evopay, db_sgp_evopay
from common.evopay.mongo_initial import mongo_initial


class TransFerData(DatabaseConnect):
    def __init__(self, envirs, path=None, title=None):
        super(TransFerData, self).__init__(envirs, path=None, title=None)
        self.get_hearder = CheckSign()
        self.tyo_config_mongo_init = mongo_initial(db_tyo_evoconfig, type='transfer')
        self.sgp_config_mongo_init = mongo_initial(db_sgp_evoconfig, type='transfer')

    def sop_data(self, sopid, location):
        # 默认节点tyo
        self.tyo_config_mongo_init.create_sop(baseInfo_sopID=sopid, baseInfo_sopName=sopid, location=location)
        self.sgp_config_mongo_init.create_sop(baseInfo_sopID=sopid, baseInfo_sopName=sopid, location=location)

    def rop_data(self, ropid, rop_nodeid="tyo", location=None):
        self.tyo_config_mongo_init.create_rop(baseInfo_ropID=ropid, baseInfo_ropName=ropid, baseInfo_nodeID=rop_nodeid,
                                              location=location)
        self.sgp_config_mongo_init.create_rop(baseInfo_ropID=ropid, baseInfo_ropName=ropid, baseInfo_nodeID=rop_nodeid,
                                              location=location)

    def relation_trans_fer(self, sopid, ropid, type="online"):
        """
        :param sopid:
        :param ropid:
        :param type:  type ；online,  offline ;默认  online
        :return:
        """
        self.tyo_config_mongo_init.create_relationTransfer_online(sopID=sopid, ropID=ropid, type=type,location="CHN")
        self.sgp_config_mongo_init.create_relationTransfer_online(sopID=sopid, ropID=ropid, type=type,location="CHN")

    def service_fee(self, sopid, ropid, location):
        self.tyo_config_mongo_init.create_serviceFee_online(sopID=sopid, ropID=ropid, location=location)
        self.sgp_config_mongo_init.create_serviceFee_online(sopID=sopid, ropID=ropid, location=location)

    def transfer_config_data(self, sopid, ropid, location='tyo', nodeid="tyo", type='online'):
        """
        如果 nodeid 为tyo,会插入tyo的数据库
        如果 nodeid 为sgp,会插入sgp的数据库
        trans_fer的配置数据
        :param sopid:  sopid
        :param ropid: ropid
        :param nodeid:   节点
        :param type:   online ,offline
        :return: None
        """
        try:
            sop_data = self.sop_data(sopid, location)
        except Exception as e:
            print('数据已插入')
        try:
            rop_data = self.rop_data(ropid, nodeid, location)
        except Exception as e:
            print('数据已插入')
        try:
            relation_transfer_data = self.relation_trans_fer(sopid, ropid, type)
        except Exception as e:
            print('数据已插入')
        try:
            service_fee_data = self.service_fee(sopid, ropid, location)
        except Exception as e:
            print('数据已插入')

        # 向对应的表插入数据

    @property
    def create_msgid(self):
        return Moudle().create_msgId()

    @property
    def create_datetime(self):
        return Moudle().create_datetime()

    def request_account_data(self, sopid, user_reference):
        data_json = {
            "createUserParticipantID": sopid,
            "userInfo": {
                "userReference": user_reference,
                "userName": {
                    "userFirstName": "first.name",
                    "userMidName": "walke.middle",
                    "userLastName": "last.name"
                },
                "identity": {
                    "idType": "passport",  # 数组 Valid values:"identificationCard"，"passport"
                    "idNumber": "passport_0001"
                },
                "residentialAddress": {
                    "address": "Road",
                    "city": "ShangHai",
                    "region": "CN",
                    "postalCode": "0010",
                    "country": "ShangHai"
                },
                "phoneNumber": "110",
                "email": "wang@gmail.com",
                "gender": "female",
                "nationality": "CN",
                "dateOfBirth": "2020",
                "countryOfBirth": "CN",
                "occupation": "CC",
                "bankName": "BOC",
                "bankAccount": "110",
                "bankSwiftCode": "110"
            }
        }
        return data_json

    def rop_list_param(self):
        data = [("sop_evopay_walker", "rop_evopay_walker_one", 'rop_evopay_walker_twop', 'standad')]
        return data
# if __name__ == '__main__':
#     sk = TransFerFunc("test")
#     sk.transfer_config_data("sop_evopay_walker", "rop_evopay_walker", nodeid='sgp')
