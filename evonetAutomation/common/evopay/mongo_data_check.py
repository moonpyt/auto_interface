# -*- coding: utf-8 -*-

import time
#CPM交易基础数据校验字段
trans_basic_CPM=['traceID','mopOrderNumber','wopOrderNumber','evonetOrderNumber','mopTransTime','wopTransTime','evonetOrderCreateTime','evonetOrderUpdateTime','wopPayTime','evonetPayTime','mopSettleDate','wopSettleDate','wopConverterCurrencyFlag','mopConverterCurrencyFlag','transAmount','transCurrency','status','wopStatus','mopStatus','userData','storeInfo','transType','category','wopID','mopID','mopToken','apiVersion','result','lockFlag']
trans_basic_CPM_failed=['traceID','mopOrderNumber','evonetOrderNumber','mopTransTime','evonetOrderCreateTime','evonetOrderUpdateTime','wopConverterCurrencyFlag','mopConverterCurrencyFlag','transAmount','transCurrency','status','wopStatus','mopStatus','storeInfo','transType','category','mopID','mopToken','apiVersion','result','lockFlag']

#MPM Notification交易基础数据校验字段
trans_basic_MPMNotification=['traceID','mopOrderNumber','wopOrderNumber','evonetOrderNumber','mopTransTime','wopTransTime','evonetPayTime','evonetOrderCreateTime','evonetOrderUpdateTime','mopSettleDate','wopSettleDate','wopConverterCurrencyFlag','mopConverterCurrencyFlag','transAmount','transCurrency','status','wopStatus','mopStatus','userData','storeInfo','transType','category','wopID','mopID','apiVersion','lockFlag','wopPayTime']
trans_basic_MPMNotification_failed = ['traceID','mopOrderNumber','wopOrderNumber','evonetOrderNumber','mopTransTime','wopTransTime','evonetOrderCreateTime','evonetOrderUpdateTime','mopSettleDate','wopSettleDate','wopConverterCurrencyFlag','mopConverterCurrencyFlag','transAmount','transCurrency','status','wopStatus','mopStatus','userData','storeInfo','transType','category','wopID','mopID','apiVersion','lockFlag']
#MPM Authentication交易基础数据校验字段
trans_basic_MPMAuthentication=['traceID','mopOrderNumber','wopOrderNumber','evonetOrderNumber','mopTransTime','wopTransTime','evonetOrderCreateTime','evonetOrderUpdateTime','wopConverterCurrencyFlag','mopConverterCurrencyFlag','transAmount','transCurrency','status','userData','storeInfo','transType','category','wopID','mopID','apiVersion','lockFlag']

#Refund交易成功基础数据校验字段
trans_basic_Refund=['traceID','mopOrderNumber','wopOrderNumber','evonetOrderNumber','mopTransTime','wopTransTime','evonetOrderCreateTime','evonetOrderUpdateTime','wopPayTime','evonetPayTime','mopSettleDate','wopSettleDate','wopConverterCurrencyFlag','mopConverterCurrencyFlag','originalEVONETOrderNumber','originalWOPOrderNumber','originalMOPOrderNumber','transAmount','transCurrency','status','wopStatus','mopStatus','storeInfo','transType','category','wopID','mopID','apiVersion','result','lockFlag']
#Refund交易wop失败基础数据校验字段
trans_basic_Refund_wop_failed=['traceID','mopOrderNumber','evonetOrderNumber','mopTransTime','evonetOrderCreateTime','evonetOrderUpdateTime','evonetPayTime','mopSettleDate','wopSettleDate','wopConverterCurrencyFlag','mopConverterCurrencyFlag','originalEVONETOrderNumber','originalWOPOrderNumber','originalMOPOrderNumber','transAmount','transCurrency','status','wopStatus','mopStatus','storeInfo','transType','category','wopID','mopID','apiVersion','result','lockFlag']

#MPM QR Verification 交易transReference表基础数据校验字段
transReference_basic=['evonetReference','isUsed','storeInfo','transAmount','wopID','mopID','mopQr','mopQrType','createTime','updateTime','deleteFlag']
#trans表result下基础数据校验字段
result=['code','message']
#CPM交易trans表userData下基础数据校验字段
userData_CPM=['wopUserReference','wopToken']
#MPM交易trans表userData下基础数据校验字段
userData_MPM=['wopUserReference']
#trans表storeInfo下基础数据校验字段
storeInfo=['id','localName','mcc']
#trans表wopSettleAmount下基础数据校验字段
wopSettleAmount_currency_transfer=['wopSettleAmount','wopSettleCurrency','wopBaseSettleFXRate','wopSettleFXRate','wopSettleSourceCurrency','wopSettleDestinationCurrency','wopSettleFXRateDate','wccr']
wopSettleAmount_currency_transfer_SourceDesCurrencySame=['wopSettleAmount','wopSettleCurrency','wopBaseSettleFXRate','wopSettleFXRate','wopSettleSourceCurrency','wopSettleDestinationCurrency','wccr']
wopSettleAmount=['wopSettleAmount','wopSettleCurrency']

