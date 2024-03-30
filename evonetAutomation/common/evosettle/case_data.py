import random
from base.date_format import DateUtil


class CaseData(object):
    # 初始化数据，最好经常更新，特别是有联机版本的时候，需要修改 wopid mopid, wopsettdate,mopsettdate,evonetordernumber
    #
    def __init__(self):
        self.time_format = DateUtil()
        self.now_time = self.time_format.evonet_format_time()

    def trans_data(self, wopid, mopid, sett_date, trans_type, evonet_order_number, refund_orig_evonet_order_nuber=None,
                   settle_mode="evonet"):
        # 按照清分格式造的数据
        # 修改时间格式，wopid,mopid,sett_date
        # 交易流水导入的时候是根据各自的 wopsettledate 或者mopsettledate 来的；
        # cpm mpmdata可能会不一样所以分开写两个data ,这样可以实时跟新 交易data
        trans_amount = 2300
        wop_settle_amount = trans_amount - 1000
        mop_settle_amount = trans_amount - 1100
        sett_data = {
            "mopTransTime": self.now_time,
            "userData": {
                "wopToken": "autotest1601275952759180501116040",
                "evonetUserReference": "autotest1601275952759180501116040"
            },
            "settleMode": settle_mode,
            "mopSettleDate": sett_date,
            "evonetOrderNumber": evonet_order_number,
            "billingConverterCurrencyFlag": True,
            "lockFlag": int(0),
            "evonetPayTime": self.now_time,
            "wopSettleDate": sett_date,
            "wopPayTime": self.now_time,
            "evonetOrderCreateTime": self.now_time,
            "mopConverterCurrencyFlag": True,
            "wopOrderNumber": str(random.randint(10000000000000, 90000000000000)),
            "status": "succeeded",
            "wopID": wopid,
            "mopID": mopid,
            "wopConverterCurrencyFlag": True,
            "wopSettleSourceCurrency": "JPY",
            "wopSettleCurrency": "JPY",
            "mopSettleCurrency": "CNY",
            "wopSettleAmount": wop_settle_amount,
            "mopSettleAmount": mop_settle_amount,
            "wopStatus": "succeeded",
            "mopStatus": "succeeded",
            "transAmount": trans_amount,
            "transCurrency": "JPY",
            "transType": trans_type,
            "category": "QR",
            "mopOrderNumber": str(random.randint(10000000000000, 900000000000000)),
            "result": {
                "message": "Success.",
                "code": "S0000"
            },
            "wopTransTime": self.now_time,
            "storeInfo": {
                "postCode": str(random.randint(10000000009, 90000000009)),
                "terminalNumber": str(random.randint(10000000009, 90000000009)),
                "phoneNumber": str(random.randint(10000000009, 90000000009)),
                "emailAddress": "evonet-global@evonet.com",
                "id": str(random.randint(10000000009, 90000000009)),
                "localName": "localName",
                "mcc": "7011",
                "city": "Shanghai",
                "englishName": "englishName",
                "country": "CNY",
                "address": "ShangHai"
            },

        }
        if trans_type == "Refund":  # 退款交易
            sett_data["originalEVONETOrderNumber"] = refund_orig_evonet_order_nuber
            sett_data["transAmount"] = 1150.0
            sett_data["originalMOPOrderNumber"] = str(random.randint(10000000009, 90000000009))
            refund_settle_amount = wop_settle_amount / 2
            sett_data["wopSettleAmount"] = refund_settle_amount
            sett_data["mopSettleAmount"] = mop_settle_amount / 2
        return sett_data

    def trans_list(self, wopid, mopid, sett_date, model):
        cpm_order_number = str(random.randint(100000000000000000000, 900000000000000000000))
        mpm_order_number = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_orig_cpm_evonet_order_nuber = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_order_number = str(random.randint(100000000000000000000, 900000000000000000000))

        cpm_sett_data = self.trans_data(wopid, mopid, sett_date, "CPM Payment", cpm_order_number,
                                        settle_mode=model
                                        )
        mpm_sett_data = self.trans_data(wopid, mopid, sett_date, "MPM Payment", mpm_order_number,
                                        settle_mode=model
                                        )
        orig_cpm_sett_data = self.trans_data(wopid, mopid, sett_date, "CPM Payment",
                                             refund_orig_cpm_evonet_order_nuber, settle_mode=model)
        # CPM退款交易
        refund_cpm_sett_data = self.trans_data(wopid, mopid, sett_date, "Refund", refund_order_number,
                                               refund_orig_evonet_order_nuber=refund_orig_cpm_evonet_order_nuber,
                                               settle_mode=model)
        sett_trans_list = [cpm_sett_data, mpm_sett_data, orig_cpm_sett_data, refund_cpm_sett_data]
        # 返回订单号顺序Wie  cpm,mpm, 退款的cpm,退款交易的订单号
        order_number_list = [cpm_order_number, mpm_order_number, refund_orig_cpm_evonet_order_nuber,
                             refund_order_number]
        return (sett_trans_list, order_number_list)

    def upi_trans_data(self, wopid, mopid, sett_date, trans_type, evonet_order_number, qrcvoucher,
                       refund_orig_evonet_order_nuber=None,
                       settle_mode="bilateral"):
        # 按照清分格式造的数据
        # 修改时间格式，wopid,mopid,sett_date
        # 交易流水导入的时候是根据各自的 wopsettledate 或者mopsettledate 来的；
        # cpm mpmdata可能会不一样所以分开写两个data ,这样可以实时跟新 交易data
        trans_amount = 2300
        wop_settle_amount = trans_amount - 1000
        mop_settle_amount = trans_amount - 1100
        sett_data = {
            "mopTransTime": self.now_time,
            "userData": {
                "wopUserReference": "wop_ting_004",
                "wopToken": "32131",
                "evonetUserReference": "08a4500727444e2b6a704edc2d24bf63"
            },
            "qrcVoucherNo": qrcvoucher,
            "settleMode": settle_mode,
            "mopSettleDate": sett_date,
            "evonetOrderNumber": evonet_order_number,
            "billingConverterCurrencyFlag": True,
            "lockFlag": int(0),
            "evonetPayTime": self.now_time,
            "wopSettleDate": sett_date,
            "wopPayTime": self.now_time,
            "evonetOrderCreateTime": self.now_time,
            "mopConverterCurrencyFlag": True,
            "wopOrderNumber": str(random.randint(10000000000000, 90000000000000)),
            "status": "succeeded",
            "wopID": wopid,
            "mopID": mopid,
            "wopConverterCurrencyFlag": True,
            "wopSettleSourceCurrency": "JPY",
            "wopSettleCurrency": "JPY",
            "mopSettleCurrency": "CNY",
            "wopSettleAmount": wop_settle_amount,
            "mopSettleAmount": mop_settle_amount,
            "wopStatus": "succeeded",
            "mopStatus": "succeeded",
            "transAmount": trans_amount,
            "transCurrency": "JPY",
            "transType": trans_type,
            "category": "QR",
            "mopOrderNumber": str(random.randint(10000000000000, 900000000000000)),
            "result": {
                "message": "Success.",
                "code": "S0000"
            },
            "rawData": {
                "retrievalReferenceNumber": "000000148186",
                "acquirerIIN": "92320446",
                "forwardingIIN": str(random.randint(10000000, 99999999)),
                "processingCode": "000000",
                "posEntryMod": "042",
                "posCondCode": "00",
                "systemTraceAuditNum": str(random.randint(100000, 999999)),
                "transmissionDateTime": "0308" + str(random.randint(100000, 999999)),
                "settleDate": "0308"
            },
            "card": {
                "networkTokenPan": "6292603496267092",
                "maskedNumber": "622934******1046",
                "numberC": "6c0b952fb37f69a9e2a72d5d619785c1df6aeab2c49330c1e5056972ef5eeab5",
                "expiryMonth": "76273461547094f0c1240a8a1a3da79d3abb",
                "expiryYear": "c85c13ffacee27f31c2bf7c6c882379e34c34afa"
            },
            "wopTransTime": self.now_time,
            "storeInfo": {
                "postCode": str(random.randint(10000000009, 90000000009)),
                "terminalNumber": str(random.randint(10000000009, 90000000009)),
                "phoneNumber": str(random.randint(10000000009, 90000000009)),
                "emailAddress": "evonet-global@evonet.com",
                "id": str(random.randint(10000000009, 90000000009)),
                "localName": "localName",
                "mcc": "7011",
                "city": "Shanghai",
                "englishName": "englishName",
                "country": "CNY",
                "address": "ShangHai"
            },

        }
        if trans_type == "Refund":  # 退款交易
            sett_data["originalEVONETOrderNumber"] = refund_orig_evonet_order_nuber
            sett_data["transAmount"] = 1150.0
            sett_data["originalMOPOrderNumber"] = str(random.randint(10000000009, 90000000009))
            refund_settle_amount = wop_settle_amount / 2
            sett_data["wopSettleAmount"] = refund_settle_amount
            sett_data["mopSettleAmount"] = mop_settle_amount / 2
        return sett_data

    def upi_daily_summary_data(self, wopid, mopid, sett_date, trans_type, trans_currency, settle_currency,
                               fee_receiveable_amount, fee_payable_amount
                               ):

        # 按照清分格式造的数据
        # 修改时间格式，wopid,mopid,sett_date
        # 交易流水导入的时候是根据各自的 wopsettledate 或者mopsettledate 来的；
        # cpm mpmdata可能会不一样所以分开写两个data ,这样可以实时跟新 交易data
        trans_amount = 2300
        wop_settle_amount = trans_amount - 1000
        mop_settle_amount = trans_amount - 1100
        data = []
        for i in range(2):
            evonet_order_number = str(random.randint(10000000000000000, 90000000000000000))
            sett_data = {"trans": {
                "mopOrderNumber": "125878777185704",
                "wopOrderNumber": "85217596137140",
                "evonetOrderNumber": evonet_order_number,
                "mopSettleDate": "20210110",
                "wopSettleDate": "20210110",
                "wopConverterCurrencyFlag": True,
                "mopConverterCurrencyFlag": True,
                "billingConverterCurrencyFlag": True,
                "originalEVONETOrderNumber": "241076352589478930767",
                "originalMOPOrderNumber": "66474213279",
                "transAmount": 1150.0,
                "transCurrency": trans_currency,
                "status": "succeeded",
                "wopStatus": "succeeded",
                "mopStatus": "succeeded",
                "mopSettleAmount": mop_settle_amount,
                "mopSettleCurrency": settle_currency,
                "wopSettleAmount": wop_settle_amount,
                "wopSettleCurrency": settle_currency,
                "wopSettleSourceCurrency": "JPY",
                "userData": {
                    "wopUserReference": "wop_ting_004",
                    "wopToken": "32131",
                    "evonetUserReference": "08a4500727444e2b6a704edc2d24bf63"
                },
                "card": {
                    "networkTokenPan": "6292603496267092",
                    "maskedNumber": "622934******1046",
                    "numberC": "6c0b952fb37f69a9e2a72d5d619785c1df6aeab2c49330c1e5056972ef5eeab5",
                    "expiryMonth": "76273461547094f0c1240a8a1a3da79d3abb",
                    "expiryYear": "c85c13ffacee27f31c2bf7c6c882379e34c34afa"
                },
                "storeInfo": {
                    "id": "54809619041",
                    "englishName": "englishName",
                    "localName": "localName",
                    "mcc": "7011",
                    "country": "CNY",
                    "city": "Shanghai",
                    "address": "ShangHai",
                    "postCode": "77463886456",
                    "terminalNumber": "63605689729",
                    "phoneNumber": "44128007361",
                    "emailAddress": "evonet-global@evonet.com"
                },
                "transType": trans_type,
                "category": "Card",
                "qrcVoucherNo": "254983730606175172716",
                "wopID": wopid,
                "mopID": mopid,
                "rawData": {
                    "retrievalReferenceNumber": "000000148186",
                    "acquirerIIN": "92320446",
                    "forwardingIIN": "34474626",
                    "processingCode": "000000",
                    "posEntryMod": "042",
                    "posCondCode": "00",
                    "systemTraceAuditNum": "543335",
                    "transmissionDateTime": "0308909340",
                    "settleDate": "0308"
                },
                "result": {
                    "code": "S0000",
                    "message": "Success."
                },
                "lockFlag": int(0),
                "settleMode": "bilateral"
            },
                "settleDate": sett_date,
                "blendKey": evonet_order_number,
                "blendType": "success",
                "clearFlag": True,
                "feeFlag": True,
                "settleFlag": True,
                "amountErrorFlag": False,
                "settleInfo": {
                    "settleMode": "bilateral",
                    "settleCurrency": settle_currency,
                    "settleAmount": wop_settle_amount,
                    "interchangeFee": 0.0,
                    "interchangeFeeRate": 0.0,
                    "serviceFeeSettleCurrency": "CNY",
                    "serviceFeeSettleAmount": 3333.0,
                    "rebate": 0.0,
                    "rebateRefund": 0.0,
                    "rebateCCR": 0.0,
                    "rebateType": "",
                    "interchangeFeeRefund": 0.0,
                    "processingFeeCollectionMethod": "daily",
                    "processingFee": 66.0,
                    "processingFeeRate": 0.0,
                    "fxProcessingFeeCollectionMethod": "daily",
                    "fxProcessingFee": 0.0,
                    "fxProcessingFeeRate": 0.0,
                    "feeReceivable": fee_receiveable_amount,
                    "feePayable": fee_payable_amount}}
            if settle_currency == "CNY":
                if trans_type == "Refund":  # 退款交易
                    sett_data["transAmount"] = 1150.0
                    sett_data["originalMOPOrderNumber"] = str(random.randint(10000000009, 90000000009))
                    sett_data["settleInfo"]["settleAmount"] = wop_settle_amount / 2
                    sett_data["settleInfo"]["processingFee"] = 33.0
                sett_data["settleInfo"]["processingFee"] = 66.66
                sett_data["settleInfo"]["feeReceivable"] = fee_receiveable_amount + 0.66
                sett_data["settleInfo"]["feePayable"] = fee_payable_amount + 0.33

            if settle_currency == "JPY":
                if trans_type == "Refund":  # 退款交易
                    sett_data["transAmount"] = 1150.0
                    sett_data["originalMOPOrderNumber"] = str(random.randint(10000000009, 90000000009))
                    sett_data["settleInfo"]["settleAmount"] = wop_settle_amount / 2
                    sett_data["settleInfo"]["processingFee"] = 33.0
                sett_data["settleInfo"]["processingFee"] = 66.0
                sett_data["settleInfo"]["feeReceivable"] = fee_receiveable_amount
                sett_data["settleInfo"]["feePayable"] = fee_payable_amount
            data.append(sett_data)
        return data

    def upi_servicefee_report(self, wopid, mopid, trans_currency, settle_date, calculated_method):
        # 银联月报造数据
        settle_data = []
        for trans_type in ["Account Credit", "Account Debit", "Refund"]:
            data = {
                "summary": {
                    "transType": trans_type,
                    "transCurrency": trans_currency,
                    "settleCurrency": "CNY",
                    "counts": 2.0,
                    "transAmount": 2333.0,
                    "transProcessingFeeSettleAmount": 3333.0,
                    "fxProcessingFeeSettleAmount": 222.0,
                    "transProcessingFee": 132.22,
                    "settleAmount": -1300.0,
                    "brand": "MOP_SETTtungpb",
                    "interchangeFee": 0.0,
                    "fxProcessingFee": 0.0,
                    "fxRebate": 0.0,
                    "netSettleAmount": -1278.0,
                    "feeReceivable": -44.0,
                    "feePayable": 66.0
                },
                "settleDate": settle_date,
                "wopID": wopid,
                "mopID": mopid,
                "serviceFeeFlag": {
                    "processingCollectionMethod": "monthly",
                    "processingCalculatedMethod": calculated_method,
                    "fxRebateCollectionMethod": "",
                    "reportType": "monthly"
                }
            }
            settle_data.append(data)
        return settle_data

    def upi_err_data(self, wopid, mopid, settle_date, trans_currency, settle_currency):
        # 生每日 Summary 的前置数据
        fee_receive_amount = 12.66
        fee_payable_amount = 66.33
        settle_amount = 444.22
        if settle_currency == "JPY":
            fee_receive_amount = 12.0
            fee_payable_amount = 66.0
            settle_amount = 444.0
        settle_data = []
        for trans_type in ["Credit Adjustment", "Debit Adjustment", "Chargeback"]:
            for i in range(2):
                data = {
                    "wopID": wopid,
                    "mopID": mopid,
                    "settleDate": settle_date,
                    "blendKey": str(random.randint(100000000000000000000000, 900000000000000000000000)),
                    "trans": {
                        "transType": trans_type,
                        "mopID": mopid,
                        "transAmount": 333.0,
                        "transCurrency": trans_currency,
                        "settleAmount": settle_amount,
                        "settleCurrency": settle_currency,
                        "transactionProcessingFee": 33.0,
                        "netSettleAmount": 33.33,
                    },
                    "upiTrans": {
                        "accountNumberC": "518e4f6292bcfafe0adf5d743a57aaeab46dd8fc9ad2071889d6443720d6d99e2313ef",
                        "maskedAccountNumber": "643259****6589",
                        "feeReceivable": fee_receive_amount,
                        "feePayable": fee_payable_amount,
                    },
                    "upiFee": {
                    }}

                data["trans"]["settleAmount"] = settle_amount
                data["upiTrans"]["feePayable"] = fee_payable_amount
                data["upiTrans"]["feeReceivable"] = fee_receive_amount
                if trans_type in ["Chargeback", "Credit Adjustment"]:
                    net_settle_aount = fee_payable_amount - settle_amount - fee_receive_amount
                else:
                    net_settle_aount = fee_payable_amount + settle_amount - fee_receive_amount

                data["trans"]["netSettleAmount"] = net_settle_aount
                settle_data.append(data)
        return settle_data

    def upi_sumamry_fee_data(self, wopid, mopid, settle_date, settle_currency="CNY"):
        # 每日summary的 Fee的数据(transFile.upiFee )
        # 卡号为：即PAN 加密后的值为 6210948000000243
        fee_receivable_amount = 55.22
        fee_payable_amount = 66.11
        if settle_currency == "JPY":
            fee_receivable_amount = 55.0
            fee_payable_amount = 66.0
        trans_list = []
        for i in range(2):
            for trans_currency in ["JPY", "CNY"]:
                for trans_type in ["Fund Disbursement", "Fee Collection"]:
                    if trans_type == "Fund Disbursement":
                        currency_code = "156"
                    if trans_type == "Fee Collection":
                        currency_code = "392"

                    data = {
                        "wopID": wopid,
                        "mopID": mopid,
                        "settleDate": settle_date,
                        "trans": {
                            "transType": trans_type,
                            "mopID": mopid,
                            "transAmount": 333.0,  # 不要修改
                            "transCurrency": trans_currency,
                            "settleAmount": 444.0,  # 不要修改
                            "settleCurrency": settle_currency,
                            "interchangeFee": 0.0,
                            "transactionProcessingFee": 0.0,
                            "fxProcessingFee": 0.0,
                            "fxRebate": 0.0,
                            "netSettleAmount": 0.0
                        },
                        "upiTrans": {
                            "feeReceivable": fee_receivable_amount,
                            "feePayable": fee_payable_amount,
                        },
                        "upiFee": {
                            "transCode": "E20",
                            "settleAmount": "D000000320714",
                            "reasonCode": str(random.randint(10000000, 90000000)),
                            "sender1": str(random.randint(10000000, 90000000)),
                            "sender2": str(random.randint(10000000, 90000000)),
                            "receiver1": str(random.randint(10000000, 90000000)),
                            "receiver2": str(random.randint(10000000, 90000000)),
                            "transDatetime": str(random.randint(10000000, 90000000)),
                            "traceNumber": str(random.randint(10000000, 90000000)),
                            "pan": "6f7be1605f2c21815229d250c2738a3d10bebea1a93e5706371171bf2f0fbf36",
                            "settleCurrency": currency_code
                        }
                    }

                    if trans_type == "Fee Collection":
                        data["upiTrans"]["feeReceivable"] = 0.0
                    trans_list.append(data)
        return trans_list

    def upi_trans_list(self, wopid, mopid, sett_date, model):
        refund_orig_debit_evonet_order_nuber = str(random.randint(100000000000000000000, 900000000000000000000))
        account_refund_order_number = str(random.randint(100000000000000000000, 900000000000000000000))
        orig_mpm_evonet_number = str(random.randint(100000000000000000000, 900000000000000000000))
        credit_evonet_number = str(random.randint(100000000000000000000, 900000000000000000000))
        mpm_refund_evonet_number = str(random.randint(100000000000000000000, 900000000000000000000))
        account_debit_qrcvoucher = str(random.randint(100000000000000000000, 900000000000000000000))
        refund_qrcvoucher = str(random.randint(100000000000000000000, 900000000000000000000))
        credit_qrcvoucher = str(random.randint(100000000000000000000, 900000000000000000000))

        mpm_sett_data = self.upi_trans_data(wopid, mopid, sett_date, "MPM Payment", orig_mpm_evonet_number,
                                            account_debit_qrcvoucher,
                                            settle_mode=model
                                            )
        # CPM退款交易
        refund_mpm_sett_data = self.upi_trans_data(wopid, mopid, sett_date, "Refund", mpm_refund_evonet_number,
                                                   refund_qrcvoucher,
                                                   refund_orig_evonet_order_nuber=orig_mpm_evonet_number,
                                                   settle_mode=model)
        # ----------------------------------------

        # 卡交易数据
        account_debit_data = self.upi_trans_data(wopid, mopid, sett_date, "Account Debit",
                                                 refund_orig_debit_evonet_order_nuber, account_debit_qrcvoucher,
                                                 settle_mode=model
                                                 )
        account_credit_data = self.upi_trans_data(wopid, mopid, sett_date, "Account Credit", credit_evonet_number,
                                                  credit_qrcvoucher)

        # MPM退款交易
        account_refund_data = self.upi_trans_data(wopid, mopid, sett_date, "Refund", account_refund_order_number,
                                                  refund_qrcvoucher,
                                                  refund_orig_evonet_order_nuber=refund_orig_debit_evonet_order_nuber,
                                                  settle_mode=model)
        account_debit_data["category"] = "Card"
        account_credit_data["category"] = "Card"
        account_refund_data["category"] = "Card"
        sett_trans_list = [mpm_sett_data, refund_mpm_sett_data, account_debit_data,
                           account_credit_data, account_refund_data]

        # 返回订单号顺序Wie  cpm,mpm, 退款的cpm,退款交易的订单号
        order_number_list = [orig_mpm_evonet_number, mpm_refund_evonet_number, refund_orig_debit_evonet_order_nuber,
                             credit_evonet_number, account_refund_order_number]

        return (sett_trans_list, order_number_list)

    def wop_service_fee_report_data(self, wopid, mopid, trans_type, trans_currency, settle_currency, count,
                                    trans_amount,
                                    settle_amount, trans_fee_amount, fxfee_amount, interchangfee, trans_fee, fx_fee,
                                    fx_rebate,
                                    net_settleAmount, settle_data, trans_collect, trans_calculate, fx_collect,
                                    fx_calculate, fxrebate_collect, report_type):
        data = {
            "summary": {
                "brand": "MOP_SETTijhsnh",
                "transType": trans_type,
                "transCurrency": trans_currency,
                "settleCurrency": settle_currency,
                "counts": count,
                "transAmount": trans_amount,
                "settleAmount": settle_amount,
                "transProcessingFeeSettleAmount": trans_fee_amount,
                "fxProcessingFeeSettleAmount": fxfee_amount,
                "interchangeFee": interchangfee,
                "transProcessingFee": trans_fee,
                "fxProcessingFee": fx_fee,
                "fxRebate": fx_rebate,
                "netSettleAmount": net_settleAmount
            },
            "settleDate": settle_data,
            "wopID": wopid,
            "mopID": mopid,
            "serviceFeeFlag": {
                "processingCollectionMethod": trans_collect,
                "processingCalculatedMethod": trans_calculate,
                "fxProcessingCollectionMethod": fx_collect,
                "fxProcessingCalculatedMethod": fx_calculate,
                "fxRebateCollectionMethod": fxrebate_collect,
                "reportType": report_type
            }
        }

    def upi_fee_data(self, wopid, mopid, settle_date):
        # 卡号为：即PAN 加密后的值为 6210948000000243
        trans_list = []
        for trans_type in ["Fund Disbursement", "Fee Collection"]:
            if trans_type == "Fund Disbursement":
                currency_code = "156"
            if trans_type == "Fee Collection":
                currency_code = "392"

            data = {
                "wopID": wopid,
                "mopID": mopid,
                "settleDate": settle_date,
                "trans": {
                    "transType": trans_type,
                    "mopID": mopid,
                    "transAmount": float(random.randint(100, 400)),
                    "transCurrency": "JPY",
                    "settleAmount": float(random.randint(100, 400)),
                    "settleCurrency": "CNY",
                    "interchangeFee": 0.0,
                    "transactionProcessingFee": 0.0,
                    "fxProcessingFee": 0.0,
                    "fxRebate": 0.0,
                    "netSettleAmount": 0.0
                },
                "upiTrans": {
                    "feeReceivable": float(random.randint(100, 300)),
                    "feePayable": float(random.randint(100, 300))
                },
                "upiFee": {
                    "transCode": "E20",
                    "settleAmount": "D000000320714",
                    "reasonCode": str(random.randint(10000000, 90000000)),
                    "sender1": str(random.randint(10000000, 90000000)),
                    "sender2": str(random.randint(10000000, 90000000)),
                    "receiver1": str(random.randint(10000000, 90000000)),
                    "receiver2": str(random.randint(10000000, 90000000)),
                    "transDatetime": str(random.randint(10000000, 90000000)),
                    "traceNumber": str(random.randint(10000000, 90000000)),
                    "pan": "6f7be1605f2c21815229d250c2738a3d10bebea1a93e5706371171bf2f0fbf36",
                    "settleCurrency": currency_code
                }
            }
            trans_list.append(data)
        return trans_list

    def bilateral_trans_summary_data(self, node_type, wopid, mopid, settle_date,
                                     trans_fee_collection_method,
                                     fx_fee_collection_method,
                                     trans_fee_calcu_method, fx_fee_calcu_method):
        # 为生月报造transSumamry交易,应为直清模式，都是一对一的
        """
        :param node_type:  wop侧或者mop侧
        :param wopid:
        :param mopid:
        :param settle_date:
        :param trans_fee_collection_method:
        :param fx_fee_collection_method:
        :param trans_fee_calcu_method:
        :param fx_fee_calcu_method:
        :return:
        """
        settle_data = []
        trans_fee = 618.96
        fx_fee = 887.12
        for trans_type in ["Refund", "MPM Payment", "CPM Payment"]:
            for trans_currency in ["CNY", "JPY"]:
                data = {
                    "summary": {
                        "brand": wopid,
                        "transType": trans_type,
                        "transCurrency": trans_currency,
                        "settleCurrency": "CNY",
                        "counts": 8.0,
                        "transAmount": 18433.0,
                        "settleAmount": 10400.0,
                        "transProcessingFeeSettleAmount": 10422.0,  # 不要改
                        "fxProcessingFeeSettleAmount": 10433.0,  # 不要改
                        "interchangeFee": -866.16,
                        "transProcessingFee": trans_fee,
                        "fxProcessingFee": fx_fee,
                        "netSettleAmount": 11039.92
                    },
                    "settleDate": settle_date,
                    "wopID": wopid,
                    "mopID": mopid,
                    "serviceFeeFlag": {
                        "processingCollectionMethod": trans_fee_collection_method,
                        "processingCalculatedMethod": trans_fee_calcu_method,
                        "fxProcessingCollectionMethod": fx_fee_collection_method,
                        "fxProcessingCalculatedMethod": fx_fee_calcu_method,
                        "reportType": "monthly"
                    }
                }
                if trans_type == "Refund":
                    data["summary"]["transProcessingFee"] = 0.0
                    data["summary"]["fxProcessingFee"] = 0.0
                    data["summary"]["transProcessingFeeSettleAmount"] = 0.0
                    data["summary"]["fxProcessingFeeSettleAmount"] = 0.0

                if node_type == "mop":
                    data["summary"]["transProcessingFee"] = trans_fee * -1
                    data["summary"]["fxProcessingFee"] = fx_fee * -1
                settle_data.append(data)
        return settle_data

    def evont_wop_trans_summary_data(self, wopid, mopid1, mopid2, settle_date,
                                     trans_fee_collection_method,
                                     fx_fee_collection_method,
                                     fxrebate_fee_collection_method,
                                     trans_fee_calcu_method, fx_fee_calcu_method):
        # 为生月报造transSumamry交易
        settle_data = []
        fxrebate = -366.64
        for mopid in [mopid1, mopid2]:
            for trans_type in ["Refund", "MPM Payment", "CPM Payment"]:
                for trans_currency in ["CNY", "JPY"]:
                    data = {
                        "summary": {
                            "brand": mopid,
                            "transType": trans_type,
                            "transCurrency": trans_currency,
                            "settleCurrency": "CNY",
                            "counts": 8.0,
                            "transAmount": 18433.0,
                            "settleAmount": 10400.0,
                            "transProcessingFeeSettleAmount": 10422.0,  # 不要改
                            "fxProcessingFeeSettleAmount": 10433.0,  # 不要改
                            "interchangeFee": -866.16,
                            "transProcessingFee": 618.96,
                            "fxProcessingFee": 887.12,
                            "fxRebate": fxrebate,
                            "netSettleAmount": 11039.92
                        },
                        "settleDate": settle_date,
                        "wopID": wopid,
                        "mopID": mopid,
                        "serviceFeeFlag": {
                            "processingCollectionMethod": trans_fee_collection_method,
                            "processingCalculatedMethod": trans_fee_calcu_method,
                            "fxProcessingCollectionMethod": fx_fee_collection_method,
                            "fxProcessingCalculatedMethod": fx_fee_calcu_method,
                            "fxRebateCollectionMethod": fxrebate_fee_collection_method,
                            "reportType": "monthly"
                        }
                    }
                    if trans_type == "Refund":
                        data["summary"]["transProcessingFee"] = 0.0
                        data["summary"]["fxProcessingFee"] = 0.0
                        data["summary"]["transProcessingFeeSettleAmount"] = 0.0
                        data["summary"]["fxProcessingFeeSettleAmount"] = 0.0
                        data["summary"]["fxRebate"] = abs(fxrebate) / 2
                    settle_data.append(data)
        return settle_data

    def evont_mop_trans_summary_data(self, mopid, wopid1, wopid2, settle_date,
                                     trans_fee_collection_method,
                                     fx_fee_collection_method,
                                     trans_fee_calcu_method, fx_fee_calcu_method):
        # 为生月报造transSumamry交易
        settle_data = []
        for wopid in [wopid1, wopid2]:
            for trans_type in ["Refund", "MPM Payment", "CPM Payment"]:
                for trans_currency in ["CNY", "JPY"]:
                    data = {
                        "summary": {
                            "brand": wopid,
                            "transType": trans_type,
                            "transCurrency": trans_currency,
                            "settleCurrency": "CNY",
                            "counts": 8.0,
                            "transAmount": 18433.0,
                            "settleAmount": 10400.0,
                            "transProcessingFeeSettleAmount": 10422.0,  # 不要改
                            "fxProcessingFeeSettleAmount": 10433.0,  # 不要改
                            "interchangeFee": -866.16,
                            "transProcessingFee": -618.96,
                            "fxProcessingFee": -887.12,
                            "netSettleAmount": 11039.92
                        },
                        "settleDate": settle_date,
                        "wopID": wopid,
                        "mopID": mopid,
                        "serviceFeeFlag": {
                            "processingCollectionMethod": trans_fee_collection_method,
                            "processingCalculatedMethod": trans_fee_calcu_method,
                            "fxProcessingCollectionMethod": fx_fee_collection_method,
                            "fxProcessingCalculatedMethod": fx_fee_calcu_method,
                            "reportType": "monthly"
                        }
                    }
                    if trans_type == "Refund":
                        data["summary"]["transProcessingFee"] = 0.0
                        data["summary"]["fxProcessingFee"] = 0.0
                        data["summary"]["transProcessingFeeSettleAmount"] = 0.0
                        data["summary"]["fxProcessingFeeSettleAmount"] = 0.0
                    settle_data.append(data)
        return settle_data

    def wop_sftp_data(self, host, name, wopid, key):
        # wop系统文件的key
        return {
            "ownerID": wopid,
            "ownerType": "wop",
            "host": host,
            "port": 22,
            "username": name,
            "rootPath": "/home/webapp/test/" + wopid + "/",
            "privateKeyC": key,
        }
