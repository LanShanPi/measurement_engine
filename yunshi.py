from qiangruo import wuxingliliang

from datetime import datetime
import requests
import copy

tiangan_dizhi = {
        "甲":["阳","木"],
        "乙":["阴","木"],
        "丙":["阳","火"],
        "丁":["阴","火"],
        "戊":["阳","土"],
        "己":["阴","土"],
        "庚":["阳","金"],
        "辛":["阴","金"],
        "壬":["阳","水"],
        "癸":["阴","水"],
        "子":["阳","水"],
        "丑":["阴","土"],
        "寅":["阳","木"],
        "卯":["阴","木"],
        "辰":["阳","土"],
        "巳":["阴","火"],
        "午":["阳","火"],
        "未":["阴","土"],
        "申":["阳","金"],
        "酉":["阴","金"],
        "戌":["阳","土"],
        "亥":["阴","水"],
    }

def get_hour_pillar(day_stem):
    # 定义天干和地支的列表
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 日干对应的天干起始点表
    day_stem_to_hour_stem_start = {
        "甲": 0, "己": 0,
        "乙": 2, "庚": 2,
        "丙": 4, "辛": 4,
        "丁": 6, "壬": 6,
        "戊": 8, "癸": 8,
    }

    """计算某天的所有时辰的时柱"""
    # 获取当天日干对应的天干起始位置
    start_index = day_stem_to_hour_stem_start[day_stem]
    
    # 遍历12个时辰
    hour_pillars = []
    for i in range(12):
        # 天干按顺序循环，取模计算
        hour_stem = heavenly_stems[(start_index + i) % 10]
        hour_branch = earthly_branches[i]
        hour_pillars.append(f"{hour_stem}{hour_branch}")
    # 输出结果
    result = {}
    for i, pillar in enumerate(hour_pillars):
        result[earthly_branches[i]+"时"] = pillar

    return result



def get_chinese_hour(hour, minute):
    """
    根据输入的小时和分钟返回对应的十二时辰名称和地支。
    """
    earthly_branches = [
        "子时", "丑时", "寅时", "卯时", "辰时", 
        "巳时", "午时", "未时", "申时", "酉时", "戌时", "亥时"
    ]
    
    # 十二时辰的时间范围（起始和结束时间的小时）
    time_ranges = [
        (23, 1),  # 子时 (23:00 - 01:00)
        (1, 3),   # 丑时 (01:00 - 03:00)
        (3, 5),   # 寅时 (03:00 - 05:00)
        (5, 7),   # 卯时 (05:00 - 07:00)
        (7, 9),   # 辰时 (07:00 - 09:00)
        (9, 11),  # 巳时 (09:00 - 11:00)
        (11, 13), # 午时 (11:00 - 13:00)
        (13, 15), # 未时 (13:00 - 15:00)
        (15, 17), # 申时 (15:00 - 17:00)
        (17, 19), # 酉时 (17:00 - 19:00)
        (19, 21), # 戌时 (19:00 - 21:00)
        (21, 23)  # 亥时 (21:00 - 23:00)
    ]

    # 判断当前时间属于哪个时辰
    for i, (start, end) in enumerate(time_ranges):
        if (start <= hour < end) or (start > end and (hour >= start or hour < end)):
            return earthly_branches[i]
    return "无效时间"

# 获取各种幸运的东西
def get_xingyun(yuansu):
    xingyun = {
        "金":{"数字":"4,9","方位":"西方","颜色":"白、金","花卉":"菊花、栀子花","食物":"辣味、脆食物","属相":"猴、鸡","形状":"圆形、弧形"},
        "木":{"数字":"3,8","方位":"东方","颜色":"绿、青","花卉":"梅花、竹子","食物":"酸味、叶菜类","属相":"虎、兔","形状":"长条形、柱状"},
        "水":{"数字":"1,6","方位":"北方","颜色":"黑、蓝","花卉":"荷花、睡莲","食物":"咸味、汤类、海鲜","属相":"鼠、猪","形状":"波浪形、不规则形"},
        "火":{"数字":"2,7","方位":"南方","颜色":"红、紫","花卉":"玫瑰、牡丹","食物":"辛辣、烧烤类","属相":"蛇、马","形状":"三角形、尖形"},
        "土":{"数字":"5,0","方位":"中央","颜色":"黄、棕","花卉":"向日葵、菊花","食物":"甘味、根茎类","属相":"牛、龙、羊、狗","形状":"方形、矩形"},
    }
    return xingyun[yuansu]


