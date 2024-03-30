
import pytest

from base.db import MongoDB
from base.read_file_path import ReadFile
from case.interface.evopay.QR_double_node_mode.test_MOPChecking import Testmopchecking
from case.interface.evopay.QR_double_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_double_node_mode.test_CPMPayment import Testcpmpayment
from case.interface.evopay.QR_double_node_mode.test_MPMQRVerification import Testmpmqrverification
from case.interface.evopay.QR_double_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication
from case.interface.evopay.QR_double_node_mode.test_MPMPayment import Testmpmpayment
from case.interface.evopay.QR_double_node_mode.test_paymentnotification import Testpaymentnotification
from case.interface.evopay.QR_double_node_mode.test_refund import Testrefund
from case.interface.evopay.QR_double_node_mode.test_cancellation import Testcancellation
from case.interface.evopay.QR_double_node_mode.test_paymentinquiry import Testpaymentinquiry
from case.interface.evopay.QR_double_node_mode.test_settle import Testsettle
from common.evopay.conf_init import db_sgp_evoconfig, db_tyo_evoconfig, db_sgp_evopay, db_tyo_evopay
from common.evopay.read_csv import ReadCSV
from common.evopay.mongo_data import singleNode_data,doubleNode_data,Delete_Mongo_Data
from config.evopay.evopay_conf import EvopayConf

data_file_mopchecking=ReadFile().read_data_file("evopay_evonet_mopchecking","QR_double_node_mode","evopay")
mopchecking_testdata=ReadCSV(data_file_mopchecking).read_data()


data_file_cpmtoken=ReadFile().read_data_file("evopay_evonet_cpmtoken","QR_double_node_mode","evopay")
cpmtoken_testdata=ReadCSV(data_file_cpmtoken).read_data()

data_file_cpmpayment=ReadFile().read_data_file("evopay_evonet_cpmpayment","QR_double_node_mode","evopay")
cpmpayment_testdata=ReadCSV(data_file_cpmpayment).read_data()

data_file_mpmqrverification=ReadFile().read_data_file("evopay_evonet_mpmqrverification","QR_double_node_mode","evopay")
mpmqrverification_testdata=ReadCSV(data_file_mpmqrverification).read_data()

data_file_mpmpaymentauthentication=ReadFile().read_data_file("evopay_evonet_mpmpaymentauthentication","QR_double_node_mode","evopay")
mpmpaymentauthentication_testdata=ReadCSV(data_file_mpmpaymentauthentication).read_data()

data_file_mpmpayment=ReadFile().read_data_file("evopay_evonet_mpmpayment","QR_double_node_mode","evopay")
mpmpayment_testdata=ReadCSV(data_file_mpmpayment).read_data()

data_file_paymentnotification=ReadFile().read_data_file("evopay_evonet_paymentnotification","QR_double_node_mode","evopay")
paymentnotification_testdata=ReadCSV(data_file_paymentnotification).read_data()


data_file_refund=ReadFile().read_data_file("evopay_evonet_refund","QR_double_node_mode","evopay")
refund_testdata=ReadCSV(data_file_refund).read_data()

data_file_cancellation=ReadFile().read_data_file("evopay_evonet_cancellation","QR_double_node_mode","evopay")
cancellation_testdata=ReadCSV(data_file_cancellation).read_data()
#
data_file_paymentinquiry=ReadFile().read_data_file("evopay_evonet_paymentinquiry","QR_double_node_mode","evopay")
paymentinquiry_testdata=ReadCSV(data_file_paymentinquiry).read_data()

# data_file_settle=ReadFile().read_data_file("evopay_evonet_settle","QR_double_node_mode","evopay")
# settle_testdata=ReadCSV(data_file_settle).read_data()

