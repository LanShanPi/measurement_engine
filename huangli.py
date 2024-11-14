
from lunar_python import Lunar,EightChar
from lunar_python.util import HolidayUtil
from datetime import datetime 
import sys
sys.path.append(r"/Users/hzl/Project/measurement_engine/data/")
from yiji import yiji_
from jixiong import jixiongshen
from nayin import nayin_
from function_tools import get_xun



def get_yiji(input_time=None):
    # input_time格式为 "2024-11-12 10:19:00"
    # 宜忌可能没有，所以返回的四个字典可能为空
    if input_time:
        target_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        target_time = datetime.now()

    date_yiji = Lunar.fromDate(target_time)
    d_yi = date_yiji.getDayYi()
    result_d_yi = {}
    for item in d_yi:
        try:
            result_d_yi[item] = yiji_["宜"][item]
        except:
            if item != "无":
                print(item,"$$$$$$$$$$$$$$$$$")
    # 忌
    result_d_ji = {}
    d_ji = date_yiji.getDayJi()
    for item in d_ji:
        try:
            result_d_ji[item] = yiji_["忌"][item]
        except:
            if item != "无":
                print(item,"$$$$$$$$$$$$$$$$$")

    time_yiji = Lunar.fromDate(target_time)
    # 宜
    result_t_yi = {}
    t_yi = time_yiji.getTimeYi()
    for item in t_yi:
        try:
            result_t_yi[item] = yiji_["宜"][item]
        except:
            if item != "无":
                print(item,"$$$$$$$$$$$$$$$$$")
    # 忌
    result_t_ji = {}
    t_ji = time_yiji.getTimeJi()
    for item in t_ji:
        try:
            result_t_ji[item] = yiji_["忌"][item]
        except:
            if item != "无":
                print(item,"$$$$$$$$$$$$$$$$$")

    return result_d_yi,result_d_ji,result_t_yi,result_t_ji

def get_chongsha(input_time=None):
    # input_time格式为 "2024-11-12 10:19:00"
    # 使用 strptime 转换为 datetime 对象
    if input_time:
        target_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        target_time = datetime.now()

    lunar_date = Lunar.fromDate(target_time)
    result = {}
    result["日冲"] = lunar_date.getDayChong()
    result["日冲干"] = lunar_date.getDayChongGan()
    result["日冲煞"] = lunar_date.getDayChongGanTie()
    result["日冲生肖"] = lunar_date.getDayChongShengXiao()
    result["日冲描述"] = lunar_date.getDayChongDesc()
    result["日煞"] = lunar_date.getDaySha()
    result["时干支"] = lunar_date.getTimeInGanZhi()
    result["时冲"] = lunar_date.getTimeChongDesc()
    result["时煞"] = lunar_date.getTimeSha()
    print(result)
    return result

def get_zhishen(input_time=None):
    if input_time:
        target_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        target_time = datetime.now()
    d = Lunar.fromDate(target_time)
    print(d.getZhiXing())
    return d.getZhiXing()

def get_jixiongshen(input_time=None):
    if input_time:
        target_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        target_time = datetime.now()
    d = Lunar.fromDate(target_time)

    # 吉神宜趋
    jishen = d.getDayJiShen()
    result_jishen = {}
    for item in jishen:
        try:
            result_jishen[item] = jixiongshen["吉神宜趋"][item]
        except:
            if item != "无":
                print(item,"$$$$$$$$$$$$$$$$$$$$$$")
    # 凶煞宜忌
    xiongsha = d.getDayXiongSha()
    result_xiongsha = {}
    for item in xiongsha:
        try:
            result_xiongsha[item] = jixiongshen["凶煞宜忌"][item]
        except:
            if item != "无":
                print(item,"$$$$$$$$$$$$$$$$$$$$$$")
    print(result_jishen)
    print(result_xiongsha)
    return result_jishen,result_xiongsha

def get_wuxing(input_time=None,gender=1):
    if input_time:
        target_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        target_time = datetime.now()
    # 获取今天的八字信息
    lunar = Lunar.fromDate(target_time)
    d = lunar.getEightChar()

    # 打印八字五行,八字五行，八字纳音，天干十神，地支十神，年月日时空亡
    print(f"{d.getYearWuXing()}, {d.getMonthWuXing()}, {d.getDayWuXing()}, {d.getTimeWuXing()}")
    print(f"{d.getYearNaYin()}, {d.getMonthNaYin()}, {d.getDayNaYin()}, {d.getTimeNaYin()}")
    print(f"{d.getYearShiShenGan()}, {d.getMonthShiShenGan()}, {d.getDayShiShenGan()}, {d.getTimeShiShenGan()}")
    print(f"{d.getYearShiShenZhi()},{d.getMonthShiShenZhi()},{d.getDayShiShenZhi()},{d.getTimeShiShenZhi()}")
    print(f"{d.getYearXunKong()},{d.getMonthXunKong()},{d.getDayXunKong()},{d.getTimeXunKong()}")
    

    # 获取胎元
    print("胎元：",d.getTaiYuan()," 胎元纳音:",d.getTaiXiNaYin())
    # 获取命宫
    print("命宫：",d.getMingGong()," 命宫纳音:",d.getMingGongNaYin())
    # 获取身宫
    print("身宫：",d.getShenGong()," 身宫纳音:",d.getShenGongNaYin())

    

    # 获取男运
    # 默认流派1的计算方法，getYun(gender, sect)获取运。gender(数字)为性别，1为男，0为女。sect(数字)为流派，1为流派1，2为流派2，不传则默认使用流派1。
    yun = d.getYun(gender,1)
    # 起运
    print(f"出生{yun.getStartYear()}年{yun.getStartMonth()}月{yun.getStartDay()}天后起运")

    # 获取大运表
    da_yun_arr = yun.getDaYun()
    dayun_list = []
    # 嵌套列表，每个元素中包含，每个大运的初始年，初始年纪，初始年干支，大运所在旬的空亡，大运初始年的纳音
    for i, da_yun in enumerate(da_yun_arr):
        if i == 0:
            continue
        xun,kongwang = get_xun(da_yun.getGanZhi())
        dayun_list.append([da_yun.getStartYear(),da_yun.getStartAge(),da_yun.getGanZhi(),kongwang,nayin_[da_yun.getGanZhi()]])
    print(dayun_list)


    # # 第1次大运流年
    # liu_nian_arr = da_yun_arr[1].getLiuNian()
    # for i, liu_nian in enumerate(liu_nian_arr):
    #     print(f"流年[{i}] = {liu_nian.getYear()}年 {liu_nian.getAge()}岁 {liu_nian.getGanZhi()}")



# get_yiji("2024-11-12 10:19:00")
# get_chongsha("2024-11-12 10:19:00")
# get_zhishen("2024-11-12 10:19:00")
# get_jixiongshen(f"2022-11-13 10:19:00")
get_wuxing(gender = 1)

# result = {"吉神":[],"凶神":[]}
# for j in range(1,13):
#     if j in [1,3,5,7,8,10,12]:
#         day = 31
#     elif j == 2:
#         day = 27
#     else:
#         day= 30

#     if j < 10:
#         month = f"0{j}"
#     else:
#         month = str(j)

#     for i in range(1,day+1):
#         if i < 10:
#             ji,xiong = get_jixiongshen(f"2022-{month}-0{i} 10:19:00")
#         else:
#             ji,xiong = get_jixiongshen(f"2022-{month}-{i} 10:19:00")
#         result["吉神"] += ji
#         result["凶神"] += xiong
# print(set(result["吉神"]),len(set(result["吉神"])))
# print(set(result["凶神"]),len(set(result["凶神"])))