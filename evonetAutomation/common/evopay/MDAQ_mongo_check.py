import requests

from base.http_request import HttpRequest
from common.evopay.conf_init import db_tyo_evopay, db_tyo_evosettle, db_tyo_evoconfig
from common.evopay.replace_data import multi_replace
from loguru import logger as log
import time,datetime
import copy

class madaq_mongo_check():
    def __init__(self,test_info=None,syboml=True):
        if syboml:
            check_mongo = {"evonetOrderNumber": "#evonetOrderNumber#"}
            self.mongo_query = multi_replace(str(check_mongo))
            query_advice = {"transactionId": "#evonetOrderNumber#"}
            self.query_advice = multi_replace(str(query_advice))
            self.test_info = test_info


    def is_true(self,find_params):
        if find_params:
            return True
        else:
            return False


    def trans_check_success(self,advice=True,fxrate_query=None):
        # ccyPair = "SGD/USD" 现在这个方法默认写死
        # sourceCurrency = "SGD"
        # 数据库trans查询此笔交易属于MDAQ的trans表中fxRateSource,fxRateRefId,fxRateCcyPair
        trans_params_mdaq = ['fxRateRefId','fxRateSource','fxRateCcyPair']
        self.mongo_result_trans = db_tyo_evopay.get_one(table='trans', query_params=eval(self.mongo_query))

        # 数据库fxrate查询正在使用的MDAQ的汇率
        if not fxrate_query:
            fxrate_query = {"fxRateSource": "MDAQ", "ccyPair": "SGD/USD","ccy1" : "SGD"}
        self.fxrate_result = db_tyo_evoconfig.get_one(table='fx_rate', query_params=fxrate_query)
        fxrate_params_mdaq = ['refID',"MDAQ","ccyPair"]

        try:
            if advice:
                for item in zip(trans_params_mdaq,fxrate_params_mdaq):
                    a = self.mongo_result_trans[item[0]]
                    b = self.fxrate_result[item[1]]
                    assert self.mongo_result_trans[item[0]] == self.fxrate_result[item[1]]
                else:
                    for each in fxrate_params_mdaq:
                        if each in self.mongo_result_trans:
                            assert False
        except AssertionError as e:
            print("Mdaq trans表中校验错误")
            raise e


    def trans_message_check(self,head_params,add_advice=True):


        try:
            self.mongo_result_transmessage = db_tyo_evopay.get_one(table='trans_message',
                                                                   query_params=eval(self.mongo_query))
            basic_params = ["beneficiary","settleDate","transType","createTime"]
            if not add_advice:
                assert self.mongo_result_transmessage
            else:
                actual_wopID ,actual_mopID= head_params["wopParticipantID"],head_params["mopParticipantID"]
                for each in basic_params:
                    assert self.is_true(self.mongo_result_transmessage[each])

                assert self.mongo_result_transmessage['wopID'] == actual_wopID
                assert self.mongo_result_transmessage['mopID'] == actual_mopID

                # trans_message和trans里面的字段值进行对比
                common_trans_message_advice = ["wopSettleCurrency", "wopSettleAmount", "mopSettleCurrency",
                                               "mopSettleAmount","evonetPayTime"]
                for each in common_trans_message_advice:
                    assert self.mongo_result_trans[each] == self.mongo_result_transmessage[each]

        except AssertionError as e:
            print("数据库校验失败")
            raise e


    def advice_initial_check(self,add_advice=True):
        try:

            self.mongo_result_advice = db_tyo_evosettle.get_one(table='advice', query_params=eval(self.query_advice))

            advice_basic = ["adviceType","adviceId","transactionId","transactionCcyType","clientRef","settleDate",
                                "reconFlag","createTime","updateTime","adviceTime","transactionTimestamp"]
            if add_advice:

               #获取transactionCcy，consumerCcy，amount的值
                transactionCcy = self.mongo_result_trans['mopSettleCurrency']
                consumerCcy = self.mongo_result_trans['wopSettleCurrency']
                amount = self.mongo_result_trans['mopSettleAmount']

                #获取ccyPair,refID实际的值
                ccyPair_conbines = [str(transactionCcy)+'/'+str(consumerCcy),str(consumerCcy)+'/'+str(transactionCcy)]
                raw_fx_rates_current = db_tyo_evosettle.get_many(table="raw_fx_rate_current",query_params={"fxRateSource" : "MDAQ"})
                for item in raw_fx_rates_current:
                    if item['ccyPair'] in ccyPair_conbines:
                        ccyPair = item['ccyPair']
                        requestedPricingRefId = item['refID']

                #获取expectValueDate实际的值
                evonetPayTime = self.mongo_result_advice["evonetPayTime"]
                dt_actual = datetime.timedelta(days=1) + evonetPayTime
                expectValueDate = dt_actual.__format__("%Y%m%d")

                # 获取transactionType实际的值
                transmessag_transtype = self.mongo_result_transmessage["transType"]
                if transmessag_transtype in ["Refund","Cancellation"]:
                    transactionType = 'REFUND'
                else:
                    transactionType = 'SALE'

                common_params = ["requestedPricingRefId","ccyPair","amount","transactionCcy","consumerCcy","expectValueDate","transactionType"]
                actual_params_value = [(i,eval(i)) for i in common_params]
                # 断言
                for each in advice_basic:
                    assert self.is_true(self.mongo_result_advice[each])
                for each in actual_params_value:
                    assert self.mongo_result_advice[each[0]] == each[1]

                # 获取docstatus的值
                if 'traceID' in self.mongo_result_advice:
                    actual_docStatus = ["IN_PROGRESS", "VALID","INVALID"]
                    assert self.mongo_result_advice["docStatus"] in actual_docStatus
                else:
                    actual_docStatus = "INITIAL"
                    assert self.mongo_result_advice["docStatus"] == actual_docStatus
            else:
                assert self.mongo_result_advice



        except AssertionError as e:
            print("数据库校验失败")
            raise e


    def advice_result_check(self,requestid=False,**kwargs):
        if not requestid:
            # 数据库fxrate查询正在使用的MDAQ的汇率
            fxrate_query = {"fxRateSource": "MDAQ", "ccy1": "SGD","ccy2": "USD"}
            requestid = db_tyo_evoconfig.get_one(table='fx_rate', query_params=fxrate_query)['refID']

        if kwargs:
            result = db_tyo_evosettle.get_one(table="advice",query_params={"transactionId":kwargs['evonetorderNum']})
            log.debug(f"查询到的result为{result}")
            try:
                if 'refund_inqy' in kwargs and result["docStatus"] == "IN_PROGRESS":
                    return result['evonetorderNum']
                else:
                    result["docStatus"] = kwargs["docStatus"]
                    result["status"] = kwargs["docStatus"]
                    assert result["requestedPricingRefId"] == requestid

            except AssertionError as e:
                print("数据库advice表docstatus校验错误,批量提交advice表不为IN_PROGRESS状态")
                raise e





    def advice_batch_check(self,traceID,actual_count,**kwargs):
        #batchId 笔数的判断
        #判断笔数
        try:

            seq = ['validCount', 'inValidCount', 'inProgressCount', 'total']
            dict = {}
            dict = dict.fromkeys(seq,0)

            if actual_count<100:
                mongo_advice_batch = db_tyo_evosettle.get_one(table='advice_batch', query_params={"traceID": traceID})
                for i in seq:
                    dict[i] = mongo_advice_batch[i]
                assert dict['validCount']+dict['inValidCount']+dict['inProgressCount'] == dict['total']
                assert actual_count == dict['total']

            else:
                mongo_result = []
                mongo_advice_batch = db_tyo_evosettle.get_many(table='advice_batch', query_params={"traceID": traceID})
                for item in mongo_advice_batch:
                    mongo_result.append(item)
                # 判断生成batchs笔数
                length = len(mongo_result)

                acual_batchs = actual_count // 100
                if actual_count % 100:
                    acual_batchs = acual_batchs + 1
                log.debug(f'length为{length}')
                log.debug(f'acual_batchs为{acual_batchs}')
                assert length == acual_batchs

                # 多笔batch判断batchId是否重复
                batchId_count = len(set([each["batchId"] for each in mongo_result]))
                assert batchId_count == acual_batchs

                # 判断交易数
                for mongo_each in  mongo_result:
                    for key,value in dict.items():
                        dict[key] = mongo_each[key] + value

                assert dict['total'] == actual_count
                assert dict['validCount']+dict['inValidCount']+dict['inProgressCount'] == dict['total']

            #是否校验inValidCount,inValidCount,inProgressCount期待值

            if kwargs:
                for key in kwargs:
                    assert dict[key] == kwargs[key]

        except AssertionError as e:
            print("advice_batch表校验失败")
            raise e

    def task(self,task_name, task_handler,time=None):
        # 触发批量提交上送定时任务如果返回失败则重试三次
        task_request = HttpRequest()
        result = task_request.mdaq_task_request(task_name, task_handler,time)
        res = result.json()
        times = 1
        while times <= 3:
            if res['status'] == 'success':
                break
            times += 1
        try:
            if res['status'] == 'success':
                return res['traceID']

        except AssertionError as e:
            print("定时任务触发失败")


    def delete_transmessage_advice(self,times=None):
        settdate_time = time.localtime()
        year = settdate_time.tm_year
        month = settdate_time.tm_mon
        day = settdate_time.tm_mday
        settdate_time = str(year)+'{:0>2d}'.format(month)+'{:0>2d}'.format(day)
        transmessage_query_params = {"settleDate" : settdate_time,}
        advice_query_params = {"docStatus" : "INITIAL",}
        db_tyo_evosettle.delete_manys("trans_message",transmessage_query_params)
        db_tyo_evosettle.delete_manys("advice",advice_query_params)

