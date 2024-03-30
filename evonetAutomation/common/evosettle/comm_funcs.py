from decimal import Decimal


class CommFuncs(object):

    def amount_conver(self, amount):
        """
        将包含千位符的字符串格式金额进行装换为 正常float的数字
        :param amount: 包含千位符的字符串数字
        :return:
        """
        if type(amount) == float:
            amount = str(amount)
        return float("".join(amount.split(",")))

    def back_value(self, field, filed_name, dest_value):
        if filed_name in dest_value:
            if len(dest_value) != 0:
                field = '"' + dest_value + '"'
            else:
                field = ""
        else:
            field = ""
        return field


class CommonName(object):

    # 返回function的name
    def __init__(self):
        self.base_task = "baseTask"
        self.settle_task = "settleTask"
        self.mdaq_resolve = "MDaqResolve"
        self.mdaq_recon = "MDaqRecon"
    fx_rate="fx_rate"
    mdaq_recon_file_title = "TraceID,BATCH_ID,ADVICE_TYPE,ADVICE_ID,TRANSACTION_ID,RELATED_ADVICE_ID,ACCOUNT_NAME,CCY_PAIR,SIDE,TRANSACTION_CURRENCY,CONSUMER_CURRENCY,TRANSACTION_CURRENCY_TYPE,AMOUNT,TRANSACTION_TYPE,SCENARIO,SETTLEMENT_AMOUNT,SETTLEMENT_CURRENCY,PAYMENT_PROVIDER,TRANSACTION_TIMESTAMP,REQUESTED_PRICING_REF_ID,BENEFICIARY,BENEFICIARY_ALIAS,CLIENT_REF,STATUS,ACTUAL_PRICING_REF_ID,PRICE,CONTRA_AMOUNT,VALUE_DATE,M_VALUE_DATE,mdaq_rate,MDAQ_PRICE,CONTRA_AMOUNT_MRATE,PROFIT_CCY,PROFIT_AMOUNT,ORIGINAL_PROFIT_AMOUNT,PROFIT_VALUE_DATE,FIXING_ADJUSTMENT,FXG_ADJ_CLIENT_PROFIT,ORIGINAL_BATCH_ID,ERROR_CODE,ERROR_REASON,PROCESS_TIMESTAMP,RECEIVE_TIMESTAMP,VALID_TIMESTAMP,DERIVED_TRANSACTION_TYPE,SERVICE_FEE,evonet_order_number,orig_evonet_order_number,settle_date,expect_value_date,recon_flag,advice_time,create_time"
    mdap_file_title = 'BATCH_ID,ADVICE_TYPE,ADVICE_ID,TRANSACTION_ID,ACCOUNT_NAME,CCY_PAIR,RELATED_ADVICE_ID,SIDE,TRANSACTION_CURRENCY,CONSUMER_CURRENCY,TRANSACTION_CURRENCY_TYPE,AMOUNT,TRANSACTION_TYPE,SCENARIO,SETTLEMENT_AMOUNT,SETTLEMENT_CURRENCY,PAYMENT_PROVIDER,TRANSACTION_TIMESTAMP,REQUESTED_PRICING_REF_ID,CLIENT_REF,ACTUAL_PRICING_REF_ID,PRICE,CONTRA_AMOUNT,VALUE_DATE,MDAQ_PRICE,CONTRA_AMOUNT_MRATE,PROFIT_CCY,PROFIT_AMOUNT,FIXING_ADJUSTMENT,STATUS,ERROR_CODE,ERROR_REASON,PROCESS_TIMESTAMP,RECEIVE_TIMESTAMP,PROFIT_VALUE_DATE,M_VALUE_DATE,VALID_TIMESTAMP,ORIGINAL_PROFIT_AMOUNT,BENEFICIARY_ALIAS,DERIVED_TRANSACTION_TYPE,SERVICE_FEE\n'
    evonet_wop_daily_daily_monthly_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                    'Transaction Amount', 'Transaction Processing Fee',
                                                    'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                    'CPM Payment', 'CNY', '248', '571,423.00', '-', '-', '-11,365.84',
                                                    '-11,365.84', 'MPM Payment', 'CNY', '248', '571,423.00', '-', '-',
                                                    '-11,365.84', '-11,365.84', 'Refund', 'CNY', '248', '571,423.00',
                                                    '-', '-', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                    '1,714,269.00', '-', '-', '-17,048.76', '-17,048.76', 'CPM Payment',
                                                    'JPY', '248', '571,423', '-', '-', '-11,365.84', '-11,365.84',
                                                    'MPM Payment', 'JPY', '248', '571,423', '-', '-', '-11,365.84',
                                                    '-11,365.84', 'Refund', 'JPY', '248', '571,423', '-', '-',
                                                    '5,682.92', '5,682.92', 'Sub-Total', '', '744', '1,714,269', '-',
                                                    '-', '-17,048.76', '-17,048.76', 'CPM Payment', 'CNY', '248',
                                                    '571,423.00', '-', '-', '-11,365.84', '-11,365.84', 'MPM Payment',
                                                    'CNY', '248', '571,423.00', '-', '-', '-11,365.84', '-11,365.84',
                                                    'Refund', 'CNY', '248', '571,423.00', '-', '-', '5,682.92',
                                                    '5,682.92', 'Sub-Total', '', '744', '1,714,269.00', '-', '-',
                                                    '-17,048.76', '-17,048.76', 'CPM Payment', 'JPY', '248', '571,423',
                                                    '-', '-', '-11,365.84', '-11,365.84', 'MPM Payment', 'JPY', '248',
                                                    '571,423', '-', '-', '-11,365.84', '-11,365.84', 'Refund', 'JPY',
                                                    '248', '571,423', '-', '-', '5,682.92', '5,682.92', 'Sub-Total', '',
                                                    '744', '1,714,269', '-', '-', '-17,048.76', '-17,048.76', '', '',
                                                    '2976', '', '-', '-', '-68,195.04', '-68,195.04']
    evonet_wop_daily_monthly_daily_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                    'Transaction Amount', 'Transaction Processing Fee',
                                                    'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                    'CPM Payment', 'CNY', '248', '571,423.00', '-', '27,500.72', '-',
                                                    '27,500.72', 'MPM Payment', 'CNY', '248', '571,423.00', '-',
                                                    '27,500.72', '-', '27,500.72', 'Refund', 'CNY', '248', '571,423.00',
                                                    '-', '0.00', '-', '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                    '-', '55,001.44', '-', '55,001.44', 'CPM Payment', 'JPY', '248',
                                                    '571,423', '-', '27,500.72', '-', '27,500.72', 'MPM Payment', 'JPY',
                                                    '248', '571,423', '-', '27,500.72', '-', '27,500.72', 'Refund',
                                                    'JPY', '248', '571,423', '-', '0.00', '-', '0.00', 'Sub-Total', '',
                                                    '744', '1,714,269', '-', '55,001.44', '-', '55,001.44',
                                                    'CPM Payment', 'CNY', '248', '571,423.00', '-', '27,500.72', '-',
                                                    '27,500.72', 'MPM Payment', 'CNY', '248', '571,423.00', '-',
                                                    '27,500.72', '-', '27,500.72', 'Refund', 'CNY', '248', '571,423.00',
                                                    '-', '0.00', '-', '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                    '-', '55,001.44', '-', '55,001.44', 'CPM Payment', 'JPY', '248',
                                                    '571,423', '-', '27,500.72', '-', '27,500.72', 'MPM Payment', 'JPY',
                                                    '248', '571,423', '-', '27,500.72', '-', '27,500.72', 'Refund',
                                                    'JPY', '248', '571,423', '-', '0.00', '-', '0.00', 'Sub-Total', '',
                                                    '744', '1,714,269', '-', '55,001.44', '-', '55,001.44', '', '',
                                                    '2976', '', '-', '220,005.76', '-', '220,005.76']
    evonet_wop_daily_monthly_daily_single_accumulation = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                          'Transaction Amount', 'Transaction Processing Fee',
                                                          'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                          'CPM Payment', 'CNY', '248', '571,423.00', '-', '23,059.19',
                                                          '-', '23,059.19', 'MPM Payment', 'CNY', '248', '571,423.00',
                                                          '-', '23,059.19', '-', '23,059.19', 'Refund', 'CNY', '248',
                                                          '571,423.00', '-', '0.00', '-', '0.00', 'Sub-Total', '',
                                                          '744', '1,714,269.00', '-', '46,118.38', '-', '46,118.38',
                                                          'CPM Payment', 'JPY', '248', '571,423', '-', '23,059.19', '-',
                                                          '23,059.19', 'MPM Payment', 'JPY', '248', '571,423', '-',
                                                          '23,059.19', '-', '23,059.19', 'Refund', 'JPY', '248',
                                                          '571,423', '-', '0.00', '-', '0.00', 'Sub-Total', '', '744',
                                                          '1,714,269', '-', '46,118.38', '-', '46,118.38',
                                                          'CPM Payment', 'CNY', '248', '571,423.00', '-', '23,059.19',
                                                          '-', '23,059.19', 'MPM Payment', 'CNY', '248', '571,423.00',
                                                          '-', '23,059.19', '-', '23,059.19', 'Refund', 'CNY', '248',
                                                          '571,423.00', '-', '0.00', '-', '0.00', 'Sub-Total', '',
                                                          '744', '1,714,269.00', '-', '46,118.38', '-', '46,118.38',
                                                          'CPM Payment', 'JPY', '248', '571,423', '-', '23,059.19', '-',
                                                          '23,059.19', 'MPM Payment', 'JPY', '248', '571,423', '-',
                                                          '23,059.19', '-', '23,059.19', 'Refund', 'JPY', '248',
                                                          '571,423', '-', '0.00', '-', '0.00', 'Sub-Total', '', '744',
                                                          '1,714,269', '-', '46,118.38', '-', '46,118.38', '', '',
                                                          '2976', '', '-', '184,473.52', '-', '184,473.52']
    evonet_wop_daily_monthly_monthly_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                      'Transaction Amount', 'Transaction Processing Fee',
                                                      'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                      'CPM Payment', 'CNY', '248', '571,423.00', '-', '27,500.72',
                                                      '-11,365.84', '16,134.88', 'MPM Payment', 'CNY', '248',
                                                      '571,423.00', '-', '27,500.72', '-11,365.84', '16,134.88',
                                                      'Refund', 'CNY', '248', '571,423.00', '-', '0.00', '5,682.92',
                                                      '5,682.92', 'Sub-Total', '', '744', '1,714,269.00', '-',
                                                      '55,001.44', '-17,048.76', '37,952.68', 'CPM Payment', 'JPY',
                                                      '248', '571,423', '-', '27,500.72', '-11,365.84', '16,134.88',
                                                      'MPM Payment', 'JPY', '248', '571,423', '-', '27,500.72',
                                                      '-11,365.84', '16,134.88', 'Refund', 'JPY', '248', '571,423', '-',
                                                      '0.00', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                      '1,714,269', '-', '55,001.44', '-17,048.76', '37,952.68',
                                                      'CPM Payment', 'CNY', '248', '571,423.00', '-', '27,500.72',
                                                      '-11,365.84', '16,134.88', 'MPM Payment', 'CNY', '248',
                                                      '571,423.00', '-', '27,500.72', '-11,365.84', '16,134.88',
                                                      'Refund', 'CNY', '248', '571,423.00', '-', '0.00', '5,682.92',
                                                      '5,682.92', 'Sub-Total', '', '744', '1,714,269.00', '-',
                                                      '55,001.44', '-17,048.76', '37,952.68', 'CPM Payment', 'JPY',
                                                      '248', '571,423', '-', '27,500.72', '-11,365.84', '16,134.88',
                                                      'MPM Payment', 'JPY', '248', '571,423', '-', '27,500.72',
                                                      '-11,365.84', '16,134.88', 'Refund', 'JPY', '248', '571,423', '-',
                                                      '0.00', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                      '1,714,269', '-', '55,001.44', '-17,048.76', '37,952.68', '', '',
                                                      '2976', '', '-', '220,005.76', '-68,195.04', '151,810.72']
    evonet_wop_daily_monthly_monthly_single_accumulation = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                            'Transaction Amount', 'Transaction Processing Fee',
                                                            'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                            'CPM Payment', 'CNY', '248', '571,423.00', '-', '23,059.19',
                                                            '-11,365.84', '11,693.35', 'MPM Payment', 'CNY', '248',
                                                            '571,423.00', '-', '23,059.19', '-11,365.84', '11,693.35',
                                                            'Refund', 'CNY', '248', '571,423.00', '-', '0.00',
                                                            '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                            '1,714,269.00', '-', '46,118.38', '-17,048.76', '29,069.62',
                                                            'CPM Payment', 'JPY', '248', '571,423', '-', '23,059.19',
                                                            '-11,365.84', '11,693.35', 'MPM Payment', 'JPY', '248',
                                                            '571,423', '-', '23,059.19', '-11,365.84', '11,693.35',
                                                            'Refund', 'JPY', '248', '571,423', '-', '0.00', '5,682.92',
                                                            '5,682.92', 'Sub-Total', '', '744', '1,714,269', '-',
                                                            '46,118.38', '-17,048.76', '29,069.62', 'CPM Payment',
                                                            'CNY', '248', '571,423.00', '-', '23,059.19', '-11,365.84',
                                                            '11,693.35', 'MPM Payment', 'CNY', '248', '571,423.00', '-',
                                                            '23,059.19', '-11,365.84', '11,693.35', 'Refund', 'CNY',
                                                            '248', '571,423.00', '-', '0.00', '5,682.92', '5,682.92',
                                                            'Sub-Total', '', '744', '1,714,269.00', '-', '46,118.38',
                                                            '-17,048.76', '29,069.62', 'CPM Payment', 'JPY', '248',
                                                            '571,423', '-', '23,059.19', '-11,365.84', '11,693.35',
                                                            'MPM Payment', 'JPY', '248', '571,423', '-', '23,059.19',
                                                            '-11,365.84', '11,693.35', 'Refund', 'JPY', '248',
                                                            '571,423', '-', '0.00', '5,682.92', '5,682.92', 'Sub-Total',
                                                            '', '744', '1,714,269', '-', '46,118.38', '-17,048.76',
                                                            '29,069.62', '', '', '2976', '', '-', '184,473.52',
                                                            '-68,195.04', '116,278.48']
    evonet_wop_monthly_daily_daily_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                    'Transaction Amount', 'Transaction Processing Fee',
                                                    'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                    'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76', '-', '-',
                                                    '19,187.76', 'MPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                    '-', '-', '19,187.76', 'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                    '-', '-', '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                    '38,375.52', '-', '-', '38,375.52', 'CPM Payment', 'JPY', '248',
                                                    '571,423', '19,187.76', '-', '-', '19,187.76', 'MPM Payment', 'JPY',
                                                    '248', '571,423', '19,187.76', '-', '-', '19,187.76', 'Refund',
                                                    'JPY', '248', '571,423', '0.00', '-', '-', '0.00', 'Sub-Total', '',
                                                    '744', '1,714,269', '38,375.52', '-', '-', '38,375.52',
                                                    'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76', '-', '-',
                                                    '19,187.76', 'MPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                    '-', '-', '19,187.76', 'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                    '-', '-', '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                    '38,375.52', '-', '-', '38,375.52', 'CPM Payment', 'JPY', '248',
                                                    '571,423', '19,187.76', '-', '-', '19,187.76', 'MPM Payment', 'JPY',
                                                    '248', '571,423', '19,187.76', '-', '-', '19,187.76', 'Refund',
                                                    'JPY', '248', '571,423', '0.00', '-', '-', '0.00', 'Sub-Total', '',
                                                    '744', '1,714,269', '38,375.52', '-', '-', '38,375.52', '', '',
                                                    '2976', '', '153,502.08', '-', '-', '153,502.08']
    evonet_wop_monthly_daily_daily_accumulation_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                          'Transaction Amount', 'Transaction Processing Fee',
                                                          'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                          'CPM Payment', 'CNY', '248', '571,423.00', '18,905.89', '-',
                                                          '-', '18,905.89', 'MPM Payment', 'CNY', '248', '571,423.00',
                                                          '18,905.89', '-', '-', '18,905.89', 'Refund', 'CNY', '248',
                                                          '571,423.00', '0.00', '-', '-', '0.00', 'Sub-Total', '',
                                                          '744', '1,714,269.00', '37,811.78', '-', '-', '37,811.78',
                                                          'CPM Payment', 'JPY', '248', '571,423', '18,905.89', '-', '-',
                                                          '18,905.89', 'MPM Payment', 'JPY', '248', '571,423',
                                                          '18,905.89', '-', '-', '18,905.89', 'Refund', 'JPY', '248',
                                                          '571,423', '0.00', '-', '-', '0.00', 'Sub-Total', '', '744',
                                                          '1,714,269', '37,811.78', '-', '-', '37,811.78',
                                                          'CPM Payment', 'CNY', '248', '571,423.00', '18,905.89', '-',
                                                          '-', '18,905.89', 'MPM Payment', 'CNY', '248', '571,423.00',
                                                          '18,905.89', '-', '-', '18,905.89', 'Refund', 'CNY', '248',
                                                          '571,423.00', '0.00', '-', '-', '0.00', 'Sub-Total', '',
                                                          '744', '1,714,269.00', '37,811.78', '-', '-', '37,811.78',
                                                          'CPM Payment', 'JPY', '248', '571,423', '18,905.89', '-', '-',
                                                          '18,905.89', 'MPM Payment', 'JPY', '248', '571,423',
                                                          '18,905.89', '-', '-', '18,905.89', 'Refund', 'JPY', '248',
                                                          '571,423', '0.00', '-', '-', '0.00', 'Sub-Total', '', '744',
                                                          '1,714,269', '37,811.78', '-', '-', '37,811.78', '', '',
                                                          '2976', '', '151,247.12', '-', '-', '151,247.12']
    evonet_wop_monthly_daily_monthly_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                      'Transaction Amount', 'Transaction Processing Fee',
                                                      'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                      'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76', '-',
                                                      '-11,365.84', '7,821.92', 'MPM Payment', 'CNY', '248',
                                                      '571,423.00', '19,187.76', '-', '-11,365.84', '7,821.92',
                                                      'Refund', 'CNY', '248', '571,423.00', '0.00', '-', '5,682.92',
                                                      '5,682.92', 'Sub-Total', '', '744', '1,714,269.00', '38,375.52',
                                                      '-', '-17,048.76', '21,326.76', 'CPM Payment', 'JPY', '248',
                                                      '571,423', '19,187.76', '-', '-11,365.84', '7,821.92',
                                                      'MPM Payment', 'JPY', '248', '571,423', '19,187.76', '-',
                                                      '-11,365.84', '7,821.92', 'Refund', 'JPY', '248', '571,423',
                                                      '0.00', '-', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                      '1,714,269', '38,375.52', '-', '-17,048.76', '21,326.76',
                                                      'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76', '-',
                                                      '-11,365.84', '7,821.92', 'MPM Payment', 'CNY', '248',
                                                      '571,423.00', '19,187.76', '-', '-11,365.84', '7,821.92',
                                                      'Refund', 'CNY', '248', '571,423.00', '0.00', '-', '5,682.92',
                                                      '5,682.92', 'Sub-Total', '', '744', '1,714,269.00', '38,375.52',
                                                      '-', '-17,048.76', '21,326.76', 'CPM Payment', 'JPY', '248',
                                                      '571,423', '19,187.76', '-', '-11,365.84', '7,821.92',
                                                      'MPM Payment', 'JPY', '248', '571,423', '19,187.76', '-',
                                                      '-11,365.84', '7,821.92', 'Refund', 'JPY', '248', '571,423',
                                                      '0.00', '-', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                      '1,714,269', '38,375.52', '-', '-17,048.76', '21,326.76', '', '',
                                                      '2976', '', '153,502.08', '-', '-68,195.04', '85,307.04']
    evonet_wop_monthly_daily_monthly_accumulation_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                            'Transaction Amount', 'Transaction Processing Fee',
                                                            'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                            'CPM Payment', 'CNY', '248', '571,423.00', '18,905.89', '-',
                                                            '-11,365.84', '7,540.05', 'MPM Payment', 'CNY', '248',
                                                            '571,423.00', '18,905.89', '-', '-11,365.84', '7,540.05',
                                                            'Refund', 'CNY', '248', '571,423.00', '0.00', '-',
                                                            '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                            '1,714,269.00', '37,811.78', '-', '-17,048.76', '20,763.02',
                                                            'CPM Payment', 'JPY', '248', '571,423', '18,905.89', '-',
                                                            '-11,365.84', '7,540.05', 'MPM Payment', 'JPY', '248',
                                                            '571,423', '18,905.89', '-', '-11,365.84', '7,540.05',
                                                            'Refund', 'JPY', '248', '571,423', '0.00', '-', '5,682.92',
                                                            '5,682.92', 'Sub-Total', '', '744', '1,714,269',
                                                            '37,811.78', '-', '-17,048.76', '20,763.02', 'CPM Payment',
                                                            'CNY', '248', '571,423.00', '18,905.89', '-', '-11,365.84',
                                                            '7,540.05', 'MPM Payment', 'CNY', '248', '571,423.00',
                                                            '18,905.89', '-', '-11,365.84', '7,540.05', 'Refund', 'CNY',
                                                            '248', '571,423.00', '0.00', '-', '5,682.92', '5,682.92',
                                                            'Sub-Total', '', '744', '1,714,269.00', '37,811.78', '-',
                                                            '-17,048.76', '20,763.02', 'CPM Payment', 'JPY', '248',
                                                            '571,423', '18,905.89', '-', '-11,365.84', '7,540.05',
                                                            'MPM Payment', 'JPY', '248', '571,423', '18,905.89', '-',
                                                            '-11,365.84', '7,540.05', 'Refund', 'JPY', '248', '571,423',
                                                            '0.00', '-', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                            '1,714,269', '37,811.78', '-', '-17,048.76', '20,763.02',
                                                            '', '', '2976', '', '151,247.12', '-', '-68,195.04',
                                                            '83,052.08']
    evonet_wop_monthly_monthly_daily_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                      'Transaction Amount', 'Transaction Processing Fee',
                                                      'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                      'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                      '27,500.72', '-', '46,688.48', 'MPM Payment', 'CNY', '248',
                                                      '571,423.00', '19,187.76', '27,500.72', '-', '46,688.48',
                                                      'Refund', 'CNY', '248', '571,423.00', '0.00', '0.00', '-', '0.00',
                                                      'Sub-Total', '', '744', '1,714,269.00', '38,375.52', '55,001.44',
                                                      '-', '93,376.96', 'CPM Payment', 'JPY', '248', '571,423',
                                                      '19,187.76', '27,500.72', '-', '46,688.48', 'MPM Payment', 'JPY',
                                                      '248', '571,423', '19,187.76', '27,500.72', '-', '46,688.48',
                                                      'Refund', 'JPY', '248', '571,423', '0.00', '0.00', '-', '0.00',
                                                      'Sub-Total', '', '744', '1,714,269', '38,375.52', '55,001.44',
                                                      '-', '93,376.96', 'CPM Payment', 'CNY', '248', '571,423.00',
                                                      '19,187.76', '27,500.72', '-', '46,688.48', 'MPM Payment', 'CNY',
                                                      '248', '571,423.00', '19,187.76', '27,500.72', '-', '46,688.48',
                                                      'Refund', 'CNY', '248', '571,423.00', '0.00', '0.00', '-', '0.00',
                                                      'Sub-Total', '', '744', '1,714,269.00', '38,375.52', '55,001.44',
                                                      '-', '93,376.96', 'CPM Payment', 'JPY', '248', '571,423',
                                                      '19,187.76', '27,500.72', '-', '46,688.48', 'MPM Payment', 'JPY',
                                                      '248', '571,423', '19,187.76', '27,500.72', '-', '46,688.48',
                                                      'Refund', 'JPY', '248', '571,423', '0.00', '0.00', '-', '0.00',
                                                      'Sub-Total', '', '744', '1,714,269', '38,375.52', '55,001.44',
                                                      '-', '93,376.96', '', '', '2976', '', '153,502.08', '220,005.76',
                                                      '-', '373,507.84']
    evonet_wop_monthly_monthly_daily_single_accumulation = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                            'Transaction Amount', 'Transaction Processing Fee',
                                                            'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                            'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                            '23,059.19', '-', '42,246.95', 'MPM Payment', 'CNY', '248',
                                                            '571,423.00', '19,187.76', '23,059.19', '-', '42,246.95',
                                                            'Refund', 'CNY', '248', '571,423.00', '0.00', '0.00', '-',
                                                            '0.00', 'Sub-Total', '', '744', '1,714,269.00', '38,375.52',
                                                            '46,118.38', '-', '84,493.90', 'CPM Payment', 'JPY', '248',
                                                            '571,423', '19,187.76', '23,059.19', '-', '42,246.95',
                                                            'MPM Payment', 'JPY', '248', '571,423', '19,187.76',
                                                            '23,059.19', '-', '42,246.95', 'Refund', 'JPY', '248',
                                                            '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total', '',
                                                            '744', '1,714,269', '38,375.52', '46,118.38', '-',
                                                            '84,493.90', 'CPM Payment', 'CNY', '248', '571,423.00',
                                                            '19,187.76', '23,059.19', '-', '42,246.95', 'MPM Payment',
                                                            'CNY', '248', '571,423.00', '19,187.76', '23,059.19', '-',
                                                            '42,246.95', 'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                            '0.00', '-', '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                            '38,375.52', '46,118.38', '-', '84,493.90', 'CPM Payment',
                                                            'JPY', '248', '571,423', '19,187.76', '23,059.19', '-',
                                                            '42,246.95', 'MPM Payment', 'JPY', '248', '571,423',
                                                            '19,187.76', '23,059.19', '-', '42,246.95', 'Refund', 'JPY',
                                                            '248', '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total',
                                                            '', '744', '1,714,269', '38,375.52', '46,118.38', '-',
                                                            '84,493.90', '', '', '2976', '', '153,502.08', '184,473.52',
                                                            '-', '337,975.60']
    evonet_wop_monthly_monthly_daily_accumulation_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                            'Transaction Amount', 'Transaction Processing Fee',
                                                            'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                            'CPM Payment', 'CNY', '248', '571,423.00', '18,905.89',
                                                            '27,500.72', '-', '46,406.61', 'MPM Payment', 'CNY', '248',
                                                            '571,423.00', '18,905.89', '27,500.72', '-', '46,406.61',
                                                            'Refund', 'CNY', '248', '571,423.00', '0.00', '0.00', '-',
                                                            '0.00', 'Sub-Total', '', '744', '1,714,269.00', '37,811.78',
                                                            '55,001.44', '-', '92,813.22', 'CPM Payment', 'JPY', '248',
                                                            '571,423', '18,905.89', '27,500.72', '-', '46,406.61',
                                                            'MPM Payment', 'JPY', '248', '571,423', '18,905.89',
                                                            '27,500.72', '-', '46,406.61', 'Refund', 'JPY', '248',
                                                            '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total', '',
                                                            '744', '1,714,269', '37,811.78', '55,001.44', '-',
                                                            '92,813.22', 'CPM Payment', 'CNY', '248', '571,423.00',
                                                            '18,905.89', '27,500.72', '-', '46,406.61', 'MPM Payment',
                                                            'CNY', '248', '571,423.00', '18,905.89', '27,500.72', '-',
                                                            '46,406.61', 'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                            '0.00', '-', '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                            '37,811.78', '55,001.44', '-', '92,813.22', 'CPM Payment',
                                                            'JPY', '248', '571,423', '18,905.89', '27,500.72', '-',
                                                            '46,406.61', 'MPM Payment', 'JPY', '248', '571,423',
                                                            '18,905.89', '27,500.72', '-', '46,406.61', 'Refund', 'JPY',
                                                            '248', '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total',
                                                            '', '744', '1,714,269', '37,811.78', '55,001.44', '-',
                                                            '92,813.22', '', '', '2976', '', '151,247.12', '220,005.76',
                                                            '-', '371,252.88']
    evonet_wop_monthly_monthly_daily_accumulation_accumulation = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                                  'Transaction Amount', 'Transaction Processing Fee',
                                                                  'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                                  'CPM Payment', 'CNY', '248', '571,423.00',
                                                                  '18,905.89', '23,059.19', '-', '41,965.08',
                                                                  'MPM Payment', 'CNY', '248', '571,423.00',
                                                                  '18,905.89', '23,059.19', '-', '41,965.08', 'Refund',
                                                                  'CNY', '248', '571,423.00', '0.00', '0.00', '-',
                                                                  '0.00', 'Sub-Total', '', '744', '1,714,269.00',
                                                                  '37,811.78', '46,118.38', '-', '83,930.16',
                                                                  'CPM Payment', 'JPY', '248', '571,423', '18,905.89',
                                                                  '23,059.19', '-', '41,965.08', 'MPM Payment', 'JPY',
                                                                  '248', '571,423', '18,905.89', '23,059.19', '-',
                                                                  '41,965.08', 'Refund', 'JPY', '248', '571,423',
                                                                  '0.00', '0.00', '-', '0.00', 'Sub-Total', '', '744',
                                                                  '1,714,269', '37,811.78', '46,118.38', '-',
                                                                  '83,930.16', 'CPM Payment', 'CNY', '248',
                                                                  '571,423.00', '18,905.89', '23,059.19', '-',
                                                                  '41,965.08', 'MPM Payment', 'CNY', '248',
                                                                  '571,423.00', '18,905.89', '23,059.19', '-',
                                                                  '41,965.08', 'Refund', 'CNY', '248', '571,423.00',
                                                                  '0.00', '0.00', '-', '0.00', 'Sub-Total', '', '744',
                                                                  '1,714,269.00', '37,811.78', '46,118.38', '-',
                                                                  '83,930.16', 'CPM Payment', 'JPY', '248', '571,423',
                                                                  '18,905.89', '23,059.19', '-', '41,965.08',
                                                                  'MPM Payment', 'JPY', '248', '571,423', '18,905.89',
                                                                  '23,059.19', '-', '41,965.08', 'Refund', 'JPY', '248',
                                                                  '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total',
                                                                  '', '744', '1,714,269', '37,811.78', '46,118.38', '-',
                                                                  '83,930.16', '', '', '2976', '', '151,247.12',
                                                                  '184,473.52', '-', '335,720.64']

    evonet_wop_monthly_monthly_monthly_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                        'Transaction Amount', 'Transaction Processing Fee',
                                                        'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                        'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                        '27,500.72', '-11,365.84', '35,322.64', 'MPM Payment', 'CNY',
                                                        '248', '571,423.00', '19,187.76', '27,500.72', '-11,365.84',
                                                        '35,322.64', 'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                        '0.00', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                        '1,714,269.00', '38,375.52', '55,001.44', '-17,048.76',
                                                        '76,328.20', 'CPM Payment', 'JPY', '248', '571,423',
                                                        '19,187.76', '27,500.72', '-11,365.84', '35,322.64',
                                                        'MPM Payment', 'JPY', '248', '571,423', '19,187.76',
                                                        '27,500.72', '-11,365.84', '35,322.64', 'Refund', 'JPY', '248',
                                                        '571,423', '0.00', '0.00', '5,682.92', '5,682.92', 'Sub-Total',
                                                        '', '744', '1,714,269', '38,375.52', '55,001.44', '-17,048.76',
                                                        '76,328.20', 'CPM Payment', 'CNY', '248', '571,423.00',
                                                        '19,187.76', '27,500.72', '-11,365.84', '35,322.64',
                                                        'MPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                        '27,500.72', '-11,365.84', '35,322.64', 'Refund', 'CNY', '248',
                                                        '571,423.00', '0.00', '0.00', '5,682.92', '5,682.92',
                                                        'Sub-Total', '', '744', '1,714,269.00', '38,375.52',
                                                        '55,001.44', '-17,048.76', '76,328.20', 'CPM Payment', 'JPY',
                                                        '248', '571,423', '19,187.76', '27,500.72', '-11,365.84',
                                                        '35,322.64', 'MPM Payment', 'JPY', '248', '571,423',
                                                        '19,187.76', '27,500.72', '-11,365.84', '35,322.64', 'Refund',
                                                        'JPY', '248', '571,423', '0.00', '0.00', '5,682.92', '5,682.92',
                                                        'Sub-Total', '', '744', '1,714,269', '38,375.52', '55,001.44',
                                                        '-17,048.76', '76,328.20', '', '', '2976', '', '153,502.08',
                                                        '220,005.76', '-68,195.04', '305,312.80']

    evonet_wop_monthly_monthly_monthly_single_accumulation = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                              'Transaction Amount', 'Transaction Processing Fee',
                                                              'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                              'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                              '23,059.19', '-11,365.84', '30,881.11', 'MPM Payment',
                                                              'CNY', '248', '571,423.00', '19,187.76', '23,059.19',
                                                              '-11,365.84', '30,881.11', 'Refund', 'CNY', '248',
                                                              '571,423.00', '0.00', '0.00', '5,682.92', '5,682.92',
                                                              'Sub-Total', '', '744', '1,714,269.00', '38,375.52',
                                                              '46,118.38', '-17,048.76', '67,445.14', 'CPM Payment',
                                                              'JPY', '248', '571,423', '19,187.76', '23,059.19',
                                                              '-11,365.84', '30,881.11', 'MPM Payment', 'JPY', '248',
                                                              '571,423', '19,187.76', '23,059.19', '-11,365.84',
                                                              '30,881.11', 'Refund', 'JPY', '248', '571,423', '0.00',
                                                              '0.00', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                              '1,714,269', '38,375.52', '46,118.38', '-17,048.76',
                                                              '67,445.14', 'CPM Payment', 'CNY', '248', '571,423.00',
                                                              '19,187.76', '23,059.19', '-11,365.84', '30,881.11',
                                                              'MPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                              '23,059.19', '-11,365.84', '30,881.11', 'Refund', 'CNY',
                                                              '248', '571,423.00', '0.00', '0.00', '5,682.92',
                                                              '5,682.92', 'Sub-Total', '', '744', '1,714,269.00',
                                                              '38,375.52', '46,118.38', '-17,048.76', '67,445.14',
                                                              'CPM Payment', 'JPY', '248', '571,423', '19,187.76',
                                                              '23,059.19', '-11,365.84', '30,881.11', 'MPM Payment',
                                                              'JPY', '248', '571,423', '19,187.76', '23,059.19',
                                                              '-11,365.84', '30,881.11', 'Refund', 'JPY', '248',
                                                              '571,423', '0.00', '0.00', '5,682.92', '5,682.92',
                                                              'Sub-Total', '', '744', '1,714,269', '38,375.52',
                                                              '46,118.38', '-17,048.76', '67,445.14', '', '', '2976',
                                                              '', '153,502.08', '184,473.52', '-68,195.04',
                                                              '269,780.56']

    evonet_wop_monthly_monthly_monthly_accumulation_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                              'Transaction Amount', 'Transaction Processing Fee',
                                                              'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                              'CPM Payment', 'CNY', '248', '571,423.00', '18,905.89',
                                                              '27,500.72', '-11,365.84', '35,040.77', 'MPM Payment',
                                                              'CNY', '248', '571,423.00', '18,905.89', '27,500.72',
                                                              '-11,365.84', '35,040.77', 'Refund', 'CNY', '248',
                                                              '571,423.00', '0.00', '0.00', '5,682.92', '5,682.92',
                                                              'Sub-Total', '', '744', '1,714,269.00', '37,811.78',
                                                              '55,001.44', '-17,048.76', '75,764.46', 'CPM Payment',
                                                              'JPY', '248', '571,423', '18,905.89', '27,500.72',
                                                              '-11,365.84', '35,040.77', 'MPM Payment', 'JPY', '248',
                                                              '571,423', '18,905.89', '27,500.72', '-11,365.84',
                                                              '35,040.77', 'Refund', 'JPY', '248', '571,423', '0.00',
                                                              '0.00', '5,682.92', '5,682.92', 'Sub-Total', '', '744',
                                                              '1,714,269', '37,811.78', '55,001.44', '-17,048.76',
                                                              '75,764.46', 'CPM Payment', 'CNY', '248', '571,423.00',
                                                              '18,905.89', '27,500.72', '-11,365.84', '35,040.77',
                                                              'MPM Payment', 'CNY', '248', '571,423.00', '18,905.89',
                                                              '27,500.72', '-11,365.84', '35,040.77', 'Refund', 'CNY',
                                                              '248', '571,423.00', '0.00', '0.00', '5,682.92',
                                                              '5,682.92', 'Sub-Total', '', '744', '1,714,269.00',
                                                              '37,811.78', '55,001.44', '-17,048.76', '75,764.46',
                                                              'CPM Payment', 'JPY', '248', '571,423', '18,905.89',
                                                              '27,500.72', '-11,365.84', '35,040.77', 'MPM Payment',
                                                              'JPY', '248', '571,423', '18,905.89', '27,500.72',
                                                              '-11,365.84', '35,040.77', 'Refund', 'JPY', '248',
                                                              '571,423', '0.00', '0.00', '5,682.92', '5,682.92',
                                                              'Sub-Total', '', '744', '1,714,269', '37,811.78',
                                                              '55,001.44', '-17,048.76', '75,764.46', '', '', '2976',
                                                              '', '151,247.12', '220,005.76', '-68,195.04',
                                                              '303,057.84']
    evonet_wop_monthly_monthly_monthly_accumulation_accumulation = ['Transaction Type', 'Transaction Currency',
                                                                    'Counts', 'Transaction Amount',
                                                                    'Transaction Processing Fee', 'FX Processing Fee',
                                                                    'FX Rebate', 'Total Service Fee', 'CPM Payment',
                                                                    'CNY', '248', '571,423.00', '18,905.89',
                                                                    '23,059.19', '-11,365.84', '30,599.24',
                                                                    'MPM Payment', 'CNY', '248', '571,423.00',
                                                                    '18,905.89', '23,059.19', '-11,365.84', '30,599.24',
                                                                    'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                                    '0.00', '5,682.92', '5,682.92', 'Sub-Total', '',
                                                                    '744', '1,714,269.00', '37,811.78', '46,118.38',
                                                                    '-17,048.76', '66,881.40', 'CPM Payment', 'JPY',
                                                                    '248', '571,423', '18,905.89', '23,059.19',
                                                                    '-11,365.84', '30,599.24', 'MPM Payment', 'JPY',
                                                                    '248', '571,423', '18,905.89', '23,059.19',
                                                                    '-11,365.84', '30,599.24', 'Refund', 'JPY', '248',
                                                                    '571,423', '0.00', '0.00', '5,682.92', '5,682.92',
                                                                    'Sub-Total', '', '744', '1,714,269', '37,811.78',
                                                                    '46,118.38', '-17,048.76', '66,881.40',
                                                                    'CPM Payment', 'CNY', '248', '571,423.00',
                                                                    '18,905.89', '23,059.19', '-11,365.84', '30,599.24',
                                                                    'MPM Payment', 'CNY', '248', '571,423.00',
                                                                    '18,905.89', '23,059.19', '-11,365.84', '30,599.24',
                                                                    'Refund', 'CNY', '248', '571,423.00', '0.00',
                                                                    '0.00', '5,682.92', '5,682.92', 'Sub-Total', '',
                                                                    '744', '1,714,269.00', '37,811.78', '46,118.38',
                                                                    '-17,048.76', '66,881.40', 'CPM Payment', 'JPY',
                                                                    '248', '571,423', '18,905.89', '23,059.19',
                                                                    '-11,365.84', '30,599.24', 'MPM Payment', 'JPY',
                                                                    '248', '571,423', '18,905.89', '23,059.19',
                                                                    '-11,365.84', '30,599.24', 'Refund', 'JPY', '248',
                                                                    '571,423', '0.00', '0.00', '5,682.92', '5,682.92',
                                                                    'Sub-Total', '', '744', '1,714,269', '37,811.78',
                                                                    '46,118.38', '-17,048.76', '66,881.40', '', '',
                                                                    '2976', '', '151,247.12', '184,473.52',
                                                                    '-68,195.04', '267,525.60']

    evonet_mop_service_daily_monthly_single_single = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                      'Transaction Amount', 'Transaction Processing Fee',
                                                      'FX Processing Fee', 'Total Service Fee', 'CPM Payment', 'CNY',
                                                      '', '248', '571,423.00', '-', '-27,500.72', '-27,500.72',
                                                      'MPM Payment', 'CNY', '', '248', '571,423.00', '-', '-27,500.72',
                                                      '-27,500.72', 'Refund', 'CNY', '', '248', '571,423.00', '-',
                                                      '0.00', '0.00', 'Sub-Total', '', '', '744', '1,714,269.00', '-',
                                                      '-55,001.44', '-55,001.44', 'CPM Payment', 'JPY', '', '248',
                                                      '571,423', '-', '-27,500.72', '-27,500.72', 'MPM Payment', 'JPY',
                                                      '', '248', '571,423', '-', '-27,500.72', '-27,500.72', 'Refund',
                                                      'JPY', '', '248', '571,423', '-', '0.00', '0.00', 'Sub-Total', '',
                                                      '', '744', '1,714,269', '-', '-55,001.44', '-55,001.44',
                                                      'CPM Payment', 'CNY', '', '248', '571,423.00', '-', '-27,500.72',
                                                      '-27,500.72', 'MPM Payment', 'CNY', '', '248', '571,423.00', '-',
                                                      '-27,500.72', '-27,500.72', 'Refund', 'CNY', '', '248',
                                                      '571,423.00', '-', '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                      '1,714,269.00', '-', '-55,001.44', '-55,001.44', 'CPM Payment',
                                                      'JPY', '', '248', '571,423', '-', '-27,500.72', '-27,500.72',
                                                      'MPM Payment', 'JPY', '', '248', '571,423', '-', '-27,500.72',
                                                      '-27,500.72', 'Refund', 'JPY', '', '248', '571,423', '-', '0.00',
                                                      '0.00', 'Sub-Total', '', '', '744', '1,714,269', '-',
                                                      '-55,001.44', '-55,001.44', '', '', '', '2976', '', '-',
                                                      '-220,005.76', '-220,005.76']
    evonet_mop_service_daily_monthly_single_accumulation = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                            'Transaction Amount', 'Transaction Processing Fee',
                                                            'FX Processing Fee', 'Total Service Fee', 'CPM Payment',
                                                            'CNY', '', '248', '571,423.00', '-', '-30,821.34',
                                                            '-30,821.34', 'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                            '-', '-30,821.34', '-30,821.34', 'Refund', 'CNY', '', '248',
                                                            '571,423.00', '-', '0.00', '0.00', 'Sub-Total', '', '',
                                                            '744', '1,714,269.00', '-', '-61,642.68', '-61,642.68',
                                                            'CPM Payment', 'JPY', '', '248', '571,423', '-',
                                                            '-30,821.34', '-30,821.34', 'MPM Payment', 'JPY', '', '248',
                                                            '571,423', '-', '-30,821.34', '-30,821.34', 'Refund', 'JPY',
                                                            '', '248', '571,423', '-', '0.00', '0.00', 'Sub-Total', '',
                                                            '', '744', '1,714,269', '-', '-61,642.68', '-61,642.68',
                                                            'CPM Payment', 'CNY', '', '248', '571,423.00', '-',
                                                            '-30,821.34', '-30,821.34', 'MPM Payment', 'CNY', '', '248',
                                                            '571,423.00', '-', '-30,821.34', '-30,821.34', 'Refund',
                                                            'CNY', '', '248', '571,423.00', '-', '0.00', '0.00',
                                                            'Sub-Total', '', '', '744', '1,714,269.00', '-',
                                                            '-61,642.68', '-61,642.68', 'CPM Payment', 'JPY', '', '248',
                                                            '571,423', '-', '-30,821.34', '-30,821.34', 'MPM Payment',
                                                            'JPY', '', '248', '571,423', '-', '-30,821.34',
                                                            '-30,821.34', 'Refund', 'JPY', '', '248', '571,423', '-',
                                                            '0.00', '0.00', 'Sub-Total', '', '', '744', '1,714,269',
                                                            '-', '-61,642.68', '-61,642.68', '', '', '', '2976', '',
                                                            '-', '-246,570.72', '-246,570.72']

    evonet_mop_service_monthly_daily_accumulation_single = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                            'Transaction Amount', 'Transaction Processing Fee',
                                                            'FX Processing Fee', 'Total Service Fee', 'CPM Payment',
                                                            'CNY', '', '248', '571,423.00', '-21,167.46', '-',
                                                            '-21,167.46', 'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                            '-21,167.46', '-', '-21,167.46', 'Refund', 'CNY', '', '248',
                                                            '571,423.00', '0.00', '-', '0.00', 'Sub-Total', '', '',
                                                            '744', '1,714,269.00', '-42,334.92', '-', '-42,334.92',
                                                            'CPM Payment', 'JPY', '', '248', '571,423', '-21,167.46',
                                                            '-', '-21,167.46', 'MPM Payment', 'JPY', '', '248',
                                                            '571,423', '-21,167.46', '-', '-21,167.46', 'Refund', 'JPY',
                                                            '', '248', '571,423', '0.00', '-', '0.00', 'Sub-Total', '',
                                                            '', '744', '1,714,269', '-42,334.92', '-', '-42,334.92',
                                                            'CPM Payment', 'CNY', '', '248', '571,423.00', '-21,167.46',
                                                            '-', '-21,167.46', 'MPM Payment', 'CNY', '', '248',
                                                            '571,423.00', '-21,167.46', '-', '-21,167.46', 'Refund',
                                                            'CNY', '', '248', '571,423.00', '0.00', '-', '0.00',
                                                            'Sub-Total', '', '', '744', '1,714,269.00', '-42,334.92',
                                                            '-', '-42,334.92', 'CPM Payment', 'JPY', '', '248',
                                                            '571,423', '-21,167.46', '-', '-21,167.46', 'MPM Payment',
                                                            'JPY', '', '248', '571,423', '-21,167.46', '-',
                                                            '-21,167.46', 'Refund', 'JPY', '', '248', '571,423', '0.00',
                                                            '-', '0.00', 'Sub-Total', '', '', '744', '1,714,269',
                                                            '-42,334.92', '-', '-42,334.92', '', '', '', '2976', '',
                                                            '-169,339.68', '-', '-169,339.68']

    evonet_mop_service_monthly_daily_single_single = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                      'Transaction Amount', 'Transaction Processing Fee',
                                                      'FX Processing Fee', 'Total Service Fee', 'CPM Payment', 'CNY',
                                                      '', '248', '571,423.00', '-19,187.76', '-', '-19,187.76',
                                                      'MPM Payment', 'CNY', '', '248', '571,423.00', '-19,187.76', '-',
                                                      '-19,187.76', 'Refund', 'CNY', '', '248', '571,423.00', '0.00',
                                                      '-', '0.00', 'Sub-Total', '', '', '744', '1,714,269.00',
                                                      '-38,375.52', '-', '-38,375.52', 'CPM Payment', 'JPY', '', '248',
                                                      '571,423', '-19,187.76', '-', '-19,187.76', 'MPM Payment', 'JPY',
                                                      '', '248', '571,423', '-19,187.76', '-', '-19,187.76', 'Refund',
                                                      'JPY', '', '248', '571,423', '0.00', '-', '0.00', 'Sub-Total', '',
                                                      '', '744', '1,714,269', '-38,375.52', '-', '-38,375.52',
                                                      'CPM Payment', 'CNY', '', '248', '571,423.00', '-19,187.76', '-',
                                                      '-19,187.76', 'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                      '-19,187.76', '-', '-19,187.76', 'Refund', 'CNY', '', '248',
                                                      '571,423.00', '0.00', '-', '0.00', 'Sub-Total', '', '', '744',
                                                      '1,714,269.00', '-38,375.52', '-', '-38,375.52', 'CPM Payment',
                                                      'JPY', '', '248', '571,423', '-19,187.76', '-', '-19,187.76',
                                                      'MPM Payment', 'JPY', '', '248', '571,423', '-19,187.76', '-',
                                                      '-19,187.76', 'Refund', 'JPY', '', '248', '571,423', '0.00', '-',
                                                      '0.00', 'Sub-Total', '', '', '744', '1,714,269', '-38,375.52',
                                                      '-', '-38,375.52', '', '', '', '2976', '', '-153,502.08', '-',
                                                      '-153,502.08']

    evonet_mop_service_monthly_monthly_accumulation_accumulation = ['Transaction Type', 'Transaction Currency', '',
                                                                    'Counts', 'Transaction Amount',
                                                                    'Transaction Processing Fee', 'FX Processing Fee',
                                                                    'Total Service Fee', 'CPM Payment', 'CNY', '',
                                                                    '248', '571,423.00', '-21,167.46', '-30,821.34',
                                                                    '-51,988.80', 'MPM Payment', 'CNY', '', '248',
                                                                    '571,423.00', '-21,167.46', '-30,821.34',
                                                                    '-51,988.80', 'Refund', 'CNY', '', '248',
                                                                    '571,423.00', '0.00', '0.00', '0.00', 'Sub-Total',
                                                                    '', '', '744', '1,714,269.00', '-42,334.92',
                                                                    '-61,642.68', '-103,977.60', 'CPM Payment', 'JPY',
                                                                    '', '248', '571,423', '-21,167.46', '-30,821.34',
                                                                    '-51,988.80', 'MPM Payment', 'JPY', '', '248',
                                                                    '571,423', '-21,167.46', '-30,821.34', '-51,988.80',
                                                                    'Refund', 'JPY', '', '248', '571,423', '0.00',
                                                                    '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                                    '1,714,269', '-42,334.92', '-61,642.68',
                                                                    '-103,977.60', 'CPM Payment', 'CNY', '', '248',
                                                                    '571,423.00', '-21,167.46', '-30,821.34',
                                                                    '-51,988.80', 'MPM Payment', 'CNY', '', '248',
                                                                    '571,423.00', '-21,167.46', '-30,821.34',
                                                                    '-51,988.80', 'Refund', 'CNY', '', '248',
                                                                    '571,423.00', '0.00', '0.00', '0.00', 'Sub-Total',
                                                                    '', '', '744', '1,714,269.00', '-42,334.92',
                                                                    '-61,642.68', '-103,977.60', 'CPM Payment', 'JPY',
                                                                    '', '248', '571,423', '-21,167.46', '-30,821.34',
                                                                    '-51,988.80', 'MPM Payment', 'JPY', '', '248',
                                                                    '571,423', '-21,167.46', '-30,821.34', '-51,988.80',
                                                                    'Refund', 'JPY', '', '248', '571,423', '0.00',
                                                                    '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                                    '1,714,269', '-42,334.92', '-61,642.68',
                                                                    '-103,977.60', '', '', '', '2976', '',
                                                                    '-169,339.68', '-246,570.72', '-415,910.40']

    evonet_mop_service_monthly_monthly_accumulation_single = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                              'Transaction Amount', 'Transaction Processing Fee',
                                                              'FX Processing Fee', 'Total Service Fee', 'CPM Payment',
                                                              'CNY', '', '248', '571,423.00', '-21,167.46',
                                                              '-27,500.72', '-48,668.18', 'MPM Payment', 'CNY', '',
                                                              '248', '571,423.00', '-21,167.46', '-27,500.72',
                                                              '-48,668.18', 'Refund', 'CNY', '', '248', '571,423.00',
                                                              '0.00', '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                              '1,714,269.00', '-42,334.92', '-55,001.44', '-97,336.36',
                                                              'CPM Payment', 'JPY', '', '248', '571,423', '-21,167.46',
                                                              '-27,500.72', '-48,668.18', 'MPM Payment', 'JPY', '',
                                                              '248', '571,423', '-21,167.46', '-27,500.72',
                                                              '-48,668.18', 'Refund', 'JPY', '', '248', '571,423',
                                                              '0.00', '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                              '1,714,269', '-42,334.92', '-55,001.44', '-97,336.36',
                                                              'CPM Payment', 'CNY', '', '248', '571,423.00',
                                                              '-21,167.46', '-27,500.72', '-48,668.18', 'MPM Payment',
                                                              'CNY', '', '248', '571,423.00', '-21,167.46',
                                                              '-27,500.72', '-48,668.18', 'Refund', 'CNY', '', '248',
                                                              '571,423.00', '0.00', '0.00', '0.00', 'Sub-Total', '', '',
                                                              '744', '1,714,269.00', '-42,334.92', '-55,001.44',
                                                              '-97,336.36', 'CPM Payment', 'JPY', '', '248', '571,423',
                                                              '-21,167.46', '-27,500.72', '-48,668.18', 'MPM Payment',
                                                              'JPY', '', '248', '571,423', '-21,167.46', '-27,500.72',
                                                              '-48,668.18', 'Refund', 'JPY', '', '248', '571,423',
                                                              '0.00', '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                              '1,714,269', '-42,334.92', '-55,001.44', '-97,336.36', '',
                                                              '', '', '2976', '', '-169,339.68', '-220,005.76',
                                                              '-389,345.44']

    evonet_mop_service_monthly_monthly_single_accumulation = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                              'Transaction Amount', 'Transaction Processing Fee',
                                                              'FX Processing Fee', 'Total Service Fee', 'CPM Payment',
                                                              'CNY', '', '200', '460,000.00', '-14,284.00',
                                                              '-20,471.35', '-34,755.35', 'MPM Payment', 'CNY', '',
                                                              '200', '460,000.00', '-14,284.00', '-20,471.35',
                                                              '-34,755.35', 'Refund', 'CNY', '', '200', '230,000.00',
                                                              '0.00', '0.00', '0.00', 'Sub-Total', '', '', '600',
                                                              '1,150,000.00', '-28,568.00', '-40,942.70', '-69,510.70',
                                                              'CPM Payment', 'JPY', '', '200', '460,000', '-14,284.00',
                                                              '-20,471.35', '-34,755.35', 'MPM Payment', 'JPY', '',
                                                              '200', '460,000', '-14,284.00', '-20,471.35',
                                                              '-34,755.35', 'Refund', 'JPY', '', '200', '230,000',
                                                              '0.00', '0.00', '0.00', 'Sub-Total', '', '', '600',
                                                              '1,150,000', '-28,568.00', '-40,942.70', '-69,510.70',
                                                              'CPM Payment', 'CNY', '', '200', '460,000.00',
                                                              '-14,284.00', '-20,471.35', '-34,755.35', 'MPM Payment',
                                                              'CNY', '', '200', '460,000.00', '-14,284.00',
                                                              '-20,471.35', '-34,755.35', 'Refund', 'CNY', '', '200',
                                                              '230,000.00', '0.00', '0.00', '0.00', 'Sub-Total', '', '',
                                                              '600', '1,150,000.00', '-28,568.00', '-40,942.70',
                                                              '-69,510.70', 'CPM Payment', 'JPY', '', '200', '460,000',
                                                              '-14,284.00', '-20,471.35', '-34,755.35', 'MPM Payment',
                                                              'JPY', '', '200', '460,000', '-14,284.00', '-20,471.35',
                                                              '-34,755.35', 'Refund', 'JPY', '', '200', '230,000',
                                                              '0.00', '0.00', '0.00', 'Sub-Total', '', '', '600',
                                                              '1,150,000', '-28,568.00', '-40,942.70', '-69,510.70', '',
                                                              '', '', '2400', '', '-114,272.00', '-163,770.80',
                                                              '-278,042.80']

    evonet_mop_service_monthly_monthly_single_single = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                        'Transaction Amount', 'Transaction Processing Fee',
                                                        'FX Processing Fee', 'Total Service Fee', 'CPM Payment', 'CNY',
                                                        '', '248', '571,423.00', '-19,187.76', '-27,500.72',
                                                        '-46,688.48', 'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                        '-19,187.76', '-27,500.72', '-46,688.48', 'Refund', 'CNY', '',
                                                        '248', '571,423.00', '0.00', '0.00', '0.00', 'Sub-Total', '',
                                                        '', '744', '1,714,269.00', '-38,375.52', '-55,001.44',
                                                        '-93,376.96', 'CPM Payment', 'JPY', '', '248', '571,423',
                                                        '-19,187.76', '-27,500.72', '-46,688.48', 'MPM Payment', 'JPY',
                                                        '', '248', '571,423', '-19,187.76', '-27,500.72', '-46,688.48',
                                                        'Refund', 'JPY', '', '248', '571,423', '0.00', '0.00', '0.00',
                                                        'Sub-Total', '', '', '744', '1,714,269', '-38,375.52',
                                                        '-55,001.44', '-93,376.96', 'CPM Payment', 'CNY', '', '248',
                                                        '571,423.00', '-19,187.76', '-27,500.72', '-46,688.48',
                                                        'MPM Payment', 'CNY', '', '248', '571,423.00', '-19,187.76',
                                                        '-27,500.72', '-46,688.48', 'Refund', 'CNY', '', '248',
                                                        '571,423.00', '0.00', '0.00', '0.00', 'Sub-Total', '', '',
                                                        '744', '1,714,269.00', '-38,375.52', '-55,001.44', '-93,376.96',
                                                        'CPM Payment', 'JPY', '', '248', '571,423', '-19,187.76',
                                                        '-27,500.72', '-46,688.48', 'MPM Payment', 'JPY', '', '248',
                                                        '571,423', '-19,187.76', '-27,500.72', '-46,688.48', 'Refund',
                                                        'JPY', '', '248', '571,423', '0.00', '0.00', '0.00',
                                                        'Sub-Total', '', '', '744', '1,714,269', '-38,375.52',
                                                        '-55,001.44', '-93,376.96', '', '', '', '2976', '',
                                                        '-153,502.08', '-220,005.76', '-373,507.84']

    bilateral_mop_service_monthly_monthly_accumulation_accumulation = ['Transaction Type', 'Transaction Currency', '',
                                                                       'Counts', 'Transaction Amount',
                                                                       'Transaction Processing Fee',
                                                                       'FX Processing Fee', 'Total Service Fee',
                                                                       'CPM Payment', 'CNY', '', '248', '571,423.00',
                                                                       '-19,228.97', '-27,587.11', '-46,816.08',
                                                                       'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                                       '-19,228.97', '-27,587.11', '-46,816.08',
                                                                       'Refund', 'CNY', '', '248', '571,423.00', '0.00',
                                                                       '0.00', '0.00', 'Sub-Total', '', '', '744',
                                                                       '1,714,269.00', '-38,457.94', '-55,174.22',
                                                                       '-93,632.16', 'CPM Payment', 'JPY', '', '248',
                                                                       '571,423', '-19,228.97', '-27,587.11',
                                                                       '-46,816.08', 'MPM Payment', 'JPY', '', '248',
                                                                       '571,423', '-19,228.97', '-27,587.11',
                                                                       '-46,816.08', 'Refund', 'JPY', '', '248',
                                                                       '571,423', '0.00', '0.00', '0.00', 'Sub-Total',
                                                                       '', '', '744', '1,714,269', '-38,457.94',
                                                                       '-55,174.22', '-93,632.16', '', '', '', '1488',
                                                                       '', '-76,915.88', '-110,348.44', '-187,264.32']
    bilateral_mop_service_monthly_monthly_accumulation_single = ['Transaction Type', 'Transaction Currency', '',
                                                                 'Counts', 'Transaction Amount',
                                                                 'Transaction Processing Fee', 'FX Processing Fee',
                                                                 'Total Service Fee', 'CPM Payment', 'CNY', '', '248',
                                                                 '571,423.00', '-19,228.97', '-27,500.72', '-46,729.69',
                                                                 'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                                 '-19,228.97', '-27,500.72', '-46,729.69', 'Refund',
                                                                 'CNY', '', '248', '571,423.00', '0.00', '0.00', '0.00',
                                                                 'Sub-Total', '', '', '744', '1,714,269.00',
                                                                 '-38,457.94', '-55,001.44', '-93,459.38',
                                                                 'CPM Payment', 'JPY', '', '248', '571,423',
                                                                 '-19,228.97', '-27,500.72', '-46,729.69',
                                                                 'MPM Payment', 'JPY', '', '248', '571,423',
                                                                 '-19,228.97', '-27,500.72', '-46,729.69', 'Refund',
                                                                 'JPY', '', '248', '571,423', '0.00', '0.00', '0.00',
                                                                 'Sub-Total', '', '', '744', '1,714,269', '-38,457.94',
                                                                 '-55,001.44', '-93,459.38', '', '', '', '1488', '',
                                                                 '-76,915.88', '-110,002.88', '-186,918.76']
    bilateral_mop_service_monthly_monthly_single_accumulation = ['Transaction Type', 'Transaction Currency', '',
                                                                 'Counts', 'Transaction Amount',
                                                                 'Transaction Processing Fee', 'FX Processing Fee',
                                                                 'Total Service Fee', 'CPM Payment', 'CNY', '', '200',
                                                                 '460,000.00', '-14,284.00', '-20,471.35', '-34,755.35',
                                                                 'MPM Payment', 'CNY', '', '200', '460,000.00',
                                                                 '-14,284.00', '-20,471.35', '-34,755.35', 'Refund',
                                                                 'CNY', '', '200', '230,000.00', '0.00', '0.00', '0.00',
                                                                 'Sub-Total', '', '', '600', '1,150,000.00',
                                                                 '-28,568.00', '-40,942.70', '-69,510.70',
                                                                 'CPM Payment', 'JPY', '', '200', '460,000',
                                                                 '-14,284.00', '-20,471.35', '-34,755.35',
                                                                 'MPM Payment', 'JPY', '', '200', '460,000',
                                                                 '-14,284.00', '-20,471.35', '-34,755.35', 'Refund',
                                                                 'JPY', '', '200', '230,000', '0.00', '0.00', '0.00',
                                                                 'Sub-Total', '', '', '600', '1,150,000', '-28,568.00',
                                                                 '-40,942.70', '-69,510.70', '', '', '', '1200', '',
                                                                 '-57,136.00', '-81,885.40', '-139,021.40']
    bilateral_mop_service_monthly_monthly_single_single = ['Transaction Type', 'Transaction Currency', '', 'Counts',
                                                           'Transaction Amount', 'Transaction Processing Fee',
                                                           'FX Processing Fee', 'Total Service Fee', 'CPM Payment',
                                                           'CNY', '', '248', '571,423.00', '-19,187.76', '-27,500.72',
                                                           '-46,688.48', 'MPM Payment', 'CNY', '', '248', '571,423.00',
                                                           '-19,187.76', '-27,500.72', '-46,688.48', 'Refund', 'CNY',
                                                           '', '248', '571,423.00', '0.00', '0.00', '0.00', 'Sub-Total',
                                                           '', '', '744', '1,714,269.00', '-38,375.52', '-55,001.44',
                                                           '-93,376.96', 'CPM Payment', 'JPY', '', '248', '571,423',
                                                           '-19,187.76', '-27,500.72', '-46,688.48', 'MPM Payment',
                                                           'JPY', '', '248', '571,423', '-19,187.76', '-27,500.72',
                                                           '-46,688.48', 'Refund', 'JPY', '', '248', '571,423', '0.00',
                                                           '0.00', '0.00', 'Sub-Total', '', '', '744', '1,714,269',
                                                           '-38,375.52', '-55,001.44', '-93,376.96', '', '', '', '1488',
                                                           '', '-76,751.04', '-110,002.88', '-186,753.92']

    bilateral_wop_service_monthly_monthly_accumulation_accumulation = ['Transaction Type', 'Transaction Currency',
                                                                       'Counts', 'Transaction Amount',
                                                                       'Transaction Processing Fee',
                                                                       'FX Processing Fee', 'FX Rebate',
                                                                       'Total Service Fee', 'CPM Payment', 'CNY', '248',
                                                                       '571,423.00', '19,228.97', '27,587.11', '-',
                                                                       '46,816.08', 'MPM Payment', 'CNY', '248',
                                                                       '571,423.00', '19,228.97', '27,587.11', '-',
                                                                       '46,816.08', 'Refund', 'CNY', '248',
                                                                       '571,423.00', '0.00', '0.00', '-', '0.00',
                                                                       'Sub-Total', '', '744', '1,714,269.00',
                                                                       '38,457.94', '55,174.22', '-', '93,632.16',
                                                                       'CPM Payment', 'JPY', '248', '571,423',
                                                                       '19,228.97', '27,587.11', '-', '46,816.08',
                                                                       'MPM Payment', 'JPY', '248', '571,423',
                                                                       '19,228.97', '27,587.11', '-', '46,816.08',
                                                                       'Refund', 'JPY', '248', '571,423', '0.00',
                                                                       '0.00', '-', '0.00', 'Sub-Total', '', '744',
                                                                       '1,714,269', '38,457.94', '55,174.22', '-',
                                                                       '93,632.16', '', '', '1488', '', '76,915.88',
                                                                       '110,348.44', '-', '187,264.32']

    bilateral_wop_service_monthly_monthly_accumulation_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                                 'Transaction Amount', 'Transaction Processing Fee',
                                                                 'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                                 'CPM Payment', 'CNY', '248', '571,423.00', '19,228.97',
                                                                 '27,500.72', '-', '46,729.69', 'MPM Payment', 'CNY',
                                                                 '248', '571,423.00', '19,228.97', '27,500.72', '-',
                                                                 '46,729.69', 'Refund', 'CNY', '248', '571,423.00',
                                                                 '0.00', '0.00', '-', '0.00', 'Sub-Total', '', '744',
                                                                 '1,714,269.00', '38,457.94', '55,001.44', '-',
                                                                 '93,459.38', 'CPM Payment', 'JPY', '248', '571,423',
                                                                 '19,228.97', '27,500.72', '-', '46,729.69',
                                                                 'MPM Payment', 'JPY', '248', '571,423', '19,228.97',
                                                                 '27,500.72', '-', '46,729.69', 'Refund', 'JPY', '248',
                                                                 '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total',
                                                                 '', '744', '1,714,269', '38,457.94', '55,001.44', '-',
                                                                 '93,459.38', '', '', '1488', '', '76,915.88',
                                                                 '110,002.88', '-', '186,918.76']

    bilateral_wop_service_monthly_monthly_single_accumulation = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                                 'Transaction Amount', 'Transaction Processing Fee',
                                                                 'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                                 'CPM Payment', 'CNY', '200', '460,000.00', '15,474.00',
                                                                 '22,177.30', '-', '37,651.30', 'MPM Payment', 'CNY',
                                                                 '200', '460,000.00', '15,474.00', '22,177.30', '-',
                                                                 '37,651.30', 'Refund', 'CNY', '200', '230,000.00',
                                                                 '0.00', '0.00', '-', '0.00', 'Sub-Total', '', '600',
                                                                 '1,150,000.00', '30,948.00', '44,354.60', '-',
                                                                 '75,302.60', 'CPM Payment', 'JPY', '200', '460,000',
                                                                 '15,474.00', '22,177.30', '-', '37,651.30',
                                                                 'MPM Payment', 'JPY', '200', '460,000', '15,474.00',
                                                                 '22,177.30', '-', '37,651.30', 'Refund', 'JPY', '200',
                                                                 '230,000', '0.00', '0.00', '-', '0.00', 'Sub-Total',
                                                                 '', '600', '1,150,000', '30,948.00', '44,354.60', '-',
                                                                 '75,302.60', '', '', '1200', '', '61,896.00',
                                                                 '88,709.20', '-', '150,605.20']

    bilateral_wop_service_monthly_monthly_single_single = ['Transaction Type', 'Transaction Currency', 'Counts',
                                                           'Transaction Amount', 'Transaction Processing Fee',
                                                           'FX Processing Fee', 'FX Rebate', 'Total Service Fee',
                                                           'CPM Payment', 'CNY', '248', '571,423.00', '19,187.76',
                                                           '27,500.72', '-', '46,688.48', 'MPM Payment', 'CNY', '248',
                                                           '571,423.00', '19,187.76', '27,500.72', '-', '46,688.48',
                                                           'Refund', 'CNY', '248', '571,423.00', '0.00', '0.00', '-',
                                                           '0.00', 'Sub-Total', '', '744', '1,714,269.00', '38,375.52',
                                                           '55,001.44', '-', '93,376.96', 'CPM Payment', 'JPY', '248',
                                                           '571,423', '19,187.76', '27,500.72', '-', '46,688.48',
                                                           'MPM Payment', 'JPY', '248', '571,423', '19,187.76',
                                                           '27,500.72', '-', '46,688.48', 'Refund', 'JPY', '248',
                                                           '571,423', '0.00', '0.00', '-', '0.00', 'Sub-Total', '',
                                                           '744', '1,714,269', '38,375.52', '55,001.44', '-',
                                                           '93,376.96', '', '', '1488', '', '76,751.04', '110,002.88',
                                                           '-', '186,753.92']

    upi_daily_summary_cny_content = ['Account Credit', 'CNY', '2', '2,300.00', '-2,600.00', '-45.32', '66.66',
                                     '-2,578.66',
                                     'Account Debit', 'CNY', '2', '2,300.00', '2,600.00', '-45.32', '66.66', '2,621.34',
                                     'Chargeback', 'CNY', '2', '666.00', '-888.44', '-25.32', '132.66', '-781.10',
                                     'Credit Adjustment', 'CNY', '2', '666.00', '-888.44', '-25.32', '132.66',
                                     '-781.10',
                                     'Debit Adjustment', 'CNY', '2', '666.00', '888.44', '-25.32', '132.66', '995.78',
                                     'Refund', 'CNY', '2', '2,300.00', '-1,300.00', '-45.32', '66.66', '-1,278.66',
                                     'Sub-Total', '', '12', '8,898.00', '-2,188.44', '-211.92', '597.96', '-1,802.40',
                                     'Account Credit', 'JPY', '2', '2,300', '-2,600.00', '-45.32', '66.66', '-2,578.66',
                                     'Account Debit', 'JPY', '2', '2,300', '2,600.00', '-45.32', '66.66', '2,621.34',
                                     'Chargeback', 'JPY', '2', '666', '-888.44', '-25.32', '132.66', '-781.10',
                                     'Credit Adjustment', 'JPY', '2', '666', '-888.44', '-25.32', '132.66', '-781.10',
                                     'Debit Adjustment', 'JPY', '2', '666', '888.44', '-25.32', '132.66', '995.78',
                                     'Refund', 'JPY', '2', '2,300', '-1,300.00', '-45.32', '66.66', '-1,278.66',
                                     'Sub-Total', '', '12', '8,898', '-2,188.44', '-211.92', '597.96', '-1,802.40',
                                     'Fee Collection', '-', '4', '-', '-', '-', '264.44', '264.44', 'Fund Disbursement',
                                     '-', '4', '-', '-', '-220.88', '264.44', '43.56', 'Sub-Total', '', '8', '-', '-',
                                     '-220.88', '528.88', '308.00', '', '', '32', '', '-4,376.88', '-644.72',
                                     '1,724.80',
                                     '-3,296.80']
    upi_daily_summary_jpy_content = ['Account Credit', 'CNY', '2', '2,300.00', '-2,600', '-44', '66', '-2,578',
                                     'Account Debit', 'CNY', '2',
                                     '2,300.00', '2,600', '-44', '66', '2,622', 'Chargeback', 'CNY', '2', '666.00',
                                     '-888', '-24', '132', '-780',
                                     'Credit Adjustment', 'CNY', '2', '666.00', '-888', '-24', '132', '-780',
                                     'Debit Adjustment', 'CNY', '2', '666.00',
                                     '888', '-24', '132', '996', 'Refund', 'CNY', '2', '2,300.00', '-1,300', '-44',
                                     '66', '-1,278', 'Sub-Total', '',
                                     '12', '8,898.00', '-2,188', '-204', '594', '-1,798', 'Account Credit', 'JPY', '2',
                                     '2,300', '-2,600', '-44', '66',
                                     '-2,578', 'Account Debit', 'JPY', '2', '2,300', '2,600', '-44', '66', '2,622',
                                     'Chargeback', 'JPY', '2', '666',
                                     '-888', '-24', '132', '-780', 'Credit Adjustment', 'JPY', '2', '666', '-888',
                                     '-24', '132', '-780',
                                     'Debit Adjustment', 'JPY', '2', '666', '888', '-24', '132', '996', 'Refund', 'JPY',
                                     '2', '2,300', '-1,300', '-44',
                                     '66', '-1,278', 'Sub-Total', '', '12', '8,898', '-2,188', '-204', '594', '-1,798',
                                     'Fee Collection', '-', '4',
                                     '-', '-', '-', '264', '264', 'Fund Disbursement', '-', '4', '-', '-', '-220',
                                     '264', '44', 'Sub-Total', '', '8',
                                     '-', '-', '-220', '528', '308', '', '', '32', '', '-4,376', '-628', '1,716',
                                     '-3,288']
    upi_servicefee_single_content = ['Account Credit', 'CNY', '62', '72,323.00', '4,098.82', 'Account Debit', 'CNY',
                                     '62', '72,323.00', '4,098.82', 'Refund', 'CNY', '62', '72,323.00', '0.00',
                                     'Sub-Total', '', '186', '216,969.00', '8,197.64', 'Account Credit', 'JPY', '62',
                                     '72,323', '4,098.82', 'Account Debit', 'JPY', '62', '72,323', '4,098.82', 'Refund',
                                     'JPY', '62', '72,323', '0.00', 'Sub-Total', '', '186', '216,969', '8,197.64', '',
                                     '', '372', '', '16,395.28']
    upi_servicefee_accumulation_content = ['Account Credit', 'CNY', '2', '2,333.00', '195.04', 'Account Debit', 'CNY',
                                           '2', '2,333.00', '195.04', 'Refund', 'CNY', '2', '2,333.00', '0.00',
                                           'Sub-Total', '', '6', '6,999.00', '390.08', 'Account Credit', 'JPY', '2',
                                           '2,333', '195.04', 'Account Debit', 'JPY', '2', '2,333', '195.04', 'Refund',
                                           'JPY', '2', '2,333', '0.00', 'Sub-Total', '', '6', '6,999', '390.08', '', '',
                                           '12', '', '780.16']

    trans_file_upi = "transFile.upi"
    trans_file_upifee = "transFile.upiFee"
    trans_file_upierr = "transFile.upiErr"
    net_work_token_pan = "networkTokenPan"
    trans_message = "trans_message"
    mop_file_resolve = "MopRefundFileResolve"
    mop_refund_trans_send = "MopRefundTransSend"
    mop_refund_file_generate = "MopRefundFileGenerate"
    trans_refund = "trans.refund"
    service_fee="serviceFee"
    relation_transfer="relationTransfer"
    trans_account="transferAccount"
    @property
    def owner_type_wop(self):
        return "wop"

    @property
    def owner_type_mop(self):
        return "mop"

    @property
    def bilateral(self):
        # 直清模式
        return "bilateral"

    @property
    def evonet(self):
        # 直清模式
        return "evonet"

    @property
    def file_init_wop(self):
        return "wop"

    # table_name
    @property
    def trans(self):
        return "trans"

    @property
    def file_info(self):
        return "fileInfo"

    @property
    def advice_file(self):
        return "advice_file"

    advice = "advice"

    @property
    def custom_config(self):
        # 直清模式
        return "customizeConfig"

    @property
    def trans_file_wop(self):
        return "transFile.wop"

    @property
    def trans_file_wop_node(self):
        return "transFile.wopNode"

    @property
    def trans_settle_wop(self):
        return "transSettle.wop"

    @property
    def settle_funcLog(self):
        return "settleFuncLog"

    @property
    def trans_settle_mop(self):
        return "transSettle.mop"

    @property
    def trans_summary_wop(self):
        return "transSummary.wop"

    @property
    def trans_summary_mop(self):
        return "transSummary.mop"

    # function name
    @property
    def wop_trans_import(self):
        return "WopTransImport"

    @property
    def wop_trans_sync(self):
        return "WopTransSync"

    @property
    def mop_trans_sync_update(self):
        return "MopTransSyncUpdate"

    @property
    def wop_trans_sync_update(self):
        return "WopTransSyncUpdate"

    @property
    def wop_trans_calc(self):
        return "WopTransFeeCalculate"

    @property
    def wop_self_sett(self):
        return "WopSelfSettle"

    @property
    def mop_self_sett(self):
        return "MopSelfSettle"

    @property
    def wop_generate_file(self):
        return "WopSettleFileGenerate"

    @property
    def mop_generate_file(self):
        return "MopSettleFileGenerate"

    @property
    def wop_fee_file(self):
        # 月报
        return "WopFeeFileGenerate"

    @property
    def mop_fee_file(self):
        # 月报
        return "MopFeeFileGenerate"

    @property
    def mop_trans_calc(self):
        return "MopTransFeeCalculate"

    @property
    def mop_trans_import(self):
        return "MopTransImport"

    @property
    def mop_trans_sync(self):
        return "MopTransSync"

    @property
    def wop_settle_file_download(self):
        return "WopSettleFileDownload"

    @property
    def wop_settle_file_resolve(self):
        return "WopSettleFileResolve"

    @property
    def wop_trans_reconcile(self):
        return "WopTransReconcile"

    @property
    def wop_fee_generate(self):
        # 月报
        return "WopFeeFileGenerate"

    @property
    def mop_fee_generate(self):
        # 月报
        return "MopFeeFileGenerate"

    @property
    def mop_settle_file_download(self):
        return "MopSettleFileDownload"

    @property
    def mop_settle_file_resolve(self):
        return "MopSettleFileResolve"

    @property
    def mop_trans_reconcile(self):
        return "MopTransReconcile"

    @property
    def file_type_Settlement(self):
        return "Settlement"

    @property
    def file_type_exception(self):
        return "Exception"

    @property
    def file_type_feecollection(self):
        return "FeeCollection"

    @property
    def file_type_ServiceFee(self):
        return "ServiceFee"

    @property
    def file_subtype_Summary(self):
        return "Summary"

    @property
    def file_subtype_Details(self):
        return "Details"

    @property
    def file_type_dispute(self):
        return "Dispute"

    @property
    def file_extension_xlsx(self):
        return "xlsx"

    @property
    def file_extension_csv(self):
        return "csv"

    @property
    def evonet_wop_list(self):
        return [('daily', 'daily', 'daily', 'single', 'single')]

    @property
    def evonet_monthly_wop_list(self):
        return [
            ('daily', 'daily', 'monthly', 'single', 'single'),
            ('daily', 'monthly', 'daily', 'single', 'single'),
            ('daily', 'monthly', 'daily', 'single', 'accumulation'),
            ('daily', 'monthly', 'monthly', 'single', 'single'),
            ('daily', 'monthly', 'monthly', 'single', 'accumulation'),
            ('monthly', 'daily', 'daily', 'single', 'single'),
            ('monthly', 'daily', 'daily', 'accumulation', 'single'),
            ('monthly', 'daily', 'monthly', 'single', 'single'),
            ('monthly', 'daily', 'monthly', 'accumulation', 'single'),
            ('monthly', 'monthly', 'daily', 'single', 'single'),
            ('monthly', 'monthly', 'daily', 'single', 'accumulation'),
            ('monthly', 'monthly', 'daily', 'accumulation', 'single'),
            ('monthly', 'monthly', 'daily', 'accumulation', 'accumulation'),
            ('monthly', 'monthly', 'monthly', 'single', 'single'),
            ('monthly', 'monthly', 'monthly', 'single', 'accumulation'),
            ('monthly', 'monthly', 'monthly', 'accumulation', 'single'),
            ('monthly', 'monthly', 'monthly', 'accumulation', 'accumulation')]

    @property
    def evonet_mop_list(self):
        return [('daily', 'daily', 'daily', 'single', 'single'),
                ('daily', 'daily', 'monthly', 'single', 'single'),
                ('daily', 'monthly', 'daily', 'single', 'single'),
                ('daily', 'monthly', 'daily', 'single', 'accumulation'),
                ('daily', 'monthly', 'monthly', 'single', 'single'),
                ('daily', 'monthly', 'monthly', 'single', 'accumulation'),
                ('monthly', 'daily', 'daily', 'single', 'single'),
                ('monthly', 'daily', 'daily', 'accumulation', 'single'),
                ('monthly', 'daily', 'monthly', 'single', 'single'),
                ('monthly', 'daily', 'monthly', 'accumulation', 'single'),
                ('monthly', 'monthly', 'daily', 'single', 'single'),
                ('monthly', 'monthly', 'daily', 'single', 'accumulation'),
                ('monthly', 'monthly', 'daily', 'accumulation', 'single'),
                ('monthly', 'monthly', 'daily', 'accumulation', 'accumulation'),
                ('monthly', 'monthly', 'monthly', 'single', 'single'),
                ('monthly', 'monthly', 'monthly', 'single', 'accumulation'),
                ('monthly', 'monthly', 'monthly', 'accumulation', 'single'),
                ('monthly', 'monthly', 'monthly', 'accumulation', 'accumulation')]

    @property
    def evonet_mop_list(self):
        return [('daily', 'daily', 'single', 'single')]

    @property
    def evonet_monthly_mop_list(self):
        return [
            ('daily', 'monthly', 'single', 'single'),
            ('daily', 'monthly', 'single', 'accumulation'),
            ('monthly', 'daily', 'single', 'single'),
            ('monthly', 'daily', 'accumulation', 'single'),
            ('monthly', 'monthly', 'single', 'single'),
            ('monthly', 'monthly', 'single', 'accumulation'),
            ('monthly', 'monthly', 'accumulation', 'single'),
            ('monthly', 'monthly', 'accumulation', 'accumulation')]

    @property
    def bilateral_list(self):
        return [('single', 'single'),
                ('single', 'accumulation'),
                ('accumulation', 'single'),
                ('accumulation', 'accumulation')]

    def upi_file_record(self, wopid, mopid, settle_date, file_name, remote_path):
        file_record = {"firstRole": wopid,
                       "secondRole": mopid,
                       "settleDate": settle_date,
                       "fileName": file_name,
                       "filePath": remote_path,
                       "fileType": "MOPFile",
                       "fileSubType": "Complex",
                       "serialNumber": "001",
                       "extension": "zip",
                       "resolveFlag": False, }
        return file_record


if __name__ == '__main__':
    s = CommFuncs()
    m = 0
    for i in ["4.9", "6.9", "6.9", "-6.9"]:
        m += Decimal(i)
