class transfer_common_values(object):
    def __init__(self):
        '''
        初始化所有的必填项，不包含可填项

        '''

        #汇率单节点查询body默认参数
        self.QueryFxRate_body_single = {
        "sendCurrency": "CNY",
        "receiveCurrency": "CAD",
        "participantID": "rop_autotest_online_01"
        }

        # 汇率单节点查询head默认参数
        self.QueryFxRate_conf_single= {
            "method":"post",
            "participantID": "sop_autotest_online_01",
            "conf_signkeyc" : "9fce499557bd463271b758389981692c",
            "body_signkeyc" : "9fce499557bd463271b758389981692c",
            "url": r"/v0/transfer/sop/fxrate"
        }

        #汇率单节点查询body默认参数
        self.PreOrder_body_single = {
            "sopOrderNumber": "#sopOrderNumber#",
            "sopOrderDateTime": "#sopOrderDateTime#",
            "participantID": "rop_autotest_online_01",
            "location": "JPN",
            "type": "Online",
            "purpose": "E-commerce business dealings",
            "relationship": "business partner",
            "sourceOfFund": "wage",
            "senderInfo": {
                "evonetUserReference": "?senderInfo.evonetUserReference?"
            },
            "receiverInfo": {
                "evonetUserReference": "?receiverInfo.evonetUserReference?"
            },
            "sendAmount": {
                "value": "100.00",
                "currency": "CNY"
            },
            "transferFee": {
                "value": "0.1",
                "currency": "CNY"
            },
            "senderTotalAmount": {
                "value": "100.01",
                "currency": "CNY"
            },
            "receiveAmount": {
                "currency": "CAD",
                "value": "100.01",

            },
            "fxRate": {
                "value": "?fxrate_value?",
                "sourceCurrency": "CNY",
                "destinationCurrency": "CAD",
            }
            }

        # 汇率单节点查询head默认参数
        self.PreOrder_conf_single= {
            "method":"post",
            "participantID": "sop_autotest_online_01",
            "conf_signkeyc" : "9fce499557bd463271b758389981692c",
            "body_signkeyc" : "9fce499557bd463271b758389981692c",
            "url": r"/v0/transfer/sop/preorder"
        }

        self.accountCreate_body_single = {
        "createUserParticipantID": "sop_autotest_online_01",
        "userInfo": {
        "bankAccount": "110",
        "bankName": "BOC",
        "bankSwiftCode": "110",
        "countryOfBirth": "CHN",
        "dateOfBirth": "2020-01-01",
        "email": "wang@gmail.com",
        "gender": "female",
        "identity": {
            "idNumber": "passport_0001",
            "idType": "passport"
        },
        "nationality": "CHN",
        "occupation": "CC",
        "phoneNumber": "110",
        "residentialAddress": {
            "address": "Road",
            "city": "ShangHai",
            "country": "ShangHai",
            "postalCode": "0010",
            "region": "CN"
        },
        "userName": {
            "userFirstName": "wang",
            "userLastName": "zhengzhi",
            "userMidName": ""
        },
        "userReference": "#userReference#"
        }
        }


        self.accountCreate_conf_single = {
            "method": "post",
            "participantID": "sop_autotest_online_01",
            "conf_signkeyc": "9fce499557bd463271b758389981692c",
            "body_signkeyc": "9fce499557bd463271b758389981692c",
            "url": r"/v0/transfer/sop/account"
        }

        self.order_body_single = {
            "evonetOrderNumber": "734310033998750709"
        }
        self.order_conf_single = {
            "method": "post",
            "participantID": "sop_autotest_online_01",
            "conf_signkeyc": "9fce499557bd463271b758389981692c",
            "body_signkeyc": "9fce499557bd463271b758389981692c",
            "url": r"/v0/transfer/sop/order"
        }

if __name__ == '__main__':
    a ={
    "createUserParticipantID": "rop_autotest_online_01",
    "userInfo": {
        "userReference": "rop_autotest_online_01",
        "userName": {
            "userFirstName": "wang",
            "userMidName": "",
            "userLastName": "zhengzhi"
        },
        "identity": {
            "idType": "passport",
            "idNumber": "passport_0001"
        }}}
    a.update({"userReference": "rop_aut1nline_01",})
    # a["userInfo"]["userName"].update({"userMidName": "123"})
    print(a)

