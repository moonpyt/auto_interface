from common.evopay.conf_init import db_tyo_evoconfig
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment
from common.evopay.replace_data import case
from loguru import logger as log


class external_send_trans:
    def __init__(self,transAmount=23000000001,transCurrency='CNY',wopID='WOP_Auto_JCoinPay_01',mopID='MOP_Auto_GrabPay_01'):
        self.transAmount = transAmount
        self.wopID = wopID
        self.mopID = mopID
        self.transCurrency = transCurrency
    def send_trans(self,interface='CPM'):
        test_info = {}
        wopParticipantID = self.wopID
        mopParticipantID = self.mopID
        test_info['pre-update table'] = None
        test_info['conf'] = None
        test_info['update_mongo'] = None
        test_info['test_id'] = '7777'
        test_info['pre-update mongo'] =None
        test_info["check_mongo_expected"] = ''

        query_params = {"baseInfo.mopID":mopParticipantID}
        mop_result = db_tyo_evoconfig.get_one("mop",query_params)
        if mop_result:
            brandID = mop_result["baseInfo"]["brandID"]
            brandID = brandID.replace("\'","\"")
            nodeID = mop_result['baseInfo']['nodeID']
        else:
            brandID = "Auto_GrabPay_01"
            nodeID = "tyo"

        if nodeID=='sgp':
            nodeID = "double"
        else:
            nodeID = "single"


        qr_query_params = {"mopID":self.mopID}
        qr_result = db_tyo_evoconfig.get_one('mpmQrIdentifier',qr_query_params)
        if qr_result:
            qrPayload = qr_result['qrIdentifier']
        else:
            qrPayload = "https://AutoGrabPay01.com"


        common_params = dict(wopParticipantID=wopParticipantID,mopParticipantID=mopParticipantID)
        test_info.update(common_params)

        if interface == 'CPM':
            #发起cpm_token交易
            result = self.post_cpmToken(brandID,test_info,nodeID)
            mopToken = result['mopToken']
            for item in mopToken:
                if item['type'] == 'Barcode':
                    mopToken_barcode_value = item['value']
                    setattr(case, 'mopToken', mopToken_barcode_value)
                else:
                    mopToken_quickResponseCode_value = item['value']
                    setattr(case, 'mopToken', mopToken_quickResponseCode_value)
            #发起cpm payment交易
            result = self.post_cpmPayment(test_info,nodeID)
            return result['evonetOrderNumber']



    def post_cpmToken(self,brandID,test_info,nodeID):
        test_info["interface"] = 'CPM Token'
        test_info["data"]="{}".format({"brandID":brandID})
        test_info["data"] = test_info["data"].replace("\'","\"")
        log.debug(f'构造的test_info的数据为{test_info}')
        cpmtoken = Testcpmtoken('testing')
        body_params, head_params = cpmtoken.common_params_init(test_info,node=nodeID)
        # 获取URL
        res = cpmtoken.post_cpmtoken(test_info, head_params, body_params,node=nodeID)
        result = res.json()
        return result

    def post_cpmPayment(self,test_info,nodeID):
        test_info["interface"] = 'CPM Payment'
        test_info["data"] = str({"transAmount": {"currency": self.transCurrency, "value": self.transAmount}})
        test_info["data"] = test_info["data"].replace("\'","\"")
        log.debug(f'构造的test_info的数据为{test_info}')
        cpmpayment = Testcpmpayment('testing')
        body_params, head_params = cpmpayment.common_params_init(test_info,node=nodeID)
        res, config_currency = cpmpayment.post_cpmpayment(test_info, head_params, body_params,node=nodeID)
        result = res.json()
        return result

    def post_mpmqrverification(self):
        pass

    def post_mpmpaymentauthentication(self):
        pass

    def post_mpmpaymentnotify(self):
        pass

    def post_refund(self):
        pass

    def post_inquiry(self):
        pass

    def post_cancel(self):
        pass

if __name__ == '__main__':
    example = external_send_trans(transAmount=1300,transCurrency='JPY',wopID='WOP_Auto_JCoinPay_01',mopID='MOP_Auto_GrabPay_01')
    print(example.send_trans())