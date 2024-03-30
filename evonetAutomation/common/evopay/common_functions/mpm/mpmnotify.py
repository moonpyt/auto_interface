class MPMnotify(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.notify_Body = {
            "evonetOrderNumber": "#evonetOrderNumber#",
            "evonetOrderCreateTime": "#evonetOrderCreateTime#",
            "userPayTime": "#userPayTime#",
            "transResult":
                {"status": "succeeded",
                 "message": "Success"}
        }

        self.notify_Conf= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/wop/paymentnotification"
        }
        self.notify_Body_double = {
            "evonetOrderNumber": "#evonetOrderNumber#",
            "evonetOrderCreateTime": "#evonetOrderCreateTime#",
            "userPayTime": "#userPayTime#",
            "transResult":
                {"status": "succeeded",
                 "message": "Success"}
        }
        self.notify_Conf_double= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/wop/paymentnotification"
        }
