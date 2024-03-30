import datetime
import time
import random
import string
class Moudle(object):
    #生成msgId-26位
    def create_msgId(self):
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        random_orderNum = random.randint(100000000, 1000000000)
        msgId_data = date_stamp + data_microsecond + str(random_orderNum)
        msgId = 'M' + str(msgId_data)
        return msgId

    def create_wopID(self):
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        msgId_data = date_stamp + data_microsecond
        msgId = 'WOPAUTO' + str(msgId_data)
        return msgId

    def create_mopID(self):
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        msgId_data = date_stamp + data_microsecond
        msgId = 'MOPAUTO' + str(msgId_data)
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

    def create_mongo_time(self):

        local_time = datetime.datetime.now()
        return local_time

    def create_refID(self,length=30):
        refID = ''
        for i in range(0,length):
            zimu = chr(random.randint(65, 122))
            shuzi = str(random.randint(0, 9))
            res = random.choice([zimu,shuzi])
            refID = refID+res
        return refID

    def create_mopOrderNumer(self):
        #生成mopOrderNum-28位
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        random_orderNum = random.randint(100000000, 1000000000)
        mopOrderNumer_data = date_stamp + data_microsecond + str(random_orderNum)
        mopOrderNumer = 'mop' + str(mopOrderNumer_data)
        return mopOrderNumer
    def create_autotestdata(self):
        #生成mopOrderNum-28位
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        random_orderNum = random.randint(100000000, 1000000000)
        autotest_data = date_stamp + data_microsecond + str(random_orderNum)
        autodata = 'autotest' + str(autotest_data)
        return autodata
    def create_mopTransTime(self):
        local_time = datetime.datetime.now()
        year = local_time.year
        month = "{:0>2d}".format(local_time.month)
        day = "{:0>2d}".format(local_time.day)
        hour = "{:0>2d}".format(local_time.hour)
        minute = "{:0>2d}".format(local_time.minute)
        second = "{:0>2d}".format(local_time.second)
        transtime = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second) + '+0800'
        return transtime
    def create_wopOrderNumber(self):
        #生成mopOrderNum-28位
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        random_orderNum = random.randint(100000000, 1000000000)
        wopOrderNumber_data = date_stamp + data_microsecond + str(random_orderNum)
        wopOrderNumber= 'wop' + str(wopOrderNumber_data)
        return wopOrderNumber
    def create_wopTransTime(self):
        local_time = datetime.datetime.now()
        year = local_time.year
        month = "{:0>2d}".format(local_time.month)
        day = "{:0>2d}".format(local_time.day)
        hour = "{:0>2d}".format(local_time.hour)
        minute = "{:0>2d}".format(local_time.minute)
        second = "{:0>2d}".format(local_time.second)
        transtime = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second) + '+0800'
        return transtime
    #生成512位随机数
    def create_512(self):
        #取64位的随机数
        random_64= random.randint(1000000000000000000000000000000000000000000000000000000000000000,9999999999999999999999999999999999999999999999999999999999999999)
        random_512=''
        #8次循环，拼接随机数
        for i in range(0,8):
            random_1=str(random_64)
            random_512=random_1+random_512
        return random_512

    # 生成2048位随机数
    def create_2048(self):
        # 取64位的随机数
        random_64 = random.randint(1000000000000000000000000000000000000000000000000000000000000000,9999999999999999999999999999999999999999999999999999999999999999)
        random_2048 = ''
        # 32次循环，拼接随机数
        for i in range(0, 32):
            random_1 = str(random_64)
            random_2048 = random_1 + random_2048
        return random_2048

    # 生成128位随机数
    def create_128(self):
        # 取64位的随机数
        random_64 = random.randint(1000000000000000000000000000000000000000000000000000000000000000,9999999999999999999999999999999999999999999999999999999999999999)
        random_128 = ''
        # 32次循环，拼接随机数
        for i in range(0, 2):
            random_1 = str(random_64)
            random_128 = random_1 + random_128
        return random_128

    # 生成1位随机数
    @staticmethod
    def create_1():
        # 取1位的随机数
        random_1 = random.choice('abcdefghijkmnlopqrstuvwhij&#%^*0123465789')
        random_1 = str(random_1)
        return random_1

    #不超过日切时间
    #当前时间加三个小时
    def less_cutoffTime(self):
        hours=time.strftime("%H",time.localtime(time.time()))
        minutes = time.strftime("%M", time.localtime(time.time()))
        if int(hours)>=int(21):
            hours="%02d"%(int(hours)-21)

            cutoffTime=str("%02d"%(int(hours)))+':'+str((minutes))+'+0800'
        else:
            cutoffTime = str("%02d" % (int(hours)+3)) + ':' + str((minutes)) + '+0800'


        return cutoffTime

    #超过日切时间
    # 当前时间减三个小时
    def over_cutoffTime(self):
        hours=time.strftime("%H",time.localtime(time.time()))
        minutes = time.strftime("%M", time.localtime(time.time()))
        if int(hours) <= int(2):
            hours = "%02d" % (21 +int(hours))
            cutoffTime = str("%02d" % (int(hours))) + ':' + str((minutes)) + '+0800'
        else:
            cutoffTime=str("%02d"%(int(hours)-3))+':'+str((minutes))+'+0800'
        return cutoffTime

    #获取当前时间 YYMMDD
    def get_currentTime(self):
        currentTime=time.strftime("%Y%m%d",time.localtime(time.time()))
        return currentTime


    #获取明日时间 YYMMDD
    def get_tomorrowTime(self):
        tomorrowTime =(datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y%m%d")
        return tomorrowTime

    # 获取昨日时间 YYMMDD

    def get_yesterdayTime(self):
        tomorrowTime = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        return tomorrowTime
    #生成特殊字符
    def special_character(self):
        datetime_now = datetime.datetime.now()
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        data_microsecond = str("%06d" % datetime_now.microsecond)
        special_character_data = date_stamp + data_microsecond
        special_character = 'special*()&^*(' + str(special_character_data)
        return special_character

    def create_params(self,n=128):
        value = ''
        for i in range(0,n):
            lowercase_letter = chr(random.randint(97, 122))
            shuzi = str(random.randint(0, 9))
            res = random.choice([lowercase_letter, shuzi])
            value = value + res
        return value


    def create_characters(self,n=128):
        value = ''
        for i in range(0,n):
            # shuzi = str(random.randint(0, 9))
            uppercase_letter = chr(random.randint(65, 90))
            lowercase_letter = chr(random.randint(97, 122))
            Special_characters = chr(random.randint(33, 48))
            ch_characters = str(random.randint(20000, 21000))
            res = random.choice([lowercase_letter,Special_characters,uppercase_letter,ch_characters])
            value = value+res
        return value

    @property
    def create_userReference(self):
        value = 'userReference_'
        for i in  range(10):
            uppercase_letter = chr(random.randint(65, 90))
            lowercase_letter = chr(random.randint(97, 122))
            res = random.choice([lowercase_letter,uppercase_letter])
            value = value + res
        return value

if __name__ == '__main__':
    print(Moudle().create_userReference)

