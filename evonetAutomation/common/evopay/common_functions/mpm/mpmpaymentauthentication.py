class MPMpaymentauthentication(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.MPMpaymentauthentication_Body = {
             "evonetReference": "#evonetReference#",
             "userData":{
                 "wopUserReference": "#autotest_data#"
             },
             "wopOrderNumber": "#wopOrderNumber#",
             "wopTransTime": "#wopTransTime#",
             "transAmount": {
                 "currency": "JPY",
                 "value": "23"}

        }
        self.MPMpaymentauthentication_Conf= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/wop/mpmpaymentauthentication"
        }

        self.MPMpaymentauthentication_Body_double = {
             "evonetReference": "#evonetReference#",
             "userData":{
                 "wopUserReference": "#autotest_data#"
             },
             "wopOrderNumber": "#wopOrderNumber#",
             "wopTransTime": "#wopTransTime#",
             "transAmount": {
                 "currency": "JPY",
                 "value": "23"}

        }
        self.MPMpaymentauthentication_Conf_double= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/wop/mpmpaymentauthentication"
        }


        self.MPMpayment_Body = {
                "userData": {
                    "wopUserReference": "WOP_Auto_JCoinPay_32",
                    "evonetUserReference": "WOP_Auto_JCoinPay_32"
                },
                "evonetReference": "#evonetReference#",
                "wopOrderNumber": "#wopOrderNumber#",
                "wopTransTime": "#wopTransTime#",
                "transAmount": {
                    "currency": "JPY",
                    "value": "23"
                }
            }


        self.MPMpayment_Conf= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_32",
            "mopParticipantID": "MOP_Auto_GrabPay_32",
            "url": r"/v0/payment/wop/mpmpayment"
        }

        self.MPMpayment_Body_double = {
                "userData": {
                    "wopUserReference": "WOP_Auto_JCoinPay_032",
                    "evonetUserReference": "WOP_Auto_JCoinPay_032"
                },
                "evonetReference": "#evonetReference#",
                "wopOrderNumber": "#wopOrderNumber#",
                "wopTransTime": "#wopTransTime#",
                "transAmount": {
                    "currency": "JPY",
                    "value": "23"
                }
            }


        self.MPMpayment_Conf_double= {
            "method": "post",
            "wopParticipantID": "WOP_Auto_JCoinPay_032",
            "mopParticipantID": "MOP_Auto_GrabPay_032",
            "url": r"/v0/payment/wop/mpmpayment"
        }

