from common.evopay.replace_data import multi_replace
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_tyo_evoconfig, db_tyo_evologs, db_sgp_evopay,db_sgp_evologs

from loguru import logger as log

class mongo_restore_billing_settle_rate:
    
    def billing_settle_rate(self,mongo_result,test_info,head_params,body_params,traceID,node='single'):
        try:
            mongo_expected = multi_replace(str(test_info['check_mongo_expected']))

                
            if 'wopID' in mongo_expected:
                mongo_wop = mongo_result['wopID']
                mongo_mop = mongo_result['mopID']
                assert eval(mongo_expected)["wopID"] == mongo_wop
                assert eval(mongo_expected)["mopID"] == mongo_mop
    
            elif 'status' in mongo_expected:
                mongo_status = mongo_result['status']
                assert eval(mongo_expected)["status"] == mongo_status
                if test_info['interface'] == 'CPM Payment':
                    mongo_wopStatus = mongo_result['wopStatus']
                    mongo_mopStatus = mongo_result['mopStatus']
                    assert eval(mongo_expected)["wopStatus"] == mongo_wopStatus
                    assert eval(mongo_expected)["mopStatus"] == mongo_mopStatus


    
    
            elif 'mopConverterCurrencyFlag' in mongo_expected:
                mongo_mopConverterCurrencyFlag = mongo_result['mopConverterCurrencyFlag']
                mongo_wopConverterCurrencyFlag = mongo_result['wopConverterCurrencyFlag']
                assert eval(mongo_expected)[
                           'mopConverterCurrencyFlag'] == mongo_mopConverterCurrencyFlag
                assert eval(mongo_expected)[
                           'wopConverterCurrencyFlag'] == mongo_wopConverterCurrencyFlag
                if test_info['interface'] == 'CPM Payment':
                    mongo_billingConverterCurrencyFlag = mongo_result['billingConverterCurrencyFlag']
                    assert eval(mongo_expected)['billingConverterCurrencyFlag'] == mongo_billingConverterCurrencyFlag

                
                
            elif 'mopSettleAmount' and 'wopSettleAmount' in mongo_expected:
                mopSettleAmount = mongo_result['mopSettleAmount']
                mopSettleCurrency = mongo_result['mopSettleCurrency']
                wopSettleAmount = mongo_result['wopSettleAmount']
                wopSettleCurrency = mongo_result['wopSettleCurrency']
                assert eval(mongo_expected)['mopSettleAmount'] == mopSettleAmount
                assert eval(mongo_expected)['mopSettleCurrency'] == mopSettleCurrency
                assert eval(mongo_expected)['wopSettleAmount'] == wopSettleAmount
                assert eval(mongo_expected)['wopSettleCurrency'] == wopSettleCurrency
                
                if 'mopSettleFXRate' in  mongo_expected:
                    mopSettleFXRate = mongo_result['mopSettleFXRate']
                    mopSettleSourceCurrency = mongo_result['mopSettleSourceCurrency']
                    mopSettleDestinationCurrency = mongo_result['mopSettleDestinationCurrency']
                    assert eval(mongo_expected)['mopSettleFXRate'] == mopSettleFXRate
                    assert eval(mongo_expected)['mopSettleSourceCurrency'] == mopSettleSourceCurrency
                    assert eval(mongo_expected)['mopSettleDestinationCurrency'] == mopSettleDestinationCurrency
                    if 'mopBaseSettleFXRate' in mongo_expected:
                        mopBaseSettleFXRate = mongo_result['mopBaseSettleFXRate']
                        assert eval(mongo_expected)['mopBaseSettleFXRate'] == mopBaseSettleFXRate
                    else:
                        if mongo_result['mopConverterCurrencyFlag'] == False:
                            if 'mopBaseSettleFXRate' in mongo_result:
                                raise AssertionError
                        
                    if 'mccr' in mongo_expected:
                        mccr = mongo_result['mccr']
                        assert eval(mongo_expected)['mccr'] == mccr
                        
                else:
                    if mongo_result['mopConverterCurrencyFlag'] == False:
                        if ('mopSettleFXRate' in mongo_result)or ('mopSettleSourceCurrency' in mongo_result):
                            raise AssertionError
                    
          
    
                if 'wopSettleFXRate' in mongo_expected:
                    wopSettleFXRate = mongo_result['wopSettleFXRate']
                    wopSettleSourceCurrency = mongo_result['wopSettleSourceCurrency']
                    wopSettleDestinationCurrency = mongo_result['wopSettleDestinationCurrency']
                    assert eval(mongo_expected)['wopSettleFXRate'] == wopSettleFXRate
                    assert eval(mongo_expected)['wopSettleSourceCurrency'] == wopSettleSourceCurrency
                    assert eval(mongo_expected)['wopSettleDestinationCurrency'] == wopSettleDestinationCurrency
                    if 'wopBaseSettleFXRate' in mongo_expected:
                        wopBaseSettleFXRate = mongo_result['wopBaseSettleFXRate']
                        assert eval(mongo_expected)['wopBaseSettleFXRate'] == wopBaseSettleFXRate
                    else:
                        if mongo_result['wopConverterCurrencyFlag'] == False:
                            if 'wopBaseSettleFXRate' in mongo_result:
                                raise AssertionError
    
                    if 'wccr' in mongo_expected:
                        mccr = mongo_result['mccr']
                        assert eval(mongo_expected)['mccr'] == mccr
    
                else:
                    if mongo_result['wopConverterCurrencyFlag'] == False:
                        if ('wopSettleFXRate' in mongo_result) or ('wopSettleSourceCurrency') in  mongo_result:
                            raise AssertionError
    
                if "billingAmount" in mongo_expected:
                    billingAmount = mongo_result['billingAmount']
                    billingCurrency = mongo_result['billingCurrency']
                    assert eval(mongo_expected)['billingAmount'] == billingAmount
                    assert eval(mongo_expected)['billingCurrency'] == billingCurrency
                    if 'billingFXRate' in mongo_expected:
                        billingFXRate = mongo_result['billingFXRate']
                        billingSourceCurrency = mongo_result['billingSourceCurrency']
                        billingDestinationCurrency = mongo_result['billingDestinationCurrency']
                        assert eval(mongo_expected)['billingDestinationCurrency'] == billingDestinationCurrency
                        assert eval(mongo_expected)['billingFXRate'] == billingFXRate
                        assert eval(mongo_expected)['billingSourceCurrency'] == billingSourceCurrency
                    if 'billingBaseFXRate' in mongo_expected:
                        billingBaseFXRate = mongo_result['billingBaseFXRate']
                        assert eval(mongo_expected)['billingBaseFXRate'] == billingBaseFXRate
                    if 'cccr' in mongo_expected:
                        cccr = mongo_result['cccr']
                        assert eval(mongo_expected)['cccr'] == cccr
                else:
                    if mongo_result['billingConverterCurrencyFlag'] == False:
                        if  'billingFXRate' in mongo_result or 'billingSourceCurrency' in mongo_result:
                            raise AssertionError
                        

            elif 'SettleDate' in mongo_expected:
                if node== 'single':
                    mongo_result_wop = db_tyo_evoconfig.get_one(table='wop', query_params={
                        'baseInfo.wopID': head_params['wopParticipantID']})
                    cutofftime = (mongo_result_wop['settleInfo']['cutoffTime'])[0:5]
                    cutofftime = cutofftime[0:2] + cutofftime[3:5]
                    if int(cutofftime) > int(1200):
                        mongo_expected_settdate = eval(multi_replace(str(test_info['check_mongo_expected'])))[
                            "cutofftime_over_UTC_12:00"]
                    else:
                        mongo_expected_settdate = eval(multi_replace(str(test_info['check_mongo_expected'])))[
                            "cutofftime_less_UTC_12:00"]
                    # 获取测试案例中的清算日期
                    mongo_expected_mopsettledate = mongo_expected_settdate['mopSettleDate']
                    mongo_expected_wopsettledate = mongo_expected_settdate['mopSettleDate']
                    # 获取数据库中的清算日期
                    mongo_result_mopsettledate = mongo_result['mopSettleDate']
                    mongo_result_wopsettledate = mongo_result['wopSettleDate']

                    # 断言清算日期
                    assert mongo_expected_mopsettledate == mongo_result_mopsettledate
                    assert mongo_expected_wopsettledate == mongo_result_wopsettledate
            else:
                print("无数据库检验")

        except AssertionError as e:
            log.debug(f'用例执行未通过,请求参数为{body_params}')
            print("用例：{}--数据库校验未通过,traceID为{}".format(test_info["title"], traceID))
            raise e

        else:
            print("用例：{}--数据库校验通过或者无校验,traceID为{}".format(test_info["title"], traceID))





    