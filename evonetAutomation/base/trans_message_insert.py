from common.evopay.conf_init import db_tyo_evopay, db_tyo_evosettle, db_tyo_evoconfig
import random
import time,datetime

class trans_message_insert():
    def __init__(self):
        self.db = db_tyo_evosettle


    def crate_orderNum(self, length=18):
        """ 随机数生成32位订单号
        """
        chars = '0123456789'
        order = ''
        for i in range(length):
            index = random.randint(0, len(chars)) - 1
            order += chars[index]
        return order


    def creat_mongo_time(self):
        dt = datetime.datetime.utcnow()
        return dt

    def get_settdate(self):
        dt = datetime.datetime.today()
        return dt.strftime("%Y%m%d")

    def get_fxRateRefID(self):
        fxrate_query = {"fxRateSource": "MDAQ", "ccy1": "SGD","ccy2": "USD"}
        fxRateRefID = db_tyo_evoconfig.get_one(table='fx_rate', query_params=fxrate_query)["refID"]
        return fxRateRefID

    def create_sale_trans(self,n=1):
        temp = []
        for i in range(0,n):
            insert_params = {}
            insert_params['evonetOrderNumber'] = self.crate_orderNum()
            insert_params['transType'] =  "CPM Payment"
            insert_params['wopID']=  "MDAQ_WOP_01"
            insert_params['mopID'] = "bccardnacfusd"
            insert_params["wopSettleCurrency"] = "USD"
            insert_params["wopSettleAmount"] = 3263.0
            insert_params["mopSettleCurrency"] = "SGD"
            insert_params["mopSettleAmount"] = 39.97
            insert_params["fxRateRefID"] = self.get_fxRateRefID()
            insert_params["fxRateCcyPair"] = "SGD/USD"
            insert_params["fxRateSource"] = "MDAQ"
            insert_params["settleDate"] = self.get_settdate()
            insert_params["beneficiary"] = "bccardnacfusd"
            insert_params["evonetPayTime"] = self.creat_mongo_time()
            insert_params["createTime"] = self.creat_mongo_time()
            temp.append(insert_params)
        self.db.insert_many('trans_message',temp)
        return insert_params['evonetOrderNumber']


    def creat_refund_trans(self,n=1):
        temp = []
        for i in range(0,n):
            insert_params = {}
            insert_params['evonetOrderNumber'] = self.crate_orderNum()
            insert_params['transType'] =  "Refund"
            insert_params['wopID']=  "MDAQ_WOP_01"
            insert_params['mopID'] = "bccardnacfusd"
            insert_params["wopSettleCurrency"] = "USD"
            insert_params["wopSettleAmount"] = 3263.0
            insert_params["mopSettleCurrency"] = "SGD"
            insert_params["mopSettleAmount"] = 39.97
            insert_params["fxRateRefID"] = self.get_fxRateRefID()
            insert_params["fxRateCcyPair"] = "SGD/USD"
            insert_params["fxRateSource"] = "MDAQ"
            insert_params["settleDate"] = self.get_settdate()
            insert_params["beneficiary"] = "bccardnacfusd"
            insert_params["evonetPayTime"] = self.creat_mongo_time()
            insert_params["createTime"] = self.creat_mongo_time()
            insert_params['origEvonetOrderNumber'] = self.create_sale_trans(n=1)
            temp.append(insert_params)
        self.db.insert_many('trans_message', temp)
        return insert_params['evonetOrderNumber'],insert_params['origEvonetOrderNumber']

if __name__ == '__main__':
    # a = trans_message_insert().creat_refund_trans(n=10)
    # b = trans_message_insert().create_sale_trans(n=10)
    # print(a,b)
    print(trans_message_insert().get_fxRateRefID())