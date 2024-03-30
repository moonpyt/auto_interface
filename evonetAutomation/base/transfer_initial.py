from base.post_interface import post_interface
from common.evopay.Initialization import initialization
from common.evopay.common_functions.transfer.transfer_common_values import transfer_common_values
import copy


class trans_initial():
    # 如果source='csv'，为自动化用例，否则为其他接口调用此接口
    # source='csv',test_info字段为必传
    # source！='csv',kwargs可变参数中,接口名字为必传,conf,body可选，格式为{"interface":"QueryFxRate","conf":{},"body":{}}
    # conf为head中需要更改的参数,对应sop,rop.body为需要发起的参数,对应对应sop,rop等相关字段,具体值参考方法中transfer_common_values()
    # 不同接口的iterface为QueryFxRate,PreOrder等

    def common_params_init(self,node='single',source='csv', test_info={},**kwargs):
        if source == 'csv':
            body_params_in_files = "%s%s_%s" % (test_info['interface'], '_body', node)
            conf_params_in_files = "%s%s_%s" % (test_info['interface'], '_conf', node)

            transfer_common_params = transfer_common_values()
            body_params = getattr(transfer_common_params, body_params_in_files)
            conf_params = getattr(transfer_common_params, conf_params_in_files)
            body_params_temp = copy.deepcopy(body_params)
            if test_info['data']:
                test_info['data'] = eval(test_info['data'])
                body_params.update(test_info['data'])
                for key,value in test_info['data'].items():
                    if type(value) == dict:
                        for key1, value1 in value.items():
                            if value1 == None:
                                body_params_temp[key].pop(key1, '404')
                    if value == None:
                        body_params_temp.pop(key,'404')
            body_params = body_params_temp
            if  test_info['conf']:
                temp_conf = eval(test_info['conf'])
                conf_params.update(temp_conf)
            return body_params, conf_params

        else:
            body_params_in_files = "%s%s_%s" % (kwargs['interface'], '_body', node)
            conf_params_in_files = "%s%s_%s" % (kwargs['interface'], '_conf', node)
            transfer_common_params = transfer_common_values()
            body_params = getattr(transfer_common_params, body_params_in_files)
            conf_params = getattr(transfer_common_params, conf_params_in_files)
            if kwargs.get("body"):
                body_params.update(kwargs["body"])
                for key, value in kwargs["body"].items():
                    if value == None:
                        body_params.pop("key", '404')

            if  kwargs.get("conf"):
                conf_params.update(kwargs["conf"])

            post_interface_request = post_interface()
            res = post_interface_request.post_request(body_params,conf_params)
            headers = res.headers
            traceID = headers.get('Traceid')
            result = res.json()
            return result

if __name__ == '__main__':
        a={'sopOrderNumber': '#sopOrderNumber#', 'sopOrderDateTime': '#sopOrderDateTime#',
                    'participantID': 'rop_autotest_online_01', 'location': 'JPN', 'type': 'Online',
                    'purpose': 'E-commerce business dealings', 'relationship': 'business partner',
                    'sourceOfFund': 'wage', 'senderInfo': {'evonetUserReference': '?senderInfo.evonetUserReference?'},
                    'receiverInfo': {'evonetUserReference': '?receiverInfo.evonetUserReference?'},
                    'sendAmount': {'value': '100.00', 'currency': 'CNY'}, 'transferFee': None,
                    'senderTotalAmount': None, 'receiveAmount': {'value': None, 'currency': 'CAD'}, 'fxRate': None,
                    'settleAmount': None}
        a.pop('fxRate',1)
        print(a)
