class MPMqrverify(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.MPMqrverify_Body = {
            "brandID": "Auto_GrabPay_01",
             "userData":{
                  "wopUserReference": "#autotest_data#",
                  "evonetUserReference": "#autotest_data#"
             },
             "qrPayload": r"https://AutoGrabPay01.com",
             "location": "JPN"
        }





        self.MPMqrverify_Conf= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/wop/mpmqrverification"
        }

        self.MPMqrverify_Body_double = {
            "brandID": "Auto_GrabPay_001",
             "userData":{
                  "wopUserReference": "#autotest_data#",
                  "evonetUserReference": "#autotest_data#"
             },
             "qrPayload": r"https://AutoGrabPay001.com",
             "location": "JPN"

        }
        self.MPMqrverify_Conf_double= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/wop/mpmqrverification"
        }
