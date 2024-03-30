# 读取配置文件
from base.db import MongoDB
from config.evopay.evopay_conf import EvopayConf

evopay_conf = EvopayConf("test")
# 初始化数据库
db_tyo_evopay = MongoDB(evopay_conf.tyo_evopay_url, "evopay")
db_tyo_evoconfig = MongoDB(evopay_conf.tyo_config_url, "evoconfig")
db_tyo_evologs = MongoDB(evopay_conf.tyo_evologs_url, "evologs")
db_tyo_evosettle = MongoDB(evopay_conf.tyo_evosettle_url, "evosettle")
db_sgp_evopay = MongoDB(evopay_conf.sgp_evopay_url, "evopay")
db_sgp_evoconfig = MongoDB(evopay_conf.sgp_config_url, "evoconfig")
db_sgp_evologs = MongoDB(evopay_conf.sgp_evologs_url, "evologs")
db_sgp_evosettle = MongoDB(evopay_conf.sgp_evosettle_url, "evosettle")
db_yapi = MongoDB(evopay_conf.yapi_url,"yapi")

if __name__ == '__main__':
    print(db_tyo_evopay.get_one("trans",{"evonetOrderNumber":"694068751183721282"}))
    print(db_tyo_evoconfig)
    print(db_tyo_evologs)
    print(db_tyo_evosettle)
    print(db_sgp_evopay)
    print(db_sgp_evoconfig)
    print(db_sgp_evologs)
    print(db_sgp_evosettle)