def calculate_supplement_element(day_element, five_elements, gender):
    """
    根据日元、五行占比和性别计算最需要补充的五行元素。
    
    参数:
    day_element (str): 日元（五行之一：“木”, “火”, “土”, “金”, “水”）
    five_elements (dict): 当前五行占比，格式如 {'金': 2.125, '火': 5.5, '木': 13.1, '土': 32.125, '水': 47.15}
    gender (str): 性别 ("female" 表示女性, "male" 表示男性)
    
    返回:
    tuple: 包含各五行需求值的字典和最需要补充的五行元素
    """
    # 根据性别设定生扶五行的目标占比
    target_support_ratio = 45 if gender == "female" else 55

    # 定义生扶五行和消耗五行
    if day_element == "木":
        support_elements = ['木', '水']
        consuming_elements = ['金', '火', '土']
    elif day_element == "火":
        support_elements = ['火', '木']
        consuming_elements = ['水', '金', '土']
    elif day_element == "土":
        support_elements = ['土', '火']
        consuming_elements = ['木', '水', '金']
    elif day_element == "金":
        support_elements = ['金', '土']
        consuming_elements = ['火', '水', '木']
    elif day_element == "水":
        support_elements = ['水', '金']
        consuming_elements = ['土', '木', '火']
    
    # 计算当前生扶五行的比例
    current_support_ratio = sum(float(five_elements[element][:-1]) for element in support_elements)
    # 计算生扶五行的需求值
    support_demand = target_support_ratio - current_support_ratio
    
    # 计算每个非生扶五行的目标比例
    target_non_support_ratio = (100 - target_support_ratio) / 3

    # 计算每个五行的需求值
    demands = {}
    for element, percentage in five_elements.items():
        if element in support_elements:
            # 对生扶五行，需求值取整体生扶需求值（只保留正需求）
            demand = support_demand if support_demand > 0 else 0
        else:
            # 对消耗五行，需求值目标为均衡目标比例
            demand = target_non_support_ratio - float(percentage[:-1])
        demands[element] = round(demand,3)

    # 动态设定用神和忌神的权重，依据support_demand绝对值进行分级调整
    abs_support_demand = abs(support_demand)
    if abs_support_demand <= 10:  # 支持需求值在0-10之间
        support_weight = 1.5
        consume_weight = 0.5
    elif 10 < abs_support_demand <= 20:  # 支持需求值在10-20之间
        support_weight = 1.7
        consume_weight = 0.3
    else:  # 支持需求值大于20
        support_weight = 2.0
        consume_weight = 0.2

    # 根据用神与忌神进行加权：使用动态调整的权重
    for element in demands:
        if element in support_elements:
            demands[element] *= support_weight  # 使用动态调整的用神权重
        elif element in consuming_elements:
            demands[element] *= consume_weight  # 使用动态调整的忌神权重

    # 确定需求值最高的五行作为补充优先的五行
    supplement_element = max(demands, key=demands.get)

    # 返回各五行需求值和建议补充的五行
    return demands, supplement_element



def tiaoxi(bazi,date=None,gender="male"):
    if date:
        current_date = date
        time_ = current_date.split("T")[1].split(":")
        hour = int(time_[0])
        minute = int(time_[1])
    else:
        # 获取当前日期和时间
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%dT%H:%M:%S")
        # 当前时间所处时辰，对应的数据
        hour = int(now.strftime("%H"))
        minute = int(now.strftime("%M"))
    # 获取当前时间的四柱
    url = "http://42.123.114.119:8599/get_four_pillars"
    params = {"date": current_date}
    try:
        response = requests.get(url, params=params)
    except:
        print("四柱数据请求失败！！！")


    # 获取当前时间日柱的天干以便推理今天十二时辰的天干地支
    day_stem = response.json()['day_pillar'][0]
    result = get_hour_pillar(day_stem)

    # 计算今天所有十二时辰的八字
    shiershichen = []
    for item in list(result.values()):
        list1 = []
        list2 = []
        list1.append(response.json()['year_pillar'][0])
        list2.append(response.json()['year_pillar'][1])
        list1.append(response.json()['month_pillar'][0])
        list2.append(response.json()['month_pillar'][1])
        list1.append(response.json()['day_pillar'][0])
        list2.append(response.json()['day_pillar'][1])
        list1.append(item[0])
        list2.append(item[1])
        shiershichen.append([list1[::],list2[::]])
        list1.clear()
        list2.clear()

    # 计算用户八字的五行力量
    bazi_sfkx,bazi_wuxing_scale,bazi_wuxing_score = wuxingliliang(bazi)

    # 计算今天所有十二时辰的五行力量
    sizhu_wuxing_score = []
    for item in shiershichen:
        _,wuxing_scale,wuxing_score = wuxingliliang(item)
        sizhu_wuxing_score.append(wuxing_score)
        # print(sizhu_wuxing_scale[-1])

    # 计算今天所有十二时辰五行力量与用户八字五行力量的和
    hebazi_score = []
    hebazi_scale = []
    for i in range(len(sizhu_wuxing_score)):
        temp = {}
        for key in list(bazi_wuxing_score.keys()):
            temp[key] = round(float(sizhu_wuxing_score[i][key])+float(bazi_wuxing_score[key]),3)
        hebazi_score.append(copy.deepcopy(temp))
        # print(hebazi_score[-1])
        # 计算总和
        total = sum(temp.values())
        # 计算占比
        percentage_data = {k: (v / total) * 100 for k, v in temp.items()}
        hebazi_scale.append({k: round(v, 3) for k, v in percentage_data.items()})
        # 根据五行力量的强弱重新从大到小排序
        hebazi_score[-1] = dict(sorted(hebazi_score[-1].items(), key=lambda item: item[1]))
        hebazi_scale[-1] = dict(sorted(hebazi_scale[-1].items(), key=lambda item: item[1]))
        # 加上百分号
        hebazi_scale[-1] = {k:str(v)+"%" for k,v in hebazi_scale[-1].items()}
        # print("****************")
        temp.clear()



    # 获取各个时辰的幸运的东西
    all = {}
    keys = list(result.keys())
    print(bazi_sfkx)
    for i in range(len(keys)):
        # 计算各个时辰所应补充元素
        demands,supplement_element = calculate_supplement_element(tiangan_dizhi[bazi[0][2]][1],hebazi_scale[i],gender)
        all[keys[i]] = {"合后五行力量":hebazi_scale[i],"五行元素需求值":demands,"各种幸运":get_xingyun(supplement_element)}


    # 获取当前时间的时辰
    current_shichen = get_chinese_hour(hour, minute)

    print(f"当前时间对应的时辰是：{current_shichen}")
    print(f"数据为：{all[current_shichen]}")
    print(f"合后五行力量：{all[current_shichen]['合后五行力量']}")
    return current_shichen,all[current_shichen],all


tiaoxi([['甲', '丙', '己', '甲'],['戌', '子', '卯', '戌']],"","male")
