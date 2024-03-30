import time

from base.read_config import Conf
from base.encrypt import Encrypt
from base.read_file_path import ReadFile
from common.evopay.conf_init import db_tyo_evoconfig, db_sgp_evoconfig, evopay_conf, db_tyo_evopay, db_sgp_evopay
from common.evopay.mongo_initial import mongo_initial

from common.evopay.moudle import Moudle
'''
配置表整理：
a.wopID_01(WOP_Auto_JCoinPay_01)，mopID_01(MOP_Auto_GrabPay_01),brandID_01(Auto_GrabPay_01),(qrPayload":"https://AutoGrabPay01.com):singleNode_create_no_currency_transfer_data(单节点无币种转换,个性化配置表清算模式为直清清算,一对一关系，有配置关系,未超过cutofftime,evonet生成token)
b.wopID_02(WOP_Auto_JCoinPay_02)，mopID_02(MOP_Auto_GrabPay_02),brandID_02(Auto_GrabPay_02):singleNode_create_currency_transfer_data_02(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，mop表不支持cpm,mpm,refund(只读取个性化表)未超过cutofftime,mop生成token)
##b.c.wopID_03(WOP_Auto_JCoinPay_03)，mopID_03(MOP_Auto_GrabPay_03),brandID_03(Auto_GrabPay_03)(单节点币种转换(transcurrency:JPY,mopsettleCurrency:JPY,wopsettleCurrency:EUR,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，超过cutofftime,mop生成token)
#d.wopID_04(WOP_Auto_JCoinPay_04)，mopID_04(MOP_Auto_GrabPay_04),brandID_04(Auto_GrabPay_04):B2(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:JPY,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
##e.wopID_05(WOP_Auto_JCoinPay_05)，mopID_05(MOP_Auto_GrabPay_05),brandID_05(Auto_GrabPay_05):singleNode_create_currency_transfer_data_0create_currency_transfer_data5(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUA,billingCurrency:JPY),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
f.wopID_06(WOP_Auto_JCoinPay_06)，mopID_06(MOP_Auto_GrabPay_06),brandID_06(Auto_GrabPay_06):singleNode_create_currency_transfer_data_06(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:CAD,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
g.wopID_07(WOP_Auto_JCoinPay_07)，mopID_07(MOP_Auto_GrabPay_07),brandID_07(Auto_GrabPay_07):singleNode_create_currency_transfer_data_07(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:EUR),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
h.wopID_08(WOP_Auto_JCoinPay_08)，mopID_08(MOP_Auto_GrabPay_08),brandID_08(Auto_GrabPay_08):singleNode_create_currency_transfer_data_08(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop清算模式为直清，wop和*，mop和*，未超过cutofftime,mop生成token)
b.wopID_09(WOP_Auto_JCoinPay_09)，mopID_09(MOP_Auto_GrabPay_09),brandID_09(Auto_GrabPay_09):singleNode_create_currency_transfer_data_09(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，evonet生成token，未超过cutofftime,mop生成token）
c.wopID_10(WOP_Auto_JCoinPay_10)，mopID_10(MOP_Auto_GrabPay_10),brandID_10(Auto_GrabPay_10):singleNode_create_currency_transfer_data_10(单节点币种转换(transcurrency:JPY,mopsettleCurrency:JPY,wopsettleCurrency:EUR,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和mop，未超过cutofftime,mop生成token)
d.wopID_11(WOP_Auto_JCoinPay_11)，mopID_11(MOP_Auto_GrabPay_11),brandID_11(Auto_GrabPay_11):singleNode_create_currency_transfer_data_11(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:JPY,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
e.wopID_12(WOP_Auto_JCoinPay_12)，mopID_12(MOP_Auto_GrabPay_12),brandID_12(Auto_GrabPay_12):singleNode_create_currency_transfer_data_12(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:JPY),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
f.wopID_13(WOP_Auto_JCoinPay_13)，mopID_13(MOP_Auto_GrabPay_13),brandID_13(Auto_GrabPay_13):singleNode_create_currency_transfer_data_13(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:CAD,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
g.wopID_14(WOP_Auto_JCoinPay_14)，mopID_14(MOP_Auto_GrabPay_14),brandID_14(Auto_GrabPay_14):singleNode_create_currency_transfer_data_14(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:EUR),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
h.wopID_15(WOP_Auto_JCoinPay_15)，mopID_15(MOP_Auto_GrabPay_15),brandID_15(Auto_GrabPay_15):singleNode_create_currency_transfer_data_15(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop清算模式为直清，wop和*，mop和*，超过cutofftime,mop生成token)
h.wopID_16(WOP_Auto_JCoinPay_16)，mopID_16(MOP_Auto_GrabPay_16),brandID_16(Auto_GrabPay_16):singleNode_create_currency_transfer_bilateral_data_16(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),(币种转换,个性化配置表清算模式为直清,一对一关系，有配置关系,未超过cutofftime,mop生成token)
h.wopID_17(WOP_Auto_JCoinPay_17)，mopID_17(MOP_Auto_GrabPay_17),brandID_17(Auto_GrabPay_17):singleNode_create_isSettlementAmountEVONETCalculated_False_01(直清模式，wop和*，mop和*，isSettlementAmountEVONETCalculated=False,cutofftime超过当前时间)
h.wopID_18(WOP_Auto_JCoinPay_18)，mopID_18(MOP_Auto_GrabPay_18),brandID_18(Auto_GrabPay_18):singleNode_create_isSettlementAmountEVONETCalculated_False_02(直清模式，wop和*，mop和*，isSettlementAmountEVONETCalculated=False,cutofftime不超过当前时间)
h.wopID_19()，mopID_19(MOP_Auto_GrabPay_19),brandID_19(Auto_GrabPay_19):singleNode_create_fxrate_01(单节点币种转换(transcurrency:JPY,mopsettleCurrency:SGD,wopsettleCurrency:NOK,billingCurrency:THB),fxrate表：(MOP:存在反向和中间汇率，SGD-JPY(0.21),JPY-USD(0.09),SGD-USD(0.41))(WOP:存在中间汇率，SGD-USD(0.41),NOK-USD(0.456))(billing:正向，反向，中间都存在NOK-THB(0.33)，THB-NOK(0.38),NOK-USD(0.51),THB-USD(0.59)))
h.wopID_20(WOP_Auto_JCoinPay_20)，mopID_20(MOP_Auto_GrabPay_20),brandID_19(Auto_GrabPay_19):singleNode_create_fxrate_02(单节点币种转换(transcurrency:JPY,mopsettleCurrency:RUB,wopsettleCurrency:AUD,billingCurrency:KRW),fxrate表：(MOP:存在正向，反向,中间汇率，JPY-RUB(0.2),RUB-JPY(0.3),JPY-USD(0.09),RUB-USD(0.11)))(WOP:存在反向，中间汇率，AUD-RUB(0.33),RUB-USD(0.345),AUD-USD(0.234))(billing:存在中间汇率，AUD-USD(0.234),KRW-USD(0.487)))
h.wopID_21(WOP_Auto_JCoinPay_21)，mopID_21(MOP_Auto_GrabPay_21),brandID_19(Auto_GrabPay_19):singleNode_create_fxrate_03(单节点币种转换(transcurrency:JPY,mopsettleCurrency:NZD,wopsettleCurrency:IDR,billingCurrency:DKK),fxrate表：(MOP:存在中间汇率，JPY-USD(0.09),NZD-USD(0.256))(WOP:存在反向 IDR-NZD(0.338))(billing:存在反向，中间汇率，DKK-IDR(0.145),IDR-USD(0.159),DKK-USD(0.195)))
h.wopID_22(WOP_Auto_JCoinPay_22)，mopID_22(MOP_Auto_GrabPay_22), brandID_22Auto_GrabPay_22):singleNode_create_isSettlementAmountEVONETCalculated_False_03(直清模式，wop和 *，mop和 *，isSettlementAmountEVONETCalculated = False, cutofftime不超过当前时间)
# g.wopID_23(WOP_Auto_JCoinPay_23)，mopID_23(MOP_Auto_GrabPay_23),brandID_23(Auto_GrabPay_23):singleNode_create_fxrate(双节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),fxrate表：(MOP:存在中间汇率，JPY-CAD(0.05))(WOP:存在反向 CAD-EUR(0.07) MCCR:0 WCCR:0)

i.wopID_A1(WOP_Auto_JCoinPay_A1)，mopID_A1(MOP_Auto_GrabPay_A1),brandID_A1(Auto_GrabPay_A1),(qrPayload":"https://AutoGrabPayA1.com):singleNode_create_wop_innormal_01(单节点,wop status=locked)
j.wopID_A2(WOP_Auto_JCoinPay_A2)，mopID_A2(MOP_Auto_GrabPay_A2),brandID_A2(Auto_GrabPay_A2),(qrPayload":"https://AutoGrabPayA2.com):singleNode_create_wop_innormal_02(单节点,wop deleteFlag=True)
k.wopID_A3(WOP_Auto_JCoinPay_A3)，mopID_A3(MOP_Auto_GrabPay_A3),brandID_A3(Auto_GrabPay_A3),(qrPayload":"https://AutoGrabPayA3.com):singleNode_create_mop_innormal_01(单节点,mop status=locked)
l.wopID_A4(WOP_Auto_JCoinPay_A4)，mopID_A4(MOP_Auto_GrabPay_A4),brandID_A4(Auto_GrabPay_A4),(qrPayload":"https://AutoGrabPayA4.com):singleNode_create_mop_innormal_02(单节点,mop deleteFlag=True)
m.wopID_A5(WOP_Auto_JCoinPay_A5)，mopID_A5(MOP_Auto_GrabPay_A5),brandID_A5(Auto_GrabPay_A5),(qrPayload":"https://AutoGrabPayA5.com):singleNode_create_relation_innormal_01(单节点,relation不存在，wop和*不存在，mop和*不存在)
n.wopID_A6(WOP_Auto_JCoinPay_A6)，mopID_A6(MOP_Auto_GrabPay_A6),brandID_A6(Auto_GrabPay_A6),(qrPayload":"https://AutoGrabPayA6.com):singleNode_create_relation_innormal_02(单节点,relation:wop和*存在)
o.wopID_A7(WOP_Auto_JCoinPay_A7)，mopID_A7(MOP_Auto_GrabPay_A7),brandID_A7(Auto_GrabPay_A7),(qrPayload":"https://AutoGrabPayA7.com):singleNode_create_relation_innormal_03(单节点,relation:mop和*存在)
p.wopID_A8(WOP_Auto_JCoinPay_A8)，mopID_A8(MOP_Auto_GrabPay_A8),brandID_A8(Auto_GrabPay_A8),(qrPayload":"https://AutoGrabPayA8.com):singleNode_create_brand_innormal(单节点,brand表没有mop对应的brandID)
p.wopID_A9(WOP_Auto_JCoinPay_A9)，mopID_A9(MOP_Auto_GrabPay_A9),brandID_A8(Auto_GrabPay_A9),(qrPayload":"https://AutoGrabPayA9.com):singleNode_create_upsupported_trans_01(单节点,，MOP不支持CPM模式,MPM模式(support模式为false))
p.wopID_A10(WOP_Auto_JCoinPay_A10)，mopID_A10(MOP_Auto_GrabPay_A10),brandID_A10(Auto_GrabPay_A10),(qrPayload":"https://AutoGrabPayA10.com):singleNode_create_upsupported_trans_02(单节点,MOP不支持CPM模式,MPM模式(内容为空))

p.wopID_A11(WOP_Auto_JCoinPay_A11)，mopID_A11(MOP_Auto_GrabPay_A11),brandID_A11(Auto_GrabPay_A11),(qrPayload":"https://AutoGrabPayA11.com):singleNode_create_mop_non_exist(单节点,relation表存在，对应的mop在mop不存在))
p.wopID_A12(WOP_Auto_JCoinPay_A12)，mopID_A12(MOP_Auto_GrabPay_A12),brandID_A12（Auto_GrabPay_A12),(qrPayload":"https://AutoGrabPayA12.com):singleNode_create_upsupported_refund_01(单节点,refund(support模式为false))
p.wopID_A13(WOP_Auto_JCoinPay_A13)，mopID_A13(MOP_Auto_GrabPay_A13),brandID_A13(Auto_GrabPay_A13),(qrPayload":"https://AutoGrabPayA13.com):singleNode_create_upsupported_refund_02(单节点,refund(内容为空))
p.wopID_A14(WOP_Auto_JCoinPay_A14)，mopID_A14(MOP_Auto_GrabPay_A14),brandID_A14(Auto_GrabPay_A14),(qrPayload":"https://AutoGrabPayA14.com):none_fxrate(fxrate表里没有汇率)

p(用于修改配置的案例).wopID_B1(WOP_Auto_JCoinPay_B1)，mopID_B1(MOP_Auto_GrabPay_B1),brandID_B1(Auto_GrabPay_B1),(qrPayload":"https://AutoGrabPayB1.com)

MOP支持的交易币种字段为空 (此用例使用默认配置）MOP支持的交易币种字段为空 (此用例使用个性化配置）evonet给或不给MOP提供货币转换evonet给或不给MOP/WOP提供货币转换没有relation, 个性化配置正常
CPM Payment,wop不存在
MPM mop不存在
个性化配置没有数据，deleteFlag=False

'''

