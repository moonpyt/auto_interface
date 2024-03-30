class mongo_verify():
    def is_true(self,data_params):
        if data_params:
            return True
        if data_params in [False,True]:
            return True
        else:
            return False


    # 数据库中除交易金额外其他字段的校验
    def mongo_verify(self,interface,db_data,result):
        if interface == 'PreOrder':
            # 成功的订单所特有的值，且值为不固定的，只能判断这个值是否存在
            trans_success_preorder_exit = ['traceID', 'ropID','sopID','isUsed','evonetOrderNumber','sopOrderNumber', 'sopOrderDatetime', 'participantID', 'location',
                                           'purpose', 'relationship', 'sourceOfFund', 'senderInfo.evonetUserReference','expiryDatetime','sopOrderDatetime','evonetOrderCreateTime'
                                           'evonetOrderUpdateTime','receiverInfo.evonetUserReference']
            trans_fail_preorder_exit = []
            assert db_data['transType'] == 'Online'
            assert db_data['lockFlag'] == int(0)
            assert db_data['apiVersion'] == 'v0'
            if db_data['result']['code'] == 'S0000':
                # 首先检验trans表基础信息
                try:
                    for item in trans_success_preorder_exit:
                        if '.' in item:
                            item = item.split('.')
                            assert self.is_true(db_data[item[0]][db_data[item[1]]]) == True
                        else:
                            assert self.is_true(db_data[item]) == True
                    assert db_data['result']['code'] ==  result['result']['code']
                    assert db_data['result']['message'] == ['result']['message']
                    assert db_data['status'] == 'processing'
                    assert db_data['sopStatus'] == 'processing'
                    assert db_data['ropStatus'] == 'processing'

                except AssertionError as e:
                    print('CPM Payment失败的交易trans表检验失败')
                    raise e
            else:
                try:
                    for item in trans_fail_preorder_exit:
                        assert self.is_true(db_data[item]) == True
                    assert db_data['status'] == 'failed'
                    assert db_data['sopStatus'] == 'failed'
                    assert db_data['ropStatus'] == 'failed'
                except AssertionError as e:
                    print('CPM Payment失败的交易trans表检验失败')
                    raise e
        if interface == 'order':
            if result['ropOrderStatus'] == 'failed':
                assert db_data['status'] == 'failed'
                assert db_data['sopStatus'] == 'failed'
                assert db_data['ropStatus'] == 'failed'
                assert db_data['result']['code'] == result['result']['code']
                assert db_data['result']['message'] == result['result']['message']

            if result['ropOrderStatus'] == 'failed':
                assert db_data['status'] == 'failed'
                assert db_data['sopStatus'] == 'failed'
                assert db_data['ropStatus'] == 'failed'
                assert db_data['result']['code'] == result['result']['code']
                assert db_data['result']['message'] == result['result']['message']

            if result['ropOrderStatus'] == 'Processing':
                assert db_data['status'] == 'Processing'
                assert db_data['sopStatus'] == 'Processing'
                assert db_data['ropStatus'] == 'Processing'
                assert db_data['result']['code'] == result['result']['code']
                assert db_data['result']['message'] == result['result']['message']









