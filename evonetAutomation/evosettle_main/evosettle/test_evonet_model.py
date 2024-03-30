import pytest
from common.evosettle.comm_funcs import CommonName
from case.interface.evosettle.dual_restruct_function import RestructFunction
from case.interface.evosettle.restruct_report_form import RestructReportForm

import time


#
class Test_EvonetMode(object):
    def test_tyo_sgp_db_init(self, envirs):
        self.evonet_model("test").tyo_sgp_db_init()

    def evonet_model_report(self, envirs):
        common_name = CommonName()
        return RestructReportForm(envirs, "20200922", common_name.evonet,
                                  common_name.evonet)

    def evonet_model(self, envirs):
        common_name = CommonName()
        return RestructFunction(envirs, "20200922", common_name.evonet,
                                common_name.evonet, )

    def test_wop_trans_import(self, envirs):
        self.evonet_model(envirs).wop_trans_import()

    def test_wop_self_settle(self, envirs):
        self.evonet_model(envirs).wop_self_settle()

    def test_wop_evonet_mode_calc_evonet_rebate(self, envirs):
        self.evonet_model(envirs).wop_evonet_mode_calc_evonet_rebate()

    def test_wop_calc_assert_lack_settlement_settle_currency(self, envirs):
        self.evonet_model(envirs).wop_calc_assert_lack_settlement_settle_currency()

    def test_mop_trans_import(self, envirs):
        self.evonet_model(envirs).mop_trans_import()

    def test_mop_self_settle(self, envirs):
        self.evonet_model(envirs).mop_self_settle()

    def test_mop_evonet_mode_calc(self, envirs):
        self.evonet_model(envirs).mop_evonet_mode_calc()

    def test_mop_calc_assert_lack_settlement_settle_currency(self, envirs):
        self.evonet_model(envirs).mop_calc_assert_lack_settlement_settle_currency()

    def test_all_sett_task_assert(self, envirs):
        self.evonet_model(envirs).all_sett_task_assert()

    def test_wop_self_settle_abnormal(self, envirs):
        self.evonet_model(envirs).wop_self_settle_abnormal()

    def test_mop_self_settle_abnormal(self, envirs):
        self.evonet_model(envirs).mop_self_settle_abnormal()

    # 18个不同配置的case
    @pytest.mark.parametrize(
        "trans_fee_collection_method, fx_fee_collection_method,fxrebate_fee_collection_method,trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().evonet_wop_list)
    def test_evonet_mode_wop_settlement_details(self, envirs, trans_fee_collection_method, fx_fee_collection_method,
                                                fxrebate_fee_collection_method,
                                                trans_fee_calcu_method, fx_fee_calcu_method):
        self.evonet_model_report(envirs).evonet_mode_wop_settlement_details(trans_fee_collection_method,
                                                                            fx_fee_collection_method,
                                                                            fxrebate_fee_collection_method,
                                                                            trans_fee_calcu_method, fx_fee_calcu_method)

    # 9个不同配置的case
    @pytest.mark.parametrize(
        "trans_fee_collection_method, fx_fee_collection_method,trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().evonet_mop_list)
    def test_evonet_mode_mop_settlement_details(self, envirs, trans_fee_collection_method, fx_fee_collection_method,
                                                trans_fee_calcu_method, fx_fee_calcu_method):
        self.evonet_model_report(envirs).evonet_mode_mop_settlement_details(trans_fee_collection_method,
                                                                            fx_fee_collection_method,
                                                                            trans_fee_calcu_method, fx_fee_calcu_method)

    # 只有daily,daily,daily了
    @pytest.mark.parametrize(
        "trans_fee_collection_method, fx_fee_collection_method,fxrebate_fee_collection_method,trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().evonet_wop_list)
    def test_evonet_mode_wop_summary(self, envirs, trans_fee_collection_method, fx_fee_collection_method,
                                     fxrebate_fee_collection_method,
                                     trans_fee_calcu_method, fx_fee_calcu_method):
        self.evonet_model_report(envirs).evonet_mode_wop_summary(trans_fee_collection_method,
                                                                 fx_fee_collection_method,
                                                                 fxrebate_fee_collection_method,
                                                                 trans_fee_calcu_method, fx_fee_calcu_method)

    # 只有daily,daily,daily了
    @pytest.mark.parametrize(
        "trans_fee_collection_method, fx_fee_collection_method,trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().evonet_mop_list)
    def test_evonet_mode_mop_summary(self, envirs, trans_fee_collection_method, fx_fee_collection_method,
                                     trans_fee_calcu_method, fx_fee_calcu_method):
        self.evonet_model_report(envirs).evonet_mode_mop_summary(trans_fee_collection_method,
                                                                 fx_fee_collection_method,
                                                                 trans_fee_calcu_method, fx_fee_calcu_method)

    def test_special_refund_resolve(self, envirs):
        self.evonet_model_report(envirs).special_refund_resolve()

    def test_special_refund_trans_send(self, envirs):
        self.evonet_model_report(envirs).special_refund_trans_send()

    def test_special_refund_file_assert(self, envirs):
        self.evonet_model_report(envirs).special_refund_file_assert()

    #  注释，后面 evonet模式没有月报了所以将下面的cas 全部注释掉
    @pytest.mark.parametrize(
        "trans_fee_collection_method, fx_fee_collection_method,fxrebate_fee_collection_method,trans_fee_calcu_method, fx_fee_calcu_method",
        CommonName().evonet_monthly_wop_list)
    def test_evonet_mode_wop_service_assert(self, envirs, trans_fee_collection_method, fx_fee_collection_method,
                                            fxrebate_fee_collection_method, trans_fee_calcu_method,
                                            fx_fee_calcu_method):
        self.evonet_model_report(envirs).evonet_mode_wop_service_assert(trans_fee_collection_method,
                                                                        fx_fee_collection_method,
                                                                        fxrebate_fee_collection_method,
                                                                        trans_fee_calcu_method, fx_fee_calcu_method)

    # @pytest.mark.parametrize(
    #     "trans_fee_collection_method, fx_fee_collection_method,trans_fee_calcu_method, fx_fee_calcu_method",
    #     CommonName().evonet_monthly_mop_list)
    # def test_evonet_mode_mop_service_assert(self, envirs, trans_fee_collection_method, fx_fee_collection_method,
    #                                         trans_fee_calcu_method, fx_fee_calcu_method):
    #     self.evonet_model_report(envirs).evonet_mode_mop_service_assert(trans_fee_collection_method,
    #                                                                     fx_fee_collection_method,
    #                                                                     trans_fee_calcu_method, fx_fee_calcu_method)
