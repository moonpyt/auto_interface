import requests
import json
import pytest

class CPM_Token_Message(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''
        self.CPM_Token_Body = {
            "brandID":"Auto_GrabPay_01",
            "userData": {
                "wopUserReference": "WOP_Auto_JCoinPay_01",
                "wopToken": "{{wopToken}}",
                "evonetUserReference": "WOP_Auto_JCoinPay_01"
            }
        }
        self.CPM_Token_Conf= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_01",
            "mopParticipantID": "MOP_Auto_GrabPay_01",
            "url": r"/v0/payment/wop/cpmtoken"
        }

        self.CPM_Token_Body_double = {
            "brandID":"Auto_GrabPay_001",
            "userData": {
                "wopUserReference": "WOP_Auto_JCoinPay_001",
                "wopToken": "{{wopToken}}",
                "evonetUserReference": "WOP_Auto_JCoinPay_001"
            }
        }
        self.CPM_Token_Conf_double= {
            "method":"post",
            "wopParticipantID": "WOP_Auto_JCoinPay_001",
            "mopParticipantID": "MOP_Auto_GrabPay_001",
            "url": r"/v0/payment/wop/cpmtoken"
        }


# if __name__ == '__main__':
#     url = "https://tyo-testing-api.pre-evonetonline.com/v0/payment/wop/cpmtoken"
#     head = {
#         "participantID":"WOP_Auto_JCoinPay_001",
#         "msgID" : "2020212312131212111",
#         "Content-Type" : "application/json",
#         "DateTime" : "20210125141959+0800",
#         "SignType" : "SHA256",
#         "Signature" : "123"
#     }
#     body = CPM_Token_Message().evonet_body
#     s = json.dumps(body)
#     res = requests.post(url=url,data=s,headers = head)
#     print(res.json())


