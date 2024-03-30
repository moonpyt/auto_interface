# -*- coding: utf-8 -*-
from base.read_file_path import ReadFile
from base.db import MongoDB
from base.read_config import Conf
from base.encrypt import Encrypt
from base.read_file_path import ReadFile
test_ini_file = ReadFile().read_ini_file(envirs="test", project="evopay")
class Check_evonet_to_partner():

    def __init__(self, database_connection):
        self.db = database_connection

    def is_true(self, data_params):
        # 判断字段是否存在
        if data_params:
            return True
        if data_params in [False, True]:
            return True
        else:
            return False

    def check_evonet_to_partner_CPMToken_useWOPToken(self,mongo_query,participantID):
        #检查由mop生成token时发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)

        for item in mongo_result:
            try:
                if item['from']=='evonet' and item['to']=='partner'and item['httpHeader']['uri']=='/mock/11/v0/payment/mop/cpmtoken':
                    assert item['payload']['wopID']==participantID
                elif item['from']=='partner' and item['to']=='EVONET':
                    assert (self.is_true(item['payload']['result']['code']) and self.is_true(item['payload']['result']['message']))==True

                    if item['payload']['result']['code']=='S0000':
                        a=item['payload']['mopToken'][0]['type']
                        assert self.is_true(a)==True
                        assert (self.is_true(item['payload']['mopToken'][0]['type']) and self.is_true(item['payload']['mopToken'][0]['value'])  and self.is_true(item['payload']['mopToken'][0]['expiryDate']))==True
                else:
                    print('此交易由evonet生成token')

            except AssertionError as e:
                print("CPMToken：evonet发送给partner和partner发送给evonet的校验失败")
                raise e
    def check_evonet_to_partner_CPMPayment(self,mongo_query,participantID,body):
        #检查CPMPayment交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' and item['httpHeader']['uri']=='/mock/11/v0/payment/wop/cpmpayment':

                    assert item['payload']['mopID'] == participantID
                    assert item['payload']['mopToken']['value']==body['mopToken']['value']
                    assert item['payload']['transAmount']['currency']==body['transAmount']['currency']
                    assert item['payload']['transAmount']['value'] == body['transAmount']['value']
                    assert item['payload']['transType']=='CPM Payment'
                    assert (self.is_true(item['payload']['userData']['wopUserReference']) and self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['evonetOrderCreateTime']) and self.is_true(item['payload']['storeInfo']['id']) and self.is_true(item['payload']['storeInfo']['localName']) and self.is_true(item['payload']['storeInfo']['mcc']))==True

                    if "billingAmount" in str(item):
                        assert (self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(item['payload']["billingAmount"]["value"])) == True
                    elif "billingFXRate" in str(item):
                        assert (self.is_true(item['payload']["billingFXRate"]["value"]) and self.is_true( item['payload']["billingFXRate"]["sourceCurrency"]) and self.is_true(
                            item['payload']["billingFXRate"]["destinationCurrency"])) == True
                    elif "settleAmount" in str(item):
                        assert (self.is_true(item['payload']["settleAmount"]["currency"]) and self.is_true(
                            item['payload']["settleAmount"]["value"])) == True
                    elif "settleFXRate" in str(item):
                        assert (self.is_true(item['payload']["settleFXRate"]["value"]) and self.is_true(
                            item['payload']["settleFXRate"]["sourceCurrency"]) and \
                                self.is_true(item['payload']["settleFXRate"]["destinationCurrency"])) == True
            except AssertionError as e:
                print("CPMPayment：evonet发送给partner校验失败")
                raise e

            try:

                if item['from'] == 'partner' and item['to'] == 'EVONET':
                    assert ( self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['wopOrderNumber']) and self.is_true(item['payload']['wopTransTime']) and self.is_true(item['payload']["result"]["code"]) and self.is_true(item['payload']["result"]["message"])) == True
                    if "billingAmount" in str(item):
                        assert (self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(item['payload']["billingAmount"]["value"])) == True
                    elif "billingFXRate" in str(item):
                        assert (self.is_true(item['payload']["billingFXRate"]["value"]) and self.is_true(
                            item['payload']["billingFXRate"]["sourceCurrency"]) and self.is_true(
                            item['payload']["billingFXRate"]["destinationCurrency"])) == True
                    elif "settleAmount" in str(item):
                        assert (self.is_true(item['payload']["settleAmount"]["currency"]) and self.is_true(
                            item['payload']["settleAmount"]["value"])) == True
                    elif "settleFXRate" in str(item):
                        assert (self.is_true(item['payload']["settleFXRate"]["value"]) and self.is_true(
                            item['payload']["settleFXRate"]["sourceCurrency"]) and \
                                self.is_true(item['payload']["settleFXRate"]["destinationCurrency"])) == True

            except AssertionError as e:
                print("CPMPayment：partner发送给evonet校验失败")
                raise e
    def check_evonet_to_partner_MPMQRVerification(self,mongo_query,participantID,body):
        # 检查MPMQRVerification交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' :

                    print("---------------evonet to partner校验--------")
                    assert item['payload']['wopID'] == participantID
                    assert item['payload']['qrPayload']==body['qrPayload']
                    assert (self.is_true(item['payload']['evonetReference']))==True
            except AssertionError as e:
                print("MPMQRVerification：evonet发送给partner校验失败")
                raise e
            try:
                if item['from'] == 'partner' and item['to'] == 'EVONET':
                    print("---------------partner to evonet 校验--------")
                    assert ( self.is_true(item['payload']['evonetReference']) and self.is_true(item['payload']["storeInfo"]["id"]) and self.is_true(item['payload']["storeInfo"]["localName"]) and self.is_true(item['payload']["storeInfo"][
                            "mcc"]) and self.is_true(item['payload']["result"]["code"]) and self.is_true(item['payload']["result"]["message"])) == True
                    if "transAmount" in str(item):
                        assert self.is_true(item['payload']["transAmount"]["currency"]) == True


            except AssertionError as e:
                print("MPMQRVerification：partner发送给evonet校验失败")
                raise e
    def check_evonet_to_partner_MPMPaymentAuthentication(self,mongo_query,participantID,body):
        # 检查MPMPaymentAuthentication交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' and item['httpHeader']['uri']=='/mock/11/v0/payment/mop/mpmpaymentauthentication':
                    assert item['payload']['wopID'] == participantID
                    assert item['payload']['userData']['wopUserReference']==body['userData']['wopUserReference']
                    assert item['payload']['evonetReference']==body['evonetReference']
                    assert item['payload']['transType'] == 'MPM Payment'
                    assert item['payload']['transAmount']['currency'] == body['transAmount']['currency']
                    assert item['payload']['transAmount']['value'] == body['transAmount']['value']

                    assert (self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['evonetOrderCreateTime']) )==True
            except AssertionError as e:
                print("MPMPaymentAuthentication：evonet发送给partner校验失败")
                raise e

            try:
                if item['from'] == 'partner' and item['to'] == 'EVONET':
                    assert ( self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['evonetReference']) and self.is_true(item['payload']["mopOrderNumber"]) and self.is_true(item['payload']['mopTransTime']) and self.is_true(item['payload']["result"]["code"]) and self.is_true(item['payload']["result"]["message"])) == True
            except AssertionError as e:
                print("MPMPaymentAuthentication：partner发送给evonet校验失败")
                raise e
    def check_evonet_to_partner_MPMPayment(self,mongo_query,participantID,body):
        # 检查MPMPaymentAuthentication交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            wop_nodeid = 'wopHost'+'.'+str(participantID)
            try:
                if item['from'] == 'evopay.tyo'  and  'mopHost'in item['to'] and item['httpHeader']['uri'] == '/mock/11/v0/payment/mop/mpmpaymentauthentication':
                    assert item['payload']['wopID'] == participantID
                    assert item['payload']['userData']['wopUserReference']==body['userData']['wopUserReference']
                    assert item['payload']['evonetReference']==body['evonetReference']
                    assert item['payload']['transType'] == 'MPM Payment'
                    assert item['payload']['transAmount']['currency'] == body['transAmount']['currency']
                    assert item['payload']['transAmount']['value'] == body['transAmount']['value']
                    assert (self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['evonetOrderCreateTime']) )==True
            except AssertionError as e:
                print("MPMPayment-Authentication：evonet发送给partner校验失败")
                raise e

            try:
                if 'mopHost'in item['from']  and item['to'] == 'evopay.tyo':
                    assert ( self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['evonetReference']) and self.is_true(item['payload']["mopOrderNumber"]) and self.is_true(item['payload']['mopTransTime']) and self.is_true(item['payload']["result"]["code"]) and self.is_true(item['payload']["result"]["message"])) == True
            except AssertionError as e:
                print("MPMPayment-Authentication：partner发送给evonet校验失败")
                raise e

            try:
                if item['from'] == 'evopay.tyo' and item['to'] == wop_nodeid and item['httpHeader']['uri'] == '/mock/11/accountDebit':
                    assert ( self.is_true(item['payload']['evonetOrderCreateTime']) and self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']["transType"]) and self.is_true(item['payload']['mopID']) and self.is_true(item['payload']["storeInfo"]["id"]) and self.is_true(item['payload']['storeInfo']["englishName"]))and self.is_true(item['payload']["transAmount"]["value"]) and self.is_true(item['payload']['transAmount']["currency"])
            except AssertionError as e:
                print("MPMPayment-accountdebit：partner发送给evonet校验失败")
                raise e

            try:
                if item['from'] == 'evopay.tyo' and 'mopHost'in item['to'] and item['httpHeader']['uri'] =='/mock/11/v0/payment/mop/paymentnotification':
                    assert ( self.is_true(item['payload']['evonetOrderCreateTime']) and self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['settleDate'])and self.is_true(item['payload']['mopOrderNumber']) and self.is_true(item['payload']['transResult']['message']) and self.is_true(item['payload']["transResult"]["status"]) and self.is_true(item['payload']['mopTransTime']) and self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(item['payload']['billingAmount']["value"]) and self.is_true(item['payload']["settleAmount"]["value"]) and self.is_true(item['payload']["settleAmount"]["currency"])and self.is_true(item['payload']["transAmount"]["value"]) and self.is_true(item['payload']["transAmount"]["currency"])) == True
            except AssertionError as e:
                print("MPMPayment-notify：partner发送给evonet校验失败")
                raise e

    def check_evonet_to_partner_MPMPaymentNotification(self,mongo_query,body):
        # 检查MPMPaymentNotification交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' and item['httpHeader']['uri']=='/mock/11/v0/payment/mop/paymentnotification':
                    assert item['payload']['evonetOrderNumber'] == body['evonetOrderNumber']
                    assert item['payload']['evonetOrderCreateTime'] == body['evonetOrderCreateTime']
                    assert item['payload']['transResult']['status']==body['transResult']['status']
                    assert item['payload']['transResult']['message'] == body['transResult']['message']
                    assert item['payload']['transAmount']['currency'] == body['transAmount']['currency']
                    assert item['payload']['transAmount']['value'] == body['transAmount']['value']

                    assert self.is_true(item['payload']['mopOrderNumber']) ==True
                    if "billingAmount" in str(item):
                        assert (self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(
                            item['payload']["billingAmount"]["value"])) == True
                    elif "billingFXRate" in str(item):
                        assert (self.is_true(item['payload']["billingFXRate"]["value"]) and self.is_true(
                            item['payload']["billingFXRate"]["sourceCurrency"]) and self.is_true(
                            item['payload']["billingFXRate"]["destinationCurrency"])) == True
                    elif "settleAmount" in str(item):
                        assert (self.is_true(item['payload']["settleAmount"]["currency"]) and self.is_true(
                            item['payload']["settleAmount"]["value"])) == True
                    elif "settleFXRate" in str(item):
                        assert (self.is_true(item['payload']["settleFXRate"]["value"]) and self.is_true(
                            item['payload']["settleFXRate"]["sourceCurrency"]) and self.is_true(item['payload']["settleFXRate"]["destinationCurrency"])) == True
            except AssertionError as e:
                print("MPMPaymentNotification：evonet发送给partner校验失败")
                raise e

            try:
                if item['from'] == 'partner' and item['to'] == 'EVONET':
                    assert ( self.is_true(item['payload']['result']['code']) and self.is_true(item['payload']['result']['message'])) == True
            except AssertionError as e:
                print("MPMPaymentNotification：partner发送给evonet的校验失败")
                raise e

    def check_evonet_to_partner_PaymentInquiry_processing(self,mongo_query):
        # 检查Inquiry处理中的交易发送partner的校验

        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' and item['httpHeader']['uri']=='/mock/11/v0/payment/mop/paymentinquiry':
                    assert self.is_true(item['payload']['evonetOrderNumber']) ==True


                elif item['from'] == 'partner' and item['to'] == 'EVONET':

                    assert (self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['wopOrderNumber']) and self.is_true(item['payload']['wopTransTime']) and self.is_true(item['payload']['transResult']['status']) and self.is_true(item['payload']['transResult']['message']) and self.is_true(item['payload']['result']['code']) and self.is_true(item['payload']['result']['message'])) == True
                    if "billingAmount" in str(item):
                        assert (self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(item['payload']["billingAmount"]["value"])) == True
                    elif "billingFXRate" in str(item):
                        assert (self.is_true(item['payload']["billingFXRate"]["value"]) and self.is_true(
                            item['payload']["billingFXRate"]["sourceCurrency"]) and self.is_true(
                            item['payload']["billingFXRate"]["destinationCurrency"])) == True
                    elif "settleAmount" in str(item):
                        assert (self.is_true(item['payload']["settleAmount"]["currency"]) and self.is_true(
                            item['payload']["settleAmount"]["value"])) == True
                    elif "settleFXRate" in str(item):
                        assert (self.is_true(item['payload']["settleFXRate"]["value"]) and self.is_true(
                            item['payload']["settleFXRate"]["sourceCurrency"]) and \
                                self.is_true(item['payload']["settleFXRate"]["destinationCurrency"])) == True
            except AssertionError as e:
                print("MPMPaymentNotification：evonet发送给partner和partner发送给evonet的校验失败")
                raise e

    def check_evonet_to_partner_refund(self, mongo_query, participantID, body):
        # 检查refund的交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' and item['httpHeader']['uri']=='/mock/11/v0/payment/mop/refund':
                    assert item['payload']['wopID'] == participantID
                    assert item['payload']['transType'] == 'Refund'
                    assert item['payload']['transAmount']['currency'] == body['transAmount']['currency']
                    assert item['payload']['transAmount']['value'] == body['transAmount']['value']

                    assert (self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(
                        item['payload']['evonetOrderCreateTime']) and self.is_true(item['payload']['originalWopOrderNumber'])) == True
                    if "billingAmount" in str(item):
                        assert (self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(item['payload']["billingAmount"]["value"])) == True
                    elif "billingFXRate" in str(item):
                        assert (self.is_true(item['payload']["billingFXRate"]["value"]) and self.is_true(
                            item['payload']["billingFXRate"]["sourceCurrency"]) and self.is_true(
                            item['payload']["billingFXRate"]["destinationCurrency"])) == True
                    elif "settleAmount" in str(item):
                        assert (self.is_true(item['payload']["settleAmount"]["currency"]) and self.is_true(
                            item['payload']["settleAmount"]["value"])) == True
                    elif "settleFXRate" in str(item):
                        assert (self.is_true(item['payload']["settleFXRate"]["value"]) and self.is_true(
                            item['payload']["settleFXRate"]["sourceCurrency"]) and \
                                self.is_true(item['payload']["settleFXRate"]["destinationCurrency"])) == True
                    elif "mopMsgRawData" in str(item):
                        assert (self.is_true(item['payload']["mopMsgRawData"]["retrievalReferenceNumber"]) and self.is_true(item['payload']["mopMsgRawData"]["acquirerIIN"])and self.is_true(item['payload']["mopMsgRawData"]["forwardingIIN"])and self.is_true(item['payload']["mopMsgRawData"]["processingCode"])and self.is_true(item['payload']["mopMsgRawData"]["posEntryMod"])and self.is_true(item['payload']["mopMsgRawData"]["posCondCode"])and self.is_true(item['payload']["mopMsgRawData"]["systemTraceAuditNum"]) and self.is_true(item['payload']["mopMsgRawData"]["transmissionDateTime"]) and self.is_true(item['payload']["mopMsgRawData"]["settleDate"]))==True
            except AssertionError as e:
                print("refund：evonet发送给partner校验失败")
                raise e

            try:
                if item['from'] == 'partner' and item['to'] == 'EVONET':
                    assert (self.is_true(item['payload']['evonetOrderNumber']) and self.is_true(item['payload']['evonetOrderCreateTime']) and self.is_true(item['payload']['wopOrderNumber']) and self.is_true(item['payload']['wopTransTime']) and self.is_true(item['payload']['result']['code']) and self.is_true(item['payload']['result']['message'])) == True
                    if "billingAmount" in str(item):
                        assert (self.is_true(item['payload']["billingAmount"]["currency"]) and self.is_true(
                            item['payload']["billingAmount"]["value"])) == True
                    elif "billingFXRate" in str(item):
                        assert (self.is_true(item['payload']["billingFXRate"]["value"]) and self.is_true(
                            item['payload']["billingFXRate"]["sourceCurrency"]) and self.is_true(
                            item['payload']["billingFXRate"]["destinationCurrency"])) == True
                    elif "settleAmount" in str(item):
                        assert (self.is_true(item['payload']["settleAmount"]["currency"]) and self.is_true(
                            item['payload']["settleAmount"]["value"])) == True
                    elif "settleFXRate" in str(item):
                        assert (self.is_true(item['payload']["settleFXRate"]["value"]) and self.is_true(
                            item['payload']["settleFXRate"]["sourceCurrency"]) and \
                                self.is_true(item['payload']["settleFXRate"]["destinationCurrency"])) == True
            except AssertionError as e:
                print("refund：partner发送给evonet校验失败")
                raise e

    def check_evonet_to_partner_cancellation(self, mongo_query, body):
        # 检查cancellation的交易发送partner的校验
        mongo_result = self.db.get_many(table='evoLogs', query_params=mongo_query)
        for item in mongo_result:
            try:
                if item['from'] == 'evonet' and item['to'] == 'partner' and item['httpHeader']['uri']=='/mock/11/v0/payment/mop/cancellation':
                    assert item['payload']['evonetOrderNumber'] == body['evonetOrderNumber']
            except AssertionError as e:
                print("cancellation：evonet发送给partner校验失败")
                raise e
            try:

                if item['from'] == 'partner' and item['to'] == 'EVONET':

                    assert ( self.is_true(item['payload']['result']['code']) and self.is_true(item['payload']['result']['message'])) == True
            except AssertionError as e:
                print("cancellation：partner发送给evonet的校验失败")
                raise e