if __name__ == '__main__':
    # time = datetime.datetime.today()
    # res = madaq_mongo_check().mdaq_request("MDaqSubmitBatchAdvice","MDaqSubmitBatchAdvice",time)
    # print(res)
    # query_advice = {"transactionId": "729440955798729638"}
    #
    # mongo_result_advice = db_tyo_evosettle.get_one(table='advice', query_params=query_advice)
    # evonetPayTime = mongo_result_advice["evonetPayTime"]
    # dt_actual = datetime.timedelta(days=1) + evonetPayTime
    # expectValueDate_actual = dt_actual.__format__("%Y%m%d")
    # print(expectValueDate_actual)

    mongo_advice_batch = db_tyo_evosettle.get_many(table='advice_batch', query_params={'traceID': '732905557983245180'})
    ll =  copy.deepcopy(mongo_advice_batch )

    mongo_advice_batch1 = [{"validCount": 1, "inValidCount": 3, "total": 4, "inProgressCount": 0},
                          {"validCount": 2, "inValidCount": 3, "total": 5, "inProgressCount": 0}]
    print(type(mongo_advice_batch))

    for each in mongo_advice_batch:
        print(each)
        print(1)

    p = mongo_advice_batch.count()


    print("-----------------------------------------")
    print(type(mongo_advice_batch))
    for each in ll:
        print(each)
        # for i in mongo_advice_batch1:
        #     print(i)
    # for i in mongo_advice_batch:
    #     print(i)
