test_ini_file = ReadFile().read_ini_file(envirs="test", project="evopay")
class Create_Mongo_Data(object):
    def __init__(self,version='v0'):
        self.db = db_tyo_evoconfig
        self.account_debit_url = evopay_conf.accountDebit
        self.authenticationNotification_url = evopay_conf.authenticationNotification
        self.notification_url = evopay_conf.transactionNotification
        self.inquiry = evopay_conf.inquiry_address
        self.cpmPayment_url = evopay_conf.cpmPayment_address
        self.refund_url = evopay_conf.refund_address
        self.cancel_url = evopay_conf.cancel_address

        self.cpmToken_url = evopay_conf.cpmToken_address
        self.mpmQrVerification_url = evopay_conf.mpmQrVerification_address
        self.mpmPaymentAuthentication_url = evopay_conf.mpmPaymentAuthentication_address
        self.paymentNotification_url = evopay_conf.paymentNotification_address




    def create_wop(self,baseInfo_wopID,baseInfo_brandID,baseInfo_nodeID,baseInfo_status,
                   settleInfo_fileInitiator,specialInfo_specialType,settleInfo_specialCategory,settleInfo_cutoffTime,settleInfo_settleCurrency,settleInfo_cpmInterchangeFeeRate,settleInfo_mpmInterchangeFeeRate,settleInfo_settleFileTime,settleInfo_isBillingAmountCalculated,settleInfo_billingCurrency,settleInfo_wccr,settleInfo_cccr,settleInfo_transactionProcessingFeeRate,settleInfo_transProcessingFeeCollectionMethod,settleInfo_fxProcessingFeeRate,settleInfo_fxProcessingFeeCollectionMethod,settleInfo_fxRebateCollectionMethod,
                   deleteFlag,operationalNode,baseInfo_signKeyC):
        insert_wop={
            "baseInfo": {
                "status":baseInfo_status,
                "wopID": baseInfo_wopID,
                "wopName": baseInfo_wopID,
                "brandID":baseInfo_brandID,
                "country":"JPN",
                "nodeID": baseInfo_nodeID,
                "businessContactName": "auto_test businessContactName",
                "businessPhone": "158955552222",
                "businessEmail": "autotest@gmail.com",
                "technologyContactName": "auto_test technologyContactName",
                "technologyPhone": "158955552222",
                "technologyEmail": "autotest@gmail.com",
                "supportContactName": "auto_test supportContactName",
                "supportPhone": "158955552222",
                "supportEmail": "autotest@gmail.com",
                "operatorContactName": "autotest",
                "operatorPhone": "158955552222",
                "operatorEmail": "autotest@gmail.com",
                "financeContactName": "auto_test financeContactName",
                "financePhone": "158955552222",
                "financeEmail": "autotest@gmail.com",
                "cutoffTime" : "12:00",
                "signKeyC": baseInfo_signKeyC,
                "accountDebit": {
                    "url":self.account_debit_url,
                    "version": evopay_conf.version_v0
                },
                "authenticationNotification": {
                    "url": self.authenticationNotification_url,
                    "version": evopay_conf.version_v0
                },
                "transactionNotification": {
                    "url": self.notification_url,
                    "version": evopay_conf.version_v0
                },
                "inquiry": {
                    "url": self.inquiry,
                    "version": evopay_conf.version_v0
                },
                "cpmPayment": {
                    "url": self.cpmPayment_url,
                    "version": evopay_conf.version_v0
                },
                "refund": {
                    "url": self.refund_url,
                    "version": evopay_conf.version_v0
                },
                "cancel": {
                    "url": self.cancel_url,
                    "version": evopay_conf.version_v0
                }
            },
            "settleInfo" : {
                "fileInitiator" : settleInfo_fileInitiator,                      # 文件发起方
                "specialCategory" : settleInfo_specialCategory,                      # 文件特殊种类
                "settleCurrency" : settleInfo_settleCurrency,                        # 清算币种
                "cutoffTime" : settleInfo_cutoffTime,                     # 日切时间
                "cpmInterchangeFeeRate" : settleInfo_cpmInterchangeFeeRate,                   # cpmInterchangeFee
                "mpmInterchangeFeeRate" : settleInfo_mpmInterchangeFeeRate,                   # mpmInterchangeFee
                "settleFileTime" : settleInfo_settleFileTime,                 # 文件生成时间
                "isBillingAmountCalculated" :settleInfo_isBillingAmountCalculated ,             # billingAmount是否计算
                "billingCurrency" : settleInfo_billingCurrency,                       # billingCurrency
                "wccr" : settleInfo_wccr,
                "cccr" :settleInfo_cccr,
                "transactionProcessingFeeRate" : settleInfo_transactionProcessingFeeRate,            # 交易处理费
                "transProcessingFeeCollectionMethod" : settleInfo_transProcessingFeeCollectionMethod,  # 交易处理费生成方式
                "fxProcessingFeeRate" :settleInfo_fxProcessingFeeRate,                     # 汇率转换费
                "fxProcessingFeeCollectionMethod" : settleInfo_fxProcessingFeeCollectionMethod,   # 汇率转换费生成方式
                "fxRebateCollectionMethod" : settleInfo_fxRebateCollectionMethod
           },
            "specialInfo": {
                "specialType": specialInfo_specialType,  # 特殊类型
                "batchRefundSettle": False
            },
               "version": int(1), # 版本
                "deleteFlag": deleteFlag, # 删除标识
                "updateUser": "auto_user", # 更新用户
                "updateTime": Moudle().create_mongo_time(), # 更新时间
                "createTime": Moudle().create_mongo_time(), # 创建时间
                "operationalNode": [ operationalNode,]#操作节点
        }
        self.db.insert_one(table='wop', insert_params=insert_wop)


    def create_mop(self, baseInfo_mopID, baseInfo_brandID, baseInfo_nodeID,baseInfo_useEVONETToken ,baseInfo_status,baseInfo_isCPMSupported,baseInfo_isMPMSupported,baseInfo_isRefundSupported,baseInfo_transCurrencies,baseInfo_schemeInfo_schemeName,baseInfo_schemeInfo_signStatus,
                   settleInfo_fileInitiator, specialInfo_specialType,
                   settleInfo_settleCurrency, settleInfo_cpmInterchangeFeeRate, settleInfo_mpmInterchangeFeeRate,
                   settleInfo_settleFileTime,
                   settleInfo_mccr, settleInfo_transactionProcessingFeeRate,
                   settleInfo_transProcessingFeeCollectionMethod, settleInfo_fxProcessingFeeRate,
                   settleInfo_fxProcessingFeeCollectionMethod, settleInfo_fxRebateCollectionMethod,settleInfo_cutoffTime,
                   deleteFlag, operationalNode, baseInfo_signKeyC):
        insert_mop = {
            "baseInfo": {
                "status": baseInfo_status,
                "mopID": baseInfo_mopID,
                "mopName": baseInfo_mopID,
                "brandID": baseInfo_brandID,
                "useEVONETToken":baseInfo_useEVONETToken,
                "country": "JPN",
                "nodeID": baseInfo_nodeID,
                "businessContactName": "auto_test businessContactName",
                "businessPhone": "158955552222",
                "businessEmail": "autotest@gmail.com",
                "technologyContactName": "auto_test technologyContactName",
                "technologyPhone": "158955552222",
                "technologyEmail": "autotest@gmail.com",
                "supportContactName": "auto_test supportContactName",
                "supportPhone": "158955552222",
                "supportEmail": "autotest@gmail.com",
                "operatorContactName": "autotest",
                "operatorPhone": "158955552222",
                "operatorEmail": "autotest@gmail.com",
                "financeContactName": "auto_test financeContactName",
                "financePhone": "158955552222",
                "financeEmail": "autotest@gmail.com",
                "isCPMSupported": baseInfo_isCPMSupported,
                "isMPMSupported": baseInfo_isMPMSupported,
                "isRefundSupported": baseInfo_isRefundSupported,
                "transCurrencies": baseInfo_transCurrencies,  #列表
                "schemeInfo": [
                {
                    "schemeName": baseInfo_schemeInfo_schemeName,
                    "signStatus": baseInfo_schemeInfo_signStatus
                }
                ],
                "signKeyC": baseInfo_signKeyC,
                "cpmToken": {
                    "url": self.cpmToken_url,
                    "version": evopay_conf.version_v0
                },
                "mpmQrVerification": {
                    "url": self.mpmQrVerification_url,
                    "version": evopay_conf.version_v0
                },
                "mpmPaymentAuthentication": {
                    "url": self.mpmPaymentAuthentication_url,
                    "version": evopay_conf.version_v0
                },
                "paymentNotification": {
                    "url": self.paymentNotification_url,
                    "version": evopay_conf.version_v0
                }
            },
            "settleInfo": {
                "fileInitiator": settleInfo_fileInitiator,  # 文件发起方
                "settleCurrency": settleInfo_settleCurrency,  # 清算币种
                "cpmInterchangeFeeRate": settleInfo_cpmInterchangeFeeRate,  # cpmInterchangeFee
                "mpmInterchangeFeeRate": settleInfo_mpmInterchangeFeeRate,  # mpmInterchangeFee
                "cutoffTime": settleInfo_cutoffTime,  # 日切时间
                "settleFileTime" : settleInfo_settleFileTime,                #文件生成时间
                "mccr" : settleInfo_mccr,
                "transactionProcessingFeeRate" : settleInfo_transactionProcessingFeeRate,           #交易处理费
                "transProcessingFeeCollectionMethod" : settleInfo_transProcessingFeeCollectionMethod,  #交易处理费生成方式
                "fxProcessingFeeRate" : settleInfo_fxProcessingFeeRate,                     # 汇率转换费
                "fxProcessingFeeCollectionMethod" : settleInfo_fxProcessingFeeCollectionMethod,   # 汇率转换费生成方式
                "fxRebateCollectionMethod" : settleInfo_fxRebateCollectionMethod
            },
            "specialInfo": {
                "specialType": specialInfo_specialType,  # 特殊类型
                "batchRefundSettle": False
            },
            "version": int(32),  # 版本
            "deleteFlag": deleteFlag,  # 删除标识
            "updateUser": "auto_user",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [operationalNode, ]  # 操作节点
        }
        self.db.insert_one(table='mop', insert_params=insert_mop)

    def create_customizeConfig(self, mopID, wopID, settleInfo_fileInitiator, status, isCPMSupported,
                   isMPMSupported, isRefundSupported, transCurrencies,settleMode,settleCurrency,isSettlementAmountEVONETCalculated,cpmInterchangeFeeRate, mpmInterchangeFeeRate, fxRateOwner,transactionProcessingFeeRate,
                   transProcessingFeeCollectionMethod, fxProcessingFeeRate,
                   fxProcessingFeeCollectionMethod,
                   deleteFlag, operationalNode,mccr=None,wccr=None):
        insert_customizeConfig = {

                        "status": status, # 状态
                        "mopID": mopID, # mopID
                        "mopName": mopID, # mopName
                        "wopID": wopID, # wopID
                        "wopName": wopID, # wopName
                        "isCPMSupported": isCPMSupported, # 是否支持CPM
                        "isMPMSupported": isMPMSupported, # 是否支持MPM
                        "isRefundSupported": isRefundSupported, # 是否支持Refund
                        "transCurrencies":transCurrencies,
                        "settleMode": settleMode, # 清算模式bilateral / evonet
                        "settleCurrency":settleCurrency , # 清算币种
                        "isSettlementAmountEVONETCalculated": isSettlementAmountEVONETCalculated, # 是否计算清算币种
                        "cpmInterchangeFeeRate": cpmInterchangeFeeRate, # cpmInterchangeFee
                        "mpmInterchangeFeeRate":mpmInterchangeFeeRate, # mpmInterchangeFee
                        "mccr": mccr,
                        "cutoffTime": Moudle().less_cutoffTime(),
                        "wccr": wccr,
                        "fxRateOwner": fxRateOwner, # 汇率归属
                        "transactionProcessingFeeRate": transactionProcessingFeeRate, # 交易处理费
                        "transProcessingFeeCollectionMethod": transProcessingFeeCollectionMethod, # 交易处理费生成方式
                        "fxProcessingFeeRate": fxProcessingFeeRate, # 汇率转换费
                        "fxProcessingFeeCollectionMethod": fxProcessingFeeCollectionMethod, # 汇率转换费生成方式
                        "fileInitiator": settleInfo_fileInitiator,
                        "version": int(1), # 版本
                        "deleteFlag": deleteFlag, # 删除标识
                        "updateUser": "auto_test", # 更新用户
                        "updateTime": Moudle().create_mongo_time(), # 更新时间
                        "createTime": Moudle().create_mongo_time(), # 创建时间
                        "operationalNode": [ # 操作节点
                        operationalNode
                        ]

        }
        self.db.insert_one(table='customizeConfig', insert_params=insert_customizeConfig)

    def create_customizeConfig01(self, mopID, wopID, settleInfo_fileInitiator, status, isCPMSupported,
                               isMPMSupported, isRefundSupported, transCurrencies, settleMode, settleCurrency,
                               isSettlementAmountEVONETCalculated, cpmInterchangeFeeRate, mpmInterchangeFeeRate,
                               fxRateOwner, transactionProcessingFeeRate,
                               transProcessingFeeCollectionMethod, fxProcessingFeeRate,
                               fxProcessingFeeCollectionMethod,
                               deleteFlag, operationalNode, mccr=None):
        insert_customizeConfig = {

            "status": status,  # 状态
            "mopID": mopID,  # mopID
            "mopName": mopID,  # mopName
            "wopID": wopID,  # wopID
            "wopName": wopID,  # wopName
            "isCPMSupported": isCPMSupported,  # 是否支持CPM
            "isMPMSupported": isMPMSupported,  # 是否支持MPM
            "isRefundSupported": isRefundSupported,  # 是否支持Refund
            "transCurrencies": transCurrencies,
            "settleMode": settleMode,  # 清算模式bilateral / evonet
            "settleCurrency": settleCurrency,  # 清算币种
            "isSettlementAmountEVONETCalculated": isSettlementAmountEVONETCalculated,  # 是否计算清算币种
            "cpmInterchangeFeeRate": cpmInterchangeFeeRate,  # cpmInterchangeFee
            "mpmInterchangeFeeRate": mpmInterchangeFeeRate,  # mpmInterchangeFee
            "mccr": mccr,
            "cutoffTime": Moudle().less_cutoffTime(),
            "fxRateOwner": fxRateOwner,  # 汇率归属
            "transactionProcessingFeeRate": transactionProcessingFeeRate,  # 交易处理费
            "transProcessingFeeCollectionMethod": transProcessingFeeCollectionMethod,  # 交易处理费生成方式
            "fxProcessingFeeRate": fxProcessingFeeRate,  # 汇率转换费
            "fxProcessingFeeCollectionMethod": fxProcessingFeeCollectionMethod,  # 汇率转换费生成方式
            "fileInitiator": settleInfo_fileInitiator,
            "version": int(1),  # 版本
            "deleteFlag": deleteFlag,  # 删除标识
            "updateUser": "auto_test",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [  # 操作节点
                operationalNode
            ]

        }
        self.db.insert_one(table='customizeConfig', insert_params=insert_customizeConfig)

    def create_relation(self,mopID,wopID,operationalNode):
        insert_relation = {
            "mopID": mopID,
            "wopID": wopID,
            "createUser": "auto_user",
            "createTime": Moudle().create_mongo_time(),
            "updateTime": Moudle().create_mongo_time(),
            "updateUser": "auto_user",
            "operationalNode": [operationalNode, ]  # 操作节点

        }

        self.db.insert_one(table='relation', insert_params=insert_relation)
        # brand表
    def create_brand(self, brandID, deleteFlag,operationalNode):
        insert_brand = {
            "deleteFlag": deleteFlag,
            "createUser": "auto_user",
            "createTime": Moudle().create_mongo_time(),
            "operationalNode": [
                operationalNode
            ],
            "brandID": brandID,
            "brandName": brandID,
            "brandLogoAddr": "https://localhost:4200/biz/brand/new",
            "version": int(1),
            "updateTime":Moudle().create_mongo_time(),
        }

        self.db.insert_one(table='brand', insert_params=insert_brand)

        # mpmQrIdentifier关系表
    def create_mpmQrIdentifier(self,mopID,qrIdentifier,deleteFlag,operationalNode):
        insert_mpmQrIdentifier = {
            "mopID": mopID,
            "mopName": mopID,
            "qrType": "QR",
            "qrIdentifier": qrIdentifier,
            "qrLength": int(32),
            "createUser": "auto_user",
            "createTime": Moudle().create_mongo_time(),
            "updateUser": "auto_user",
            "updateTime": Moudle().create_mongo_time(),
            "deleteFlag": deleteFlag,
            "operationalNode": [operationalNode, ]  # 操作节点
        }

        self.db.insert_one(table='mpmQrIdentifier', insert_params=insert_mpmQrIdentifier)

        # cpmTokenIdentifier关系表
    def create_cpmTokenIdentifier(self, mopID, useEVONETStandard, deleteFlag,operationalNode):
        insert_cpmTokenIdentifier = {
            "mopID": mopID,
            "mopName": mopID,
            "useEVONETStandard": useEVONETStandard,
            "createTime": Moudle().create_mongo_time(),
            "updateTime": Moudle().create_mongo_time(),
            "deleteFlag": deleteFlag,
            "operationalNode": [operationalNode, ]  # 操作节点
        }

        self.db.insert_one(table='cpmTokenIdentifier', insert_params=insert_cpmTokenIdentifier)

    #fxrate表
    def create_fx_Rate(self,ccyPair,ccy1,ccy1Code,ccy2,ccy2Code,bid,ask,mid,fxRateOwner='auto_user',deleteFlag=False):
        insert_fxRate={
            "ccyPair": ccyPair,
            "ccy1": ccy1,
            "ccy1Code": ccy1Code,
            "ccy2": ccy2,
            "ccy2Code": ccy2Code,
            "bid": bid,
            "ask": ask,
            "mid": mid,
            "fxRateOwner": fxRateOwner,
            "updateTime":  Moudle().create_mongo_time(),
            "createTime":  Moudle().create_mongo_time(),
            "createUser": "auto_user",
            "updateUser": "auto_user",
            "deleteFlag": deleteFlag,
            "version":0,
            "refID": Moudle().create_refID(),
            "fxRateSource": "MDAQ",
            "operationalNode": ['tyo', ]  # 操作节点
        }
        self.db.insert_one(table='fx_rate', insert_params=insert_fxRate)



