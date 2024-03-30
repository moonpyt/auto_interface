from base.encrypt import Encrypt
from base.read_config import Conf
from base.read_file_path import ReadFile


class EvopayConf(object):
    def __init__(self, envirs):
        test_ini_file = ReadFile().read_ini_file(envirs=envirs, project="evopay")
        parser = Conf(test_ini_file)
        self.wopparticipantID = parser.get("test_data", "wopparticipantID")
        self.mopparticipantID = parser.get("test_data", "mopparticipantID")
        self.signkey = Encrypt().decrypt(parser.get("test_data", "signkey"))
        self.base_url_wop = parser.get("test_data", "base_url_wop")
        self.base_url_mop = parser.get("test_data", "base_url_mop")
        self.tyo_evopay_url = Encrypt().decrypt(parser.get("mongoDB", "tyo_evopay_url"))
        self.sgp_evopay_url = Encrypt().decrypt(parser.get("mongoDB", "sgp_evopay_url"))
        self.sgp_config_url = Encrypt().decrypt(parser.get("mongoDB", "sgp_config_url"))
        self.tyo_config_url = Encrypt().decrypt(parser.get("mongoDB", "tyo_config_url"))
        self.tyo_evologs_url = Encrypt().decrypt(parser.get("mongoDB", "tyo_evologs_url"))
        self.sgp_evologs_url = Encrypt().decrypt(parser.get("mongoDB", "sgp_evologs_url"))
        self.tyo_evosettle_url = Encrypt().decrypt(parser.get("mongoDB", "tyo_evosettle_url"))
        self.sgp_evosettle_url = Encrypt().decrypt(parser.get("mongoDB", "sgp_evosettle_url"))
        self.tyo_signkeyC = parser.get("mongoDB", "tyo_signkeyC")
        self.sgp_signkeyC = parser.get("mongoDB", "sgp_signkeyC")
        self.inquiry_address = parser.get("mongoDB", "inquiry_address")
        self.cpmPayment_address = parser.get("mongoDB", "cpmPayment_address")
        self.refund_address = parser.get("mongoDB", "refund_address")
        self.cancel_address = parser.get("mongoDB", "cancel_address")
        self.cpmToken_address = parser.get("mongoDB", "cpmToken_address")
        self.mpmQrVerification_address = parser.get("mongoDB", "mpmQrVerification_address")
        self.mpmPaymentAuthentication_address =parser.get("mongoDB", "mpmPaymentAuthentication_address")
        self.paymentNotification_address = parser.get("mongoDB", "paymentNotification_address")
        self.accountDebit = parser.get("mongoDB", "accountDebit")
        self.authenticationNotification = parser.get("mongoDB", "authenticationNotification")
        self.transactionNotification = parser.get("mongoDB", "transactionNotification")
        self.yapi_url = parser.get("mongoDB","yapi_url")
        self.version_v0 = parser.get("mongoDB","address_version_v0")
        self.mdap_func_url = parser.get("task","mdap_func_url")
        self.transfer_notification = parser.get("transfer","notification_address")
        self.transfer_userVerification= parser.get("transfer","userVerification_address")
        self.transfer_order = parser.get("transfer","order_address")
        self.transfer_inquiry = parser.get("transfer","inquiry_address")


