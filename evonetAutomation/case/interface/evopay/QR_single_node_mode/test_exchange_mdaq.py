import pytest

from base.read_file_path import ReadFile
from case.interface.evopay.QR_single_node_mode.test_paymentinquiry import Testpaymentinquiry as test_paymentinquiry_sample
from common.evopay.conf_init import db_tyo_evopay
from common.evopay.read_csv import ReadCSV
from loguru import logger as log
from common.evopay.replace_data import multi_replace
from common.evopay.MDAQ_mongo_check import madaq_mongo_check
from base.trans_message_insert import trans_message_insert

data_file=ReadFile().read_data_file("evopay_evonet_exchange_mdaq","QR_single_node_mode","evopay")
exchange_testdata=ReadCSV(data_file).read_data()

submit_test_cases = [
    ("start_task", 'SALE', 1, 'REFUND', 1),
    ("start_task", 'SALE', 101, 'REFUND', 0),
    ("start_task", 'SALE', 230, 'REFUND', 50)
]
class Testexchange():
    def __init__(self,envirs):
        self.envirs=envirs

    @pytest.mark.parametrize("test_info",exchange_testdata)
    def testexchange(self, test_info):
        if test_info["interface"] != 'start_task':
            testexchangemdaq = test_paymentinquiry_sample(self.envirs)
            result,traceID,body_params,head_params = testexchangemdaq.test_paymentinquiry(test_info)
            log.debug(f'result是{result},traceID是{traceID}')
            if result['result']['code'] == 'S0000' and test_info["interface"] not in ['CPM Token','MPM QR Verification','MPM Payment Authentication']:
                trans_sample = madaq_mongo_check()
                trans_sample.trans_check_success()
                trans_sample.trans_message_check(head_params)
                trans_sample.advice_initial_check()

            else:
                add_advice = False
                trans_sample = madaq_mongo_check()

#################################################################################################################################
    # 运行批量上送等相关case
    @pytest.mark.parametrize('title, transtype, transtime, transtypes, transtimes', submit_test_cases)
    def submit_test_cases(self,title, transtype, transtime, transtypes, transtimes):
        forward_evonetorderNum = []
        reforward_evonetorderNum = []
        trans_sample = madaq_mongo_check(syboml=False)


        if title == "start_task":
            if transtime == 1 and transtimes == 1 :
                trans_sample.delete_transmessage_advice()
                evonetorderNum = trans_message_insert().create_sale_trans(n=transtime)
                forward_evonetorderNum.append(evonetorderNum)
                originalevonetorderNum,refundevonetorderNum = trans_message_insert().creat_refund_trans(n=transtimes)
                forward_evonetorderNum.append(originalevonetorderNum)
                reforward_evonetorderNum.append(refundevonetorderNum)

                #获得提交上送定时任务返回的traceid

                traceID = trans_sample.task("MDaqSubmitBatchAdvice", "SubmitBatchAdvice")

                # 校验批量提交返回之后advice表订单的状态
                for evonetorderNum in forward_evonetorderNum:
                    trans_sample.advice_result_check(evonetorderNum=evonetorderNum,docStatus='IN_PROGRESS',type='SALE')
                for refundevonetorderNum in reforward_evonetorderNum:
                    trans_sample.advice_result_check(evonetorderNum=refundevonetorderNum,docStatus='IN_PROGRESS',type='REFUND')

                # 校验批量提交返回之后batch表
                trans_sample.advice_batch_check(traceID,3,inProgressCount=3)

                # 触发批量batch查询上送定时任务
                trans_sample.task("MDaqQueryBatchAdvice", "QueryBatchAdvice")
                # 校验批量提交返回之后advice表订单的状态
                for i in forward_evonetorderNum:
                    trans_sample.advice_result_check(evonetorderNum=i, docStatus='VALID')
                for i in reforward_evonetorderNum:
                    ordernum = trans_sample.advice_result_check(evonetorderNum=i, docStatus='VALID',refund_inqy=True)
                # 校验批量提交返回之后batch表
                if not ordernum:
                    trans_sample.advice_batch_check(traceID,3,validCount=2, inProgressCount=1)
                times=0
                while ordernum:
                    trans_sample.advice_batch_check(traceID,validCount=2,inProgressCount=1)
                    traceID = trans_sample.task("MDaqQueryBatchAdvice", "QueryBatchAdvice")
                    ordernum = trans_sample.advice_result_check(evonetorderNum=ordernum, docStatus='VALID', refund_inqy=True)
                    times = times+1
                    if times >=5:
                        break
            elif transtime == 101 :
                trans_message_insert().create_sale_trans(n=transtime)
                # 获得提交上送定时任务返回的traceid
                traceID = trans_sample.task("MDaqSubmitBatchAdvice", "SubmitBatchAdvice")
                # 校验批量提交返回之后batch表
                trans_sample.advice_batch_check(traceID,actual_count=101,inProgressCount=101)
                # 触发批量batch查询上送定时任务
                trans_sample.task("MDaqQueryBatchAdvice", "QueryBatchAdvice")
                trans_sample.advice_batch_check(traceID,101, validCount=101)

            elif transtime == 230 and transtimes == 50:
                trans_message_insert().creat_refund_trans(n=transtimes)
                trans_message_insert().create_sale_trans(n=transtime)
                # 获得提交上送定时任务返回的traceid
                traceID = trans_sample.task("MDaqSubmitBatchAdvice", "SubmitBatchAdvice")
                # 校验批量提交返回之后batch表
                trans_sample.advice_batch_check(traceID,330,inProgressCount=330)
                # 触发批量batch查询上送定时任务
                trans_sample.task("MDaqQueryBatchAdvice", "QueryBatchAdvice")
                trans_sample.advice_batch_check(traceID,330, validCount=280,inProgressCount=50)



















