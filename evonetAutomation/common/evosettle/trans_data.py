import datetime
import time
import random
from base.date_format import DateUtil

format = DateUtil()


class GenerateNumber(object):
    # 生成订单号
    def create_msgId(self):
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        random_orderNum = random.randint(100000000, 1000000000)
        msgId_data = date_stamp + data_microsecond + str(random_orderNum)
        msgId = 'M' + str(msgId_data)
        return msgId

    def create_datetime(self):
        local_time = datetime.datetime.now()
        year = local_time.year
        month = "{:0>2d}".format(local_time.month)
        day = "{:0>2d}".format(local_time.day)
        hour = "{:0>2d}".format(local_time.hour)
        minute = "{:0>2d}".format(local_time.minute)
        second = "{:0>2d}".format(local_time.second)
        transtime = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second) + '+0800'
        return transtime
