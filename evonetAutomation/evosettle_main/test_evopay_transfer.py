import pytest
from common.evosettle.comm_funcs import CommonName
from case.interface.transfer.evopay_trans_fer import EvopayTransFer
from common.evopay_transfer.trans_fer_func import TransFerFunc, TransFerData


class Test_evopay_trans_fer(object):

    def evopay_transfer(self, envirs):
        return EvopayTransFer(envirs)

    @pytest.mark.parametrize("sopid, ropid_one, ropid_two, key_desc", TransFerData("test").rop_list_param())
    def test_standad_rop_list(self, envirs, sopid, ropid_one, ropid_two, key_desc):
        self.evopay_transfer(envirs).standad_rop_list(sopid, ropid_one, ropid_two, key_desc)
