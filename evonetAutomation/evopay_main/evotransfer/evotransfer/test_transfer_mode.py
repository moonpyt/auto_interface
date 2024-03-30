import pytest

from base.read_file_path import ReadFile
from case.interface.transfer.test_preorder import Testpreorder
from case.interface.transfer.test_fxrate import Testfxrate
from case.interface.transfer.test_order import Testorder
from case.interface.transfer.test_soptransfercode import Testsoptransfercode
from common.evopay.read_csv import ReadCSV

data_file_fxrate = ReadFile().read_data_file("evotransfer_fxrate", "tranfer_mode", "evopay")
fxrate_testdata = ReadCSV(data_file_fxrate).read_data()

data_file_preorder = ReadFile().read_data_file("evotransfer_preorder", "tranfer_mode", "evopay")
preorder_testdata = ReadCSV(data_file_preorder).read_data()

data_file_order = ReadFile().read_data_file("evotransfer_order", "tranfer_mode", "evopay")
order_testdata = ReadCSV(data_file_order).read_data()

data_file_soptransfercode = ReadFile().read_data_file("evotransfer_soptransfercode", "tranfer_mode", "evopay")
soptransfercode_testdata = ReadCSV(data_file_soptransfercode).read_data()



class Test_QR_single_node_mode(object):
    def test_setup_module(self):
        pass

    def test_teardown_module(self):
        pass

    def transfer_fxrate(self, envirs):
        return Testfxrate(envirs)
    @pytest.mark.parametrize('test_info', fxrate_testdata)
    def test_fxrate(self, envirs, test_info):
        self.transfer_fxrate(envirs).testfxrate(test_info)

    def transfer_preorder(self, envirs):
        return Testpreorder(envirs)
    @pytest.mark.parametrize('test_info', preorder_testdata)
    def test_preorder(self, envirs, test_info):
        self.transfer_preorder(envirs).testpreorder(test_info)

    def transfer_order(self, envirs):
        return Testorder(envirs)
    @pytest.mark.parametrize('test_info', preorder_testdata)
    def test_preorder(self, envirs, test_info):
        self.transfer_order(envirs).testorder(test_info)

    def transfer_order(self, envirs):
        return Testorder(envirs)
    @pytest.mark.parametrize('test_info', preorder_testdata)
    def test_preorder(self, envirs, test_info):
        self.transfer_order(envirs).testorder(test_info)

    def transfer_soptransfercode(self, envirs):
        return Testsoptransfercode(envirs)
    @pytest.mark.parametrize('test_info', preorder_testdata)
    def test_soptransfercoder(self, envirs, test_info):
        self.transfer_soptransfercode(envirs).testsoptransfercode(test_info)
