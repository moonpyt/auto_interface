import pytest

from base.read_file_path import ReadFile
from case.interface.evopay.QR_single_node_mode.test_MOPChecking import Testmopchecking
from case.interface.evopay.QR_single_node_mode.test_CPMToken import Testcpmtoken
from case.interface.evopay.QR_single_node_mode.test_CPMPayment import Testcpmpayment
from case.interface.evopay.QR_single_node_mode.test_MPMQRVerification import Testmpmqrverification
from case.interface.evopay.QR_single_node_mode.test_MPMPaymentAuthentication import Testmpmpaymentauthentication
from case.interface.evopay.QR_single_node_mode.test_MPMPayment import Testmpmpayment
from case.interface.evopay.QR_single_node_mode.test_paymentnotification import Testpaymentnotification
from case.interface.evopay.QR_single_node_mode.test_refund import Testrefund
from case.interface.evopay.QR_single_node_mode.test_cancellation import Testcancellation
from case.interface.evopay.QR_single_node_mode.test_paymentinquiry import Testpaymentinquiry
from case.interface.evopay.QR_single_node_mode.test_settle import Testsettle
from base.db import MongoDB
from base.read_file_path import ReadFile
from common.evopay.conf_init import db_sgp_evoconfig, db_tyo_evoconfig, db_sgp_evopay, db_tyo_evopay
from base.read_config import Conf
from base.encrypt import Encrypt
from common.evopay.read_csv import ReadCSV
from common.evopay.mongo_data import singleNode_data, doubleNode_data, Delete_Mongo_Data

data_file_mopchecking = ReadFile().read_data_file("evopay_evonet_mopchecking", "QR_single_node_mode", "evopay")
mopchecking_testdata = ReadCSV(data_file_mopchecking).read_data()

data_file_cpmtoken = ReadFile().read_data_file("evopay_evonet_cpmtoken", "QR_single_node_mode", "evopay")
cpmtoken_testdata = ReadCSV(data_file_cpmtoken).read_data()

data_file_cpmpayment = ReadFile().read_data_file("evopay_evonet_cpmpayment", "QR_single_node_mode", "evopay")
cpmpayment_testdata = ReadCSV(data_file_cpmpayment).read_data()



data_file_mpmqrverification = ReadFile().read_data_file("evopay_evonet_mpmqrverification", "QR_single_node_mode",
                                                        "evopay")
mpmqrverification_testdata = ReadCSV(data_file_mpmqrverification).read_data()

data_file_mpmpaymentauthentication = ReadFile().read_data_file("evopay_evonet_mpmpaymentauthentication",
                                                               "QR_single_node_mode", "evopay")
mpmpaymentauthentication_testdata = ReadCSV(data_file_mpmpaymentauthentication).read_data()
# #
data_file_paymentnotification = ReadFile().read_data_file("evopay_evonet_paymentnotification", "QR_single_node_mode",
                                                          "evopay")
paymentnotification_testdata = ReadCSV(data_file_paymentnotification).read_data()
#
#

data_file_mpmpayment = ReadFile().read_data_file("evopay_evonet_mpmpayment", "QR_single_node_mode", "evopay")
mpmpayment_testdata = ReadCSV(data_file_mpmpayment).read_data()

data_file_refund = ReadFile().read_data_file("evopay_evonet_refund", "QR_single_node_mode", "evopay")
refund_testdata = ReadCSV(data_file_refund).read_data()
#
data_file_cancellation = ReadFile().read_data_file("evopay_evonet_cancellation", "QR_single_node_mode", "evopay")
cancellation_testdata = ReadCSV(data_file_cancellation).read_data()

data_file_paymentinquiry = ReadFile().read_data_file("evopay_evonet_paymentinquiry", "QR_single_node_mode", "evopay")
paymentinquiry_testdata = ReadCSV(data_file_paymentinquiry).read_data()


special_file_cpmpayment = ReadFile().read_data_file("special_refund_forward", "QR_single_node_mode", "evopay")
special_cpmpayment_testdata = ReadCSV(special_file_cpmpayment).read_data()


# #
# # data_file_settle=ReadFile().read_data_file("evopay_evonet_settle","QR_single_node_mode","evopay")
# # settle_testdata=ReadCSV(data_file_settle).read_data()

class Test_QR_single_node_mode(object):
    def test_setup_module(self):
        Delete_Mongo_Data(db_sgp_evoconfig).delete_config()
        Delete_Mongo_Data(db_tyo_evoconfig).delete_config()
        Delete_Mongo_Data(db_sgp_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_001"})
        Delete_Mongo_Data(db_sgp_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_01"})
        Delete_Mongo_Data(db_tyo_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_01"})
        Delete_Mongo_Data(db_tyo_evopay).delete_trans(query_params={"wopID": "WOP_Auto_JCoinPay_001"})

    def test_teardown_module(self):
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


    def special_evopay_trans_cpmpayment(self, envirs):
        return Testcpmpayment(envirs)

    @pytest.mark.parametrize('test_info', special_cpmpayment_testdata)
    def test_special_CPMPayment(self, envirs, test_info):
        for i in range(6):
            self.special_evopay_trans_cpmpayment(envirs).test_cpmpayment(test_info)


