import time

from base import db
from base.read_config import Conf
from base.encrypt import Encrypt
from base.read_file_path import ReadFile
from common.evopay.conf_init import db_tyo_evoconfig, db_sgp_evoconfig, evopay_conf, db_tyo_evopay, db_sgp_evopay
from common.evopay.mongo_initial import mongo_initial

from common.evopay.moudle import Moudle

# test_ini_file = ReadFile().read_ini_file(envirs="test", project="evopay")
from common.evosettle.mongo_data import Delete_Mongo_Data


class create_transfer_conf():
    def __init__(self):
        self.mongo = mongo_initial(db_tyo_evoconfig,type='transfer')
        # self.sop.settleInfo_settleCurrency = 'JPY'

    def create_sop_autotest_online_01(self):
        sopID, ropID = 'sop_autotest_online_01','rop_autotest_online_01'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID)

    def create_sop_autotest_online_sgd01(self):
        sopID, ropID = 'sop_autotest_online_sgd01','rop_autotest_online_sgd01'
        currency = 'SGD'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID,settleInfo_settleCurrency=currency)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID,ropFeeCurrency=currency,ropSettleFeeCurrency=currency)

    def create_sop_autotest_online_sek01(self):
        sopID,ropID = 'sop_autotest_online_sek01','rop_autotest_online_sek01'
        currency = 'SEK'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID,settleInfo_settleCurrency=currency)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID,sopFeeCurrency=currency,sopSettleFeeCurrency=currency)

    def create_sop_autotest_online_jpyjpy01(self):
        sopID,ropID = 'sop_autotest_online_jpyjpy01','rop_autotest_online_jpyjpy01'
        currency = 'JPY'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID,settleInfo_settleCurrency=currency)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID,settleInfo_settleCurrency=currency)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID,sopFeeCurrency=currency,sopSettleFeeCurrency=currency,ropFeeCurrency=currency,ropSettleFeeCurrency=currency)

    def create_sop_autotest_online_GBPNZD01(self):
        sopID,ropID = 'sop_autotest_online_GBP01','rop_autotest_online_NZD02'
        currency1 = 'GBP'
        currency2 = 'NZD'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID,settleInfo_settleCurrency=currency1)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID,settleInfo_settleCurrency=currency2)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID,sopFeeCurrency=currency1,sopSettleFeeCurrency=currency1,ropFeeCurrency=currency2,ropSettleFeeCurrency=currency2)

    def create_sop_autotest_online_VNDNZD01(self):
        sopID,ropID = 'sop_autotest_online_VND01','rop_autotest_online_NZD01'
        currency1 = 'VND'
        currency2 = 'NZD'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID,settleInfo_settleCurrency=currency1)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID,settleInfo_settleCurrency=currency2)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID,sopFeeCurrency=currency1,sopSettleFeeCurrency=currency1,ropFeeCurrency=currency2,ropSettleFeeCurrency=currency2)

    def create_sop_autotest_online_ZARDKK01(self):
        sopID,ropID = 'sop_autotest_online_ZAR01','rop_autotest_online_DKK01'
        currency1 = 'ZAR'
        currency2 = 'DKK'
        self.mongo.create_sop(baseInfo_sopID=sopID,baseInfo_sopName=sopID,settleInfo_settleCurrency=currency1)
        self.mongo.create_rop(baseInfo_ropID=ropID,baseInfo_ropName=ropID,settleInfo_settleCurrency=currency2)
        self.mongo.create_relationTransfer_online(sopID=sopID,ropID=ropID)
        self.mongo.create_serviceFee_online(sopID=sopID,ropID=ropID,sopFeeCurrency=currency1,sopSettleFeeCurrency=currency1,ropFeeCurrency=currency2,ropSettleFeeCurrency=currency2)

if __name__ == '__main__':



    db_tyo_evoconfig.delete_manys(table='sop', query_params={"baseInfo.sopID": {"$regex": "^sop_autotest"}})
    db_tyo_evoconfig.delete_manys(table='rop', query_params={"baseInfo.ropID": {"$regex": "^rop_autotest"}})
    db_tyo_evoconfig.delete_manys(table='relationTransfer', query_params={"sopID": {"$regex": "^sop_autotest"}})
    db_tyo_evoconfig.delete_manys(table='serviceFee', query_params={"sopID": {"$regex": "^sop_autotest"}})
    ex = create_transfer_conf()
    ex.create_sop_autotest_online_01()
    ex.create_sop_autotest_online_sek01()
    ex.create_sop_autotest_online_sgd01()
    ex.create_sop_autotest_online_GBPNZD01()
    ex.create_sop_autotest_online_jpyjpy01()
    ex.create_sop_autotest_online_VNDNZD01()
    ex.create_sop_autotest_online_ZARDKK01()