class Update_Mongo_Data(object):
    def __init__(self,node,database,database_name='evoconfig'):
        #database为测试案例中的database,node为单节点或双节点
        self.node=node
        if database=='sgp':
            if database_name == 'evopay':
                self.db = db_sgp_evopay
            else:
                self.db = db_sgp_evoconfig
            self.wopID='WOP_Auto_JCoinPay_B01'
            self.mopID = 'MOP_Auto_GrabPay_B01'
            self.brandID = 'Auto_GrabPay_B01'
            self.nodeID_wop='tyo'
            self.nodeID_mop = 'sgp'
        else:
            if database_name == 'evopay':
                self.db = db_tyo_evopay
                self.db_sgp = db_sgp_evopay
            else:
                self.db = db_tyo_evoconfig
                self.db_sgp = db_sgp_evoconfig
            if node=='single':
                self.wopID = 'WOP_Auto_JCoinPay_B1'
                self.mopID = 'MOP_Auto_GrabPay_B1'
                self.brandID = 'Auto_GrabPay_B1'
                self.settleCurrency = 'JPY'
                self.billingCurrency = 'JPY'
                self.nodeID_wop = 'tyo'
                self.nodeID_mop = 'tyo'
            else:

                self.wopID = 'WOP_Auto_JCoinPay_B01'
                self.mopID = 'MOP_Auto_GrabPay_B01'
                self.settleCurrency = 'JPY'
                self.billingCurrency = 'JPY'
                self.brandID = 'Auto_GrabPay_B01'
                self.nodeID_wop = 'tyo'
                self.nodeID_mop = 'sgp'

    def updata_data(self, table, query_params, update_params):
        self.db.update_one(table=table,query_params=query_params,updata_params=update_params)

    def unset_many_data(self,table, query_params, update_params):
        self.db.unset_many(table=table,query_params=query_params,unset_params=update_params)

    def update_data_reset(self,table,query_params,update_params):

        if ('True' in str(update_params) and 'apiSpecialMode' not in str(update_params)) and ('settleInfo.billingCurrency' not in str(update_params)) and \
            ('settleInfo.settleCurrency' not in str(update_params)):

            query_params_reset=eval(str(update_params).replace('True','False'))
            self.db.update_one(table=table, query_params=query_params, updata_params=query_params_reset)
        elif 'False' in str(update_params) and 'apiSpecialMode' not in str(update_params):

            query_params_reset = eval(str(update_params).replace('False', 'True'))
            self.db.update_one(table=table, query_params=query_params, updata_params=query_params_reset)
        elif 'locked' in str(update_params):
            query_params_reset = eval(str(update_params).replace('locked', 'active'))
            self.db.update_one(table=table, query_params=query_params, updata_params=query_params_reset)
        elif '*' in str(update_params):
            if 'wopID' in str(update_params):
                query_params_reset = eval(str(update_params).replace('*', self.wopID))
                self.db.update_one(table=table, query_params=query_params, updata_params=query_params_reset)
            elif 'mopID' in str(update_params):
                query_params_reset = eval(str(update_params).replace('*',self.mopID))
                self.db.update_one(table=table, query_params=query_params, updata_params=query_params_reset)

        else:
            if 'wop' in table:

                self.db.delete_one(table=table,query_params=query_params)
                self.db_sgp.delete_one(table=table, query_params=query_params)
                common_dict_info = {"wccr": 0.0, "cccr": 0.0}

                if 'WOP_Auto_JCoinPay_031' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_031","baseInfo_brandID": "Auto_GrabPay_031",
                    "settleInfo_settleCurrency": "JPY","settleInfo_billingCurrency": "JPY",'settleInfo_isBillingAmountCalculated' : False,}

                elif 'WOP_Auto_JCoinPay_032' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_032","baseInfo_brandID": "Auto_GrabPay_032",
                    "settleInfo_settleCurrency": "JPY","settleInfo_billingCurrency": "JPY",'settleInfo_isBillingAmountCalculated' : False,}

                elif 'WOP_Auto_JCoinPay_003' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_003","baseInfo_brandID": "Auto_GrabPay_003",
                    "settleInfo_settleCurrency": "EUR","settleInfo_billingCurrency": "USD"}

                elif 'WOP_Auto_JCoinPay_004' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_004", "baseInfo_brandID": "Auto_GrabPay_004",
                                 "settleInfo_settleCurrency": "JPY", "settleInfo_billingCurrency": "USD","settleInfo_wccr": 0.12, "settleInfo_cccr": 0.15}

                elif 'WOP_Auto_JCoinPay_31' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_31","baseInfo_brandID": "Auto_GrabPay_31",
                    "settleInfo_settleCurrency": "JPY","settleInfo_billingCurrency": "JPY",'settleInfo_isBillingAmountCalculated' : False,}

                elif 'WOP_Auto_JCoinPay_03' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_03","baseInfo_brandID": "Auto_GrabPay_03",
                    "settleInfo_settleCurrency": "EUR","settleInfo_billingCurrency": "USD"}

                elif 'WOP_Auto_JCoinPay_04' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_04", "baseInfo_brandID": "Auto_GrabPay_04",
                                 "settleInfo_settleCurrency": "JPY", "settleInfo_billingCurrency": "USD","settleInfo_wccr": 0.12, "settleInfo_cccr": 0.15}

                elif 'WOP_Auto_JCoinPay_32' in str(query_params):
                    dict_info = {"baseInfo_wopID": "WOP_Auto_JCoinPay_32","baseInfo_brandID": "Auto_GrabPay_32",
                    "settleInfo_settleCurrency": "JPY","settleInfo_billingCurrency": "JPY",'settleInfo_isBillingAmountCalculated' : False}
                common_dict_info.update(dict_info)
                mongo_initial(db_tyo_evoconfig).create_wop(**common_dict_info)

            if 'mop' in table:
                self.db.delete_one(table=table, query_params=query_params)
                self.db_sgp.delete_one(table=table, query_params=query_params)
                common_dict_info = {"settleCurrency": "JPY","baseInfo_nodeID": "tyo"}
                if 'MOP_Auto_GrabPay_032' in str(query_params):
                    dict_info = {"baseInfo_mopID": "MOP_Auto_GrabPay_032","baseInfo_brandID": "Auto_GrabPay_032",
                    "settleInfo_settleCurrency": "JPY","baseInfo_nodeID": "sgp"}

                elif 'MOP_Auto_GrabPay_09' in str(query_params):
                    dict_info = {"baseInfo_mopID": "MOP_Auto_GrabPay_09","baseInfo_brandID": "Auto_GrabPay_09",
                    "baseInfo_transCurrencies":[{"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                 "settleInfo_settleCurrency":"CAD","baseInfo_nodeID": "sgp","settleInfo_mccr": 0.17}

                elif 'MOP_Auto_GrabPay_009' in str(query_params):
                    dict_info = {"baseInfo_mopID": "MOP_Auto_GrabPay_009","baseInfo_brandID": "Auto_GrabPay_009",
                    "baseInfo_transCurrencies":[{"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                 "settleInfo_settleCurrency":"CAD","baseInfo_nodeID": "sgp","settleInfo_mccr": 0.17}

                elif 'MOP_Auto_GrabPay_B01' in str(query_params):
                    dict_info = {"baseInfo_mopID": "MOP_Auto_GrabPay_B01","baseInfo_brandID": "Auto_GrabPay_B01"}



                elif 'MOP_Auto_GrabPay_32' in str(query_params):
                    dict_info = {"baseInfo_mopID": "MOP_Auto_GrabPay_32", "baseInfo_brandID": "Auto_GrabPay_32",
                                 "settleInfo_settleCurrency": "JPY", "baseInfo_nodeID": "tyo"}

                elif 'MOP_Auto_GrabPay_B1' in str(query_params):
                    dict_info = {"baseInfo_mopID": "MOP_Auto_GrabPay_B1", "baseInfo_brandID": "Auto_GrabPay_B1"}
                common_dict_info.update(dict_info)
                mongo_initial(db_tyo_evoconfig).create_mop(**common_dict_info)


            if table == 'customizeConfig':
                self.db.delete_one(table=table, query_params=query_params)
                self.db_sgp.delete_one(table=table, query_params=query_params)
                common_dict_info = {
                'isSettlementAmountEVONETCalculated' :True,
                'settleCurrency' :'JPY',
                'mccr' : 0.0}

                if 'WOP_Auto_JCoinPay_002' in str(query_params):
                    dict_info = {'wopID' :'WOP_Auto_JCoinPay_002',
                    'mopID' : 'MOP_Auto_GrabPay_002',
                    'mccr ': 0.13,
                    'wccr':0.12}
                    mongo_initial(db_tyo_evoconfig).create_cusomizeConfig(**dict_info)
                elif 'WOP_Auto_JCoinPay_02' in str(query_params):
                    dict_info = {'wopID' :'WOP_Auto_JCoinPay_02',
                    'mopID' : 'MOP_Auto_GrabPay_02',
                    'mccr ': 0.13,
                    'wccr':0.12}
                    mongo_initial(db_tyo_evoconfig).create_cusomizeConfig(**dict_info)

                else:
                    if 'MOP_Auto_GrabPay_031' in str(query_params):
                        dict_info ={
                        'wopID' :'WOP_Auto_JCoinPay_031',
                        'mopID' : 'MOP_Auto_GrabPay_031'}

                    elif 'MOP_Auto_GrabPay_032' in str(query_params):
                        dict_info ={
                        'wopID' :'WOP_Auto_JCoinPay_032',
                        'mopID' : 'MOP_Auto_GrabPay_032'}


                    elif 'WOP_Auto_JCoinPay_bilateral001' in str(query_params):
                        dict_info ={
                        'wopID' :'WOP_Auto_JCoinPay_bilateral001',
                        'mopID' : 'MOP_Auto_GrabPay_bilateral001',
                        'mccr' :0.13,
                        'settleCurrency':'CAD'
                        }

                    elif 'MOP_Auto_GrabPay_31' in str(query_params):
                        dict_info ={
                        'wopID' :'WOP_Auto_JCoinPay_31',
                        'mopID' : 'MOP_Auto_GrabPay_31'}

                    elif 'MOP_Auto_GrabPay_32' in str(query_params):
                        dict_info ={
                        'wopID' :'WOP_Auto_JCoinPay_32',
                        'mopID' : 'MOP_Auto_GrabPay_32'}

                    elif 'WOP_Auto_JCoinPay_bilateral01' in str(query_params):
                        dict_info ={
                        'wopID' :'WOP_Auto_JCoinPay_bilateral01',
                        'mopID' : 'MOP_Auto_GrabPay_bilateral01',
                        'mccr' :0.13,
                        'settleCurrency':'CAD'
                        }

                    common_dict_info.update(dict_info)
                    mongo_initial(db_tyo_evoconfig).create_customizeConfig01(**common_dict_info)

            if table == 'relation':
            # 前置条件：修改relation中的wopID（先删除这个mop，然后新增语句）
                self.db.delete_one(table=table, query_params=update_params)
                self.db_sgp.delete_one(table=table, query_params=query_params)
                Create_Mongo_Data(self.db).create_relation(mopID=self.mopID,
                                                               wopID=self.wopID,operationalNode='tyo')
            
            if table == 'brand':
            # 前置条件：修改relation中的wopID（先删除这个mop，然后新增语句）
                self.db.delete_one(table=table, query_params=update_params)
                self.db_sgp.delete_one(table=table, query_params=query_params)
                Create_Mongo_Data(self.db).create_brand(brandID=self.brandID,
                                                               deleteFlag=False,operationalNode='tyo')

    def delete_data(self, table, query_params):
        self.db.delete_manys(table=table,query_params=query_params)
        self.db_sgp.delete_one(table=table, query_params=query_params)

    def delete_data_reset(self, table):
        if table=='relation':
            Create_Mongo_Data(self.db).create_relation(mopID=self.mopID,
                                                                wopID=self.wopID,operationalNode='tyo')

        if table=='wop':
            Create_Mongo_Data(self.db).create_wop(baseInfo_wopID=self.wopID,
                                                           baseInfo_brandID=self.brandID, baseInfo_nodeID=self.nodeID_wop,
                                                           baseInfo_status='active',
                                                           settleInfo_fileInitiator='evonet',
                                                           settleInfo_specialCategory='',
                                                           settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                           settleInfo_settleCurrency='JPY',
                                                           settleInfo_cpmInterchangeFeeRate=0.0,
                                                           settleInfo_mpmInterchangeFeeRate=0.0,
                                                           settleInfo_settleFileTime='09:00+0800',
                                                           settleInfo_isBillingAmountCalculated=False,
                                                           settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                           settleInfo_cccr=0.0,
                                                           settleInfo_transactionProcessingFeeRate=0.0,
                                                           settleInfo_transProcessingFeeCollectionMethod='daily',
                                                           settleInfo_fxProcessingFeeRate=0.0,
                                                           settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                           settleInfo_fxRebateCollectionMethod='daily',
                                                           specialInfo_specialType='',
                                                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        if table == 'mop':
            Create_Mongo_Data(self.db).create_mop(baseInfo_mopID=self.mopID,
                                                           baseInfo_brandID=self.brandID, baseInfo_nodeID=self.nodeID_mop,
                                                           baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                           baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                           baseInfo_isRefundSupported=True,
                                                           baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                           baseInfo_schemeInfo_schemeName='',
                                                           baseInfo_schemeInfo_signStatus='',
                                                           settleInfo_fileInitiator='evonet',
                                                           settleInfo_settleCurrency='JPY',
                                                           settleInfo_cpmInterchangeFeeRate=0.0,
                                                           settleInfo_mpmInterchangeFeeRate=0.0,
                                                           settleInfo_settleFileTime="09:00+0800",
                                                           settleInfo_mccr=0.0,
                                                           settleInfo_transactionProcessingFeeRate=0.0,
                                                           settleInfo_transProcessingFeeCollectionMethod='daily',
                                                           settleInfo_fxProcessingFeeRate=0.0,
                                                           settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                           settleInfo_fxRebateCollectionMethod='daily',
                                                           settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                           specialInfo_specialType='',
                                                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

class Delete_Mongo_Data(object):
    def __init__(self,database_connection):
        self.db = database_connection  #evoconfig
    def delete_config(self):


        self.db.delete_manys(table='wop', query_params={"baseInfo.wopID" :{"$regex":"^WOP_Auto"}})
        self.db.delete_manys(table='mop', query_params={"baseInfo.mopID":{"$regex":"^MOP_Auto"}})
        self.db.delete_manys(table='customizeConfig', query_params={"wopID": {"$regex": "^WOP_Auto"}})
        self.db.delete_manys(table='brand', query_params={"brandID": {"$regex": "^Auto"}})
        self.db.delete_manys(table='relation', query_params={"wopID": {"$regex": "^WOP_Auto"}})
        self.db.delete_manys(table='relation', query_params={"mopID": {"$regex": "^MOP_Auto"}})
        self.db.delete_manys(table='mpmQrIdentifier', query_params={"mopID": {"$regex": "^MOP_Auto"}})
        self.db.delete_manys(table='cpmTokenIdentifier', query_params={"mopID": {"$regex": "^MOP_Auto"}})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": {"$regex": "^auto_user"}})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet","ccy1":"JPY","ccy2":"CAD"})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet", "ccy1": "CAD","ccy2": "EUR"})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet", "ccy1": "EUR","ccy2": "USD"})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet", "ccy1": "JPY","ccy2": "EUR"})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet", "ccy1": "CAD","ccy2": "JPY"})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet", "ccy1": "JPY","ccy2": "USD"})
        self.db.delete_manys(table='fx_rate', query_params={"fxRateOwner": "evonet", "ccy1": "CAD","ccy2": "USD"})
    def delete_trans(self,query_params):
        #删除trans表数据
        self.db.delete_manys(table='trans', query_params=query_params)


class singleNode_data():
    def create_settle_data_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_single_direct_wop',baseInfo_brandID='Auto_single_direct_wop', baseInfo_nodeID='tyo',baseInfo_status='active',settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily', deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_single_direct_mop', baseInfo_brandID='Auto_single_direct_wop', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies= [ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                                                                          settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                                          settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                                                                          settleInfo_settleFileTime="09:00+0800",
                                                                          settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                                          settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                                                                          settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily',
                                                                        settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                                          deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_single_direct_mop', wopID='WOP_Auto_single_direct_wop', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                                                                          isMPMSupported=True, isRefundSupported=True, transCurrencies=  ['JPY','HKD','SGD']
            ,settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                                                                          transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                                                                          fxProcessingFeeCollectionMethod='daily',
                                                                          deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_single_direct_mop',wopID='WOP_Auto_single_direct_wop',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_single_direct_wop', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_single_direct_mop', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_single_direct_mop',qrIdentifier='https://single_direct_wop.com',deleteFlag=False,operationalNode='tyo')


    def create_settle_data_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_single_evonet_model',baseInfo_brandID='Auto_single_evonet_model', baseInfo_nodeID='tyo',baseInfo_status='active',settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily', deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_single_evonet_model', baseInfo_brandID='Auto_single_evonet_model', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                                                                          settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                                          settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                                                                          settleInfo_settleFileTime="09:00+0800",
                                                                          settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                                          settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                                                                          settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                                          deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_single_evonet_model', wopID='WOP_Auto_single_evonet_model', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                                                                          isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                                                                          transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                                                                          fxProcessingFeeCollectionMethod='daily',
                                                                          deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_single_evonet_model',wopID='WOP_Auto_single_evonet_model',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_single_evonet_model', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_single_evonet_model', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_single_evonet_model',qrIdentifier='https://single_evonet_model.com',deleteFlag=False,operationalNode='tyo')

    def create_settle_data_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_single_direct_evonet',
                                                       baseInfo_brandID='Auto_single_direct_evonet',
                                                       baseInfo_nodeID='tyo', baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_single_direct_evonet',
                                                       baseInfo_brandID='Auto_single_direct_evonet',
                                                       baseInfo_nodeID='tyo', baseInfo_status='active',
                                                       baseInfo_useEVONETToken=True, baseInfo_isCPMSupported=True,
                                                       baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_single_direct_evonet',
                                                                   wopID='WOP_Auto_single_direct_evonet',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active', isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0, mccr=0.0, wccr=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_single_direct_evonet',
                                                            wopID='WOP_Auto_single_direct_evonet',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_single_direct_evonet', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_single_direct_evonet',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_single_direct_evonet',
                                                                   qrIdentifier='https://single_direct_evonet.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    # #wopID_01(WOP_Auto_JCoinPay_01)，mopID_01(MOP_Auto_GrabPay_01),brandID_01(Auto_GrabPay_01),(qrPayload":"https://AutoGrabPay01.com):singleNode_create_no_currency_transfer_data(单节点无币种转换,个性化配置表清算模式为直清清算,一对一关系，有配置关系,未超过cutofftime,evonet生成token)
    def create_no_currency_transfer_data(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_01',baseInfo_brandID='Auto_GrabPay_01', baseInfo_nodeID='tyo',baseInfo_status='active',settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily', deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_01', baseInfo_brandID='Auto_GrabPay_01', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                                                                          settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                                          settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                                                                          settleInfo_settleFileTime="09:00+0800",
                                                                          settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                                          settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                                                                          settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                                          deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_01', wopID='WOP_Auto_JCoinPay_01', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                                                                          isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                                                                          transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                                                                          fxProcessingFeeCollectionMethod='daily',
                                                                          deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_01',wopID='WOP_Auto_JCoinPay_01',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_01', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_01', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_01',qrIdentifier='https://AutoGrabPay01.com',deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/HKD',ccy1='JPY',ccy1Code='392',ccy2='HKD',ccy2Code='344',bid=0.3,ask=0.2,mid=0.4)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='HKD/JPY',ccy1='HKD',ccy1Code='344',ccy2='JPY',ccy2Code='392',bid=0.3,ask=0.2,mid=0.4)






    def updata_config_data(self):
            # #wopID_B1(WOP_Auto_JCoinPay_B1)，mopID_B1(MOP_Auto_GrabPay_B1),brandID_B1(Auto_GrabPay_B1),(qrPayload":"https://AutoGrabPayB1.com):singleNode_create_no_currency_transfer_data(用于修改配置的wopID,mopID)


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_B1',baseInfo_brandID='Auto_GrabPay_B1',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        print('wop_success')
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_B1', baseInfo_brandID='Auto_GrabPay_B1', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_B1', wopID='WOP_Auto_JCoinPay_B1', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_B1',wopID='WOP_Auto_JCoinPay_B1',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_B1', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_B1', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_B1',qrIdentifier='https://AutoGrabPayB1.com',deleteFlag=False,operationalNode='tyo')

    
            # #wopID_A1(WOP_Auto_JCoinPay_A1)，mopID_A1(MOP_Auto_GrabPay_A1),brandID_A1(Auto_GrabPay_A1),(qrPayload":"https://AutoGrabPayA1.com):singleNode_create_wop_innormal_01(单节点,wop status=locked)
    def create_wop_innormal_01(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A1',baseInfo_brandID='Auto_GrabPay_A1',baseInfo_nodeID='tyo',baseInfo_status='locked',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A1', baseInfo_brandID='Auto_GrabPay_A1', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A1', wopID='WOP_Auto_JCoinPay_A1', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A1',wopID='WOP_Auto_JCoinPay_A1',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A1', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A1', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A1',qrIdentifier='https://AutoGrabPayA1.com',deleteFlag=False,operationalNode='tyo')
    # #wopID_A2(WOP_Auto_JCoinPay_A2)，mopID_A2(MOP_Auto_GrabPay_A2),brandID_A2(Auto_GrabPay_A2),(qrPayload":"https://AutoGrabPayA2.com):singleNode_create_wop_innormal_02(单节点,wop deleteFlag=True)
    def create_wop_innormal_02(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A2',baseInfo_brandID='Auto_GrabPay_A2',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=True,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A2', baseInfo_brandID='Auto_GrabPay_A2', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A2', wopID='WOP_Auto_JCoinPay_A2', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A2',wopID='WOP_Auto_JCoinPay_A2',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A2', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A2', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A2',qrIdentifier='https://AutoGrabPayA2.com',deleteFlag=False,operationalNode='tyo')
    # #wopID_A3(WOP_Auto_JCoinPay_A3)，mopID_A3(MOP_Auto_GrabPay_A3),brandID_A3(Auto_GrabPay_A3),(qrPayload":"https://AutoGrabPayA3.com):singleNode_create_mop_innormal_01(单节点,mop status=locked)
    def create_mop_innormal_01(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A3',baseInfo_brandID='Auto_GrabPay_A3',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A3', baseInfo_brandID='Auto_GrabPay_A3', baseInfo_nodeID='tyo', baseInfo_status='locked',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0, settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A3', wopID='WOP_Auto_JCoinPay_A3', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A3',wopID='WOP_Auto_JCoinPay_A3',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A3', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A3', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A3',qrIdentifier='https://AutoGrabPayA3.com',deleteFlag=False,operationalNode='tyo')
# #l.wopID_A4(WOP_Auto_JCoinPay_A4)，mopID_A4(MOP_Auto_GrabPay_A4),brandID_A4(Auto_GrabPay_A4),(qrPayload":"https://AutoGrabPayA4.com):singleNode_create_mop_innormal_02(单节点,mop deleteFlag=True)
    def create_mop_innormal_02(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A4',baseInfo_brandID='Auto_GrabPay_A4',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A4', baseInfo_brandID='Auto_GrabPay_A4', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=True, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A4', wopID='WOP_Auto_JCoinPay_A4', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A4',wopID='WOP_Auto_JCoinPay_A4',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A4', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A4', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A4',qrIdentifier='https://AutoGrabPayA4.com',deleteFlag=False,operationalNode='tyo')
# #wopID_A5(WOP_Auto_JCoinPay_A5)，mopID_A5(MOP_Auto_GrabPay_A5),brandID_A5(Auto_GrabPay_A5),(qrPayload":"https://AutoGrabPayA5.com):singleNode_create_relation_innormal_01(单节点,relation不存在，wop和*不存在，mop和*不存在)
    def create_relation_innormal_01(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A5',baseInfo_brandID='Auto_GrabPay_A5',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A5', baseInfo_brandID='Auto_GrabPay_A5', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A5', wopID='WOP_Auto_JCoinPay_A5', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A5', deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A5', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A5',qrIdentifier='https://AutoGrabPayA5.com',deleteFlag=False,operationalNode='tyo')
# #n.wopID_A6(WOP_Auto_JCoinPay_A6)，mopID_A6(MOP_Auto_GrabPay_A6),brandID_A6(Auto_GrabPay_A6),(qrPayload":"https://AutoGrabPayA6.com):singleNode_create_relation_innormal_02(单节点,relation:wop和*存在)
    def create_relation_innormal_02(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A6',baseInfo_brandID='Auto_GrabPay_A6',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A6', baseInfo_brandID='Auto_GrabPay_A6', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A6', wopID='WOP_Auto_JCoinPay_A6', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_A6',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A6', deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A6', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A6',qrIdentifier='https://AutoGrabPayA6.com',deleteFlag=False,operationalNode='tyo')
        # #o.wopID_A7(WOP_Auto_JCoinPay_A7)，mopID_A7(MOP_Auto_GrabPay_A7),brandID_A7(Auto_GrabPay_A7),(qrPayload":"https://AutoGrabPayA7.com):singleNode_create_relation_innormal_03(单节点,relation:mop和*存在)
    def create_relation_innormal_03(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A7',baseInfo_brandID='Auto_GrabPay_A7',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A7', baseInfo_brandID='Auto_GrabPay_A7', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A7', wopID='WOP_Auto_JCoinPay_A7', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A7',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A7', deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A7', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A7',qrIdentifier='https://AutoGrabPayA7.com',deleteFlag=False,operationalNode='tyo')
    # #.wopID_A8(WOP_Auto_JCoinPay_A8)，mopID_A8(MOP_Auto_GrabPay_A8),brandID_A8(Auto_GrabPay_A8),(qrPayload":"https://AutoGrabPayA8.com):singleNode_create_brand_innormal(单节点,brand表没有mop对应的brandID)
    def create_brand_innormal(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A8',baseInfo_brandID='Auto_GrabPay_A8',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A8', baseInfo_brandID='Auto_GrabPay_A8', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0, settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A8', wopID='WOP_Auto_JCoinPay_A8', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A8',wopID='WOP_Auto_JCoinPay_A8',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A8', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A8',qrIdentifier='https://AutoGrabPayA8.com',deleteFlag=False,operationalNode='tyo')
# #.wopID_A9(WOP_Auto_JCoinPay_A9)，mopID_A9(MOP_Auto_GrabPay_A9),brandID_A9(Auto_GrabPay_A9),(qrPayload":"https://AutoGrabPayA9.com):singleNode_create_upsupported_trans_01(单节点,，MOP不支持CPM模式,MPM模式(support模式为false))
    def create_upsupported_trans_01(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A9',baseInfo_brandID='Auto_GrabPay_A9',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A9', baseInfo_brandID='Auto_GrabPay_A9', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=False,baseInfo_isMPMSupported=False,baseInfo_isRefundSupported=False,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A9', wopID='WOP_Auto_JCoinPay_A9', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=False,
                           isMPMSupported=False, isRefundSupported=False, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A9',wopID='WOP_Auto_JCoinPay_A9',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A9', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A9', deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A9',qrIdentifier='https://AutoGrabPayA9.com',deleteFlag=False,operationalNode='tyo')
# #b.wopID_02(WOP_Auto_JCoinPay_02)，mopID_02(MOP_Auto_GrabPay_02),brandID_02(Auto_GrabPay_02):singleNode_create_currency_transfer_data_02(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，evonet生成token，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_02(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_02',baseInfo_brandID='Auto_GrabPay_02',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='EUR',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='02:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='USD',settleInfo_wccr=0.14,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_02', baseInfo_brandID='Auto_GrabPay_02', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='CAD', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="02:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_02', wopID='WOP_Auto_JCoinPay_02', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.13,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_02',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_02',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_02', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_02', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_02',qrIdentifier='https://AutoGrabPay02.com',deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/CAD',ccy1='JPY',ccy1Code='392',ccy2='CAD',ccy2Code='124',bid=0.06,ask=0.05,mid=0.07)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='CAD/EUR',ccy1='CAD',ccy1Code='124',ccy2='EUR',ccy2Code='978',bid=0.08,ask=0.07,mid=0.09)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='EUR/USD',ccy1='EUR',ccy1Code='978',ccy2='USD',ccy2Code='840',bid=0.1,ask=0.09,mid=0.11)
##b.c.wopID_03(WOP_Auto_JCoinPay_03)，mopID_03(MOP_Auto_GrabPay_03),brandID_03(Auto_GrabPay_03)(单节点币种转换(transcurrency:JPY,mopsettleCurrency:JPY,wopsettleCurrency:EUR,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，超过cutofftime,mop生成token)
    def create_currency_transfer_data_03(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_03',baseInfo_brandID='Auto_GrabPay_03',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().over_cutoffTime(),settleInfo_settleCurrency='EUR',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='USD',settleInfo_wccr=0.12,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_03', baseInfo_brandID='Auto_GrabPay_03', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_03', wopID='WOP_Auto_JCoinPay_03', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.11,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_03',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_03',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_03', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_03', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_03',qrIdentifier='https://AutoGrabPay03.com',deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/EUR', ccy1='JPY', ccy1Code='392', ccy2='EUR',ccy2Code='978', bid=0.05, ask=0.04, mid=0.06)

        #Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="978",sourceCurrency="EUR",destinationCurrencyNumber="840",destinationCurrency="USD", value=0.09,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
#d.wopID_04(WOP_Auto_JCoinPay_04)，mopID_04(MOP_Auto_GrabPay_04),brandID_04(Auto_GrabPay_04):singleNode_create_currency_transfer_data_04(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:JPY,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_04(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_04',baseInfo_brandID='Auto_GrabPay_04',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='USD',settleInfo_wccr=0.12,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_04', baseInfo_brandID='Auto_GrabPay_04', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='CAD', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_04', wopID='WOP_Auto_JCoinPay_04', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.11,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_04',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_04',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_04', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_04', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_04',qrIdentifier='https://AutoGrabPay04.com',deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='CAD/JPY',ccy1='CAD',ccy1Code='124',ccy2='JPY',ccy2Code='392',bid=0.08,ask=0.07,mid=0.09)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/USD',ccy1='JPY',ccy1Code='392',ccy2='USD',ccy2Code='840',bid=0.1,ask=0.09,mid=0.11)






##e.wopID_05(WOP_Auto_JCoinPay_05)，mopID_05(MOP_Auto_GrabPay_05),brandID_05(Auto_GrabPay_05):singleNode_create_currency_transfer_data_05(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUA,billingCurrency:JPY),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_05(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_05',baseInfo_brandID='Auto_GrabPay_05',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='EUR',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.12,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_05', baseInfo_brandID='Auto_GrabPay_05', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='CAD', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_05', wopID='WOP_Auto_JCoinPay_05', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.11,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_05',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_05',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_05', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_05', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_05',qrIdentifier='https://AutoGrabPay05.com',deleteFlag=False,operationalNode='tyo')

        #Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="124",destinationCurrency="CAD", value=0.05,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="124",sourceCurrency="CAD",destinationCurrencyNumber="978",destinationCurrency="EUR", value=0.07,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
#f.wopID_06(WOP_Auto_JCoinPay_06)，mopID_06(MOP_Auto_GrabPay_06),brandID_06(Auto_GrabPay_06):singleNode_create_currency_transfer_data_06(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:CAD,billingCurrency:USD),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_06(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_06',
                                                       baseInfo_brandID='Auto_GrabPay_06', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_06',
                                                       baseInfo_brandID='Auto_GrabPay_06', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_06',
                                                                   wopID='WOP_Auto_JCoinPay_06',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')


        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_06', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_06',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_06', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_06',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_06',
                                                                   qrIdentifier='https://AutoGrabPay06.com',
                                                                   deleteFlag=False,operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="124",destinationCurrency="CAD", value=0.05,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="124",sourceCurrency="CAD",destinationCurrencyNumber="840",destinationCurrency="USD", value=0.11,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='CAD/USD',ccy1='CAD',ccy1Code='124',ccy2='USD',ccy2Code='840',bid=0.12,ask=0.11,mid=0.13)
    # g.wopID_07(WOP_Auto_JCoinPay_07)，mopID_07(MOP_Auto_GrabPay_07),brandID_07(Auto_GrabPay_07):singleNode_create_currency_transfer_data_07(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:EUR),读取个性化配置，个性化配置表清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_07(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_07',
                                                       baseInfo_brandID='Auto_GrabPay_07', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='EUR', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_07',
                                                       baseInfo_brandID='Auto_GrabPay_07', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_07',
                                                                   wopID='WOP_Auto_JCoinPay_07',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_07', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_07',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_07', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_07',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_07',
                                                                   qrIdentifier='https://AutoGrabPay07.com',
                                                                   deleteFlag=False,operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="124",destinationCurrency="CAD", value=0.05,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="124", sourceCurrency="CAD",
        #                                                   destinationCurrencyNumber="840", destinationCurrency="USD",
        #                                                   value=0.11, deleteFlag=False, fxRateOwner='auto_user',operationalNode='tyo')

        # b.wopID_09(WOP_Auto_JCoinPay_09)，mopID_09(MOP_Auto_GrabPay_09), brandID_09(Auto_GrabPay_09): singleNode_create_currency_transfer_data_09(单节点币种转换( transcurrency:JPY, mopsettleCurrency: CAD, wopsettleCurrency: EUR, billingCurrency: USD), 无个性化配置，读取wop / mop表配置，清算模式为evonet清算, wop和 *，mop和 *，evonet生成token，未超过cutofftime, mop生成token）
    def create_currency_transfer_data_09(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_09',
                                                       baseInfo_brandID='Auto_GrabPay_09', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_09',
                                                       baseInfo_brandID='Auto_GrabPay_09', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))


        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_09', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_09',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_09', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_09',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_09',
                                                                   qrIdentifier='https://AutoGrabPay09.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/CAD',ccy1='JPY',ccy1Code='392',ccy2='CAD',ccy2Code='124',bid=0.06,ask=0.05,mid=0.07,fxRateOwner='evonet')
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='CAD/EUR',ccy1='CAD',ccy1Code='124',ccy2='EUR',ccy2Code='978',bid=0.08,ask=0.07,mid=0.09,fxRateOwner='evonet')
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='EUR/USD',ccy1='EUR',ccy1Code='978',ccy2='USD',ccy2Code='840',bid=0.1,ask=0.09,mid=0.11,fxRateOwner='evonet')

    #c.wopID_10(WOP_Auto_JCoinPay_10)，mopID_10(MOP_Auto_GrabPay_10),brandID_10(Auto_GrabPay_10):singleNode_create_currency_transfer_data_10(单节点币种转换(transcurrency:JPY,mopsettleCurrency:JPY,wopsettleCurrency:EUR,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_10(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_10',
                                                       baseInfo_brandID='Auto_GrabPay_10', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_10',
                                                       baseInfo_brandID='Auto_GrabPay_10', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_10', wopID='WOP_Auto_JCoinPay_10',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_10',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_10', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_10',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_10',
                                                                   qrIdentifier='https://AutoGrabPay10.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/EUR', ccy1='JPY', ccy1Code='392', ccy2='EUR',ccy2Code='978', bid=0.05, ask=0.04, mid=0.06,fxRateOwner='evonet')
    #d.wopID_11(WOP_Auto_JCoinPay_11)，mopID_11(MOP_Auto_GrabPay_11),brandID_11(Auto_GrabPay_11):singleNode_create_currency_transfer_data_11(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:JPY,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_11(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_11',baseInfo_brandID='Auto_GrabPay_11',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='USD',settleInfo_wccr=0.12,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_11', baseInfo_brandID='Auto_GrabPay_11', baseInfo_nodeID='tyo', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='CAD', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

    

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_11',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_11',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_11', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_11', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_11',qrIdentifier='https://AutoGrabPay11.com',deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='CAD/JPY',ccy1='CAD',ccy1Code='124',ccy2='JPY',ccy2Code='392',bid=0.08,ask=0.07,mid=0.09,fxRateOwner='evonet')
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/USD',ccy1='JPY',ccy1Code='392',ccy2='USD',ccy2Code='840',bid=0.1,ask=0.09,mid=0.11,fxRateOwner='evonet')
    #e.wopID_12(WOP_Auto_JCoinPay_12)，mopID_12(MOP_Auto_GrabPay_12),brandID_12(Auto_GrabPay_12):singleNode_create_currency_transfer_data_12(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:JPY),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)

    def create_currency_transfer_data_12(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_12',
                                                       baseInfo_brandID='Auto_GrabPay_12', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_12',
                                                       baseInfo_brandID='Auto_GrabPay_12', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_12', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_12',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_12', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_12',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_12',
                                                                   qrIdentifier='https://AutoGrabPay12.com',
                                                                   deleteFlag=False,operationalNode='tyo')
    #f.wopID_13(WOP_Auto_JCoinPay_13)，mopID_13(MOP_Auto_GrabPay_13),brandID_13(Auto_GrabPay_13):singleNode_create_currency_transfer_data_13(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:CAD,billingCurrency:USD),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_13(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_13',
                                                       baseInfo_brandID='Auto_GrabPay_13', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_13',
                                                       baseInfo_brandID='Auto_GrabPay_13', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))



        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_13', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_13',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_13', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_13',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_13',
                                                                   qrIdentifier='https://AutoGrabPay13.com',
                                                                   deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='CAD/USD', ccy1='CAD', ccy1Code='124', ccy2='USD', ccy2Code='840', bid=0.12, ask=0.11, mid=0.13,fxRateOwner='evonet')
    #g.wopID_14(WOP_Auto_JCoinPay_14)，mopID_14(MOP_Auto_GrabPay_14),brandID_14(Auto_GrabPay_14):singleNode_create_currency_transfer_data_14(单节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:EUR),无个性化配置，读取wop/mop表配置，清算模式为evonet清算,wop和*，mop和*，未超过cutofftime,mop生成token)
    def create_currency_transfer_data_14(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_14',
                                                       baseInfo_brandID='Auto_GrabPay_14', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='EUR', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_14',
                                                       baseInfo_brandID='Auto_GrabPay_14', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

     

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_14', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_14',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_14', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_14',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_14',
                                                                   qrIdentifier='https://AutoGrabPay14.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        # p.wopID_A12(WOP_Auto_JCoinPay_A12)，mopID_A12(MOP_Auto_GrabPay_A12), brandID_A12（Auto_GrabPay_A12), (qrPayload":"https: // AutoGrabPayA12.com): singleNode_create_upsupported_refund_01( 单节点, refund(support模式为false))

    def create_currency_transfer_data_bilateral01(self):
        common_dict_info={'baseInfo_brandID':'Auto_GrabPay_bilateral01','baseInfo_nodeID':'tyo',}
        wop_params = {'baseInfo_wopID':'WOP_Auto_JCoinPay_bilateral01','settleInfo_settleCurrency':'EUR','settleInfo_billingCurrency':'EUR',
                      'settleInfo_wccr':0.12,'settleInfo_cccr':0.15,'baseInfo_brandID':'Auto_GrabPay_bilateral01'}

        mop_params = {'baseInfo_mopID':'MOP_Auto_GrabPay_bilateral01','baseInfo_mopID':'MOP_Auto_GrabPay_bilateral01',
                      'baseInfo_brandID':'Auto_GrabPay_bilateral01','settleInfo_settleCurrency':'CAD','settleInfo_mccr':0.17,
                      "baseInfo_transCurrencies": [{"currency": "JPY", "mccr": 0.12}, {"currency": "HKD", "mccr": 0.3}, {"currency": "SGD", "mccr": 0.3}],}
        customizeConfig01_params = {'mopID':'MOP_Auto_GrabPay_bilateral01','wopID':'WOP_Auto_JCoinPay_bilateral01',
                                    'settleCurrency':'CAD','mccr':0.13,   }
        mongo_initial(db_tyo_evoconfig).create_wop(**wop_params)
        mongo_initial(db_tyo_evoconfig).create_mop(**mop_params)
        mongo_initial(db_tyo_evoconfig).create_customizeConfig01(**customizeConfig01_params)
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_bilateral01', wopID='WOP_Auto_JCoinPay_bilateral01',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_bilateral01', deleteFlag=False,
                                                         operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_bilateral01',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_bilateral01',
                                                                   qrIdentifier='https://AutoGrabPaybilateral01.com',
                                                                   deleteFlag=False, operationalNode='tyo')
    def singleNode_create_upsupported_refund_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A12',
                                                       baseInfo_brandID='Auto_GrabPay_A12', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', settleInfo_fileInitiator='evonet',
                                                       specialInfo_specialType='', settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', deleteFlag=False,
                                                       operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A12',
                                                       baseInfo_brandID='Auto_GrabPay_A12', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=False,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A12',
                                                                   wopID='WOP_Auto_JCoinPay_A12',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=False,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A12', wopID='WOP_Auto_JCoinPay_A12',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A12', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A12',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A12',
                                                                   qrIdentifier='https://AutoGrabPayA12.com',
                                                                   deleteFlag=False,operationalNode='tyo')
