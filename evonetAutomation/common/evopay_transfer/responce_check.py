class responce_check():
    def is_true(self,data_params):
        if data_params:
            return True

        if data_params in [False,True]:
            return True

        else:
            return False

    def response_verify(self,interface,result):
        if interface == 'PreOrder':
            preorder_success = ['evonetOrderNumber','evonetOrderDatetime']
            if result["result"]["code"] in ['S0000','S0005']:
                for each in preorder_success:
                    assert self.is_true(result[each]) == True
            else:
                preorder_fail = ['sendAmount','transferFee','senderTotalAmount','settleAmount','receiveAmount','fxRate']
                for each in preorder_success:
                    assert self.is_true(result[each]) == False
                for each in preorder_fail:
                    assert self.is_true(result[each]) == False
