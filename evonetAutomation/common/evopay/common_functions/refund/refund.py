class Refund(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.Refund_Body = {
        "originalEvonetOrderNumber": "#originalEvonetOrderNumber#",
        "mopOrderNumber": "#mopOrderNumber#",
        "mopTransTime": "#mopTransTime#",
        "transAmount":
            {"currency": "JPY",
             "value": "23"}
        }

        self.Refund_Conf= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/mop/refund"
        }

        self.Refund_Body_double = {
        "originalEvonetOrderNumber": "#originalEvonetOrderNumber#",
        "mopOrderNumber": "#mopOrderNumber#",
        "mopTransTime": "#mopTransTime#",
        "transAmount":
            {"currency": "JPY",
             "value": "23"}
        }

        self.Refund_Conf_double= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/mop/refund"
        }
