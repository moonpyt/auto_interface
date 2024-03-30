import random
from base.db import MongoDB
from base.read_config import Conf
from base.encrypt import Encrypt
from base.read_file_path import ReadFile
# from common.evopay.conf_init import evopay_conf

from common.evopay.moudle import Moudle

test_ini_file = ReadFile().read_ini_file(envirs="test", project="evopay")


class Create_Mongo_Data(object):
    def __init__(self):
        self.url_json = {
            "url": "http://jp3evonet-Testing:9090/mock/11/accountDebit",
            "version": "v0"
        }
        # self.url_json = "http://jp3evonet-Testing:9090/mock/11/accountDebit"

    def create_wop(self, baseInfo_wopID, baseInfo_brandID, baseInfo_nodeID, baseInfo_status,
                   settleInfo_fileInitiator, settleInfo_specialType, settleInfo_specialCategory, settleInfo_cutoffTime,
                   settleInfo_settleCurrency, settleInfo_cpmInterchangeFeeRate, settleInfo_mpmInterchangeFeeRate,
                   settleInfo_settleFileTime, settleInfo_isBillingAmountCalculated, settleInfo_billingCurrency,
                   settleInfo_wccr, settleInfo_cccr, settleInfo_transactionProcessingFeeRate,
                   settleInfo_transProcessingFeeCollectionMethod, settleInfo_fxProcessingFeeRate,
                   settleInfo_fxProcessingFeeCollectionMethod, settleInfo_fxRebateCollectionMethod,
                   deleteFlag, operationalNode, baseInfo_signKeyC=None, calcul_method="accumulation"):
        insert_wop = {
            "baseInfo": {
                "deleteFlag": False,
                "status": baseInfo_status,
                "wopID": baseInfo_wopID,
                "wopName": baseInfo_wopID,
                "brandID": baseInfo_brandID,
                "country": "JPN",
                "nodeID": baseInfo_nodeID,
                "businessContactName": "auto_test_businessContactName",
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
                "signKeyC": "5b18706bd8968363f995de1cbaa4d5eeea9cd8a40767f61269789bec7bfd424178111a40ad7213178cdab53498104401",
                "accountDebit": self.url_json,
                "authenticationNotification": self.url_json,
                "transactionNotification": self.url_json,
                "inquiry": self.url_json,
                "cpmPayment": self.url_json,
                "refund": self.url_json,
                "cancel": self.url_json
            },
            "settleInfo": {
                "fileInitiator": settleInfo_fileInitiator,  # 文件发起方
                "specialType": settleInfo_specialType,  # 特殊类型
                "specialCategory": settleInfo_specialCategory,  # 文件特殊种类
                "settleCurrency": settleInfo_settleCurrency,  # 清算币种
                "cutoffTime": settleInfo_cutoffTime,  # 日切时间
                "cpmInterchangeFeeRate": settleInfo_cpmInterchangeFeeRate,  # cpmInterchangeFee
                "mpmInterchangeFeeRate": settleInfo_mpmInterchangeFeeRate,  # mpmInterchangeFee
                "settleFileTime": settleInfo_settleFileTime,  # 文件生成时间
                "isBillingAmountCalculated": settleInfo_isBillingAmountCalculated,  # billingAmount是否计算
                "billingCurrency": settleInfo_billingCurrency,  # billingCurrency

                "wccr": settleInfo_wccr,
                "cccr": settleInfo_cccr,
                "transactionProcessingFeeRate": settleInfo_transactionProcessingFeeRate,  # 交易处理费
                "transProcessingFeeCollectionMethod": settleInfo_transProcessingFeeCollectionMethod,  # 交易处理费生成方式
                "transProcessingFeeCalculatedMethod": calcul_method,
                "fxProcessingFeeRate": settleInfo_fxProcessingFeeRate,  # 汇率转换费
                "fxProcessingFeeCollectionMethod": settleInfo_fxProcessingFeeCollectionMethod,  # 汇率转换费生成方式
                "fxProcessingFeeCalculatedMethod": "accumulation",
                "fxRebateCollectionMethod": settleInfo_fxRebateCollectionMethod
            },
            "specialInfo": {
                "specialType": "", #// UPI 特殊模式
                "mpmPaymentCardScheme":True, #// MPMPayment交易流程是否兼容卡组织模式
        "batchRefundSettle": True, #// 以文件提供方式，进行批量退款处理（清分处理流程）
        },
            "version": int(1),  # 版本
            "deleteFlag": deleteFlag,  # 删除标识
            "updateUser": "auto_walker_user",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [operationalNode, ]  # 操作节点
        }
        # 新建wop表
        return insert_wop

    def create_mop(self, baseInfo_mopID, baseInfo_brandID, baseInfo_nodeID, baseInfo_useEVONETToken, baseInfo_status,
                   baseInfo_isCPMSupported, baseInfo_isMPMSupported, baseInfo_isRefundSupported,
                   baseInfo_transCurrencies, baseInfo_schemeInfo_schemeName, baseInfo_schemeInfo_signStatus,
                   settleInfo_fileInitiator, settleInfo_specialType,
                   settleInfo_settleCurrency, settleInfo_cpmInterchangeFeeRate, settleInfo_mpmInterchangeFeeRate,
                   settleInfo_settleFileTime,
                   settleInfo_mccr, settleInfo_transactionProcessingFeeRate,
                   settleInfo_transProcessingFeeCollectionMethod, settleInfo_fxProcessingFeeRate,
                   settleInfo_fxProcessingFeeCollectionMethod, settleInfo_fxRebateCollectionMethod,
                   deleteFlag, operationalNode, baseInfo_signKeyC=None, calcul_method="accumulation"):
        insert_mop = {
            "baseInfo": {
                "deleteFlag": False,
                "status": baseInfo_status,
                "mopID": baseInfo_mopID,
                "mopName": baseInfo_mopID,
                "brandID": baseInfo_brandID,
                "useEVONETToken": baseInfo_useEVONETToken,
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
                "transCurrencies": [
                    {
                        "currency": "JPY",
                        "mccr": 0.8
                    },
                    {
                        "currency": "CNY",
                        "mccr": 0.9
                    }
                ],
                "schemeInfo": [
                    {
                        "schemeName": baseInfo_schemeInfo_schemeName,
                        "signStatus": baseInfo_schemeInfo_signStatus
                    }
                ],

                "signKeyC": "5b18706bd8968363f995de1cbaa4d5eeea9cd8a40767f61269789bec7bfd424178111a40ad7213178cdab53498104401",
                "cpmToken": self.url_json,
                "mpmQrVerification": self.url_json,
                "mpmPaymentAuthentication": self.url_json,
                "paymentNotification": self.url_json,
            },
            "settleInfo": {
                "specialType": settleInfo_specialType,  # 特殊类型
                "settleCurrency": settleInfo_settleCurrency,  # 清算币种
                "cpmInterchangeFeeRate": settleInfo_cpmInterchangeFeeRate,  # cpmInterchangeFee
                "mpmInterchangeFeeRate": settleInfo_mpmInterchangeFeeRate,  # mpmInterchangeFee
                "cutoffTime": "13:12+0800",  # 日切时间
                "settleFileTime": settleInfo_settleFileTime,  # 文件生成时间
                "mccr": settleInfo_mccr,
                "transactionProcessingFeeRate": settleInfo_transactionProcessingFeeRate,  # 交易处理费
                "transProcessingFeeCollectionMethod": settleInfo_transProcessingFeeCollectionMethod,  # 交易处理费生成方式
                "transProcessingFeeCalculatedMethod": calcul_method,
                "fxProcessingFeeRate": settleInfo_fxProcessingFeeRate,  # 汇率转换费
                "fxProcessingFeeCollectionMethod": settleInfo_fxProcessingFeeCollectionMethod,  # 汇率转换费生成方式
                "fxProcessingFeeCalculatedMethod": "single",
            },
            "specialInfo": {
                "specialType": "",  # // UPI 特殊模式
                "mpmPaymentCardScheme": True,  # // MPMPayment交易流程是否兼容卡组织模式
                "batchRefundSettle": True,  # // 以文件提供方式，进行批量退款处理（清分处理流程）
            },
            "version": int(1),  # 版本
            "deleteFlag": deleteFlag,  # 删除标识
            "updateUser": "auto_user",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [operationalNode, ]  # 操作节点
        }
        return insert_mop

    def create_customizeConfig(self, mopID, wopID, settleInfo_fileInitiator, status, isCPMSupported,
                               isMPMSupported, isRefundSupported, transCurrencies, settleMode, settleCurrency,
                               isSettlementAmountEVONETCalculated, cpmInterchangeFeeRate, mpmInterchangeFeeRate, mccr,
                               wccr, fxRateOwner, transactionProcessingFeeRate,
                               transProcessingFeeCollectionMethod, fxProcessingFeeRate,
                               fxProcessingFeeCollectionMethod,
                               deleteFlag, operationalNode, signKeyC=None, calcul_method="single"):
        # 新建custom表信息
        insert_customizeConfig = {
            "status": status,  # 状态
            "mopID": mopID,  # mopID
            "mopName": mopID,  # mopName
            "wopID": wopID,  # wopID
            "wopName": wopID,  # wopName
            "isCPMSupported": isCPMSupported,  # 是否支持CPM
            "isMPMSupported": isMPMSupported,  # 是否支持MPM
            "isRefundSupported": isRefundSupported,  # 是否支持Refund

            "settleMode": settleMode,  # 清算模式bilateral / evonet
            "settleCurrency": settleCurrency,  # 清算币种
            "isSettlementAmountEVONETCalculated": isSettlementAmountEVONETCalculated,  # 是否计算清算币种
            "cpmInterchangeFeeRate": cpmInterchangeFeeRate,  # cpmInterchangeFee
            "mpmInterchangeFeeRate": mpmInterchangeFeeRate,  # mpmInterchangeFee
            "mccr": mccr,
            "wccr": wccr,
            "fxRateOwner": fxRateOwner,  # 汇率归属
            "transactionProcessingFeeRate": transactionProcessingFeeRate,  # 交易处理费
            "transProcessingFeeCollectionMethod": transProcessingFeeCollectionMethod,  # 交易处理费生成方式
            "transProcessingFeeCalculatedMethod": calcul_method,
            "fxProcessingFeeRate": fxProcessingFeeRate,  # 汇率转换费
            "fxProcessingFeeCollectionMethod": fxProcessingFeeCollectionMethod,  # 汇率转换费生成方式
            "fxProcessingFeeCalculatedMethod": "single",
            "fileInitiator": settleInfo_fileInitiator,
            "version": int(1),  # 版本
            "deleteFlag": deleteFlag,  # 删除标识
            "updateUser": "auto_test",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [  # 操作节点
                operationalNode
            ],
            "transCurrencies": [
                {
                    "currency": "JPY",
                    "mccr": 0.8
                },
                {
                    "currency": "CNY",
                    "mccr": 0.9
                }
            ]
        }
        return insert_customizeConfig

    def create_relation(self, wopID, mopID):
        # 新建relations
        insert_relation = {
            "deleteFlag": False,
            "mopID": mopID,
            "wopID": wopID,
            "createUser": "auto_user",
            "createTime": Moudle().create_mongo_time(),
            "updateTime": Moudle().create_mongo_time(),
            "updateUser": "auto_user",
            "operationalNode": [
                "tyo"
            ]

        }
        return insert_relation

    def create_brand(self, brandID, deleteFlag, operationalNode):
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
            "updateTime": Moudle().create_mongo_time(),
        }
        return insert_brand

    def create_mpmQrIdentifier(self, mopID, qrIdentifier, deleteFlag):
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
            "deleteFlag": deleteFlag
        }
        return insert_mpmQrIdentifier

    def create_cpmTokenIdentifier(self, mopID, useEVONETStandard, deleteFlag):
        insert_cpmTokenIdentifier = {
            "mopID": mopID,
            "mopName": mopID,
            "useEVONETStandard": useEVONETStandard,
            "createTime": Moudle().create_mongo_time(),
            "updateTime": Moudle().create_mongo_time(),
            "deleteFlag": deleteFlag
        }
        return insert_cpmTokenIdentifier

    def create_fxRate(self, sourceCurrencyNumber, sourceCurrency, destinationCurrencyNumber, destinationCurrency, value,
                      deleteFlag):
        insert_fxRate = {
            "sourceCurrency": sourceCurrency,
            "destinationCurrency": destinationCurrencyNumber,
            "value": value,
            "updateTime": Moudle().create_mongo_time(),
            "createTime": Moudle().create_mongo_time(),
            "deleteFlag": deleteFlag,
            "fxRateOwner": destinationCurrency,
            "destinationCurrencyNumber": "344",
            "sourceCurrencyNumber": sourceCurrencyNumber
        }
        return insert_fxRate