#p.wopID_A13(WOP_Auto_JCoinPay_A13)，mopID_A13(MOP_Auto_GrabPay_A13),brandID_A13(Auto_GrabPay_A13),(qrPayload":"https://AutoGrabPayA13.com):singleNode_create_upsupported_refund_02(单节点,refund(内容为空))
    def singleNode_create_upsupported_refund_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A13',
                                                       baseInfo_brandID='Auto_GrabPay_A13', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', settleInfo_fileInitiator='evonet',
                                                       specialInfo_specialType='', settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', deleteFlag=False,
                                                       operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A13',
                                                       baseInfo_brandID='Auto_GrabPay_A13', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=None,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A13',
                                                                   wopID='WOP_Auto_JCoinPay_A13',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported='',
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A13', wopID='WOP_Auto_JCoinPay_A13',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A13', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A13',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A13',
                                                                   qrIdentifier='https://AutoGrabPayA13.com',
                                                                   deleteFlag=False,operationalNode='tyo')
#h.wopID_17(WOP_Auto_JCoinPay_17)，mopID_17(MOP_Auto_GrabPay_17),brandID_17(Auto_GrabPay_17):singleNode_create_isSettlementAmountEVONETCalculated_False_01(直清模式，wop和*，mop和*，isSettlementAmountEVONETCalculated=False,cutofftime超过当前时间)

    def create_isSettlementAmountEVONETCalculated_False_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_17',
                                                       baseInfo_brandID='Auto_GrabPay_17', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='17:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_17',
                                                       baseInfo_brandID='Auto_GrabPay_17', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="17:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_17',
                                                                   wopID='WOP_Auto_JCoinPay_17',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='bilateral',
                                                                   settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=False,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                    fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo',mccr=0.12,wccr=0.11)

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_17', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_17',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_17', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_17',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_17',
                                                                   qrIdentifier='https://AutoGrabPay17.com',
                                                                   deleteFlag=False,operationalNode='tyo')
      #  h.wopID_18(WOP_Auto_JCoinPay_18)，mopID_18(MOP_Auto_GrabPay_18), brandID_18Auto_GrabPay_18):singleNode_create_isSettlementAmountEVONETCalculated_False_02(直清模式，wop和 *，mop和 *，isSettlementAmountEVONETCalculated = False, cutofftime不超过当前时间)

    def create_isSettlementAmountEVONETCalculated_False_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_18',
                                                       baseInfo_brandID='Auto_GrabPay_18', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='18:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_18',
                                                       baseInfo_brandID='Auto_GrabPay_18', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="18:00+0800",
                                                       settleInfo_mccr=0.18,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_18',
                                                                   wopID='WOP_Auto_JCoinPay_18',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='bilateral',
                                                                   settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=False,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_18', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_18',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_18', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_18',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_18',
                                                                   qrIdentifier='https://AutoGrabPay18.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        #  h.wopID_22(WOP_Auto_JCoinPay_22)，mopID_22(MOP_Auto_GrabPay_22), brandID_22Auto_GrabPay_22):singleNode_create_isSettlementAmountEVONETCalculated_False_03(直清模式，wop和 *，mop和 *，isSettlementAmountEVONETCalculated = False, cutofftime不超过当前时间)

    def create_isSettlementAmountEVONETCalculated_False_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_22',
                                                       baseInfo_brandID='Auto_GrabPay_22', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       settleInfo_settleCurrency='HKD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='18:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_22',
                                                       baseInfo_brandID='Auto_GrabPay_22', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='HKD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="18:00+0800",
                                                       settleInfo_mccr=0.18,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_22',
                                                                   wopID='WOP_Auto_JCoinPay_22',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[
                                                                       {"currency": "JPY", "mccr": 0.11},
                                                                       {"currency": "HKD", "mccr": 0.3},
                                                                       {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='bilateral',
                                                                   settleCurrency='HKD',
                                                                   isSettlementAmountEVONETCalculated=False,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_22', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_22',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_22', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_22',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_22',
                                                                   qrIdentifier='https://AutoGrabPay22.com',
                                                                   deleteFlag=False, operationalNode='tyo')
#h.wopID_19(WOP_Auto_JCoinPay_19)，mopID_19(MOP_Auto_GrabPay_19),brandID_19(Auto_GrabPay_19):singleNode_create_fxrate_01(个性化表中mcc,wccr为null,单节点币种转换(transcurrency:JPY,mopsettleCurrency:SGD,wopsettleCurrency:NOK,billingCurrency:THB),fxrate表：(MOP:存在反向和中间汇率，SGD-JPY(0.21),JPY-USD(0.09),SGD-USD(0.41))(WOP:存在中间汇率，SGD-USD(0.41),NOK-USD(0.456))(billing:正向，反向，中间都存在NOK-THB(0.33)，THB-NOK(0.38),NOK-USD(0.456),THB-USD(0.59)))


    def create_fxrate_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_19',
                                                       baseInfo_brandID='Auto_GrabPay_19', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='NOK',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='19:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='THB', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_19',
                                                       baseInfo_brandID='Auto_GrabPay_19', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='SGD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="19:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_19',
                                                                   wopID='WOP_Auto_JCoinPay_19',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                    fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_19', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_19',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_19', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_19',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_19',
                                                                   qrIdentifier='https://AutoGrabPay19.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='SGD/JPY',ccy1='SGD',ccy1Code='702',ccy2='JPY',ccy2Code='392',bid=0.22,ask=0.21,mid=0.23)

        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="840",destinationCurrency="USD", value=0.09,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='SGD/USD',ccy1='SGD',ccy1Code='702',ccy2='USD',ccy2Code='940',bid=0.42,ask=0.41,mid=0.43)
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="702", sourceCurrency="SGD",
        #                                                   destinationCurrencyNumber="940", destinationCurrency="USD",
        #                                                   value=0.41, deleteFlag=False, fxRateOwner='auto_user',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='NOK/USD',ccy1='NOK',ccy1Code='576',ccy2='USD',ccy2Code='840',bid=0.466,ask=0.456,mid=0.477)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='NOK/THB',ccy1='NOK',ccy1Code='576',ccy2='THB',ccy2Code='764',bid=0.44,ask=0.33,mid=0.55)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='THB/NOK',ccy1='THB',ccy1Code='764',ccy2='NOK',ccy2Code='576',bid=0.45,ask=0.38,mid=0.56)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='THB/USD',ccy1='THB',ccy1Code='764',ccy2='USD',ccy2Code='840',bid=0.66,ask=0.59,mid=0.77)
