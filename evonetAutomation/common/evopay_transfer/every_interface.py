from base.transfer_initial import trans_initial


class every_interface():

    def exteral_post_fxrate(self, **kwargs):
        '''
        发送fxrate请求,以下参数可选，传入形式必须为下
        head_participant=value,body_participant=value,sendCurrency=value,receiveCurrency=value
        '''
        temp = {"interface": "QueryFxRate"}
        body = {}
        if kwargs['head_participant']:
            temp.update({"conf": {"participantID": kwargs['head_participant']}})

        if kwargs['body_participant']:
            body.update({"participantID": kwargs['body_participant']})

        if kwargs['sendCurrency']:
            body.update({"sendCurrency": kwargs['sendCurrency']})

        if kwargs['receiveCurrency']:
            body.update({"receiveCurrency": kwargs['receiveCurrency']})
        temp.update(body)

        initial = trans_initial()
        post_fxrate_result = initial.common_params_init(source='option', node='single', **temp)
        return post_fxrate_result

    def exteral_post_preorder(self, **kwargs):

        '''
        preorder,以下参数可选，传入形式必须为下
        head_participant=value,body_participant=value,sendCurrency=value,receiveCurrency=value
        '''
        temp = {"interface": "QueryFxRate"}
        body = {}
        if kwargs['head_participant']:
            temp.update({"conf": {"participantID": kwargs['head_participant']}})

        if kwargs['body_participant']:
            body.update({"participantID": kwargs['body_participant']})

        result_sop = self.exteral_post_sop_account_create(head_participant=kwargs['body_participant'],
                                                          body_participant=kwargs['body_participant'])
        result_rop = self.exteral_post_rop_account_create(head_participant=kwargs['head_participant'],
                                                          body_participant=kwargs['head_participant'])
        result_fxrate = self.exteral_post_fxrate(**kwargs)
        if kwargs["senderInfo"]['evonetUserReference']:
            body["senderInfo"]['evonetUserReference'] = kwargs["senderInfo"]['evonetUserReference']
        else:
            body["senderInfo"]['evonetUserReference'] = result_sop["senderInfo"]['evonetUserReference']

        if kwargs["receiverInfo"]['evonetUserReference']:
            body["receiverInfo"]['evonetUserReference'] = kwargs["receiverInfo"]['evonetUserReference']
        else:
            body["receiverInfo"]['evonetUserReference'] = result_rop["receiverInfo"]['evonetUserReference']

        if kwargs["fxRate"]:
            body["fxRate"] = kwargs["fxRate"]
        else:
            body["fxRate"] = result_fxrate["fxRate"]
        temp.update(body)

        initial = trans_initial()
        post_preorder_result = initial.common_params_init(source='option', node='single', **temp)
        return post_preorder_result

    def exteral_post_order(self, **kwargs):
        '''
        order,以下参数可选，传入形式必须为下
        head_participant=value,evonetOrderNumber=value
        '''
        temp = {"interface": "order"}
        body = {}
        if kwargs['evonetOrderNumber']:
            body.update({"evonetOrderNumber": kwargs['evonetOrderNumber']})
        else:
            preorder_result = self.exteral_post_preorder(**kwargs)
            body.update({"evonetOrderNumber": preorder_result['evonetOrderNumber']})

        if kwargs['head_participant']:
            temp.update({"conf": {"participantID": kwargs['head_participant']}})

        temp.update(body)
        initial = trans_initial()
        post_order_result = initial.common_params_init(source='option', node='single', **temp)
        return post_order_result

    def exteral_post_sop_account_create(self, **kwargs):
        '''
        sop_account,以下参数可选，传入形式必须为下
        head_participant=value,body_participant=value
        '''
        temp = {"interface": "accountCreate"}
        body = {}
        if kwargs['head_participant']:
            temp.update({"conf": {"participantID": kwargs['head_participant']}})

        if kwargs['body_participant']:
            body.update({"createUserParticipantID": kwargs['body_participant']})
        temp.update(body)
        initial = trans_initial()
        post_account_create_result = initial.common_params_init(source='option', node='single', **temp)
        return post_account_create_result

    def exteral_post_rop_account_create(self, **kwargs):
        '''
        rop_account,以下参数可选，传入形式必须为下
        head_participant=value,body_participant=value
        '''
        temp = {"interface": "accountCreate"}
        body = {}
        if kwargs['head_participant']:
            temp.update({"conf": {"participantID": kwargs['head_participant'],
                                  "url": r"/v0/transfer/rop/account"}})

        if kwargs['body_participant']:
            body.update({"createUserParticipantID": kwargs['body_participant']})
        temp.update(body)
        initial = trans_initial()
        post_account_create_result = initial.common_params_init(source='option', node='single', **temp)
        return post_account_create_result