class Delete_Mongo_Data(object):
    def __init__(self, nodeID_url):
        test_ini_file = ReadFile().read_ini_file(envirs='test', project="evopay")
        test_mongo_url = Conf(test_ini_file).get("mongoDB", nodeID_url)  # tyo_config_url
        mongo_url = Encrypt().decrypt(test_mongo_url)
        self.db = MongoDB(url=mongo_url, database='evoconfig')

    def delete_config(self):
        # 删除wop表数据

        self.db.delete_manys(table='wopV1', query_params={"baseInfo.wopID": {"$regex": "^WOP_Auto"}})
        self.db.delete_manys(table='mopV1', query_params={"baseInfo.mopID": {"$regex": "^MOP_Auto"}})
        self.db.delete_manys(table='customizeConfigV1', query_params={"wopID": {"$regex": "^WOP_Auto"}})
        self.db.delete_manys(table='brand', query_params={"brandID": {"$regex": "^Auto"}})
        self.db.delete_manys(table='relation', query_params={"wopID": {"$regex": "^WOP_Auto"}})
        self.db.delete_manys(table='relation', query_params={"mopID": {"$regex": "^MOP_Auto"}})
        self.db.delete_manys(table='mpmQrIdentifier', query_params={"mopID": {"$regex": "^MOP_Auto"}})
        self.db.delete_manys(table='cpmTokenIdentifier', query_params={"mopID": {"$regex": "^MOP_Auto"}})


