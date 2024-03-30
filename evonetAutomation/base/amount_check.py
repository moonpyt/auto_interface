from base import db
from base.read_file_path import ReadFile
from common.evopay.conf_init import db_tyo_evoconfig
from common.evopay.read_csv import ReadCSV
from loguru import logger as log
from decimal import Decimal

class amount_check():
    def __init__(self):
        self.fxRateOwner = 'evonet'

    def get(self,test_info,head_params,config_currency):
        self.test_info = test_info
        self.mopSettleCurrency = test_info['mopSettleCurrency']
        self.wopSettleCurrency = test_info['wopSettleCurrency']
        self.billingCurrency = test_info['billingCurrency']
        self.flag_SettlementAmount = True
        self.flag_billingAmont= True

        self.congfig_wop(head_params,config_currency)

    def congfig_wop(self,head_params,config_currency):
        log.debug(f"config_currency的值为{config_currency}")
        # 判断fxRateOwner在数据库中customizeConfig储存的值
        query_params = {"wopID": head_params["wopParticipantID"]}
        fxRateOwner_mongo = db_tyo_evoconfig.get_one('customizeConfig', query_params)
        if fxRateOwner_mongo:
            temp_fxRateOwner = fxRateOwner_mongo['fxRateOwner']
            if temp_fxRateOwner:
                self.fxRateOwner = temp_fxRateOwner


        if config_currency:
            for key,value in config_currency.items():
                if key == 'wopSettleCurrency':
                    self.wopSettleCurrency=value
                elif key == 'mopSettleCurrency':
                    self.mopSettleCurrency=value
                elif key == 'billingCurrency':
                    self.billingCurrency=value
                elif key == 'isSettlementAmountEVONETCalculated':
                    self.flag_SettlementAmount = value
                elif key == 'isBillingAmountCalculated':
                    self.flag_billingAmont = value

    def case_caculate(self,transCurrency='JPY',transAmount=23.0):
        amount = {}
        if (transCurrency == self.mopSettleCurrency) and (self.mopSettleCurrency == self.wopSettleCurrency) and (
                self.wopSettleCurrency == self.billingCurrency):
            if self.flag_SettlementAmount:
                wopSettleAmount, mopSettleAmount =transAmount,transAmount
                temp = dict(wopSettleAmount=wopSettleAmount, mopSettleAmount=wopSettleAmount)
                amount.update(temp)
            if self.flag_billingAmont:
                billingAmount = transAmount
                temp = dict(billingAmount=billingAmount)
                amount.update(temp)

        elif (transCurrency != self.mopSettleCurrency) and (self.mopSettleCurrency == self.wopSettleCurrency) and (
                self.wopSettleCurrency == self.billingCurrency):
            #计算mop侧的值
            if self.flag_SettlementAmount:
                temp = self.caculate(type='transCurrecy!=mopSettleCurrency')
                amount.update(temp)

                #计算wop侧金额wopBaseSettleFXRate、wopSettleFXRate、wopSettleAmount
                temp = self.caculate(type='wopSettleCurrency==mopSettleCurrency')
                amount.update(temp)

            if self.flag_billingAmont:
                #计算用户侧billingAmount、billingBaseFXRate、billingFXRate
                temp = self.caculate(type='wopSettleCurrency==billingCurrency',amount=amount)
                amount.update(temp)


        elif (transCurrency != self.mopSettleCurrency) and (self.mopSettleCurrency != self.wopSettleCurrency) and (
                self.wopSettleCurrency == self.billingCurrency):
            if self.flag_SettlementAmount:
                # 计算mop侧的值
                temp = self.caculate(type='transCurrecy!=mopSettleCurrency')
                amount.update(temp)

                #计算wop侧的值
                if self.wopSettleCurrency == transCurrency:
                    wopSettleAmount = transAmount
                    temp = dict(wopSettleAmount=wopSettleAmount)
                else:
                    temp = self.caculate(type='mopSettleCurrency!=wopSettleCurrency',amount=amount)
                amount.update(temp)

            if self.flag_billingAmont:
                #计算用户侧的值
                if self.billingCurrency == transCurrency:
                    billingAmount = transAmount
                    temp = dict(billingAmount=billingAmount)
                else:
                    temp = self.caculate(type='wopSettleCurrency==billingCurrency',amount=amount)
                amount.update(temp)


        elif (transCurrency!= self.mopSettleCurrency) and (self.mopSettleCurrency != self.wopSettleCurrency) and (
                 self.wopSettleCurrency != self.billingCurrency):
            if self.flag_SettlementAmount:
                # 计算mop侧的值
                temp = self.caculate(type='transCurrecy!=mopSettleCurrency')
                amount.update(temp)

                # 计算wop侧的值
                if self.wopSettleCurrency == transCurrency:
                    wopSettleAmount = transAmount
                    temp = dict(wopSettleAmount=wopSettleAmount)
                else:
                    temp = self.caculate(type='mopSettleCurrency!=wopSettleCurrency', amount=amount)
                amount.update(temp)

            if self.flag_billingAmont:
                # 计算用户侧的值
                if self.billingCurrency == transCurrency:
                    billingAmount = transAmount
                    temp = dict(billingAmount=billingAmount)
                else:
                    temp = self.caculate(type='wopSettleCurrency!=billingCurrency', amount=amount)
                amount.update(temp)



        elif (transCurrency == self.mopSettleCurrency) and (self.mopSettleCurrency != self.wopSettleCurrency) and (
                self.wopSettleCurrency == self.billingCurrency):
            if self.flag_SettlementAmount:
                # 计算mop侧的值
                mopSettleAmount = transAmount
                temp = dict(mopSettleAmount=mopSettleAmount)
                amount.update(temp)

                # 计算wop侧的值
                temp = self.caculate(type='mopSettleCurrency!=wopSettleCurrency', amount=amount)
                amount.update(temp)
            if self.flag_billingAmont:
                # 计算用户侧的值
                temp = self.caculate(type='wopSettleCurrency==billingCurrency', amount=amount)
                amount.update(temp)

        elif (transCurrency == self.mopSettleCurrency) and (self.mopSettleCurrency != self.wopSettleCurrency) and (
                self.wopSettleCurrency != self.billingCurrency):
            if self.flag_SettlementAmount:
                # 计算mop侧的值
                mopSettleAmount = transAmount
                temp = dict(mopSettleAmount=mopSettleAmount)
                amount.update(temp)

                # 计算wop侧的值
                temp = self.caculate(type='mopSettleCurrency!=wopSettleCurrency', amount=amount)
                amount.update(temp)

            if self.flag_billingAmont:
                # 计算用户侧的值
                if self.billingCurrency == transCurrency:
                    billingAmount = transAmount
                    temp = dict(billingAmount=billingAmount)

                else:
                    temp = self.caculate(type='wopSettleCurrency!=billingCurrency', amount=amount)
                amount.update(temp)

        elif (transCurrency == self.mopSettleCurrency) and (self.mopSettleCurrency == self.wopSettleCurrency) and (
                self.wopSettleCurrency != self.billingCurrency):
            if self.flag_SettlementAmount:
                # 计算mop侧的值
                mopSettleAmount = transAmount
                temp = dict(mopSettleAmount=mopSettleAmount)
                amount.update(temp)
                # 计算wop侧的值
                wopSettleAmount = transAmount
                temp = dict(wopSettleAmount=wopSettleAmount)
                amount.update(temp)
            if self.flag_billingAmont:
                # 计算用户侧的值
                temp = self.caculate(type='wopSettleCurrency!=billingCurrency', amount=amount)
                amount.update(temp)

        log.debug(f'amount的值为{amount}')
        return amount


    def caculate(self,type,amount=None,transCurrency='JPY',transAmount=23.0):
        #transCurrency != self.mopSettleCurrency

        if type == 'transCurrecy!=mopSettleCurrency':
            # 计算mop侧金额mopBaseSettleFXRate、mopSettleFXRate、mopSettleAmount
            mop_fx_rate = self.get_fx_rate(transCurrency, self.mopSettleCurrency,)
            mop_fx_rate = self.accurate_format_fxrate(mop_fx_rate)

            mopSettleAmount = transAmount * mop_fx_rate
            if self.test_info.get("mccr"):
                mopSettleAmount = mopSettleAmount * (1+self.test_info["mccr"])
            mopSettleAmount = self.accurate_format_transamount(mopSettleAmount,self.mopSettleCurrency)

            mopBaseSettleFXRate = mop_fx_rate
            if self.test_info.get("mccr"):
                mopSettleFXRate = mopBaseSettleFXRate * (1+self.test_info["mccr"])
            else:
                mopSettleFXRate = mopBaseSettleFXRate
            mopSettleFXRate = self.accurate_format_fxrate(mopSettleFXRate)

            amount = dict(mopSettleAmount=mopSettleAmount,mopSettleFXRate=mopSettleFXRate,mopBaseSettleFXRate=mopBaseSettleFXRate)

        elif type == 'mopSettleCurrency!=wopSettleCurrency':
            # 计算wop侧金额wopBaseSettleFXRate、wopSettleFXRate、wopSettleAmount
            wop_fx_rate = self.get_fx_rate(self.mopSettleCurrency, self.wopSettleCurrency)
            wop_fx_rate = self.accurate_format_fxrate(wop_fx_rate)
            if self.test_info.get("wccr"):
                wopSettleAmount = amount['mopSettleAmount']*wop_fx_rate*(1 + self.test_info['wccr'])
            else:
                wopSettleAmount = amount['mopSettleAmount'] * wop_fx_rate
            wopSettleAmount = self.accurate_format_transamount(wopSettleAmount,self.wopSettleCurrency)

            wopSettleFXRate = self.accurate_format_fxrate(wopSettleAmount/transAmount)
            wopBaseSettleFXRate = wopSettleFXRate
            if self.test_info.get("wccr"):
                wopBaseSettleFXRate = self.accurate_format_fxrate(wopSettleFXRate / (1+self.test_info['wccr']))

            amount = dict(wopSettleAmount=wopSettleAmount, wopSettleFXRate=wopSettleFXRate,wopBaseSettleFXRate=wopBaseSettleFXRate)

        elif type == 'wopSettleCurrency==billingCurrency':
            billingBaseFXRate = amount['wopSettleFXRate']
            if self.test_info.get("cccr"):
                billingFXRate = billingBaseFXRate * (1+self.test_info['cccr'])
                billingAmount = amount['wopSettleAmount'] * (1+self.test_info['cccr'])
            else:
                billingFXRate = billingBaseFXRate
                billingAmount = amount['wopSettleAmount']
            billingFXRate = self.accurate_format_fxrate(billingFXRate)
            billingAmount = self.accurate_format_transamount(billingAmount, self.billingCurrency)

            amount = dict(billingAmount=billingAmount,billingFXRate=billingFXRate,billingBaseFXRate=billingBaseFXRate)

        elif type == 'mopSettleCurrency==wopSettleCurrency':
            wopBaseSettleFXRate = amount['mopSettleFXRate']
            if self.test_info.get("wccr"):
                wopSettleFXRate = wopBaseSettleFXRate * (1+self.test_info['wccr'])
                wopSettleAmount = amount['mopSettleAmount'] * (1+self.test_info['wccr'])
            else:
                wopSettleFXRate = wopBaseSettleFXRate
                wopSettleAmount = amount['mopSettleAmount']
            wopSettleFXRate = self.accurate_format_fxrate(wopSettleFXRate)
            wopSettleAmount = self.accurate_format_transamount(wopSettleAmount, self.wopSettleCurrency)
            amount = dict(wopSettleAmount=wopSettleAmount, wopSettleFXRate=wopSettleFXRate,wopBaseSettleFXRate=wopBaseSettleFXRate)

        elif type == 'wopSettleCurrency!=billingCurrency':
            # 计算wop侧金额wopBaseSettleFXRate、wopSettleFXRate、wopSettleAmount
            billing_fx_rate = self.get_fx_rate(self.wopSettleCurrency, self.billingCurrency)
            billing_fx_rate = self.accurate_format_fxrate(billing_fx_rate)

            if self.test_info.get("cccr"):
                billingAmount = amount['wopSettleAmount'] * billing_fx_rate* (1 + self.test_info['cccr'])
            else:
                billingAmount = amount['wopSettleAmount'] * billing_fx_rate

            billingAmount = self.accurate_format_transamount(billingAmount, self.billingCurrency)

            billingFXRate = self.accurate_format_fxrate(billingAmount / transAmount)
            billingBaseFXRate = billingFXRate
            if self.test_info.get("cccr"):
                billingBaseFXRate = self.accurate_format_fxrate(billingFXRate/(1+self.test_info['cccr']))

            amount = dict(billingAmount=billingAmount,billingFXRate=billingFXRate,billingBaseFXRate=billingBaseFXRate)

        return amount


    def mongo_assert(self,calculate_value,mongo_actulal,expect_value):
        calculate_value.update(expect_value)
        total_expect = calculate_value
        log.debug(f'total_expect的值为{total_expect}')
        try:
            for each in total_expect:
                assert total_expect[each] == mongo_actulal[each]
            option_fxrate_params = ['mopBaseSettleFXRate','mopSettleFXRate','mopSettleSourceCurrency','mopSettleDestinationCurrency','mccr',
                                    'wopBaseSettleFXRate','wopSettleFXRate','wopSettleSourceCurrency','wopSettleDestinationCurrency','wccr',
                                    'billingFXRate', 'billingBaseFXRate', 'billingSourceCurrency','billingDestinationCurrency', 'cccr',
                                    ]
            for each in option_fxrate_params:
                if each not in total_expect:
                    assert each not in mongo_actulal
        except AssertionError as e:
            log.error("字段值存储的有误")
            raise e


    def get_fx_rate(self,sourcecurrency,destinationcurrency,transtype='payment'):
        if not self.fxRateOwner:
            self.fxRateOwner = "auto_user"
        if transtype == 'transfer':
            ask="bid"
            bid="ask"
        else:
            ask = "ask"
            bid="bid"

        ratemiddle_syboml = False
        fx_rate = None
        #先去fx_rate表中获得正向汇率
        query_fx_rate = {"ccy1":sourcecurrency,"ccy2":destinationcurrency,"fxRateOwner":self.fxRateOwner}
        result = db_tyo_evoconfig.get_one("fx_rate",query_fx_rate)
        if result:
            fx_rate = result[ask]
        else:
            # 再次获取反向汇率
            query_fx_rate = {"ccy1": destinationcurrency, "ccy2": sourcecurrency, "fxRateOwner": self.fxRateOwner}
            result_reverse = db_tyo_evoconfig.get_one("fx_rate", query_fx_rate)
            if result_reverse:
                fx_rate = 1 / result_reverse[bid]
            else:
                #去取中间汇率
                ratemiddle_syboml = True

        #中间汇率取值的四种情况
        if ratemiddle_syboml:
            case_one = db_tyo_evoconfig.get_one("fx_rate", {"ccy1": sourcecurrency, "ccy2": "USD", "fxRateOwner": self.fxRateOwner})

            case_two = db_tyo_evoconfig.get_one("fx_rate", {"ccy1": "USD", "ccy2": destinationcurrency, "fxRateOwner": self.fxRateOwner})

            case_three = db_tyo_evoconfig.get_one("fx_rate", {"ccy1": "USD", "ccy2": sourcecurrency, "fxRateOwner": self.fxRateOwner})

            case_four = db_tyo_evoconfig.get_one("fx_rate", {"ccy1": destinationcurrency, "ccy2": "USD", "fxRateOwner": self.fxRateOwner})

            if case_one and case_two:
                fx_rate = case_one[ask] * case_two[ask]

            elif case_one and case_four:
                fx_rate = case_one[ask] * (1 / case_four[bid])

            elif case_three and case_four:
                fx_rate = (1/case_three[bid]) * (1 / case_four[bid])

            elif case_three and case_two:
                fx_rate = (1 / case_three[bid]) * case_two[ask]

        print(fx_rate)
        #返回值为小数后15位
        return fx_rate

    #不同的币种计算出的金额保留小数位不同
    def format_transamount(self,transamount,trancurrency):
        if trancurrency == 'JPY':
            transamount = eval("{:.0f}".format(transamount) + '.0')

        else:
            transamount = eval("{:.2f}".format(transamount))
        return transamount

    #保留几位小数
    def format_fxrate(self,fxrate,n=4):
        fxrate = eval('{fxrate:.{n}f}'.format(fxrate=fxrate,n=n))
        return fxrate

    # 不同的币种计算出的金额保留小数位不同
    def accurate_format_transamount(self,transamount,trancurrency):
        if trancurrency in ['JPY','KRW'] :
            transamount = Decimal(str(transamount)).quantize(Decimal("1."),rounding="ROUND_HALF_UP")
            transamount = eval('{}.0'.format(transamount))

        else:
            transamount = Decimal(str(transamount)).quantize(Decimal("0.01"),rounding="ROUND_HALF_UP")
            transamount = eval('{}'.format(transamount))
        return transamount

    #保留几位小数的方法，用0填充，返回字符串，比如传入int:1，返回str:1.0000
    def accurate_format_fill_fxrate(self,bid,n=4,fill=True):
        n = '0.0' +(n-2)*'0'+'1'
        bid = Decimal(str(bid)).quantize(Decimal(n),rounding="ROUND_HALF_UP")
        if fill:
            self.fill_str(bid)
        return str(bid)

    def fill_str(self,bid,n=4):
        bid = '{bid:0.{n}f}'.format(bid=bid,n=n)
        return bid


    #保留几位小数的方法,返回小数
    def accurate_format_fxrate(self,fxrate):
        fxrate = str(fxrate)
        fxrate = Decimal(str(fxrate)).quantize(Decimal("0.0001"),rounding="ROUND_HALF_UP")
        fxrate = eval('{}'.format(fxrate))
        return fxrate


