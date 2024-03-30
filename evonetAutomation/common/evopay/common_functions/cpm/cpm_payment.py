



class CPM_Payment_Message(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.CPM_Token_Body = {
            "brandID":"Auto_GrabPay_01",
            "userData":
                {"wopUserReference": "weixinweixin_01",
                 "wopToken": "123456"}
        }
        self.CPM_Token_Conf= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID" : "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/wop/cpmtoken"
        }
        self.CPM_Payment_Body = {
             "mopToken": {"value": "#mopToken#"},
             "mopOrderNumber": "#mopOrderNumber#",
             "mopTransTime": "#mopTransTime#",
             "transAmount": {"currency": "JPY", "value": "23"},
             "storeInfo": {"id": "auto storeId", "localName": "auto localName", "mcc": "7011"}
        }

        self.CPM_Payment_Conf= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/mop/cpmpayment"
        }

        self.CPM_Token_Body = {
            "brandID":"Auto_GrabPay_01",
            "userData":
                {"wopUserReference": "weixinweixin_01",
                 "wopToken": "123456"}
        }
        self.CPM_Token_Conf= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID" : "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/wop/cpmtoken"
        }
        self.CPM_Payment_Body_double = {
             "mopToken": {"value": "#mopToken#"},
             "mopOrderNumber": "#mopOrderNumber#",
             "mopTransTime": "#mopTransTime#",
             "transAmount": {"currency": "JPY", "value": "23"},
             "storeInfo": {"id": "auto storeId", "localName": "auto localName", "mcc": "7011"}
        }

        self.CPM_Payment_Conf_double= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/mop/cpmpayment"
        }