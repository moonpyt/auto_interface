class Inquiry(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.Inquiry_Body = {
            "evonetOrderNumber": "#MPMevonetOrderNumber"
        }

        self.Inquiry_Conf= {
            "method": "get",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/mop/paymentinquiry?evonetOrderNumber=#MPMevonetOrderNumber#"
        }
        self.Inquiry_Body_Common = {
            "evonetOrderNumber": "#evonetOrderNumber"
        }

        self.Inquiry_Conf_Common= {
            "method": "get",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/mop/paymentinquiry?evonetOrderNumber=#evonetOrderNumber#"
        }

        self.Inquiry_Body_double = {
            "evonetOrderNumber": "#MPMevonetOrderNumber"
        }

        self.Inquiry_Conf_double= {
            "method": "get",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/mop/paymentinquiry?evonetOrderNumber=#MPMevonetOrderNumber#"
        }
        self.Inquiry_Body_Common_double = {
            "evonetOrderNumber": "#evonetOrderNumber"
        }

        self.Inquiry_Conf_Common_double= {
            "method": "get",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/mop/paymentinquiry?evonetOrderNumber=#evonetOrderNumber#"
        }

