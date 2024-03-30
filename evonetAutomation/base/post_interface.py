from base.http_request import HttpRequest
from common.evopay.check_partner_sign import CheckSign
from common.evopay.mongo_data import Update_Mongo_Data
from common.evopay.moudle import Moudle
from common.evopay.replace_data import multi_replace
from common.evopay.conf_init import evopay_conf, db_tyo_evopay, db_sgp_evopay, db_sgp_evologs,db_tyo_evologs
from base.amount_check import amount_check


class post_interface():
    def post_request(self,body_params,conf_params,test_info={},node='single'):
        check_sign_url = conf_params['url']
        base_url = evopay_conf.base_url_wop
        url = base_url + check_sign_url
        # 获取method
        method = conf_params['method']
        # 判断是否有数据进行替换,获取body
        data = multi_replace(str(body_params))

        # 获取url需要的各项参数
        datetime = Moudle().create_datetime()
        header_method = method.upper()
        msgID = Moudle().create_msgId()
        # 获取participantID，替换数据
        participantID = conf_params['participantID']

        if node == 'single':
            pre_update_database = 'tyo'

        if test_info.get('pre-update table'):
            if test_info['pre-update mongo']:
                if '&' in test_info['pre-update table']:
                    pre_update_table = test_info['pre-update table'].split('&')
                    pre_query_mongo = test_info['pre-query mongo'].split('&')
                    pre_update_mongo = test_info['pre-update mongo'].split('&')
                    length = len(pre_update_table)
                else:
                    length = 1
                    pre_update_table = test_info['pre-update table'].split('$')
                    pre_query_mongo = test_info['pre-query mongo'].split('$')
                    pre_update_mongo = test_info['pre-update mongo'].split('$')

                for i in range(length):
                    Update_Mongo_Data(node=node, database=pre_update_database).updata_data(
                        table=pre_update_table[i],
                        query_params=eval(pre_query_mongo[i]),
                        update_params=eval(pre_update_mongo[i]))
            else:
                Update_Mongo_Data(node=node, database=test_info['pre-update database']).delete_data(
                    table=test_info['pre-update table'],
                    query_params=eval(test_info['pre-query mongo']))

        # self,method,url,participantID,msgID,datetime,signkey,data
        header = CheckSign().check_sign_post(method=header_method, url=check_sign_url, participantID=participantID,
                                             msgID=msgID, datetime=datetime, signkey=evopay_conf.signkey, data=data)

        # 发送请求
        res = HttpRequest().send(method=method, url=url, headers=header, json=eval(data))
        result = res.json()
        headers = res.headers

        if test_info.get('pre-update table'):
            if test_info['pre-update mongo']:
                if '&' in test_info['pre-update table']:
                    pre_update_table = test_info['pre-update table'].split('&')
                    pre_query_mongo = test_info['pre-query mongo'].split('&')
                    pre_update_mongo = test_info['pre-update mongo'].split('&')
                    length = len(pre_update_table)
                else:
                    length = 1
                    pre_update_table = test_info['pre-update table'].split('$')
                    pre_query_mongo = test_info['pre-query mongo'].split('$')
                    pre_update_mongo = test_info['pre-update mongo'].split('$')
                for i in range(length):
                    Update_Mongo_Data(node=node, database=pre_update_database).update_data_reset(
                        table=pre_update_table[i],
                        query_params=eval(pre_query_mongo[i]),
                        update_params=eval(pre_update_mongo[i]))
            else:
                Update_Mongo_Data(node=node, database=pre_update_database).delete_data_reset(
                    table=test_info['pre-update table'])

        return res
