import pytest
from common.evosettle.comm_funcs import CommonName
from case.interface.evosettle.dual_restruct_function import RestructFunction
from case.interface.evosettle.restruct_report_form import RestructReportForm


#
class Test_DualEvonetMode(object):
    # def test_tyo_sgp_db_init(self, envirs):
    #     self.wop_fileinit("test").tyo_sgp_db_init()

    def wop_fileinit(self, envirs):
        common_name = CommonName()
        return RestructFunction(envirs, "20200922", common_name.bilateral,
                                common_name.file_init_wop, )

    def wop_fileinit_report(self, envirs):
        common_name = CommonName()
        return RestructReportForm(envirs, "20200922", common_name.bilateral,
                                  common_name.file_init_wop)

    def test_wop_trans_import(self, envirs):
        self.wop_fileinit(envirs).wop_trans_import()

    def test_mop_trans_import(self, envirs):
        self.wop_fileinit(envirs).mop_trans_import()

    def test_wop_file_download_resolve_reconcile(self, envirs):
        self.wop_fileinit(envirs).wop_file_download_resolve_reconcile()

    def test_wop_file_extra_trans_resolve_reconcile(self, envirs):
        self.wop_fileinit(envirs).wop_file_extra_trans_resolve_reconcile()

    def test_wop_file_full_extra_resolve_reconcile(self, envirs):
        self.wop_fileinit(envirs).wop_file_full_extra_resolve_reconcile()

    def test_wop_file_lack_reconcile(self, envirs):
        self.wop_fileinit(envirs).wop_file_lack_reconcile()

    def test_wop_file_reconcile_status_assert(self, envirs):
        self.wop_fileinit(envirs).wop_file_reconcile_status_assert()

    def test_wop_calc_custom_config(self, envirs):
        self.wop_fileinit(envirs).wop_calc_custom_config()

    def test_wop_calc_three_currency(self, envirs):
        self.wop_fileinit(envirs).wop_calc_three_currency()

    def test_wop_calc_fee_type_single_accumulation(self, envirs):
        self.wop_fileinit(envirs).wop_calc_fee_type_single_accumulation()

    def test_wop_calc_daily_single(self, envirs):
        self.wop_fileinit(envirs).wop_calc_daily_single()

    def test_wop_wop_fileinit_calc_refund_calc(self, envirs):
        self.wop_fileinit(envirs).wop_wop_fileinit_calc_refund_calc()

    # mop侧
    def test_mop_file_download_resolve_reconcile(self, envirs):
        self.wop_fileinit(envirs).mop_file_download_resolve_reconcile()

    def test_mop_file_extra_trans_resolve_reconcile(self, envirs):
        self.wop_fileinit(envirs).mop_file_extra_trans_resolve_reconcile()

    def test_mop_file_full_extra_resolve_reconcile(self, envirs):
        self.wop_fileinit(envirs).mop_file_full_extra_resolve_reconcile()

    def test_mop_file_lack_reconcile(self, envirs):
        self.wop_fileinit(envirs).mop_file_lack_reconcile()

    def test_mop_file_reconcile_status_assert(self, envirs):
        self.wop_fileinit(envirs).mop_file_reconcile_status_assert()

    def test_mop_calc_custom_config(self, envirs):
        self.wop_fileinit(envirs).mop_calc_custom_config()

    def test_mop_calc_three_currency(self, envirs):
        self.wop_fileinit(envirs).mop_calc_three_currency()

    def test_mop_calc_fee_type_single_accumulation(self, envirs):
        self.wop_fileinit(envirs).mop_calc_fee_type_single_accumulation()

    def test_mop_calc_daily_single(self, envirs):
        self.wop_fileinit(envirs).mop_calc_daily_single()

    def test_mop_wop_fileinit_calc_refund_calc(self, envirs):
        self.wop_fileinit(envirs).mop_wop_fileinit_calc_refund_calc()

    @pytest.mark.parametrize(
        "trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().bilateral_list)
    def test_bilateral_mode_wop_settlement_details(self, envirs,
                                                   trans_fee_calcu_method, fx_fee_calcu_method):
        self.wop_fileinit_report(envirs).bilateral_mode_wop_settlement_details(
            trans_fee_calcu_method,
            fx_fee_calcu_method)

    # 9个不同配置的case
    @pytest.mark.parametrize(
        "trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().bilateral_list)
    def test_bilateral_mode_mop_settlement_details(self, envirs, trans_fee_calcu_method, fx_fee_calcu_method):
        self.wop_fileinit_report(envirs).bilateral_mode_mop_settlement_details(
            trans_fee_calcu_method,
            fx_fee_calcu_method)

    @pytest.mark.parametrize("trans_fee_calcu_method, fx_fee_calcu_method", CommonName().bilateral_list)
    def test_bilateral_mop_service_assert(self, envirs, trans_fee_calcu_method, fx_fee_calcu_method):
        self.wop_fileinit_report(envirs).bilateral_mop_service_assert(trans_fee_calcu_method, fx_fee_calcu_method)
