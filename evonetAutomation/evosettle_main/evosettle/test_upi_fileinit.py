import pytest
from common.evosettle.comm_funcs import CommonName
from case.interface.evosettle.dual_upi_function import UpiFunction


#
class Test_UpiFileinit(object):

    def upi_fileinit(self, envirs):
        common_name = CommonName()
        return UpiFunction(envirs, "20210110", common_name.bilateral,
                           'mop')

    def test_upi_trans_import(self, envirs):
        self.upi_fileinit(envirs).upi_trans_import()

    def test_upi_calcc(self, envirs):
        self.upi_fileinit(envirs).upi_calcc()

    def test_upi_settlement_details(self, envirs):
        self.upi_fileinit(envirs).upi_calcc()

    def test_upi_fee_collection_details_assert(self, envirs):
        self.upi_fileinit(envirs).upi_fee_collection_details_assert()

    def test_upi_feecollection_detail_resolve_assert(self, envirs):
        self.upi_fileinit(envirs).upi_feecollection_detail_resolve_assert()

    def test_upi_dispute_detail_resolve_assert(self, envirs):
        self.upi_fileinit(envirs).upi_dispute_detail_resolve_assert()

    def test_upi_exception_details_assert(self, envirs):
        self.upi_fileinit(envirs).upi_exception_details_assert()

    def test_upi_icom_detail_resolve_assert(self, envirs):
        self.upi_fileinit(envirs).upi_icom_detail_resolve_assert()

    def test_upi_daily_summary_assert(self, envirs):
        self.upi_fileinit(envirs).upi_daily_summary_assert()

    def test_upi_icom_reconcile_assert(self, envirs):
        self.upi_fileinit(envirs).upi_icom_reconcile_assert()

    def test_upi_service_fee_report(self, envirs):
        self.upi_fileinit(envirs).upi_service_fee_report()