class get_config_currency:
    def __init__(self,head_params):
        self.head_params = head_params
    def get(self):
        config = {}
        wop_query_params = {"baseInfo.wopID":self.head_params['wopParticipantID']}
        wop_result = db_tyo_evoconfig.get_one("wop",wop_query_params)
        mop_query_params = {"baseInfo.mopID":self.head_params['mopParticipantID']}
        mop_result = db_tyo_evoconfig.get_one("mop",mop_query_params)
        customizeConfig_query_params = {"mopID": self.head_params['mopParticipantID']}
        customizeConfig_result = db_tyo_evoconfig.get_one("customizeConfig",customizeConfig_query_params)
        if wop_result:
            billingCurrency = wop_result['settleInfo']['billingCurrency']
            wopSettleCurrency = wop_result['settleInfo']['settleCurrency']
            isBillingAmountCalculated = wop_result['settleInfo']['isBillingAmountCalculated']
            temp = dict(billingCurrency=billingCurrency,wopSettleCurrency=wopSettleCurrency,isBillingAmountCalculated=isBillingAmountCalculated)
            config.update(temp)
        if mop_result:
            mopSettleCurrency = wop_result['settleInfo']['settleCurrency']
            temp = dict(mopSettleCurrency=mopSettleCurrency)
            config.update(temp)
        if customizeConfig_result:
            wopSettleCurrency = customizeConfig_result["settleCurrency"]
            mopSettleCurrency = customizeConfig_result["settleCurrency"]
            if customizeConfig_result["settleCurrency"]:
                isSettlementAmountEVONETCalculated = customizeConfig_result["isSettlementAmountEVONETCalculated"]
            else:
                isSettlementAmountEVONETCalculated = True
            temp = dict(wopSettleCurrency=wopSettleCurrency,mopSettleCurrency=mopSettleCurrency,isSettlementAmountEVONETCalculated=isSettlementAmountEVONETCalculated)
            config.update(temp)
        return config


if __name__ == '__main__':
    # data_file = ReadFile().read_data_file("evopay_evonet_cpmpayment", "QR_single_node_mode", "evopay")
    # cpmpayment_testdata = ReadCSV(data_file).read_data()
    # test_info = eval(cpmpayment_testdata[0]['check_mongo_expected'])
    # print(type(test_info))
    # eg = amount_check(test_info)
    # print(eg.accurate_ormat_fxrate(1.23565656565))
    # print(type(eg.accurate_accurate_format_fxrate(1.23565656565)))
    # print(eg.accurate_format_transamount(23.333,'JPY'))
    # print(type(eg.accurate_format_transamount(23.333, 'JPY')))
    wop_query_params = {"baseInfo.wopID": "WOP_Auto_JCoinPay_031"}
    wop_result = db_tyo_evoconfig.get_one("wop", wop_query_params)
    print(wop_result)
    billingCurrency = wop_result['settleInfo']
    billingCurrency = wop_result['settleInfo']['billingCurrency']
    print(billingCurrency)