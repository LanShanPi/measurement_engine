# # 安装必要库：pip install sxtwl
# from datetime import datetime, timedelta
# import sxtwl
# from pytz import timezone

# class JieQiCalculator:
#     def __init__(self, lat=31.23, lon=121.47, tz='Asia/Shanghai'):
#         """初始化地理坐标与时区
#         Args:
#             lat: 纬度（默认上海） 
#             lon: 经度（默认上海）
#             tz: 时区（默认东八区）
#         """
#         self.tz = timezone(tz)
#         self.lunar = sxtwl.Lunar()
        
#     def get_jieqi_range(self, year):
#         """获取指定年份的节气时间表（精确到秒）"""
#         jq = self.lunar.getJieQiByYear(year)
#         return {sxtwl.JQmc[jd.JD]: self._jd_to_local(jd) for jd in jq}
    
#     def _jd_to_local(self, jd_obj):
#         """儒略日转本地时间"""
#         utc_time = datetime.utcfromtimestamp(jd_obj.getUTC().timestamp())
#         return utc_time.astimezone(self.tz)
    
#     def get_ganzhi(self, dt):
#         """获取指定时间的四柱信息"""
#         day = self.lunar.getDayBySolar(dt.year, dt.month, dt.day)
#         return {
#             '年柱': self.lunar.getYearGZ(day.year),
#             '月柱': self.lunar.getMonthGZ(day.month, day.day),
#             '日柱': self.lunar.getDayGZ(day.year, day.month, day.day),
#             '时柱': self.lunar.getHourGZ(day.hour, day.day)
#         }
    
#     def validate_birth_time(self, birth_time):
#         """验证出生时间是否在节气交接关键期"""
#         jq_list = self.get_jieqi_range(birth_time.year)
#         for name, time in jq_list.items():
#             if abs((birth_time - time).total_seconds()) < 7200:  # 2小时内
#                 return f"临界节气：{name} {time.strftime('%Y-%m-%d %H:%M:%S')}"
#         return "无临界节气影响"

# # 使用示例
# if __name__ == '__main__':
#     calculator = JieQiCalculator()
    
#     # 获取2024年节气表
#     jieqi_2024 = calculator.get_jieqi_range(2024)
#     for name, time in jieqi_2024.items():
#         print(f"{name}: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
#     # 验证出生时间
#     birth_time = datetime(2024, 2, 4, 10, 30).astimezone(timezone('Asia/Shanghai'))
#     print(calculator.validate_birth_time(birth_time))
    
#     # 获取四柱
#     print(calculator.get_ganzhi(datetime(2024, 5, 5, 14, 30)))


from lunar_python import LunarYear, Solar

# 获取2020年的节气对应的儒略日
lunar_year = LunarYear.fromYear(2020)
jie_qi_julian_days = lunar_year.getJieQiJulianDays()

# 遍历所有节气
for julian_day in jie_qi_julian_days:
    solar = Solar.fromJulianDay(julian_day)  # 转换为阳历
    lunar = solar.getLunar()  # 获取对应的农历
    print(f"{julian_day} = {solar.toYmdHms()} {lunar.getJieQi()}")