class Test_QR_double_node_mode(object):
    def test_setup_module(self):
        Delete_Mongo_Data(db_sgp_evoconfig).delete_config()
        Delete_Mongo_Data(db_tyo_evoconfig).delete_config()
        Delete_Mongo_Data(db_sgp_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_001"})
        Delete_Mongo_Data(db_sgp_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_01"})
        Delete_Mongo_Data(db_tyo_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_01"})
        Delete_Mongo_Data(db_tyo_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_001"})

        singleNode_data().create_no_currency_transfer_data()
        singleNode_data().create_brand_innormal()
        singleNode_data().create_mop_innormal_01()
        singleNode_data().create_mop_innormal_02()
        singleNode_data().create_wop_innormal_01()
        singleNode_data().create_wop_innormal_02()
        singleNode_data().create_relation_innormal_01()
        singleNode_data().create_relation_innormal_02()
        singleNode_data().create_relation_innormal_03()
        singleNode_data().create_currency_transfer_data_02()
        singleNode_data().create_currency_transfer_data_03()
        singleNode_data().create_currency_transfer_data_04()
        singleNode_data().create_currency_transfer_data_05()
        singleNode_data().updata_config_data()
        singleNode_data().singleNode_create_upsupported_refund_01()
        singleNode_data().create_currency_transfer_data_06()
        singleNode_data().create_currency_transfer_data_07()
        singleNode_data().create_currency_transfer_data_09()
        singleNode_data().create_currency_transfer_data_10()
        singleNode_data().create_currency_transfer_data_11()
        singleNode_data().create_currency_transfer_data_12()
        singleNode_data().create_currency_transfer_data_13()
        singleNode_data().create_currency_transfer_data_14()
        singleNode_data().create_isSettlementAmountEVONETCalculated_False_01()
        singleNode_data().create_isSettlementAmountEVONETCalculated_False_02()
        singleNode_data().create_isSettlementAmountEVONETCalculated_False_03()
        singleNode_data().create_fxrate_01()
        singleNode_data().create_fxrate_02()
        singleNode_data().create_fxrate_03()
        singleNode_data().create_upsupported_trans_01()
        singleNode_data().none_fxrate()
        singleNode_data().create_currency_transfer_data_23()
        singleNode_data().create_direct_evonet_dual_31()
        singleNode_data().create_direct_evonet_dual_32()
        singleNode_data().create_yapi_single_01()
        singleNode_data().create_currency_transfer_data_bilateral01()

        # 双节点

        doubleNode_data().create_no_currency_transfer_data()
        doubleNode_data().create_currency_transfer_data_002()
        doubleNode_data().update_config_data_B01()
        doubleNode_data().create_currency_transfer_data_03()
        doubleNode_data().create_currency_transfer_data_04()
        doubleNode_data().create_currency_transfer_data_05()

        doubleNode_data().create_currency_transfer_data_06()
        doubleNode_data().create_currency_transfer_data_07()
        doubleNode_data().create_currency_transfer_data_09()
        doubleNode_data().create_currency_transfer_data_10()
        doubleNode_data().create_currency_transfer_data_13()
        doubleNode_data().create_isSettlementAmountEVONETCalculated_False_01()
        doubleNode_data().create_isSettlementAmountEVONETCalculated_False_02()
        doubleNode_data().create_isSettlementAmountEVONETCalculated_False_03()
        doubleNode_data().create_fxrate_01()
        doubleNode_data().create_fxrate_02()
        doubleNode_data().create_fxrate_03()
        doubleNode_data().create_relation_innormal_01()
        doubleNode_data().create_relation_innormal_02()
        doubleNode_data().create_relation_innormal_03()
        doubleNode_data().create_upsupported_trans_01()
        doubleNode_data().none_fxrate()
        doubleNode_data().create_currency_transfer_data_023()
        doubleNode_data().create_direct_evonet_dual_031()
        doubleNode_data().create_direct_evonet_dual_032()
        doubleNode_data().create_yapi_double_001()
        doubleNode_data().create_currency_transfer_data_bilateral001()


    def evopay_trans_mopchecking(self, envirs):
        return Testmopchecking(envirs)
    @pytest.mark.parametrize('test_info', mopchecking_testdata)
    def test_MOPChecking(self, envirs, test_info):
        self.evopay_trans_mopchecking(envirs).test_mopchecking(test_info)




    def evopay_trans_cpmtoken(self,envirs):
        return Testcpmtoken(envirs)
    @pytest.mark.parametrize('test_info', cpmtoken_testdata)
    def test_CPMToken(self,envirs,test_info):
        self.evopay_trans_cpmtoken(envirs).test_cpmtoken(test_info)

    def evopay_trans_cpmpayment(self, envirs):
        return Testcpmpayment(envirs)

    @pytest.mark.parametrize('test_info', cpmpayment_testdata)
    def test_CPMPayment(self, envirs, test_info):
        self.evopay_trans_cpmpayment(envirs).test_cpmpayment(test_info)


    def evopay_trans_mpmqrverification(self, envirs):
        return Testmpmqrverification(envirs)

    @pytest.mark.parametrize('test_info', mpmqrverification_testdata)
    def test_MPMQRVerification(self, envirs, test_info):
        self.evopay_trans_mpmqrverification(envirs).test_mpmqrverification(test_info)


    def evopay_trans_mpmpaymentauthentication(self, envirs):
        return Testmpmpaymentauthentication(envirs)

    @pytest.mark.parametrize('test_info', mpmpaymentauthentication_testdata)
    def test_MPMPaymentAuthentication(self, envirs, test_info):
        self.evopay_trans_mpmpaymentauthentication(envirs).test_mpmpaymentauthentication(test_info)


    def evopay_trans_mpmpayment(self, envirs):
        return Testmpmpayment(envirs)
    @pytest.mark.parametrize('test_info', mpmpayment_testdata)
    def test_MPMPayment(self, envirs, test_info):
        self.evopay_trans_mpmpayment(envirs).test_mpmpayment(test_info)

    def evopay_trans_paymentnotification(self, envirs):
        return Testpaymentnotification(envirs)

    @pytest.mark.parametrize('test_info', paymentnotification_testdata)
    def test_PaymentNotification(self, envirs, test_info):
        self.evopay_trans_paymentnotification(envirs).test_paymentnotification(test_info)

    def evopay_trans_refund(self, envirs):
        return Testrefund(envirs)

    @pytest.mark.parametrize('test_info', refund_testdata)
    def test_refund(self, envirs, test_info):
        self.evopay_trans_refund(envirs).test_refund(test_info)

    def evopay_trans_cancellation(self, envirs):
        return Testcancellation(envirs)

    @pytest.mark.parametrize('test_info', cancellation_testdata)
    def test_cancellation(self, envirs, test_info):
        self.evopay_trans_cancellation(envirs).test_cancellation(test_info)
    def evopay_trans_paymentinquiry(self, envirs):
        return Testpaymentinquiry(envirs)

    @pytest.mark.parametrize('test_info', paymentinquiry_testdata)
    def test_paymentinquiry(self, envirs, test_info):
        self.evopay_trans_paymentinquiry(envirs).test_paymentinquiry(test_info)

    # def evopay_trans_settle(self, envirs):
    #     return Testsettle(envirs)
    #
    # @pytest.mark.parametrize('test_info', settle_testdata)
    # def test_settle(self, envirs, test_info):
    #     self.evopay_trans_settle(envirs).test_settle(test_info)



