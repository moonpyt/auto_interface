class Cancel(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.Cancel_Body = {
            "evonetOrderNumber": "#originalEvonetOrderNumber#"
        }

        self.Cancel_Conf= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/mop/cancellation"
        }

        self.Cancel_Body_double = {
            "evonetOrderNumber": "#originalEvonetOrderNumber#"
        }

        self.Cancel_Conf_double= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/mop/cancellation"
        }