#h.wopID_20(WOP_Auto_JCoinPay_20)，mopID_20(MOP_Auto_GrabPay_20),brandID_20(Auto_GrabPay_20):singleNode_create_fxrate_02(单节点币种转换(transcurrency:JPY,mopsettleCurrency:RUB,wopsettleCurrency:AUD,billingCurrency:KRW),fxrate表：(MOP:存在正向，反向,中间汇率，JPY-RUB(0.2),RUB-JPY(0.3),JPY-USD(0.09),RUB-USD(0.11)))(WOP:存在反向，中间汇率，AUD-RUB(0.33),RUB-USD(0.11),AUD-USD(0.234))(billing:存在中间汇率，AUD-USD(0.234),KRW-USD(0.487)))

    def create_fxrate_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_20',
                                                       baseInfo_brandID='Auto_GrabPay_20', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='AUD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='20:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='KRW', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_20',
                                                       baseInfo_brandID='Auto_GrabPay_20', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='RUB',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="20:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_20',
                                                                   wopID='WOP_Auto_JCoinPay_20',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_20', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_20',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_20', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_20',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_20',
                                                                   qrIdentifier='https://AutoGrabPay20.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='JPY/RUB',ccy1='JPY',ccy1Code='392',ccy2='RUB',ccy2Code='810',bid=0.3,ask=0.2,mid=0.4)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='RUB/JPY',ccy1='RUB',ccy1Code='810',ccy2='JPY',ccy2Code='392',bid=0.4,ask=0.3,mid=0.5)

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='RUB/USD',ccy1='RUB',ccy1Code='810',ccy2='USD',ccy2Code='940',bid=0.12,ask=0.11,mid=0.13)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='AUD/RUB',ccy1='AUD',ccy1Code='036',ccy2='RUB',ccy2Code='810',bid=0.43,ask=0.33,mid=0.53)

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='AUD/USD',ccy1='AUD',ccy1Code='036',ccy2='USD',ccy2Code='840',bid=0.334,ask=0.234,mid=0.534)

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='KRW/USD',ccy1='KRW',ccy1Code='410',ccy2='USD',ccy2Code='840',bid=0.587,ask=0.487,mid=0.687)

        # h.wopID_21(WOP_Auto_JCoinPay_21)，mopID_21(MOP_Auto_GrabPay_21),brandID_19(Auto_GrabPay_19):singleNode_create_fxrate_02(单节点币种转换(transcurrency:JPY,mopsettleCurrency:NZD,wopsettleCurrency:IDR,billingCurrency:DKK),fxrate表：(MOP:存在中间汇率，JPY-USD(0.09),NZD-USD(0.256))(WOP:存在反向 IDR-NZD(0.338))(billing:存在反向，中间汇率，DKK-IDR(0.145),IDR-USD(0.159),DKK-USD(0.195)))

    def create_fxrate_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_21',
                                                       baseInfo_brandID='Auto_GrabPay_21', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='IDR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='21:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='DKK', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_21',
                                                       baseInfo_brandID='Auto_GrabPay_21', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='NZD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="21:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_21',
                                                                   wopID='WOP_Auto_JCoinPay_21',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_21', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_21',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_21', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_21',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_21',
                                                                   qrIdentifier='https://AutoGrabPay21.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='NZD/USD',ccy1='NZD',ccy1Code='554',ccy2='USD',ccy2Code='840',bid=0.356,ask=0.256,mid=0.456)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='IDR/NZD',ccy1='IDR',ccy1Code='360',ccy2='NZD',ccy2Code='554',bid=0.438,ask=0.338,mid=0.538)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='DKK/IDR',ccy1='DKK',ccy1Code='208',ccy2='IDR',ccy2Code='360',bid=0.245,ask=0.145,mid=0.345)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='IDR/USD',ccy1='IDR',ccy1Code='360',ccy2='USD',ccy2Code='840',bid=0.259,ask=0.159,mid=0.359)
        Create_Mongo_Data(db_tyo_evoconfig).create_fx_Rate(ccyPair='DKK/USD',ccy1='DKK',ccy1Code='208',ccy2='USD',ccy2Code='840',bid=0.295,ask=0.195,mid=0.395)

        # g.wopID_23(WOP_Auto_JCoinPay_23)，mopID_23(MOP_Auto_GrabPay_23),brandID_23(Auto_GrabPay_23):singleNode_create_fxrate(双节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),fxrate表：(MOP:存在中间汇率，JPY-CAD(0.05))(WOP:存在反向 CAD-EUR(0.07) MCCR:0 WCCR:0)
    def create_currency_transfer_data_23(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_23',
                                                       baseInfo_brandID='Auto_GrabPay_23', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='02:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_23',
                                                       baseInfo_brandID='Auto_GrabPay_23', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="02:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_23',
                                                                   wopID='WOP_Auto_JCoinPay_23',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0},
                                                                                    {"currency": "HKD", "mccr": 0},
                                                                                    {"currency": "SGD", "mccr": 0}],
                                                                   settleMode='evonet', settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   mccr=0, wccr=0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_23', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_23',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_23', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_23',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_23',
                                                                   qrIdentifier='https://AutoGrabPay23.com',
                                                                   deleteFlag=False, operationalNode='tyo')
    def none_fxrate(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A14',
                                                       baseInfo_brandID='Auto_GrabPay_A14', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='CHF',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='02:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A14',
                                                       baseInfo_brandID='Auto_GrabPay_A14', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CHF',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="02:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A14',
                                                                   wopID='WOP_Auto_JCoinPay_A14',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='evonet', settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A14', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_A14',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A14', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A14',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A14',
                                                                   qrIdentifier='https://AutoGrabPayA14.com',
                                                                   deleteFlag=False, operationalNode='tyo')

        # g.wopID_31(WOP_Auto_JCoinPay_31)，mopID_23(MOP_Auto_GrabPay_31),brandID_31(Auto_GrabPay_31)直清模式 交易币种JPY wopfx_rate=1 mopfx_rate=1 mccr=wccr=1

    def create_direct_evonet_dual_31(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_31',
                                                       baseInfo_brandID='Auto_GrabPay_31',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_31',
                                                       baseInfo_brandID='Auto_GrabPay_31',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='bilateral', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_31',
                                                                   wopID='WOP_Auto_JCoinPay_31',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_31',
                                                            wopID='WOP_Auto_JCoinPay_31', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_31', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_31',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_31',
                                                                   qrIdentifier='https://AutoGrabPay31.com',
                                                                   deleteFlag=False, operationalNode='tyo')


    def create_yapi_single_01(self):
        Create_Mongo_Data(db_tyo_evoconfig,version='customize').create_wop(baseInfo_wopID='WOP_Auto_YapiWop_01',
                                                       baseInfo_brandID='Auto_Yapi_01',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig,version='customize').create_mop(baseInfo_mopID='MOP_Auto_YapiMop_01',
                                                       baseInfo_brandID='Auto_Yapi_01',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='bilateral', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_YapiMop_01',
                                                                   wopID='WOP_Auto_YapiWop_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_YapiMop_01',
                                                            wopID='WOP_Auto_YapiWop_01', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_Yapi_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_YapiMop_01',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_YapiMop_01',
                                                                   qrIdentifier='https://AutoYapiPay01.com',
                                                                   deleteFlag=False, operationalNode='tyo')




    def create_direct_evonet_dual_32(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_32',
                                                       baseInfo_brandID='Auto_GrabPay_32',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_32',
                                                       baseInfo_brandID='Auto_GrabPay_32',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='bilateral', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))


        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_32',
                                                            wopID='WOP_Auto_JCoinPay_32', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_32', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_32',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_32',
                                                                   qrIdentifier='https://AutoGrabPay32.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_MDAQ_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='MDAQ_WOP_01',
                                                       baseInfo_brandID='MDAQ_01',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='USD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='CNY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='bccardnacfusd',
                                                       baseInfo_brandID='MDAQ_01',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet',
                                                       specialInfo_specialType='',
                                                       settleInfo_settleCurrency='SGD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='bccardnacfusd',
                                                            wopID='MDAQ_WOP_01', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='MDAQ_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='bccardnacfusd',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='bccardnacfusd',
                                                                   qrIdentifier='https://bccardnacfusd.com',
                                                                   deleteFlag=False, operationalNode='tyo')



