from datetime import *
import time 

class DateUtil():


	def format_time(self,localtime):
		# 将时间改为‘2011-1-12 00：00：00格式'
		endtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(localtime))
		# endtime=time.strftime("%Y%m%d%H%M%S", time.localtime(localtime))
		return endtime
	def year_format_time(self,localtime):
		# 将时间改为‘2011-1-12 00：00：00格式'
		endtime=time.strftime("%Y%m%d", time.localtime(localtime))
		# endtime=time.strftime("%Y%m%d%H%M%S", time.localtime(localtime))
		return endtime


	#把datetime转成字符串 
	def datetime_to_string(self,dt):
		return dt.strftime("%Y-%m-%d-%H")



	def sett_time(self,localtime):
		#返回时间格式为 20201122
		endtime = time.strftime("%Y%m%d", time.localtime(localtime))
		return  endtime
	def string_to_datetime(self,string):
		return datetime.strptime(string, "%Y-%m-%d-%H")
	  
	#把字符串转成时间戳形式 
	def string_toTimestamp(self,strTime): 
		return time.mktime(self.string_to_datetime(strTime).timetuple())
	  
	def evonet_format_time(self):
		# 返回格式如 2020-07-31T10:55:23.000+0000
		endtime = datetime.now()
		return endtime
		#把字符串转成datetime


	def get_time_yesterday(self):
		#获取前两天 datetime类型的时间
		today = datetime.now()
		yesterday = today + timedelta(days=-2)  # 减去两天
		return yesterday

if __name__ == "__main__":
	print("test")
	dateUtil = DateUtil()
	print('date.time:', dateUtil.get_time_yesterday())
	print(type(dateUtil.get_time_yesterday()))
	# print('date.today():' , date.today()).