class CreateConfig(object):
    def __init__(self):
        self.create_mongo_config = Create_Mongo_Data()

    def create_config_info(self, wopid, mopid, model, fileinit, date_monthly_type, date_daily_type,
                           brand_id, mop_node_id):

        wop_data = self.create_mongo_config.create_wop(baseInfo_wopID=wopid,
                                                       baseInfo_brandID=brand_id, baseInfo_nodeID='tyo',
                                                       baseInfo_status='active',
                                                       settleInfo_fileInitiator=fileinit, settleInfo_specialType='',
                                                       settleInfo_specialCategory='',
                                                       settleInfo_cutoffTime='23:00+0800',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0632658,
                                                       settleInfo_mpmInterchangeFeeRate=0.08328446,
                                                       settleInfo_settleFileTime='03:00+0800',
                                                       settleInfo_isBillingAmountCalculated=False,
                                                       settleInfo_billingCurrency='JPY', settleInfo_wccr=0.04951753628,
                                                       settleInfo_cccr=0.0,
                                                       settleInfo_transactionProcessingFeeRate=0.0585173,
                                                       settleInfo_transProcessingFeeCollectionMethod=date_daily_type,
                                                       settleInfo_fxProcessingFeeRate=0.0712973,
                                                       settleInfo_fxProcessingFeeCollectionMethod=date_daily_type,
                                                       settleInfo_fxRebateCollectionMethod=date_daily_type,
                                                       deleteFlag=False, operationalNode='tyo')

        mop_data = self.create_mongo_config.create_mop(baseInfo_mopID=mopid,
                                                       baseInfo_brandID=brand_id, baseInfo_nodeID=mop_node_id,
                                                       baseInfo_status='active', baseInfo_useEVONETToken=True,
                                                       baseInfo_isCPMSupported=True, baseInfo_isMPMSupported=True,
                                                       baseInfo_isRefundSupported=True,
                                                       baseInfo_transCurrencies=['JPY', 'HKD', 'SGD'],
                                                       baseInfo_schemeInfo_schemeName='',
                                                       baseInfo_schemeInfo_signStatus='',
                                                       settleInfo_fileInitiator=fileinit, settleInfo_specialType='',
                                                       settleInfo_settleCurrency='JPY',
                                                       settleInfo_cpmInterchangeFeeRate=0.0632658,
                                                       settleInfo_mpmInterchangeFeeRate=0.08328446,
                                                       settleInfo_settleFileTime="03:00+0800",
                                                       settleInfo_mccr=0.0725964,
                                                       settleInfo_transactionProcessingFeeRate=0.0495173,
                                                       settleInfo_transProcessingFeeCollectionMethod=date_daily_type,
                                                       settleInfo_fxProcessingFeeRate=0.0752973,
                                                       settleInfo_fxProcessingFeeCollectionMethod=date_daily_type,
                                                       settleInfo_fxRebateCollectionMethod=date_daily_type,
                                                       deleteFlag=False, operationalNode="tyo")
        custom_data = self.create_mongo_config.create_customizeConfig(mopID=mopid,
                                                                      wopID=wopid,
                                                                      settleInfo_fileInitiator=fileinit,
                                                                      status='active',
                                                                      isCPMSupported=True,
                                                                      isMPMSupported=True, isRefundSupported=True,
                                                                      transCurrencies=['JPY', 'HKD', 'SGD'],
                                                                      settleMode=model, settleCurrency='JPY',
                                                                      isSettlementAmountEVONETCalculated=True,
                                                                      cpmInterchangeFeeRate=0.0632658,
                                                                      mpmInterchangeFeeRate=0.08328446,
                                                                      mccr=0.0725964, wccr=0.036539518235,
                                                                      fxRateOwner='auto_user',
                                                                      transactionProcessingFeeRate=0.0595173,
                                                                      transProcessingFeeCollectionMethod=date_monthly_type,
                                                                      fxProcessingFeeRate=0.0852973,
                                                                      fxProcessingFeeCollectionMethod=date_monthly_type,
                                                                      deleteFlag=False, operationalNode='tyo')
        if model == "bilateral":
            custom_data.pop("wccr")

        if model == "evonet":  # 如果是evonet模式则customizeconfi 表不需要这三个参数
            custom_data.pop("cpmInterchangeFeeRate")
            custom_data.pop("mpmInterchangeFeeRate")
            custom_data.pop("settleCurrency")
            custom_data.pop("fxRateOwner")
            custom_data.pop("transProcessingFeeCollectionMethod")
            custom_data.pop("transProcessingFeeCalculatedMethod")
            custom_data.pop("fxProcessingFeeCollectionMethod")
            custom_data.pop("fxProcessingFeeCalculatedMethod")

        if model == "bilateral" and fileinit == "mop":
            mop_data["specialInfo"]["specialType"] = "UPI"
            wop_data["specialInfo"]["specialType"] = "UPI"
        if model == "bilateral":
            # 设置清算时间；直清模式下只会去找 customizeconfig表的日切时间
            wop_data["settleInfo"]["cutoffTime"] = "06:00+0800"
            mop_data["settleInfo"]["cutoffTime"] = "06:00+0800"
            custom_data["cutoffTime"] = "00:00+0800"
        if model == "evonet":
            # evonet模式下取各自的日切时间
            wop_data["cutoffTime"] = "00:00+0800"
            mop_data["cutoffTime"] = "00:00+0800"
        relation_data = self.create_mongo_config.create_relation(mopID=mopid, wopID=wopid)
        return wop_data, mop_data, custom_data, relation_data


if __name__ == '__main__':
    pass