#trans表mopSettleAmount下基础数据校验字段
mopSettleAmount_currency_transfer=['mopSettleAmount','mopSettleCurrency','mopBaseSettleFXRate','mopSettleFXRate','mopSettleSourceCurrency','mopSettleDestinationCurrency','mopSettleFXRateDate','mccr']
mopSettleAmount=['mopSettleAmount','mopSettleCurrency']

#trans表billingAmount下基础数据校验字段
billingAmount_currency_transfer=['billingAmount','billingCurrency','billingFXRate','billingSourceCurrency','billingDestinationCurrency','billingFXRateDate','cccr']
billingAmount=['billingAmount','billingCurrency','billingFXRate','billingSourceCurrency','billingDestinationCurrency']
billingAmount_currency_transfer_SourceDesCurrencySame=['billingAmount','billingCurrency','billingFXRate','billingSourceCurrency','billingDestinationCurrency','cccr']



#CPM Token 交易tokenValue表基础数据校验字段
tokenValue_basic=['wopID','mopID','qrList','isUsed','userData','createTime','updateTime','deleteFlag']
#CPM Token交易tokenValue表userData字段下的基础数据校验字段
userData_CPMToken=['evonetUserReference','wopUserReference']
#CPM Token交易tokenValue表userData.card字段下的基础数据校验字段
userData_card_CPMToken=['networkTokenPan']
#CPM Token交易tokenValue表transAmount字段下的基础数据校验字段
transAmount=['value','currency']
class Checkmongo():

    def is_true(self,data_params):
        if data_params:
            return True

        if data_params in [False,True]:
            return True

        else:
            return False

        # 断言CPM Token接口数据库存储数据
    def check_CPMToken_mongo(self, test_data_interface,db_data):
        if test_data_interface == "CPM Token":

            # db_data=self.db.get_one(mongo_table,query_params)
            try:
                for item in tokenValue_basic:
                    assert self.is_true(db_data[item]) == True

            except AssertionError as e:
                print("CPM Token-tokenVault表数据存储错误")
                raise e
        # 断言trans表数据库存储数据
    def check_trans_mongo(self, test_data_interface,db_data):
        if test_data_interface == "CPM Payment":
            if db_data['result']['code']=='S0000':


                #首先检验trans表基础信息
                try:
                    for item in trans_basic_CPM:
                        assert self.is_true(db_data[item])== True

                    for item in userData_CPM:
                        assert self.is_true(db_data['userData'][item])== True

                    for item in storeInfo:
                        assert self.is_true(db_data['storeInfo'][item]) == True
                    for item in result:
                        assert self.is_true(db_data['result'][item]) == True
                    #如果计算了wopSettleAmout，校验里面的数值是否存在
                    try:

                        if 'wopSettleAmount' in db_data:
                            if db_data['wopConverterCurrencyFlag']==True :
                                if db_data['wopSettleSourceCurrency']!=db_data['wopSettleDestinationCurrency']:
                                    for item in wopSettleAmount_currency_transfer:
                                        assert self.is_true(db_data[item]) == True
                                else:
                                    for item in wopSettleAmount_currency_transfer_SourceDesCurrencySame:
                                        assert self.is_true(db_data[item]) == True
                            else:
                                    for item in wopSettleAmount:
                                        assert self.is_true(db_data[item]) == True

                        elif 'mopSettleAmount' in db_data:
                            if db_data['mopConverterCurrencyFlag'] == True:
                                for item in mopSettleAmount_currency_transfer:
                                    assert self.is_true(db_data[item]) == True
                            else:
                                for item in mopSettleAmount:
                                    assert self.is_true(db_data[item]) == True

                        elif 'billingAmount' in db_data:
                            if db_data['billingSourceCurrency'] != db_data['billingDestinationCurrency']:
                                for item in billingAmount_currency_transfer:

                                    assert self.is_true(db_data[item]) == True
                            else:
                                for item in billingAmount_currency_transfer_SourceDesCurrencySame:
                                    assert self.is_true(db_data[item]) == True
                        else:
                            print("无清算金额校验")
                    except AssertionError as e:
                        print("清算金额校验失败")
                        raise e

                except AssertionError as e:
                    print("CPM Payment成功的交易trans表检验失败")
                    raise e
            else:
                try:
                    for item in trans_basic_CPM_failed:
                        assert self.is_true(db_data[item]) == True

                    for item in storeInfo:
                        assert self.is_true(db_data['storeInfo'][item]) == True
                    for item in result:
                        assert self.is_true(db_data['result'][item]) == True
                except AssertionError as e:
                    print("CPM Payment失败的交易trans表检验失败")
                    raise e



        #校验MPM Payment Authentication trans表交易
        elif test_data_interface == "MPM Payment Authentication":

            #首先检验trans表基础信息
            try:
                for item in trans_basic_MPMAuthentication:
                    assert self.is_true(db_data[item])==True
                    # for item in userData_MPM:
                    #     assert self.is_true(db_data['userData'][item])==True
                for item in storeInfo:
                    assert self.is_true(db_data['storeInfo'][item]) == True


                #如果计算了wopSettleAmout，校验里面的数值是否存在
                try:

                    if 'wopSettleAmount' in db_data:
                        if db_data['wopConverterCurrencyFlag']==True :
                            if db_data['wopSettleSourceCurrency']!=db_data['wopSettleDestinationCurrency']:
                                for item in wopSettleAmount_currency_transfer:
                                    assert self.is_true(db_data[item]) == True
                            else:
                                for item in wopSettleAmount_currency_transfer_SourceDesCurrencySame:
                                    assert self.is_true(db_data[item]) == True
                        else:
                            for item in wopSettleAmount:
                                assert self.is_true(db_data[item]) == True

                    elif 'mopSettleAmount' in db_data:
                        if db_data['mopConverterCurrencyFlag'] == True:
                            for item in mopSettleAmount_currency_transfer:
                                assert self.is_true(db_data[item]) == True
                        else:
                            for item in mopSettleAmount:
                                assert self.is_true(db_data[item]) == True

                    elif 'billingAmount' in db_data:
                        if db_data['billingSourceCurrency'] != db_data['billingDestinationCurrency']:
                            for item in billingAmount_currency_transfer:

                                assert self.is_true(db_data[item]) == True
                        else:
                            for item in billingAmount_currency_transfer_SourceDesCurrencySame:
                                assert self.is_true(db_data[item]) == True
                    else:
                        print("无清算金额校验")
                except AssertionError as e:
                    print("清算金额校验失败")
                    raise e
            except AssertionError as e:
                print("MPM Payment Authentication交易trans表检验失败")
                raise e
        elif test_data_interface == "Payment Notification":
            if db_data['result']['code'] == 'S0000' and db_data['status'] == 'successed':

                # 首先检验trans表基础信息
                try:
                    a = db_data
                    print(a)
                    for item in trans_basic_MPMNotification:
                        assert self.is_true(db_data[item]) == True

                    for item in storeInfo:
                        assert self.is_true(db_data['storeInfo'][item]) == True
                except AssertionError as e:
                    print("Payment Notification交易trans表检验失败")
                    raise e
            else:
                try:
                    for item in trans_basic_MPMNotification_failed:
                        assert self.is_true(db_data[item]) == True

                    for item in storeInfo:
                        assert self.is_true(db_data['storeInfo'][item]) == True
                    for item in result:
                        assert self.is_true(db_data['result'][item]) == True
                except AssertionError as e:
                    print("CPM Payment失败的交易trans表检验失败")
                    raise e
        elif test_data_interface == "Refund":

            # 首先检验trans表基础信息
            try:
                if db_data['status']=='succeeded' and db_data['wopStatus']=='succeeded' and  db_data['mopStatus']=='succeeded':
                    for item in trans_basic_Refund:
                        assert self.is_true(db_data[item]) == True
                    for item in storeInfo:
                        assert self.is_true(db_data['storeInfo'][item]) == True
                    for item in result:
                        assert self.is_true(db_data['result'][item]) == True
                elif db_data['status']=='succeeded' and db_data['wopStatus']=='failed' and  db_data['mopStatus']=='succeeded':
                    for item in trans_basic_Refund_wop_failed:
                        assert self.is_true(db_data[item]) == True
                    for item in storeInfo:
                        assert self.is_true(db_data['storeInfo'][item]) == True
                    for item in result:
                        assert self.is_true(db_data['result'][item]) == True
                # 如果计算了wopSettleAmout，校验里面的数值是否存在
                try:

                    if 'wopSettleAmount' in db_data:
                        if db_data['wopConverterCurrencyFlag']==True :
                            if db_data['wopSettleSourceCurrency']!=db_data['wopSettleDestinationCurrency']:
                                for item in wopSettleAmount_currency_transfer:
                                    assert self.is_true(db_data[item]) == True
                            else:
                                for item in wopSettleAmount_currency_transfer_SourceDesCurrencySame:
                                    assert self.is_true(db_data[item]) == True
                        else:
                            if db_data['mopSettleSourceCurrency'] != db_data['mopSettleDestinationCurrency']:
                                for item in wopSettleAmount:
                                    assert self.is_true(db_data[item]) == True

                    elif 'mopSettleAmount' in db_data:
                        if db_data['mopConverterCurrencyFlag'] == True:
                            for item in mopSettleAmount_currency_transfer:
                                assert self.is_true(db_data[item]) == True
                        else:
                            for item in mopSettleAmount:
                                assert self.is_true(db_data[item]) == True

                    elif 'billingAmount' in db_data:
                        if db_data['billingSourceCurrency'] != db_data['billingDestinationCurrency']:
                            for item in billingAmount_currency_transfer:

                                assert self.is_true(db_data[item]) == True
                        else:
                            for item in billingAmount_currency_transfer_SourceDesCurrencySame:
                                assert self.is_true(db_data[item]) == True
                    else:
                        print("无清算金额校验")
                except AssertionError as e:
                    print("Refund交易trans表检验失败")
                    raise e
            except AssertionError as e:
                print("Refund交易trans表检验失败")
                raise e
        else:
            print("测试数据超出以上接口校验")
    # 断言trans表数据库存储数据
    def check_transReference_mongo(self, test_data_interface, db_data):
        if test_data_interface == "MPM QR Verification":


            try:
                for item in transReference_basic:
                    assert self.is_true(db_data[item]) == True
                for item in transAmount:
                    assert self.is_true(db_data['transAmount'][item]) == True
                for item in storeInfo:
                    assert self.is_true(db_data['storeInfo'][item]) == True

            except AssertionError as e:
                print("MPM QR Verification-transReference表数据存储错误")
                raise e
    #断言成功的数据存入trans表
    def check_trans_success(self,test_data_interface, db_data):
        if test_data_interface == "CPM Payment":
            try:
                assert db_data['result']['code']=='S0000'
                assert db_data['result']['message']=='Success.'
                assert db_data['lockFlag'] == int(0)
                assert db_data['category'] == 'QR'
                assert db_data['apiVersion'] == 'v0'
                assert db_data['transType'] == 'CPM Payment'
                assert db_data['status'] == 'succeeded'
                assert db_data['wopStatus'] == 'succeeded'
                assert db_data['mopStatus'] == 'succeeded'
            except AssertionError as e:
                print("CPM Payment成功的交易检验通过")
                raise e
        elif test_data_interface == "Payment Notification":
            try:
                assert db_data['category'] == 'QR'
                assert db_data['apiVersion'] == 'v0'
                assert db_data['transType'] in ['MPM Payment','CPM Payment']
                assert db_data['status'] in ['succeeded','failed','processing']
                assert db_data['wopStatus'] in ['succeeded', 'failed','processing']
                assert db_data['mopStatus'] in ['succeeded', 'failed', 'processing']
                # assert db_data['lockFlag'] == 0
            except AssertionError as e:
                print("MPM Payment成功的交易检验通过")
                raise e
        elif test_data_interface == "Refund" :
            try:
                assert db_data['result']['code']=='S0000'
                assert db_data['result']['message'] in ['Success.','processing']
                assert db_data['lockFlag'] == int(0)
                assert db_data['category'] == 'QR'
                assert db_data['apiVersion'] == 'v0'
                assert db_data['transType'] == 'Refund'
                assert db_data['status'] == 'succeeded'
                assert db_data['wopStatus'] in  ['succeeded','processing']
                assert db_data['mopStatus'] == 'succeeded'
            except AssertionError as e:
                print("Refund成功的交易检验通过")
                raise e
        elif test_data_interface == "MPM Payment Authentication":
            try:
                assert db_data['lockFlag'] == int(0)
                assert db_data['category'] == 'QR'
                assert db_data['apiVersion'] == 'v0'
                assert db_data['transType'] == 'MPM Payment'
                assert db_data['status']== 'authorizing'
            except AssertionError as e:
                print("Refund成功的交易检验通过")
                raise e



