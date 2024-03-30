from base.read_config import Conf
from common.evopay.conf_init import db_tyo_evoconfig, evopay_conf
from common.evopay.evonet_to_partner_check import test_ini_file
from common.evopay.moudle import Moudle


class mongo_initial:
    def __init__(self, database_connection, version='v0', type='payment'):
        self.version = version
        self.db = database_connection

        if type == 'payment':
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
        else:
            self.transfer_notification = evopay_conf.transfer_notification
            self.transfer_userVerification = evopay_conf.transfer_userVerification
            self.transfer_order = evopay_conf.transfer_order
            self.transfer_inquiry = evopay_conf.transfer_inquiry

    def create_sop(self, **kwargs):
        sop_params = {
            "baseInfo_sopID": "sopID_HarsyaTest_01",
            "baseInfo_sopName": "sopID_HarsyaTest_01",
            "baseInfo_sopLogo": "https://tyo-testing-portal.pre-evonetonline.com/assets/logo.png",
            "baseInfo_nodeID": "tyo",
            "baseInfo_signKeyC": "5b18706bd8968363f995de1cbaa4d5eeea9cd8a40767f61269789bec7bfd424178111a40ad7213178cdab53498104401",
            "settleInfo_settleCurrency": "JPY",
            "settleInfo_fxRateOwner": "auto_user",
            "settleInfo_isSettlementAmountEVONETCalculated": True,
            "settleInfo_serviceFee": 0.1,
            "settleInfo_transferMode": "offline",
            "settleInfo_transferCurrency": "CNY",
            "settleInfo_senderFee": 0.3,
            "status": "active",
            "location" : "CHN",
            "deleteFlag": False,
            "operationalNode": "tyo"
        }
        sop_params.update(kwargs)
        insert_sop = {
            "baseInfo": {
                "sopID": sop_params['baseInfo_sopID'],
                "sopName": sop_params['baseInfo_sopName'],
                "sopLogo": sop_params['baseInfo_sopLogo'],
                "nodeID": sop_params['baseInfo_nodeID'],
                "signKeyC": sop_params['baseInfo_signKeyC'],
                "country": sop_params['location'],
                "notification": {
                    "url": self.transfer_notification,
                    "version": "v0"
                }
            },
            "settleInfo": {
                "settleCurrency": sop_params.get('settleInfo_settleCurrency'),
                "serviceFee" : sop_params.get('settleInfo_serviceFee'),
                "fxRateOwner": sop_params.get('settleInfo_fxRateOwner'),
                "transferMode": sop_params.get('settleInfo_transferMode'),
                "transferCurrency": sop_params.get('settleInfo_transferCurrency'),
                "senderFee": sop_params.get('settleInfo_senderFee'),
                "isSettlementAmountEVONETCalculated": sop_params.get('settleInfo_isSettlementAmountEVONETCalculated')
            },
            "status": sop_params.get('status'),
            "version": int(1),
            "deleteFlag": sop_params.get('deleteFlag'),
            "updateUser": "auto_user",

            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [sop_params.get('operationalNode')]  # 操作节点
        }

        self.db.insert_one(table='sop', insert_params=insert_sop)

    def create_rop(self, **kwargs):
        rop_params = {
            "baseInfo_ropID": "ropID_ropHarsyaTest_01",
            "baseInfo_ropName": "sopID_HarsyaTest_01",
            "baseInfo_ropLogo": "https://tyo-testing-portal.pre-evonetonline.com/assets/logo.png",
            "baseInfo_nodeID": "tyo",
            "location": "CHN",
            "baseInfo_signKeyC": "5b18706bd8968363f995de1cbaa4d5eeea9cd8a40767f61269789bec7bfd424178111a40ad7213178cdab53498104401",
            "settleInfo_settleCurrency": "HKD",
            "settleInfo_serviceFee": 0.1,
            "status": "active",
            "deleteFlag": False,
            "operationalNode": "tyo",

        }
        rop_params.update(kwargs)
        insert_rop = {
            "baseInfo": {
                "country": rop_params['location'],
                "ropID": rop_params['baseInfo_ropID'],
                "ropName": rop_params['baseInfo_ropName'],
                "ropLogo": rop_params['baseInfo_ropLogo'],
                "nodeID": rop_params['baseInfo_nodeID'],
                "signKeyC": rop_params['baseInfo_signKeyC'],
                "userVerification": {
                    "url": self.transfer_userVerification,
                    "version": "v0"
                },
                "order": {
                    "url": self.transfer_order,
                    "version": "v0"
                },
                "inquiry": {
                    "url": self.transfer_inquiry,
                    "version": "v0"
                }
            },
            "settleInfo": {
                "settleCurrency": rop_params.get('settleInfo_settleCurrency'),
                "serviceFee": rop_params.get('settleInfo_serviceFee'),
            },
            "status": rop_params.get('status'),
            "version": int(1),
            "deleteFlag": rop_params.get('deleteFlag'),
            "updateUser": "auto_user",
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [rop_params.get('operationalNode')]  # 操作节点

        }
        self.db.insert_one(table='rop', insert_params=insert_rop)

    def create_relationTransfer_online(self, **kwargs):
        relation_params = {
            "ropID": "ropID_ropHarsyaTest_01",
            "sopID": "sopID_HarsyaTest_01",
            "settlementMode" : "EVONET",
            "type": "Online",
            "location": "CHN",
            "deleteFlag": False
        }
        relation_params.update(kwargs)
        insert_relation = {
            "ropID": relation_params['ropID'],
            "sopID": relation_params['sopID'],
            "type": relation_params['type'],
            "location": relation_params['location'],
            "settlementMode":relation_params['settlementMode'],
            "version": int(1),
            "deleteFlag": relation_params.get('deleteFlag'),
            "operationalNode": [relation_params.get('operationalNode')]  # 操作节点
        }
        self.db.insert_one(table='relationTransfer', insert_params=insert_relation)

    def create_relationTransfer_offline(self, **kwargs):
        relation_params = {
            "ropID": "ropID_ropHarsyaTest_01_off",
            "sopID": "sopID_HarsyaTest_01_off",
            "location": "CHN",
            "tpspID": "tpspID_tpsppHarsyaTest01_off",
            "type": "Offline"
        }
        relation_params.update(kwargs)
        insert_relation = {
            "ropID": relation_params['ropID'],
            "sopID": relation_params['sopID'],
            "location": relation_params['location'],
            "type": relation_params['type'],
            "version": int(1),
            "deleteFlag": relation_params.get('deleteFlag'),
            "operationalNode": [relation_params.get('operationalNode')]  # 操作节点
        }
        self.db.insert_one(table='relationTransfer', insert_params=insert_relation)

    def create_serviceFee_online(self, **kwargs):
        serviceFee_params = {
            "transferMode": "offline",
            "ropID": "ropID_ropHarsyaTest_01",
            "sopID": "sopID_HarsyaTest_01",
            "transferCurrency" : "CNY",
            "senderFee": 1,
            "sopSettlementCurrency": "JPY",
            "sopServiceFee": 1,
            "ropSettlementCurrency": "HKD",
            "ropServiceFee": 0.1,
            "location": "CHN",
            "fxRateOwner": "auto_user",
            "deleteFlag": False,
        }
        serviceFee_params.update(kwargs)
        insert_serviceFee = {
            "transferMode": serviceFee_params['transferMode'],
            "ropID": serviceFee_params['ropID'],
            "sopID": serviceFee_params['sopID'],
            "transferCurrency": serviceFee_params['transferCurrency'],
            "senderFee": serviceFee_params['senderFee'],
            "sopSettlementCurrency": serviceFee_params['sopSettlementCurrency'],
            "sopServiceFee": serviceFee_params['sopServiceFee'],
            "ropSettlementCurrency": serviceFee_params['ropSettlementCurrency'],
            "ropServiceFee": serviceFee_params['ropServiceFee'],
            "location": serviceFee_params['location'],
            "deleteFlag": serviceFee_params.get('deleteFlag'),
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time()  # 创建时间
        }
        self.db.insert_one(table='serviceFee', insert_params=insert_serviceFee)

    def create_serviceFee_offline(self, **kwargs):
        serviceFee_params = {
            "transferMode" : "offline",
            "ropID": "ropID_ropHarsyaTest_01",
            "sopID": "sopID_HarsyaTest_01",
            "transferCurrency" : "CNY",
            "senderFee": 1,
            "sopSettlementCurrency": "JPY",
            "sopServiceFee": 1,
            "ropSettlementCurrency": "HKD",
            "ropServiceFee": 0.1,
            "tpspSettlementCurrency":"HKD",
            "tpspRebateFee":0.1,
            "location": "CHN",
            "fxRateOwner": "auto_user",
            "deleteFlag": False,
        }
        serviceFee_params.update(kwargs)
        insert_serviceFee = {
            "transferMode": serviceFee_params['transferMode'],
            "ropID": serviceFee_params['ropID'],
            "sopID": serviceFee_params['sopID'],
            "transferCurrency": serviceFee_params['transferCurrency'],
            "senderFee": serviceFee_params['senderFee'],
            "sopSettlementCurrency": serviceFee_params['sopSettlementCurrency'],
            "sopServiceFee": serviceFee_params['sopServiceFee'],
            "ropSettlementCurrency": serviceFee_params['ropSettlementCurrency'],
            "ropServiceFee": serviceFee_params['ropServiceFee'],
            "tpspSettlementCurrency": serviceFee_params['tpspSettlementCurrency'],
            "tpspRebateFee": serviceFee_params['tpspRebateFee'],
            "location": serviceFee_params['location'],
            "deleteFlag": serviceFee_params.get('deleteFlag'),
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time()  # 创建时间
        }
        self.db.insert_one(table='serviceFee', insert_params=insert_serviceFee)

    def create_wop(self, **kwargs):
        wop_parameters = {
            'baseInfo_wopID': 'WOP_Auto_JCoinPay_01', 'baseInfo_brandID': 'MOP_Auto_GrabPay_01',
            'baseInfo_nodeID': 'tyo', 'baseInfo_status': 'active', 'settleInfo_fileInitiator': 'evonet',
            'baseInfo_status': 'active', 'baseInfo_brandID': 'Auto_GrabPay_01',
            'specialInfo_specialType': '', 'settleInfo_specialCategory': '',
            'settleInfo_cutoffTime': Moudle().less_cutoffTime(),
            'settleInfo_settleCurrency': 'EUR',
            'settleInfo_cpmInterchangeFeeRate': 0.0,
            'settleInfo_mpmInterchangeFeeRate': 0.0,
            'settleInfo_settleFileTime': '09:00+0800',
            'settleInfo_isBillingAmountCalculated': True,
            'settleInfo_billingCurrency': 'EUR',
            'settleInfo_wccr': 0.12,
            'settleInfo_cccr': 0.15,
            'settleInfo_transactionProcessingFeeRate': 0.0,
            'settleInfo_transProcessingFeeCollectionMethod': 'daily',
            'settleInfo_fxProcessingFeeRate': 0.0,
            'settleInfo_fxProcessingFeeCollectionMethod': 'daily',
            'settleInfo_fxRebateCollectionMethod ': 'daily',
            'deleteFlag': False,
            'operationalNode': 'tyo',
            'baseInfo_signKeyC': Conf(test_ini_file).get("mongoDB", "tyo_signkeyC")
        }
        wop_parameters.update(kwargs)
        insert_wop = {
            "baseInfo": {
                "status": wop_parameters['baseInfo_status'],
                "wopID": wop_parameters['baseInfo_wopID'],
                "wopName": wop_parameters['baseInfo_wopID'],
                "brandID": wop_parameters['baseInfo_brandID'],
                "country": "JPN",
                "nodeID": wop_parameters['baseInfo_nodeID'],
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
                "cutoffTime": "12:00",
                "signKeyC": wop_parameters['baseInfo_signKeyC'],
                "accountDebit": {
                    "url": self.account_debit_url,
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
            "settleInfo": {
                "fileInitiator": wop_parameters.get('settleInfo_fileInitiator'),  # 文件发起方
                "specialCategory": wop_parameters.get('settleInfo_specialCategory'),  # 文件特殊种类
                "settleCurrency": wop_parameters.get('settleInfo_settleCurrency'),  # 清算币种
                "cutoffTime": wop_parameters.get('settleInfo_cutoffTime'),  # 日切时间
                "cpmInterchangeFeeRate": wop_parameters.get('settleInfo_cpmInterchangeFeeRate'),  # cpmInterchangeFee
                "mpmInterchangeFeeRate": wop_parameters.get('settleInfo_mpmInterchangeFeeRate'),  # mpmInterchangeFee
                "settleFileTime": wop_parameters.get('settleInfo_settleFileTime'),  # 文件生成时间
                "isBillingAmountCalculated": wop_parameters.get('settleInfo_isBillingAmountCalculated'),
                # billingAmount是否计算
                "billingCurrency": wop_parameters.get('settleInfo_billingCurrency'),  # billingCurrency
                "wccr": wop_parameters.get('settleInfo_wccr'),
                "cccr": wop_parameters.get('settleInfo_cccr'),
                "transactionProcessingFeeRate": wop_parameters.get('settleInfo_transactionProcessingFeeRate'),  # 交易处理费
                "transProcessingFeeCollectionMethod": wop_parameters.get(
                    'settleInfo_transProcessingFeeCollectionMethod'),
                # 交易处理费生成方式
                "fxProcessingFeeRate": wop_parameters.get('settleInfo_fxProcessingFeeRate'),  # 汇率转换费
                "fxProcessingFeeCollectionMethod": wop_parameters.get('settleInfo_fxProcessingFeeCollectionMethod'),
                # 汇率转换费生成方式
                "fxRebateCollectionMethod": wop_parameters.get('settleInfo_fxRebateCollectionMethod'),
            },
            "specialInfo": {
                "specialType": wop_parameters.get('specialInfo_specialType'),  # 特殊类型
                "batchRefundSettle": False
            },
            "version": int(1),  # 版本
            "deleteFlag": wop_parameters.get('deleteFlag'),  # 删除标识
            "updateUser": "auto_user",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [wop_parameters.get('operationalNode')]  # 操作节点
        }

        self.db.insert_one(table='wop', insert_params=insert_wop)

    def create_customizeConfig01(self, **kwargs):
        customizeConfig01_parameters = {'wopID': 'WOP_Auto_JCoinPay_01', 'settleInfo_fileInitiator': 'evonet',
                                        'status': 'active', 'isCPMSupported': True, 'mopID': 'MOP_Auto_GrabPay_01',
                                        'isMPMSupported': True, 'isRefundSupported': True,
                                        'transCurrencies': [{"currency": "JPY", "mccr": 0.11},
                                                            {"currency": "HKD", "mccr": 0.3},
                                                            {"currency": "SGD", "mccr": 0.3}],
                                        'settleMode': 'bilateral',
                                        'settleCurrency': 'JPY',
                                        'isSettlementAmountEVONETCalculated': True,
                                        'cpmInterchangeFeeRate': 0.0, 'mpmInterchangeFeeRate': 0.0,
                                        'mccr': 0.13, 'fxRateOwner': 'auto_user',
                                        'transactionProcessingFeeRate': 0.0,
                                        'transProcessingFeeCollectionMethod': 'daily',
                                        'fxProcessingFeeRate': 0.0, 'fxProcessingFeeCollectionMethod': 'daily',
                                        'deleteFlag': False, 'operationalNode': 'tyo'}
        customizeConfig01_parameters.update(kwargs)
        insert_customizeConfig = {
            "status": customizeConfig01_parameters.get('status'),  # 状态
            "mopID": customizeConfig01_parameters.get('mopID'),  # mopID
            "mopName": customizeConfig01_parameters.get('mopID'),  # mopName
            "wopID": customizeConfig01_parameters.get('wopID'),  # wopID
            "wopName": customizeConfig01_parameters.get('wopID'),
            "isCPMSupported": customizeConfig01_parameters.get('isCPMSupported'),  # 是否支持CPM
            "isMPMSupported": customizeConfig01_parameters.get('isMPMSupported'),  # 是否支持MPM
            "isRefundSupported": customizeConfig01_parameters.get('isRefundSupported'),  # 是否支持Refund
            "transCurrencies": customizeConfig01_parameters.get('transCurrencies'),
            "settleMode": customizeConfig01_parameters.get('settleMode'),  # 清算模式bilateral / evonet
            "settleCurrency": customizeConfig01_parameters.get('settleCurrency'),  # 清算币种
            "isSettlementAmountEVONETCalculated": customizeConfig01_parameters.get(
                'isSettlementAmountEVONETCalculated'),
            # 是否计算清算币种
            "cpmInterchangeFeeRate": customizeConfig01_parameters.get('cpmInterchangeFeeRate'),  # cpmInterchangeFee
            "mpmInterchangeFeeRate": customizeConfig01_parameters.get('mpmInterchangeFeeRate'),  # mpmInterchangeFee
            "mccr": customizeConfig01_parameters.get('mccr'),
            "cutoffTime": Moudle().less_cutoffTime(),
            "fxRateOwner": customizeConfig01_parameters.get('fxRateOwner'),  # 汇率归属
            "transactionProcessingFeeRate": customizeConfig01_parameters.get('transactionProcessingFeeRate'),  # 交易处理费
            "transProcessingFeeCollectionMethod": customizeConfig01_parameters.get(
                'transProcessingFeeCollectionMethod'),
            # 交易处理费生成方式
            "fxProcessingFeeRate": customizeConfig01_parameters.get('fxProcessingFeeRate'),  # 汇率转换费
            "fxProcessingFeeCollectionMethod": customizeConfig01_parameters.get('fxProcessingFeeCollectionMethod'),
            # 汇率转换费生成方式
            "fileInitiator": customizeConfig01_parameters.get('settleInfo_fileInitiator'),
            "version": int(1),  # 版本
            "deleteFlag": customizeConfig01_parameters.get('deleteFlag'),  # 删除标识
            "updateUser": "auto_test",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [  # 操作节点
                customizeConfig01_parameters.get('operationalNode')
            ]}
        self.db.insert_one(table='customizeConfig', insert_params=insert_customizeConfig)

    def create_cusomizeConfig(self, **kwargs):
        customizeConfig_parameters = {'wopID': 'WOP_Auto_JCoinPay_01', 'settleInfo_fileInitiator': 'evonet',
                                      'status': 'active', 'isCPMSupported': True, 'mopID': 'MOP_Auto_GrabPay_002',
                                      'isMPMSupported': True, 'isRefundSupported': True,
                                      'transCurrencies': [{"currency": "JPY", "mccr": 0.11},
                                                          {"currency": "HKD", "mccr": 0.3},
                                                          {"currency": "SGD", "mccr": 0.3}],
                                      'settleMode': 'evonet',
                                      'settleCurrency': '',
                                      'isSettlementAmountEVONETCalculated': True,
                                      'cpmInterchangeFeeRate': 0.0, 'mpmInterchangeFeeRate': 0.0,
                                      'mccr': 0.13, 'wccr': 0.12, 'fxRateOwner': 'auto_user',
                                      'transactionProcessingFeeRate': 0.0,
                                      'transProcessingFeeCollectionMethod': 'daily',
                                      'fxProcessingFeeRate': 0.0, 'fxProcessingFeeCollectionMethod': 'daily',
                                      'deleteFlag': False, 'operationalNode': 'tyo'}
        customizeConfig_parameters.update(kwargs)

        insert_customizeConfig = {
            "status": customizeConfig_parameters.get('status'),  # 状态
            "mopID": customizeConfig_parameters.get('mopID'),  # mopID
            "mopName": customizeConfig_parameters.get('mopID'),  # mopName
            "wopID": customizeConfig_parameters.get('wopID'),  # wopID
            "wopName": customizeConfig_parameters.get('wopID'),
            "isCPMSupported": customizeConfig_parameters.get('isCPMSupported'),  # 是否支持CPM
            "isMPMSupported": customizeConfig_parameters.get('isMPMSupported'),  # 是否支持MPM
            "isRefundSupported": customizeConfig_parameters.get('isRefundSupported'),  # 是否支持Refund
            "transCurrencies": customizeConfig_parameters.get('transCurrencies'),
            "settleMode": customizeConfig_parameters.get('settleMode'),  # 清算模式bilateral / evonet
            "settleCurrency": customizeConfig_parameters.get('settleCurrency'),  # 清算币种
            "isSettlementAmountEVONETCalculated": customizeConfig_parameters.get('isSettlementAmountEVONETCalculated'),
            # 是否计算清算币种
            "cpmInterchangeFeeRate": customizeConfig_parameters.get('cpmInterchangeFeeRate'),  # cpmInterchangeFee
            "mpmInterchangeFeeRate": customizeConfig_parameters.get('mpmInterchangeFeeRate'),  # mpmInterchangeFee
            "mccr": customizeConfig_parameters.get('mccr'),
            "cutoffTime": Moudle().less_cutoffTime(),
            "wccr": customizeConfig_parameters.get('wccr'),
            "fxRateOwner": customizeConfig_parameters.get('fxRateOwner'),  # 汇率归属
            "transactionProcessingFeeRate": customizeConfig_parameters.get('transactionProcessingFeeRate'),  # 交易处理费
            "transProcessingFeeCollectionMethod": customizeConfig_parameters.get('transProcessingFeeCollectionMethod'),
            # 交易处理费生成方式
            "fxProcessingFeeRate": customizeConfig_parameters.get('fxProcessingFeeRate'),  # 汇率转换费
            "fxProcessingFeeCollectionMethod": customizeConfig_parameters.get('fxProcessingFeeCollectionMethod'),
            # 汇率转换费生成方式
            "fileInitiator": customizeConfig_parameters.get('settleInfo_fileInitiator'),
            "version": int(1),  # 版本
            "deleteFlag": customizeConfig_parameters.get('deleteFlag'),  # 删除标识
            "updateUser": "auto_test",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [  # 操作节点
                customizeConfig_parameters.get('operationalNode')
            ]}
        self.db.insert_one(table='customizeConfig', insert_params=insert_customizeConfig)

    def create_mop(self, **kwargs):
        mop_parameters = {
            "baseInfo_mopID": "MOP_Auto_GrabPay_03",
            "baseInfo_brandID": "Auto_GrabPay_03",
            "baseInfo_nodeID": "tyo", "baseInfo_status": "active",
            "baseInfo_useEVONETToken": False,
            "baseInfo_isCPMSupported": True,
            "baseInfo_isMPMSupported": True,
            "baseInfo_isRefundSupported": True,
            "baseInfo_transCurrencies": [{"currency": "JPY", "mccr": 0.11}, {"currency": "HKD", "mccr": 0.3},
                                         {"currency": "SGD", "mccr": 0.3}],
            "baseInfo_schemeInfo_schemeName": '',
            "baseInfo_schemeInfo_signStatus": '',
            "settleInfo_fileInitiator": 'evonet',
            "specialInfo_specialType": '',
            "settleInfo_settleCurrency": 'JPY',
            "settleInfo_cpmInterchangeFeeRate": 0.0,
            "settleInfo_mpmInterchangeFeeRate": 0.0,
            "settleInfo_cutoffTime": Moudle().less_cutoffTime(),
            "settleInfo_settleFileTime": "09:00+0800",
            "settleInfo_mccr": 0.0,
            "settleInfo_transactionProcessingFeeRate": 0.0,
            "settleInfo_transProcessingFeeCollectionMethod": 'daily',
            "settleInfo_fxProcessingFeeRate": 0.0,
            "settleInfo_fxProcessingFeeCollectionMethod": 'daily',
            "settleInfo_fxRebateCollectionMethod": 'daily',
            "deleteFlag": False,
            "operationalNode": 'tyo',
            "baseInfo_signKeyC": Conf(test_ini_file).get("mongoDB", "tyo_signkeyC")
        }
        mop_parameters.update(kwargs)

        insert_mop = {
            "baseInfo": {
                "status": mop_parameters.get("baseInfo_status"),
                "mopID": mop_parameters.get("baseInfo_mopID"),
                "mopName": mop_parameters.get("baseInfo_mopID"),
                "brandID": mop_parameters.get("baseInfo_brandID"),
                "useEVONETToken": mop_parameters.get("baseInfo_useEVONETToken"),
                "country": "JPN",
                "nodeID": mop_parameters.get("baseInfo_nodeID"),
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
                "isCPMSupported": mop_parameters.get("baseInfo_isCPMSupported"),
                "isMPMSupported": mop_parameters.get("baseInfo_isMPMSupported"),
                "isRefundSupported": mop_parameters.get("baseInfo_isRefundSupported"),
                "transCurrencies": mop_parameters.get("baseInfo_transCurrencies"),  # 列表
                "schemeInfo": [
                    {
                        "schemeName": mop_parameters.get("baseInfo_schemeInfo_schemeName"),
                        "signStatus": mop_parameters.get("baseInfo_schemeInfo_signStatus")
                    }
                ],
                "signKeyC": mop_parameters.get("baseInfo_signKeyC"),
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
                "fileInitiator": mop_parameters.get("settleInfo_fileInitiator"),  # 文件发起方
                "settleCurrency": mop_parameters.get("settleInfo_settleCurrency"),  # 清算币种
                "cpmInterchangeFeeRate": mop_parameters.get("settleInfo_cpmInterchangeFeeRate"),  # cpmInterchangeFee
                "mpmInterchangeFeeRate": mop_parameters.get("settleInfo_mpmInterchangeFeeRate"),  # mpmInterchangeFee
                "cutoffTime": mop_parameters.get("settleInfo_cutoffTime"),  # 日切时间

                "settleFileTime": mop_parameters.get("settleInfo_settleFileTime"),  # 文件生成时间
                "mccr": mop_parameters.get("settleInfo_mccr"),
                "transactionProcessingFeeRate": mop_parameters.get("settleInfo_transactionProcessingFeeRate"),  # 交易处理费
                "transProcessingFeeCollectionMethod": mop_parameters.get(
                    "settleInfo_transProcessingFeeCollectionMethod"),  # 交易处理费生成方式
                "fxProcessingFeeRate": mop_parameters.get("settleInfo_fxProcessingFeeRate"),  # 汇率转换费
                "fxProcessingFeeCollectionMethod": mop_parameters.get("settleInfo_fxProcessingFeeCollectionMethod"),
                # 汇率转换费生成方式
                "fxRebateCollectionMethod": mop_parameters.get("settleInfo_fxRebateCollectionMethod")
            },
            "specialInfo": {
                "specialType": mop_parameters.get("specialInfo_specialType"),  # 特殊类型
                "batchRefundSettle": False
            },
            "version": int(32),  # 版本
            "deleteFlag": mop_parameters.get("deleteFlag"),  # 删除标识
            "updateUser": "auto_user",  # 更新用户
            "updateTime": Moudle().create_mongo_time(),  # 更新时间
            "createTime": Moudle().create_mongo_time(),  # 创建时间
            "operationalNode": [mop_parameters.get("operationalNode"), ]  # 操作节点
        }
        self.db.insert_one(table='mop', insert_params=insert_mop)
