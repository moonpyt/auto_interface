
class Mop_Checking(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.Mop_checking_Body = {
            "location": "JPN"
        }
        self.Mop_checking_Conf= {
            "method":"get",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/wop/mopchecking?location=JPN"
        }

        self.Mop_checking_Body_double = {
            "location": "JPN"
        }
        self.Mop_checking_Conf_double= {
            "method":"get",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/wop/mopchecking?location=JPN"
        }