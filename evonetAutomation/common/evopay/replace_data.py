import re
from base.read_file_path import ReadFile
from base.read_config import Conf
from common.evopay.conf_init import evopay_conf
from common.evopay.moudle import Moudle
from base.encrypt import Encrypt


class TestData:
    """这个类专门用来保存临时变量的"""
    pass


case = TestData()


def multi_replace(data):
    test_ini_file = ReadFile().read_ini_file(envirs="test", project="evopay")

    r = r"#(.+?)#"
    res = re.findall(r, str(data))
    for item in res:
        replaced_data = '#' + item + '#'
        if item in ['mopOrderNumber','sopOrderDateTime','userReference','mopTransTime','sopOrderNumber','wopOrderNumber', 'wopTransTime', 'createTime', 'wopID', 'mopID',
                    'evonetOrderCreateTime', 'userPayTime', 'create_512', 'create_2048', 'create_128', 'autotest_data',
                    'create_1','get_currentTime', 'get_tomorrowTime', 'get_yesterdayTime', 'special_character']:
            if item == 'mopOrderNumber':
                replace_data = Moudle().create_mopOrderNumer()
            elif item == 'sopOrderNumber':
                replace_data = Moudle().create_params()
            elif item == 'userReference':
                replace_data = Moudle().create_userReference
            elif item == 'create_512':
                replace_data = Moudle().create_512()
            elif item == 'create_2048':
                replace_data = Moudle().create_2048()
            elif item == 'create_128':
                replace_data = Moudle().create_128()
            elif item == 'create_1':
                replace_data = Moudle().create_1()
            elif item == 'sopOrderDateTime':
                replace_data = Moudle().create_datetime()
            elif item == 'autotest_data':
                replace_data = Moudle().create_autotestdata()
            elif item == 'wopID':
                replace_data = Moudle().create_wopID()
            elif item == 'mopID':
                replace_data = Moudle().create_mopID()
            elif item == 'mopTransTime' or item == 'wopTransTime' or item == 'evonetOrderCreateTime' or item == 'userPayTime' or item == 'createTime':
                replace_data = Moudle().create_mopTransTime()
            elif item in 'get_currentTime':
                replace_data = Moudle().get_currentTime()
            elif item == 'get_tomorrowTime':
                replace_data = Moudle().get_tomorrowTime()
            elif item == 'get_yesterdayTime':
                replace_data = Moudle().get_yesterdayTime()
            elif item == 'special_character':
                replace_data = Moudle().special_character()
            else:
                replace_data = Moudle().create_wopOrderNumber()

            data = data.replace(replaced_data, replace_data)
        elif item == "inquiry_address":
            data = data.replace(replaced_data, evopay_conf.inquiry_address)
        elif item == "cpmPayment_address":
            data = data.replace(replaced_data, evopay_conf.cpmPayment_address)
        elif item == "refund_address":
            data = data.replace(replaced_data, evopay_conf.refund_address)
        elif item == "cancel_address":
            data = data.replace(replaced_data, evopay_conf.cancel_address)
        elif item == "cpmToken_address":
            data = data.replace(replaced_data, evopay_conf.cpmToken_address)
        elif item == "mpmQrVerification_address":
            data = data.replace(replaced_data, evopay_conf.mpmQrVerification_address)
        elif item == "mpmPaymentAuthentication_address":
            data = data.replace(replaced_data, evopay_conf.mpmPaymentAuthentication_address)
        elif item == "paymentNotification_address":
            data = data.replace(replaced_data, evopay_conf.paymentNotification_address)
        elif item == "signkeyC":
            data = data.replace(replaced_data, evopay_conf.signkeyC)
        else:
            data=data.replace(replaced_data,getattr(case,item))


    return data
