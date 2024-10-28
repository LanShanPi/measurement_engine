# # 天干、地支、生肖列表
# TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
# DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
# SHENGXIAO = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

# # 基准年份：2024年 甲辰龙年
# BASE_YEAR = 2024
# BASE_TIANGAN_INDEX = TIANGAN.index('甲')
# BASE_DIZHI_INDEX = DIZHI.index('辰')
# BASE_SHENGXIAO_INDEX = SHENGXIAO.index('龙')

# def calculate_liunian(year):
#     # 计算输入年份与基准年份的差距
#     delta = year - BASE_YEAR
    
#     # 计算天干的索引
#     tiangan_index = (BASE_TIANGAN_INDEX + delta) % 10
#     if tiangan_index < 0:  # 如果年份在基准年之前，处理负数循环
#         tiangan_index += 10
    
#     # 计算地支的索引
#     dizhi_index = (BASE_DIZHI_INDEX + delta) % 12
#     if dizhi_index < 0:
#         dizhi_index += 12
    
#     # 计算生肖的索引
#     shengxiao_index = (BASE_SHENGXIAO_INDEX + delta) % 12
#     if shengxiao_index < 0:
#         shengxiao_index += 12

#     # 得出流年的天干、地支和生肖
#     tiangan = TIANGAN[tiangan_index]
#     dizhi = DIZHI[dizhi_index]
#     shengxiao = SHENGXIAO[shengxiao_index]

#     # 输出结果
#     return f"{year}年：{tiangan}{dizhi}年，生肖：{shengxiao}"

# # 测试用例
# print(calculate_liunian(2022))  # 输出：2024年：甲辰年，生肖：龙



from datetime import datetime
from lunar_python import Lunar
d = Lunar.fromDate(datetime.now())

# 宜
l = d.getDayYi()
print(l)

# 忌
l = d.getDayJi()
print(l)