# -*- coding: utf-8 -*-
class Checkresponse():
    def is_true(self,response_date):
        if response_date:
            return True
        else:
            return False
    #断言MOP Checking接口返回的数据
    def check_MOPChecking_res(self,test_data_interface,response):
        """

        :param test_data_interface: 传入测试案例中的接口
        :param response:request的返回,json格式
        :return:
        """
        try:
            assert (self.is_true(response["result"]["code"] )and self.is_true(response["result"]["message"]) )is True
            if "mopInfo" in str(response):
                for item in (response["mopInfo"]):
                    assert (self.is_true(item["brandName"]) and self.is_true(item["brandID"]) and self.is_true(item["brandLogo"]) and self.is_true(item["mopList"]))==True
                        # assert item["brandName"],item["brandID"],item["brandLogo"] ,item["mopList"]

        except AssertionError as e:
            print("MOP Checking接口返回数据不正常")
            raise e

        # 断言CPM Token接口返回的数据
    def check_CPMToken_res(self, test_data_interface,response):
        try:
            assert (self.is_true(response["result"]["code"]) and self.is_true(response["result"]["message"]))==True
            if "mopToken" in str(response):
                #response["mopToken"]返回的是数组，需要遍历数组
                for item in response["mopToken"]:
                    assert (self.is_true(item["type"]) and self.is_true(item["value"]) and self.is_true(item["expiryDate"]))==True

        except AssertionError as e:
            print("CPM Token返回数据不正常")
            raise e
        # 断言CPM Payment接口返回的数据
    def check_CPMPayment_res(self,test_data_interface,response):
        try:
            assert (self.is_true(response["result"]["code"]) and self.is_true(response["result"]["message"]) and self.is_true(response["evonetOrderNumber"]) and self.is_true(response["evonetOrderCreateTime"]) and self.is_true(response["mopOrderNumber"]) and self.is_true(response["mopTransTime"]) and self.is_true(response["transType"]) ) == True
            if "billingAmount" in str(response):
                assert (self.is_true(response["billingAmount"]["currency"]) and self.is_true(response["billingAmount"]["value"])) == True
            elif "billingFXRate" in str(response):
                assert (self.is_true(response["billingFXRate"]["value"]) and self.is_true(response["billingFXRate"]["sourceCurrency"]) and self.is_true(response["billingFXRate"]["destinationCurrency"]) )== True
            elif "settleAmount" in str(response):
                assert (self.is_true(response["settleAmount"]["currency"]) and self.is_true(response["settleAmount"]["value"])) == True
            elif "settleFXRate" in str(response):
                assert (self.is_true(response["settleFXRate"]["value"]) and self.is_true(response["settleFXRate"]["sourceCurrency"]) and \
                        self.is_true(response["settleFXRate"]["destinationCurrency"])) == True
        except AssertionError as e:
            print("CPM Payment返回数据不正常")
            raise e

    # 断言MPM QR Verification接口返回的数据
    def check_MPMQRVerification_res(self, test_data_interface, response):
        try:
            assert ( self.is_true(response["evonetReference"]) and self.is_true(response["result"]["code"]) and self.is_true(response["result"]["message"])) == True
            if "transAmount" in str(response):
                assert  self.is_true(response["transAmount"]["currency"])==True
            elif "storeInfo" in str(response):
                assert (self.is_true(response["storeInfo"]["id"]) and self.is_true(response["storeInfo"]["localName"]) and self.is_true(response["storeInfo"][
                        "mcc"]))==True
        except AssertionError as e:
            print("MPM QR Verification返回数据不正常")
            raise e

            # 断言MPM Payment Authentication接口返回的数据

    def check_MPMPaymentAuthentication_res(self, test_data_interface, response):
        try:
            assert (self.is_true(response["result"]["code"]) and self.is_true(
                response["result"]["message"]) and self.is_true(response["evonetReference"]) and self.is_true(
                response["evonetOrderNumber"]) and self.is_true(
                response["evonetOrderCreateTime"]) and self.is_true(
                response["wopOrderNumber"]) and self.is_true(
                response["transType"])) == True
            try:
                if 'billingAmount' in str(response):
                    assert self.is_true(response["billingAmount"]["currency"]) and self.is_true(
                        response["billingAmount"]["value"]) == True

                elif "billingFXRate" in str(response):
                    assert self.is_true(response["billingFXRate"]["value"]) and self.is_true(
                        response["billingFXRate"]["sourceCurrency"]) and \
                           self.is_true(response["billingFXRate"]["destinationCurrency"]) == True
                elif "settleAmount" in str(response):
                    assert self.is_true(response["settleAmount"]["currency"]) and self.is_true(
                        response["settleAmount"]["value"]) == True
                elif "settleFXRate" in str(response):
                    assert self.is_true(response["settleFXRate"]["value"]) and self.is_true(
                        response["settleFXRate"]["sourceCurrency"]) and \
                           self.is_true(response["settleFXRate"]["destinationCurrency"]) == True
            except AssertionError as e:
                print("MPM Payment Authentication非必返的数据不正常")
                raise e
            else:
                print("MPM Payment Authentication非必返的都没返回或非必返检验通过")

        except AssertionError as e:
            print("MPM Payment Authentication返回数据不正常")
            raise e
    #断言mpm返回的数据（evonet->wop mpmpayment接口）
    def check_MPMPayment_res(self, test_data_interface, response):
        try:
            assert (self.is_true(response["result"]["code"]) and self.is_true(
                response["result"]["message"]) and self.is_true(response["evonetReference"]) and self.is_true(
                response["evonetOrderNumber"]) and self.is_true(
                response["evonetOrderCreateTime"]) and self.is_true(
                response["wopOrderNumber"]) and self.is_true(
                response["transType"])) == True

            if response["result"]["code"]=='S0000':
                 assert (self.is_true(response["mopID"]) and self.is_true(response["settleDate"]) and self.is_true(response["evonetReference"]))

        except AssertionError as e:
            print("MPM Payment Authentication返回数据不正常")
            raise e




        #断言Payment Inquiry接口返回的数据
    def check_PaymentInquiry_res(self,test_data_interface, response):
        try:
            assert (self.is_true(response["mopOrderNumber"])  and self.is_true(response["evonetOrderNumber"]) and self.is_true(response["result"]["code"]) and self.is_true(response["result"]["message"])) == True
            if "transResult" in str(response):
                assert (self.is_true(response["transResult"]["status"]) and self.is_true(response["transResult"]["message"])) == True
            elif "billingAmount" in str(response):
                assert (self.is_true(response["billingAmount"]["currency"]) and self.is_true(response["billingAmount"]["value"])) == True
            elif "billingFXRate" in str(response):
                assert (self.is_true(response["billingFXRate"]["value"]) and self.is_true(response["billingFXRate"]["baseCurrency"]) and \
                        self.is_true(response["billingFXRate"]["quoteCurrency"])) == True
            elif "settleAmount" in str(response):
                assert (self.is_true(response["settleAmount"]["currency"]) and self.is_true(response["settleAmount"]["value"])) == True
            elif "settleFXRate" in str(response):
                assert (self.is_true(response["settleFXRate"]["value"]) and self.is_true(response["billingFXRate"]["baseCurrency"]) and \
                        self.is_true(response["settleFXRate"]["quoteCurrency"]) and self.is_true(response["settleFXRate"]["date"]) and \
                        self.is_true(response["settleFXRate"]["markup"])) == True
        except AssertionError as e:
            print("Payment Inquiry返回数据不正常")
            raise e
     #断言refund接口返回的数据
    def check_refund_res(self,test_data_interface, response):
        try:
            assert (self.is_true(response["result"]["code"]) and self.is_true(response["result"]["message"]) and self.is_true(response["evonetOrderNumber"]) and self.is_true(response["evonetOrderCreateTime"]) and self.is_true(response["mopOrderNumber"]) and self.is_true(response["mopTransTime"] ))==True
            if "billingAmount" in str(response):
                assert (self.is_true(response["billingAmount"]["currency"]) and self.is_true(response["billingAmount"]["value"] ))== True
            elif "billingFXRate" in str(response):
                assert (self.is_true(response["billingFXRate"]["value"]) and self.is_true(response["billingFXRate"]["baseCurrency"]) and \
                        self.is_true(response["billingFXRate"]["quoteCurrency"]))== True
            elif "settleAmount" in str(response):
                assert (self.is_true(response["settleAmount"]["currency"]) and self.is_true(response["settleAmount"]["value"])) == True
            elif "settleFXRate" in str(response):
                assert (self.is_true(response["settleFXRate"]["value"]) and self.is_true(response["billingFXRate"]["sourceCurrency"]) and \
                        self.is_true(response["settleFXRate"]["destinationCurrency"])) == True
        except AssertionError as e:
            print("refund返回数据不正常")
            raise e
  #断言cancellation接口返回的数据
    def check_cancellation_res(self,test_data_interface, response):
        try:
            assert (self.is_true(response["result"]["code"]) and self.is_true(response["result"]["message"]))==True

        except AssertionError as e:
            print("cancellation返回数据不正常")
            raise e