# cc=Delete_Mongo_Data('tyo_config_url').delete_config()
# dd=Delete_Mongo_Data('sgp_config_url').delete_config()
#双节点：# #wopID_001(WOP_Auto_JCoinPay_001)，mopID_001(MOP_Auto_GrabPay_001),brandID_001(Auto_GrabPay_001),(qrPayload":"https://AutoGrabPay01.com):singleNode_create_no_currency_transfer_data(单节点无币种转换,个性化配置表清算模式为直清清算,一对一关系，有配置关系,未超过cutofftime,evonet生成token)

class doubleNode_data():
    def create_settle_data_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_direct_wop_dual_fileinit_01',
                                                       baseInfo_brandID='Auto_direct_dual_fileinit_01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_direct_wop_dual_01',
                                                       baseInfo_brandID='Auto_direct_dual_fileinit_01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_direct_wop_dual_01',
                                                                   wopID='WOP_direct_wop_dual_fileinit_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_direct_wop_dual_01', wopID='WOP_direct_wop_dual_fileinit_01',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_direct_dual_fileinit_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_direct_wop_dual_01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_direct_wop_dual_01',
                                                                   qrIdentifier='https://Autodirectwop009.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='392',sourceCurrency='JPY',destinationCurrencyNumber='344',destinationCurrency='HKD',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='344',sourceCurrency='HKD',destinationCurrencyNumber='392',destinationCurrency='JPY',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        Create_Mongo_Data(db_sgp_evoconfig).create_wop(baseInfo_wopID='WOP_direct_wop_dual_fileinit_01',
                                                       baseInfo_brandID='Auto_direct_dual_fileinit_01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "sgp_signkeyC"))

        Create_Mongo_Data(db_sgp_evoconfig).create_mop(baseInfo_mopID='MOP_direct_wop_dual_01',
                                                       baseInfo_brandID='Auto_direct_dual_fileinit_01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "sgp_signkeyC"))

        Create_Mongo_Data(db_sgp_evoconfig).create_customizeConfig(mopID='MOP_direct_wop_dual_01',
                                                                   wopID='WOP_direct_wop_dual_fileinit_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')
        #
        Create_Mongo_Data(db_sgp_evoconfig).create_relation(mopID='MOP_direct_wop_dual_01', wopID='WOP_direct_wop_dual_fileinit_01',operationalNode='tyo')

        Create_Mongo_Data(db_sgp_evoconfig).create_brand(brandID='Auto_direct_dual_fileinit_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_sgp_evoconfig).create_cpmTokenIdentifier(mopID='MOP_direct_wop_dual_01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_sgp_evoconfig).create_mpmQrIdentifier(mopID='MOP_direct_wop_dual_01',
                                                                   qrIdentifier='https://Autodirectwop009.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_settle_data_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_direct_evonet_dual_01',
                                                       baseInfo_brandID='Auto_direct_evonet_dual_01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_direct_evonet_dual_01',
                                                       baseInfo_brandID='Auto_direct_evonet_dual_01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_direct_evonet_dual_01',
                                                                   wopID='WOP_direct_evonet_dual_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_direct_evonet_dual_01', wopID='WOP_direct_evonet_dual_01',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_direct_evonet_dual_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_direct_evonet_dual_01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_direct_evonet_dual_01',
                                                                   qrIdentifier='https://Autodirectevonetdual001.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='392',sourceCurrency='JPY',destinationCurrencyNumber='344',destinationCurrency='HKD',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='344',sourceCurrency='HKD',destinationCurrencyNumber='392',destinationCurrency='JPY',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        Create_Mongo_Data(db_sgp_evoconfig).create_wop(baseInfo_wopID='WOP_direct_evonet_dual_01',
                                                       baseInfo_brandID='Auto_direct_evonet_dual_01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "sgp_signkeyC"))

        Create_Mongo_Data(db_sgp_evoconfig).create_mop(baseInfo_mopID='MOP_direct_evonet_dual_01',
                                                       baseInfo_brandID='Auto_direct_evonet_dual_01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "sgp_signkeyC"))

        Create_Mongo_Data(db_sgp_evoconfig).create_customizeConfig(mopID='MOP_direct_evonet_dual_01',
                                                                   wopID='WOP_direct_evonet_dual_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')
        #
        Create_Mongo_Data(db_sgp_evoconfig).create_relation(mopID='MOP_direct_evonet_dual_01', wopID='WOP_direct_evonet_dual_01',operationalNode='tyo')

        Create_Mongo_Data(db_sgp_evoconfig).create_brand(brandID='Auto_direct_evonet_dual_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_sgp_evoconfig).create_cpmTokenIdentifier(mopID='MOP_direct_evonet_dual_01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_sgp_evoconfig).create_mpmQrIdentifier(mopID='MOP_direct_evonet_dual_01',
                                                                   qrIdentifier='https://Autodirectevonetdual001.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_settle_data_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_evonet_model_dual_01',
                                                       baseInfo_brandID='Auto_model_evonet_dual_01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_evonet_dual_single_01',
                                                       baseInfo_brandID='Auto_model_evonet_dual_01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_evonet_dual_single_01',
                                                                   wopID='WOP_evonet_model_dual_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_evonet_dual_single_01', wopID='WOP_evonet_model_dual_01',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_model_evonet_dual_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_evonet_dual_single_01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_evonet_dual_single_01',
                                                                   qrIdentifier='https://Autoevonetmodeldual001.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='392',sourceCurrency='JPY',destinationCurrencyNumber='344',destinationCurrency='HKD',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='344',sourceCurrency='HKD',destinationCurrencyNumber='392',destinationCurrency='JPY',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        Create_Mongo_Data(db_sgp_evoconfig).create_wop(baseInfo_wopID='WOP_evonet_model_dual_01',
                                                       baseInfo_brandID='Auto_model_evonet_dual_01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "sgp_signkeyC"))

        Create_Mongo_Data(db_sgp_evoconfig).create_mop(baseInfo_mopID='MOP_evonet_dual_single_01',
                                                       baseInfo_brandID='Auto_model_evonet_dual_01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "sgp_signkeyC"))

        Create_Mongo_Data(db_sgp_evoconfig).create_customizeConfig(mopID='MOP_evonet_dual_single_01',
                                                                   wopID='WOP_evonet_model_dual_01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')
        #
        Create_Mongo_Data(db_sgp_evoconfig).create_relation(mopID='MOP_evonet_dual_single_01', wopID='WOP_evonet_model_dual_01',operationalNode='tyo')

        Create_Mongo_Data(db_sgp_evoconfig).create_brand(brandID='Auto_model_evonet_dual_01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_sgp_evoconfig).create_cpmTokenIdentifier(mopID='MOP_evonet_dual_single_01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_sgp_evoconfig).create_mpmQrIdentifier(mopID='MOP_evonet_dual_single_01',
                                                                   qrIdentifier='https://Autoevonetmodeldual001.com',
                                                                   deleteFlag=False,operationalNode='tyo')


    def create_no_currency_transfer_data(self):

            Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_001',
                                                           baseInfo_brandID='Auto_GrabPay_001', baseInfo_nodeID='tyo',
                                                           baseInfo_status='active',
                               settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                               deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

            Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_001', baseInfo_brandID='Auto_GrabPay_001', baseInfo_nodeID='sgp', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                               settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                               settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                               settleInfo_settleFileTime="09:00+0800",
                               settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                               settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                               settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                               deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

            Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_001', wopID='WOP_Auto_JCoinPay_001', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                               isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                               transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                               fxProcessingFeeCollectionMethod='daily',
                               deleteFlag=False, operationalNode='tyo')

            Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_001',wopID='WOP_Auto_JCoinPay_001',operationalNode='tyo')

            Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_001', deleteFlag=False,operationalNode='tyo')

            Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_001', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
            Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_001',qrIdentifier='https://AutoGrabPay001.com',deleteFlag=False,operationalNode='tyo')

            # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='392',sourceCurrency='JPY',destinationCurrencyNumber='344',destinationCurrency='HKD',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
            # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='344',sourceCurrency='HKD',destinationCurrencyNumber='392',destinationCurrency='JPY',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')


           # #wopID_A01(WOP_Auto_JCoinPay_A01)，mopID_A01(MOP_Auto_GrabPay_A01),brandID_A01(Auto_GrabPay_A01),(qrPayload":"https://AutoGrabPayA01.com):singleNode_create_wop_innormal_01(单节点,SGP wop status=locked)
    def create_wop_innormal_01(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A01',baseInfo_brandID='Auto_GrabPay_A01',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A01', baseInfo_brandID='Auto_GrabPay_A01', baseInfo_nodeID='sgp', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A01', wopID='WOP_Auto_JCoinPay_A01', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A01',wopID='WOP_Auto_JCoinPay_A01',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A01', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A01', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A01',qrIdentifier='https://AutoGrabPayA01.com',deleteFlag=False,operationalNode='tyo')
     
    # #wopID_A02(WOP_Auto_JCoinPay_A02)，mopID_A02(MOP_Auto_GrabPay_A02),brandID_A02(Auto_GrabPay_A02),(qrPayload":"https://AutoGrabPayA02.com):singleNode_create_wop_innormal_02(单节点,SGP wop deleteFlag=True)
    def create_wop_innormal_02(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A02',baseInfo_brandID='Auto_GrabPay_A02',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='JPY',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='02:00+0800',settleInfo_isBillingAmountCalculated=False,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.0,settleInfo_cccr=0.0,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A02', baseInfo_brandID='Auto_GrabPay_A02', baseInfo_nodeID='sgp', baseInfo_status='active',baseInfo_useEVONETToken=True,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="02:00+0800",
                           settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A02', wopID='WOP_Auto_JCoinPay_A02', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='bilateral',settleCurrency='JPY',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.0,wccr=0.0, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A02',wopID='WOP_Auto_JCoinPay_A02',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A02', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A02', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A02',qrIdentifier='https://AutoGrabPayA02.com',deleteFlag=False,operationalNode='tyo')
       



    # #wopID_A03(WOP_Auto_JCoinPay_A03)，mopID_A03(MOP_Auto_GrabPay_A03),brandID_A03(Auto_GrabPay_A03),(qrPayload":"https://AutoGrabPayA03.com):singleNode_create_mop_innormal_01(单节点,SGP mop status=locked)

    def create_mop_innormal_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A03',
                                                       baseInfo_brandID='Auto_GrabPay_A03', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A03',
                                                       baseInfo_brandID='Auto_GrabPay_A03', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A03',
                                                                   wopID='WOP_Auto_JCoinPay_A03',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active', isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0, mccr=0.0, wccr=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A03',
                                                            wopID='WOP_Auto_JCoinPay_A03',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A03', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A03',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A03',
                                                                   qrIdentifier='https://AutoGrabPayA03.com',
                                                                   deleteFlag=False,operationalNode='tyo')
      
    # #l.wopID_A04(WOP_Auto_JCoinPay_A04)，mopID_A04(MOP_Auto_GrabPay_A04),brandID_A04(Auto_GrabPay_A04),(qrPayload":"https://AutoGrabPayA04.com):singleNode_create_mop_innormal_02(单节点,SGP mop deleteFlag=True)
    def create_mop_innormal_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A04',
                                                       baseInfo_brandID='Auto_GrabPay_A04', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A04',
                                                       baseInfo_brandID='Auto_GrabPay_A04', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A04',
                                                                   wopID='WOP_Auto_JCoinPay_A04',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active', isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0, mccr=0.0, wccr=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A04',
                                                            wopID='WOP_Auto_JCoinPay_A04',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A04', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A04',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A04',
                                                                   qrIdentifier='https://AutoGrabPayA04.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    
    # #wopID_A5(WOP_Auto_JCoinPay_A5)，mopID_A5(MOP_Auto_GrabPay_A5),brandID_A5(Auto_GrabPay_A5),(qrPayload":"https://AutoGrabPayA5.com):singleNode_create_relation_innormal_01(单节点,relation不存在，wop和*不存在，mop和*不存在)
    def create_relation_innormal_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A05',
                                                       baseInfo_brandID='Auto_GrabPay_A05', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A05',
                                                       baseInfo_brandID='Auto_GrabPay_A05', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A05',
                                                                   wopID='WOP_Auto_JCoinPay_A05',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active', isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0, mccr=0.0, wccr=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A05', deleteFlag=False,
                                                         operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A05',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A05',
                                                                   qrIdentifier='https://AutoGrabPayA05.com',
                                                                   deleteFlag=False,operationalNode='tyo')
     
    # #n.wopID_A06(WOP_Auto_JCoinPay_A06)，mopID_A06(MOP_Auto_GrabPay_A06),brandID_A06(Auto_GrabPay_A06),(qrPayload":"https://AutoGrabPayA06.com):singleNode_create_relation_innormal_02(单节点,relation:wop和*存在)
    def create_relation_innormal_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A06',
                                                       baseInfo_brandID='Auto_GrabPay_A06', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A06',
                                                       baseInfo_brandID='Auto_GrabPay_A06', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A06',
                                                                   wopID='WOP_Auto_JCoinPay_A06',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active', isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0, mccr=0.0, wccr=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_A06',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A06', deleteFlag=False,
                                                         operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A06',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A06',
                                                                   qrIdentifier='https://AutoGrabPayA06.com',
                                                                   deleteFlag=False,operationalNode='tyo')
      

        # #o.wopID_A07(WOP_Auto_JCoinPay_A07)，mopID_A07(MOP_Auto_GrabPay_A07),brandID_A07(Auto_GrabPay_A07),(qrPayload":"https://AutoGrabPayA07.com):singleNode_create_relation_innormal_03(单节点,relation:mop和*存在)

    def create_relation_innormal_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A07',
                                                       baseInfo_brandID='Auto_GrabPay_A07', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))
        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A07',
                                                       baseInfo_brandID='Auto_GrabPay_A07', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A07',
                                                                   wopID='WOP_Auto_JCoinPay_A07',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active', isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0, mccr=0.0, wccr=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_A07',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A07', deleteFlag=False,
                                                         operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A07',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A07',
                                                                   qrIdentifier='https://AutoGrabPayA07.com',
                                                                   deleteFlag=False,operationalNode='tyo')
      

    def create_upsupported_trans_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A09',
                                                       baseInfo_brandID='Auto_GrabPay_A09', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A09',
                                                       baseInfo_brandID='Auto_GrabPay_A09', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A09',
                                                                   wopID='WOP_Auto_JCoinPay_A09',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=False,
                                                                   isMPMSupported=False, isRefundSupported=False,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A09', wopID='WOP_Auto_JCoinPay_A09',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A09', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A09',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A09',
                                                                   qrIdentifier='https://AutoGrabPayA09.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='392',sourceCurrency='JPY',destinationCurrencyNumber='344',destinationCurrency='HKD',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber='344',sourceCurrency='HKD',destinationCurrencyNumber='392',destinationCurrency='JPY',value=0.2,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
     
    #用于修改配置的参数
    def update_config_data_B01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_B01',
                                                       baseInfo_brandID='Auto_GrabPay_B01', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_B01',
                                                       baseInfo_brandID='Auto_GrabPay_B01', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_B01',
                                                                   wopID='WOP_Auto_JCoinPay_B01',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_B01', wopID='WOP_Auto_JCoinPay_B01',operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_B01', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_B01',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_B01',
                                                                   qrIdentifier='https://AutoGrabPayB01.com',
                                                                   deleteFlag=False,operationalNode='tyo')

        #用于修改配置，relation表中wop和*，mop和*

    def create_isSettlementAmountEVONETCalculated_False_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_017',
                                                       baseInfo_brandID='Auto_GrabPay_017', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='17:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_017',
                                                       baseInfo_brandID='Auto_GrabPay_017', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.3},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="17:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_017',
                                                                   wopID='WOP_Auto_JCoinPay_017',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='bilateral',
                                                                   settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=False,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo', mccr=0.12,
                                                                   wccr=0.11)

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_017', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_017',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_017', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_017',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_017',
                                                                   qrIdentifier='https://AutoGrabPay017.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_isSettlementAmountEVONETCalculated_False_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_018',
                                                       baseInfo_brandID='Auto_GrabPay_018', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='18:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_018',
                                                       baseInfo_brandID='Auto_GrabPay_018', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.3},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="18:00+0800",
                                                       settleInfo_mccr=0.18,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_018',
                                                                   wopID='WOP_Auto_JCoinPay_018',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='bilateral',
                                                                   settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=False,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_018', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_018',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_018', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_018',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_018',
                                                                   qrIdentifier='https://AutoGrabPay018.com',
                                                                   deleteFlag=False,operationalNode='tyo')
    def create_currency_transfer_data_002(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_002',baseInfo_brandID='Auto_GrabPay_002',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='EUR',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='02:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='USD',settleInfo_wccr=0.14,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_002', baseInfo_brandID='Auto_GrabPay_002', baseInfo_nodeID='sgp', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='CAD', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="02:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_002', wopID='WOP_Auto_JCoinPay_002', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.13,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_002',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_002',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_002', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_002', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_002',qrIdentifier='https://AutoGrabPay002.com',deleteFlag=False,operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="124",destinationCurrency="CAD", value=0.05,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="124",sourceCurrency="CAD",destinationCurrencyNumber="978",destinationCurrency="EUR", value=0.07,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="978",sourceCurrency="EUR",destinationCurrencyNumber="840",destinationCurrency="USD", value=0.09,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
    def create_currency_transfer_data_03(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_003',baseInfo_brandID='Auto_GrabPay_003',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().over_cutoffTime(),settleInfo_settleCurrency='EUR',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='USD',settleInfo_wccr=0.12,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_003', baseInfo_brandID='Auto_GrabPay_003', baseInfo_nodeID='sgp', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='JPY', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_003', wopID='WOP_Auto_JCoinPay_003', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.11,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_003',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_003',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_003', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_003', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_003',qrIdentifier='https://AutoGrabPay003.com',deleteFlag=False,operationalNode='tyo')

        # Create_Mongo_Data(db_sgp_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="978",destinationCurrency="EUR", value=0.04,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')

    def create_fxrate_01(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_019',
                                                       baseInfo_brandID='Auto_GrabPay_019', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='NOK',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='19:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='THB', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_019',
                                                       baseInfo_brandID='Auto_GrabPay_019', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.3},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='SGD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="19:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_019',
                                                                   wopID='WOP_Auto_JCoinPay_019',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_019', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_019',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_019', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_019',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_019',
                                                                   qrIdentifier='https://AutoGrabPay019.com',
                                                                   deleteFlag=False,operationalNode='tyo')


    def create_currency_transfer_data_09(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_009',
                                                       baseInfo_brandID='Auto_GrabPay_009', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_009',
                                                       baseInfo_brandID='Auto_GrabPay_009', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.17},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_009', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_009',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_009', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_009',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_009',
                                                                   qrIdentifier='https://AutoGrabPay009.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_currency_transfer_data_10(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_010',
                                                       baseInfo_brandID='Auto_GrabPay_010', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_010',
                                                       baseInfo_brandID='Auto_GrabPay_010', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.3},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_010', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_010',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_010', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_010',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_010',
                                                                   qrIdentifier='https://AutoGrabPay010.com',
                                                                   deleteFlag=False,operationalNode='tyo')
        # Create_Mongo_Data(db_sgp_evoconfig).create_fxRate(sourceCurrencyNumber="392", sourceCurrency="JPY",
        #                                                   destinationCurrencyNumber="978", destinationCurrency="EUR",
        #                                                   value=0.04, deleteFlag=False, fxRateOwner='evonet',operationalNode='tyo')

    def create_currency_transfer_data_13(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_013',
                                                       baseInfo_brandID='Auto_GrabPay_013', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_013',
                                                       baseInfo_brandID='Auto_GrabPay_013', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.17},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_013', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_013',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_013', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_013',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_013',
                                                                   qrIdentifier='https://AutoGrabPay013.com',
                                                                   deleteFlag=False,operationalNode='tyo')
        # Create_Mongo_Data(db_sgp_evoconfig).create_fxRate(sourceCurrencyNumber="124", sourceCurrency="CAD",
        #                                                   destinationCurrencyNumber="840", destinationCurrency="USD",
        #                                                   value=0.11, deleteFlag=False, fxRateOwner='evonet',operationalNode='tyo')

    def create_fxrate_02(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_020',
                                                       baseInfo_brandID='Auto_GrabPay_020', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='AUD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='20:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='KRW', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_020',
                                                       baseInfo_brandID='Auto_GrabPay_020', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.17},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='RUB',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="20:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_020',
                                                                   wopID='WOP_Auto_JCoinPay_020',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_020', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_020',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_020', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_020',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_020',
                                                                   qrIdentifier='https://AutoGrabPay020.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_fxrate_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_021',
                                                       baseInfo_brandID='Auto_GrabPay_021', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='IDR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='21:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='DKK', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_021',
                                                       baseInfo_brandID='Auto_GrabPay_021', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='NZD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="21:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_021',
                                                                   wopID='WOP_Auto_JCoinPay_021',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.17},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_021', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_021',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_021', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_021',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_021',
                                                                   qrIdentifier='https://AutoGrabPay021.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_currency_transfer_data_04(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_004',
                                                       baseInfo_brandID='Auto_GrabPay_004', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_004',
                                                       baseInfo_brandID='Auto_GrabPay_004', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_004',
                                                                   wopID='WOP_Auto_JCoinPay_004',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='evonet', settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_004', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_004',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_004', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_004',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_004',
                                                                   qrIdentifier='https://AutoGrabPay004.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_currency_transfer_data_05(self):


        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_005',baseInfo_brandID='Auto_GrabPay_005',baseInfo_nodeID='tyo',baseInfo_status='active',
                           settleInfo_fileInitiator='evonet',specialInfo_specialType='',settleInfo_specialCategory='',settleInfo_cutoffTime=Moudle().less_cutoffTime(),settleInfo_settleCurrency='EUR',settleInfo_cpmInterchangeFeeRate=0.0,settleInfo_mpmInterchangeFeeRate=0.0,settleInfo_settleFileTime='09:00+0800',settleInfo_isBillingAmountCalculated=True,settleInfo_billingCurrency='JPY',settleInfo_wccr=0.12,settleInfo_cccr=0.15,settleInfo_transactionProcessingFeeRate=0.0,settleInfo_transProcessingFeeCollectionMethod='daily',settleInfo_fxProcessingFeeRate=0.0,settleInfo_fxProcessingFeeCollectionMethod='daily',settleInfo_fxRebateCollectionMethod='daily',
                           deleteFlag=False,operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_005', baseInfo_brandID='Auto_GrabPay_005', baseInfo_nodeID='sgp', baseInfo_status='active',baseInfo_useEVONETToken=False,baseInfo_isCPMSupported=True,baseInfo_isMPMSupported=True,baseInfo_isRefundSupported=True,baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],baseInfo_schemeInfo_schemeName='',baseInfo_schemeInfo_signStatus='',
                           settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                           settleInfo_settleCurrency='CAD', settleInfo_cpmInterchangeFeeRate=0.0, settleInfo_mpmInterchangeFeeRate=0.0,
                           settleInfo_settleFileTime="09:00+0800",
                           settleInfo_mccr=0.17, settleInfo_transactionProcessingFeeRate=0.0,
                           settleInfo_transProcessingFeeCollectionMethod='daily', settleInfo_fxProcessingFeeRate=0.0,
                           settleInfo_fxProcessingFeeCollectionMethod='daily', settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                           deleteFlag=False, operationalNode='tyo',baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB", "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_005', wopID='WOP_Auto_JCoinPay_005', settleInfo_fileInitiator='evonet', status='active', isCPMSupported=True,
                           isMPMSupported=True, isRefundSupported=True, transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],settleMode='evonet',settleCurrency='',isSettlementAmountEVONETCalculated=True, cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,mccr=0.11,wccr=0.12, fxRateOwner='auto_user',transactionProcessingFeeRate=0.0,
                           transProcessingFeeCollectionMethod='daily', fxProcessingFeeRate=0.0,
                           fxProcessingFeeCollectionMethod='daily',
                           deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_005',wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*',wopID='WOP_Auto_JCoinPay_005',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_005', deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_005', useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_005',qrIdentifier='https://AutoGrabPay005.com',deleteFlag=False,operationalNode='tyo')
    def create_currency_transfer_data_06(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_006',
                                                       baseInfo_brandID='Auto_GrabPay_006', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_006',
                                                       baseInfo_brandID='Auto_GrabPay_006', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_006',
                                                                   wopID='WOP_Auto_JCoinPay_006',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')


        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_006', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_006',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_006', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_006',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_006',
                                                                   qrIdentifier='https://AutoGrabPay006.com',
                                                                   deleteFlag=False,operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="392",sourceCurrency="JPY",destinationCurrencyNumber="124",destinationCurrency="CAD", value=0.05,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
        # Create_Mongo_Data(db_tyo_evoconfig).create_fxRate(sourceCurrencyNumber="124",sourceCurrency="CAD",destinationCurrencyNumber="840",destinationCurrency="USD", value=0.11,deleteFlag=False,fxRateOwner='auto_user',operationalNode='tyo')
    def create_currency_transfer_data_07(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_007',
                                                       baseInfo_brandID='Auto_GrabPay_007', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='EUR', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_007',
                                                       baseInfo_brandID='Auto_GrabPay_007', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_007',
                                                                   wopID='WOP_Auto_JCoinPay_007',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[ {"currency" : "JPY","mccr" : 0.11},{"currency" : "HKD","mccr" : 0.3 },{"currency" : "SGD","mccr" : 0.3}], settleMode='evonet',
                                                                   settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_007', wopID='*',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_007',operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_007', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_007',
                                                                      useEVONETStandard=True, deleteFlag=False,operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_007',
                                                                   qrIdentifier='https://AutoGrabPay007.com',
                                                                   deleteFlag=False,operationalNode='tyo')

    def create_isSettlementAmountEVONETCalculated_False_03(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_022',
                                                       baseInfo_brandID='Auto_GrabPay_022', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       settleInfo_settleCurrency='HKD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='18:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_022',
                                                       baseInfo_brandID='Auto_GrabPay_022', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='HKD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="18:00+0800",
                                                       settleInfo_mccr=0.18,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily', settleInfo_cutoffTime=Moudle().over_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_022',
                                                                   wopID='WOP_Auto_JCoinPay_022',
                                                                   settleInfo_fileInitiator='evonet',
                                                                   status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[
                                                                       {"currency": "JPY", "mccr": 0.11},
                                                                       {"currency": "HKD", "mccr": 0.3},
                                                                       {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='bilateral',
                                                                   settleCurrency='HKD',
                                                                   isSettlementAmountEVONETCalculated=False,
                                                                   cpmInterchangeFeeRate=0.0,
                                                                   mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_022', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_022',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_022', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_022',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_022',
                                                                   qrIdentifier='https://AutoGrabPay022.com',
                                                                   deleteFlag=False, operationalNode='tyo')
        # g.wopID_023(WOP_Auto_JCoinPay_023)，mopID_023(MOP_Auto_GrabPay_023),brandID_023(Auto_GrabPay_023):singleNode_create_fxrate(双节点币种转换(transcurrency:JPY,mopsettleCurrency:CAD,wopsettleCurrency:EUR,billingCurrency:USD),fxrate表：(MOP:存在中间汇率，JPY-CAD(0.05))(WOP:存在反向 CAD-EUR(0.07) MCCR:0 WCCR:0)
        # 个性化配置表MCCR为0,WCCR为0 023

    def create_currency_transfer_data_023(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_023',
                                                       baseInfo_brandID='Auto_GrabPay_023', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='02:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_023',
                                                       baseInfo_brandID='Auto_GrabPay_023', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="02:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_023',
                                                                   wopID='WOP_Auto_JCoinPay_023',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0},
                                                                                    {"currency": "HKD", "mccr": 0},
                                                                                    {"currency": "SGD", "mccr": 0}],
                                                                   settleMode='evonet', settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0, wccr=0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_023', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_023',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_023', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_023',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_023',
                                                                   qrIdentifier='https://AutoGrabPay023.com',
                                                                   deleteFlag=False, operationalNode='tyo')
    def none_fxrate(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_A014',
                                                       baseInfo_brandID='Auto_GrabPay_A014', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='CHF',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='02:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_A014',
                                                       baseInfo_brandID='Auto_GrabPay_A014', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CHF',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="02:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_A014',
                                                                   wopID='WOP_Auto_JCoinPay_A014',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='evonet', settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.11, wccr=0.12, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_A014', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='*', wopID='WOP_Auto_JCoinPay_A014',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_A014', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_A014',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_A014',
                                                                   qrIdentifier='https://AutoGrabPayA014.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_direct_evonet_dual_031(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_031',
                                                       baseInfo_brandID='Auto_GrabPay_031',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_031',
                                                       baseInfo_brandID='Auto_GrabPay_031',
                                                       baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='bilateral', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_031',
                                                                   wopID='WOP_Auto_JCoinPay_031',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_031',
                                                            wopID='WOP_Auto_JCoinPay_031', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_031', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_031',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_031',
                                                                   qrIdentifier='https://AutoGrabPay031.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_yapi_double_001(self):
        Create_Mongo_Data(db_tyo_evoconfig,version='customize').create_wop(baseInfo_wopID='WOP_Auto_YapiWop_001',
                                                       baseInfo_brandID='Auto_Yapi_001',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig,version='customize').create_mop(baseInfo_mopID='MOP_Auto_YapiMop_001',
                                                       baseInfo_brandID='Auto_Yapi_001',
                                                       baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='bilateral', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_YapiMop_001',
                                                                   wopID='WOP_Auto_YapiWop_001',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                    {"currency": "HKD", "mccr": 0.3},
                                                                                    {"currency": "SGD", "mccr": 0.3}],
                                                                   settleMode='bilateral', settleCurrency='JPY',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0.0, wccr=0.0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_YapiMop_001',
                                                            wopID='WOP_Auto_YapiWop_001', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_Yapi_001', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_YapiMop_001',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_YapiMop_001',
                                                                   qrIdentifier='https://AutoYapiPay001.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_direct_evonet_dual_032(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_032',
                                                       baseInfo_brandID='Auto_GrabPay_032',
                                                       baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='09:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.0,
                                                       settleInfo_cccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_032',
                                                       baseInfo_brandID='Auto_GrabPay_032',
                                                       baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='bilateral', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="09:00+0800",
                                                       settleInfo_mccr=0.0, settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))


        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_032',
                                                            wopID='WOP_Auto_JCoinPay_032', operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_032', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_032',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_032',
                                                                   qrIdentifier='https://AutoGrabPay032.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_currency_transfer_data_bilateral001(self):
        wop_params = {'baseInfo_wopID': 'WOP_Auto_JCoinPay_bilateral001', 'settleInfo_settleCurrency': 'EUR',
                      'settleInfo_billingCurrency': 'EUR',
                      'settleInfo_wccr': 0.12, 'settleInfo_cccr': 0.15, 'baseInfo_brandID': 'Auto_GrabPay_bilateral001'}

        mop_params = {'baseInfo_mopID': 'MOP_Auto_GrabPay_bilateral001',
                      'baseInfo_mopID': 'MOP_Auto_GrabPay_bilateral001',
                      'baseInfo_brandID': 'Auto_GrabPay_bilateral001', 'settleInfo_settleCurrency': 'CAD',
                      'settleInfo_mccr': 0.17, "baseInfo_nodeID": "sgp",
                      "baseInfo_transCurrencies": [{"currency": "JPY", "mccr": 0.12}, {"currency": "HKD", "mccr": 0.3},
                                                   {"currency": "SGD", "mccr": 0.3}]}
        customizeConfig01_params = {'mopID': 'MOP_Auto_GrabPay_bilateral001',
                                    'wopID': 'WOP_Auto_JCoinPay_bilateral001',
                                    'settleCurrency': 'CAD', 'mccr': 0.13, }
        mongo_initial(db_tyo_evoconfig).create_wop(**wop_params)
        mongo_initial(db_tyo_evoconfig).create_mop(**mop_params)
        mongo_initial(db_tyo_evoconfig).create_customizeConfig01(**customizeConfig01_params)

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_bilateral001',
                                                            wopID='WOP_Auto_JCoinPay_bilateral001',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_bilateral001', deleteFlag=False,
                                                         operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_bilateral0001',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_bilateral001',
                                                                   qrIdentifier='https://AutoGrabPaybilateral001.com',
                                                                   deleteFlag=False, operationalNode='tyo')

    def create_wop_mop_no_relation_033(self):
        Create_Mongo_Data(db_tyo_evoconfig).create_wop(baseInfo_wopID='WOP_Auto_JCoinPay_033',
                                                       baseInfo_brandID='Auto_GrabPay_033', baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       settleInfo_settleCurrency='EUR',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime='02:00+0800',
                                                       settleInfo_isBillingAmountCalculated=True,
                                                       settleInfo_billingCurrency='USD', settleInfo_wccr=0.12,
                                                       settleInfo_cccr=0.15,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_mop(baseInfo_mopID='MOP_Auto_GrabPay_033',
                                                       baseInfo_brandID='Auto_GrabPay_033', baseInfo_nodeID='sgp',
                                                       baseInfo_status='active', baseInfo_useEVONETToken=False,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=[{"currency": "JPY", "mccr": 0.11},
                                                                                 {"currency": "HKD", "mccr": 0.3},
                                                                                 {"currency": "SGD", "mccr": 0.3}],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator='evonet', specialInfo_specialType='',
                                                       settleInfo_settleCurrency='CAD',
                                                       settleInfo_cpmInterchangeFeeRate=0.0,
                                                       settleInfo_mpmInterchangeFeeRate=0.0,
                                                       settleInfo_settleFileTime="02:00+0800",
                                                       settleInfo_mccr=0.17,
                                                       settleInfo_transactionProcessingFeeRate=0.0,
                                                       settleInfo_transProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxProcessingFeeRate=0.0,
                                                       settleInfo_fxProcessingFeeCollectionMethod='daily',
                                                       settleInfo_fxRebateCollectionMethod='daily',
                                                       settleInfo_cutoffTime=Moudle().less_cutoffTime(),
                                                       deleteFlag=False, operationalNode='tyo',
                                                       baseInfo_signKeyC=Conf(test_ini_file).get("mongoDB",
                                                                                                 "tyo_signkeyC"))

        Create_Mongo_Data(db_tyo_evoconfig).create_customizeConfig(mopID='MOP_Auto_GrabPay_033',
                                                                   wopID='WOP_Auto_JCoinPay_033',
                                                                   settleInfo_fileInitiator='evonet', status='active',
                                                                   isCPMSupported=True,
                                                                   isMPMSupported=True, isRefundSupported=True,
                                                                   transCurrencies=[{"currency": "JPY", "mccr": 0},
                                                                                    {"currency": "HKD", "mccr": 0},
                                                                                    {"currency": "SGD", "mccr": 0}],
                                                                   settleMode='evonet', settleCurrency='',
                                                                   isSettlementAmountEVONETCalculated=True,
                                                                   cpmInterchangeFeeRate=0.0, mpmInterchangeFeeRate=0.0,
                                                                   mccr=0, wccr=0, fxRateOwner='auto_user',
                                                                   transactionProcessingFeeRate=0.0,
                                                                   transProcessingFeeCollectionMethod='daily',
                                                                   fxProcessingFeeRate=0.0,
                                                                   fxProcessingFeeCollectionMethod='daily',
                                                                   deleteFlag=False, operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_relation(mopID='MOP_Auto_GrabPay_033', wopID='*',
                                                            operationalNode='tyo')
        Create_Mongo_Data(db_tyo_evoconfig).create_brand(brandID='Auto_GrabPay_033', deleteFlag=False,
                                                         operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_cpmTokenIdentifier(mopID='MOP_Auto_GrabPay_033',
                                                                      useEVONETStandard=True, deleteFlag=False,
                                                                      operationalNode='tyo')

        Create_Mongo_Data(db_tyo_evoconfig).create_mpmQrIdentifier(mopID='MOP_Auto_GrabPay_033',
                                                                   qrIdentifier='https://AutoGrabPay033.com',
                                                                   deleteFlag=False, operationalNode='tyo')
if __name__ == '__main__':


    # cc=Delete_Mongo_Data('tyo_config_url').delete_config()
    # dd=Delete_Mongo_Data('sgp_config_url').delete_config()
    # aa=doubleNode_data().create_no_currency_transfer_data()
    # doubleNode_data().create_settle_data_01()
    # doubleNode_data().create_settle_data_02()
    # doubleNode_data().create_settle_data_03()
    # doubleNode_data().create_no_currency_transfer_data()
    # doubleNode_data().create_currency_transfer_data_02()
    # doubleNode_data().update_config_data_B01()
    # doubleNode_data().create_currency_transfer_data_03()
    # doubleNode_data().create_currency_transfer_data_04()
    # doubleNode_data().create_currency_transfer_data_05()
    # doubleNode_data().create_wop_mop_no_relation_033()

    # doubleNode_data().create_currency_transfer_data_06()
    # doubleNode_data().create_currency_transfer_data_07()
    # doubleNode_data().create_currency_transfer_data_09()
    #  doubleNode_data().create_currency_transfer_data_10()
    # # doubleNode_data().create_currency_transfer_data_13()
    # doubleNode_data().create_isSettlementAmountEVONETCalculated_False_01()
    # doubleNode_data().create_isSettlementAmountEVONETCalculated_False_02()
    # doubleNode_data().create_isSettlementAmountEVONETCalculated_False_03()
    # doubleNode_data().create_fxrate_01()
    # doubleNode_data().create_fxrate_02()
    # doubleNode_data().create_fxrate_03()
    # doubleNode_data().create_relation_innormal_01()
    # doubleNode_data().create_relation_innormal_02()
    # doubleNode_data().create_relation_innormal_03()
    # doubleNode_data().create_upsupported_trans_01()
    # doubleNode_data().none_fxrate()
    # doubleNode_data().create_currency_transfer_data_023()

    # doubleNode_data().create_direct_evonet_dual_031()
    # doubleNode_data().create_direct_evonet_dual_032()
    # doubleNode_data().create_apispecialmode_wop_001()
    # doubleNode_data().create_apispecialmode_wop_002()
    # doubleNode_data().create_apispecialmode_wop_003()
    # doubleNode_data().create_apispecialmode_wop_004()
    # doubleNode_data().create_yapi_double_001()
    # doubleNode_data().create_currency_transfer_data_bilateral001()

    # singleNode_data().create_no_currency_transfer_data()
    # singleNode_data().create_brand_innormal()
    # singleNode_data().create_mop_innormal_01()
    # singleNode_data().create_mop_innormal_02()
    # singleNode_data().create_wop_innormal_01()
    # singleNode_data().create_wop_innormal_02()
    # singleNode_data().create_relation_innormal_01()
    # singleNode_data().create_relation_innormal_02()
    # singleNode_data().create_relation_innormal_03()
    # singleNode_data().create_currency_transfer_data_02()
    # singleNode_data().create_currency_transfer_data_03()
    # singleNode_data().create_currency_transfer_data_04()
    # singleNode_data().create_currency_transfer_data_05()
    # singleNode_data().updata_config_data()
    #
    # singleNode_data().singleNode_create_upsupported_refund_01()
    # singleNode_data().create_yapi_single_01()

    # singleNode_data().create_currency_transfer_data_bilateral01()
    # singleNode_data().create_settle_data_01()
    # singleNode_data().create_settle_data_02()
    # singleNode_data().create_settle_data_03()

    #
    # singleNode_data().create_currency_transfer_data_06()
    # singleNode_data().create_currency_transfer_data_07()
    # singleNode_data().create_currency_transfer_data_09()
    # singleNode_data().create_currency_transfer_data_10()
    # singleNode_data().create_currency_transfer_data_11()
    # singleNode_data().create_currency_transfer_data_12()
    # singleNode_data().create_currency_transfer_data_13()
    # singleNode_data().create_currency_transfer_data_14()
    # singleNode_data().create_isSettlementAmountEVONETCalculated_False_01()
    # singleNode_data().create_isSettlementAmountEVONETCalculated_False_02()
    # singleNode_data().create_isSettlementAmountEVONETCalculated_False_03()
    # singleNode_data().create_fxrate_01()
    # singleNode_data().create_fxrate_02()
    # singleNode_data().create_fxrate_03()
    # singleNode_data().create_upsupported_trans_01()
    # singleNode_data().none_fxrate()
    # singleNode_data().create_currency_transfer_data_23()
    # singleNode_data().create_direct_evonet_dual_31()
    # singleNode_data().create_direct_evonet_dual_32()

    #
    # Delete_Mongo_Data('sgp_config_url', 'evoconfig').delete_config()
    # Delete_Mongo_Data('tyo_config_url', 'evoconfig').delete_config()

    #MDAQ测试数据
    # singleNode_data().create_MDAQ_01()
    a = Create_Mongo_Data()
    # a.create_fx_Rate(ccyPair='JPY/USD',ccy1='JPY',ccy1Code='392',ccy2='USD',ccy2Code='840',bid=0.00818,ask=0.00918,mid=0.01918,fxRateOwner='evonet')
    # a.create_fx_Rate(ccyPair='USD/JPY',ccy2='JPY',ccy2Code='392',ccy1='USD',ccy1Code='840',bid=105.93,ask=108.93,mid=103.93,fxRateOwner='evonet')
    #
    #
    # a.create_fx_Rate(ccyPair='JPY/HKD',ccy1='JPY',ccy1Code='392',ccy2='HKD',ccy2Code='344',bid=0.0713,ask=0.0817,mid=0.0723,fxRateOwner='evonet')
    # a.create_fx_Rate(ccyPair='HKD/JPY',ccy2='JPY',ccy2Code='392',ccy1='HKD',ccy1Code='344',bid=15.6154,ask=14.0168,mid=14.0268,fxRateOwner='evonet')
    #
    #
    # a.create_fx_Rate(ccyPair='HKD/USD',ccy1='HKD',ccy1Code='344',ccy2='USD',ccy2Code='840',bid=0.1311,ask=0.1288,mid=0.1222,fxRateOwner='evonet')
    # a.create_fx_Rate(ccyPair='USD/HKD',ccy2='HKD',ccy2Code='344',ccy1='USD',ccy1Code='840',bid=7.2124,ask=7.7624,mid=7.6624,fxRateOwner='evonet')
    #
    # a.create_fx_Rate(ccyPair='CAD/USD',ccy1='CAD',ccy1Code='124',ccy2='USD',ccy2Code='840',bid='0.807',ask='0.8307',mid='0.723',fxRateOwner='evonet')
    # a.create_fx_Rate(ccyPair='USD/CAD',ccy1='USD',ccy1Code='840',ccy2='CAD',ccy2Code='124',bid=1.3031,ask=1.2038,mid=1.1038,fxRateOwner='evonet')


    # a.create_fx_Rate(ccyPair='HKD/CAD',ccy1='HKD',ccy1Code='344',ccy2='CAD',ccy2Code='124',bid=0.121,ask=0.1551,mid=0.131,fxRateOwner='evonet')

    #SOP GBP,rop NZD send CNY REV CAD
    a.create_fx_Rate(ccyPair='GBP/USD',ccy1='GBP',ccy1Code='826',ccy2='USD',ccy2Code='840',bid=1.3131,ask=1.4151,mid=1.4331,fxRateOwner='evonet')
    a.create_fx_Rate(ccyPair='USD/GBP',ccy1='USD',ccy1Code='840',ccy2='GBP',ccy2Code='826',bid=0.6051,ask=0.7067,mid=0.7767,fxRateOwner='evonet')
    a.create_fx_Rate(ccyPair='NZD/USD',ccy1='NZD',ccy1Code='554',ccy2='USD',ccy2Code='840',bid=0.725,ask=0.7305,mid=0.788,fxRateOwner='evonet')



    #SOP VND,rop SEK send CNY REV CAD
    a.create_fx_Rate(ccyPair='USD/VND',ccy1='USD',ccy1Code='840',ccy2='VND',ccy2Code='704',bid=23160,ask=23060,mid=23260,fxRateOwner='evonet')
    a.create_fx_Rate(ccyPair='SEK/USD',ccy1='SEK',ccy1Code='752',ccy2='USD',ccy2Code='840',bid=0.1311,ask=0.1205,mid=0.1405,fxRateOwner='evonet')

    #SOP ZAR,rop DKK send TRY REV CAD
    a.create_fx_Rate(ccyPair='USD/ZAR',ccy1='USD',ccy1Code='840',ccy2='ZAR',ccy2Code='710',bid=13.9069,ask=13.8066,mid=13.8266,fxRateOwner='evonet')
    a.create_fx_Rate(ccyPair='USD/DKK',ccy1='USD',ccy1Code='840',ccy2='DKK',ccy2Code='208',bid=6.0789,ask=6.12,mid=6.0719,fxRateOwner='evonet')


































