from lunar_python import Lunar,EightChar
from datetime import datetime 

import json
def get_changsheng(bazi, dayun_data=None,arg3=None,mark=False ):
    """
    计算八字和大运的长生状态。
    arg3:目标时间的四柱信息
    mark用来标记是否只计算大运的长生，为False时计算八字和大运的长生，为True时只计算大运长生，默认为False
    """
    day_gan = bazi[0][-2]
    # data = json.loads(arg3)
    # time_year_zhi = data["year_pillar"][-1]
    # time_month_zhi = data["month_pillar"][-1]
    # time_day_zhi = data["day_pillar"][-1]
    # time_hour_zhi = data["hour_pillar"][-1]

    bazi_year_zhi = bazi[1][0]
    bazi_month_zhi = bazi[1][1]
    bazi_day_zhi = bazi[1][2]
    bazi_hour_zhi = bazi[1][3]
    # 十二长生状态与地支的对应关系
    longsheng_table = {
        '甲': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
        '乙': ['午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未'],
        '丙': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '丁': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '戊': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '己': ['午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未'],
        '庚': ['子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑'],
        '辛': ['亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子'],
        '壬': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '癸': ['卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅']
    }

    # 十二长生状态名称
    longsheng_states = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']

    def get_longsheng_state(day_gan, zhi):
        """
        计算日干在地支中的十二长生状态。
        
        :param day_gan: 日干 (如 '甲')
        :param zhi: 地支 (如 '辰')
        :return: 对应的长生状态 (如 '衰')
        """
        if day_gan in longsheng_table:
            # 找到对应地支在长生状态中的位置
            try:
                index = longsheng_table[day_gan].index(zhi)
                return longsheng_states[index]
            except ValueError:
                return None
        return None

    # 计算大运长生
    # 两种类型，一种直接是大运年的年柱，比如："2024,甲辰"
    # 另一种是列表形势，如：["2024,甲辰","2025,乙巳"...]
    # dayun_changsheng返回格式统一为:["胎","养"...]
    dayun_changsheng = []
    if dayun_data:
        if isinstance(dayun_data, str):
            dayun_changsheng.append(get_longsheng_state(day_gan,dayun_data.split(",")[1][-1]))
        else:
            for item in dayun_data:
                dayun_changsheng.append(get_longsheng_state(day_gan,item.split(",")[1][-1]))

    #'time_year_changsheng': get_longsheng_state(day_gan, time_year_zhi),
    # 'time_month_changsheng': get_longsheng_state(day_gan, time_month_zhi),
    # 'time_day_changsheng': get_longsheng_state(day_gan, time_day_zhi),
    # 'time_hour_changsheng': get_longsheng_state(day_gan, time_hour_zhi),

    # 计算长生状态
    # result存储的长生状态顺序为[八字年，八字月，八字日，八字时，大运]
    result = []
    if bazi and not mark:
        # 只计算八字长生
        result.append(get_longsheng_state(day_gan, bazi_year_zhi)),
        result.append(get_longsheng_state(day_gan, bazi_month_zhi))
        result.append(get_longsheng_state(day_gan, bazi_day_zhi))
        result.append(get_longsheng_state(day_gan, bazi_hour_zhi))
        return result
    elif mark:
        # 只计算大运长生
        result.append(dayun_changsheng)
        return result


def get_mingzhu_shishen(bazi):
    """
    获取命主的十神符号
    """
    day_gan = bazi[0][-2]
    tiangan = {
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
    }
    dizhi = {
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
    # [item1,item2,item3,item4]，item1为我生，item2为我克，item3为生我，item4为克我
    shengke = {
        "金":["水","木","土","火"],
        "木":["火","土","水","金"],
        "水":["木","火","金","土"],
        "火":["土","金","木","水"],
        "土":["金","水","火","木"],
    }

    shishenguize = {
        "食伤":{"阳阳":"食神","阴阴":"食神","阳阴":"伤官","阴阳":"伤官"},
        "财星":{"阳阳":"偏财","阴阴":"偏财","阳阴":"正财","阴阳":"正财"},
        "印星":{"阳阳":"偏印","阴阴":"偏印","阳阴":"正印","阴阳":"正印"},
        "官杀":{"阳阳":"七杀","阴阴":"七杀","阳阴":"正官","阴阳":"正官"},
        "比肩":{"阳阳":"比肩","阴阴":"比肩","阳阴":"比劫","阴阳":"比劫"},  
    }

    def get_item(wuxing,rigan=None):
        # 获取所有为属性为wuxing天干地支字符和其对应的属性:"甲*阳"
        if rigan:
            tiangan_ = [key+"*"+value_list[0] for key, value_list in tiangan.items() if wuxing in value_list and rigan != key]
        else:
            tiangan_ = [key+"*"+value_list[0] for key, value_list in tiangan.items() if wuxing in value_list]
        dizhi_ = [key+"*"+value_list[0] for key, value_list in dizhi.items() if wuxing in value_list]
        # 返回格式为["甲*阳","未*阴"...]
        return tiangan_+dizhi_
    
    day_gan_data = tiangan[day_gan]
    shengke_data = shengke[day_gan_data[1]]
    result = {
        "比肩":[],
        "比劫":[],
        "偏印":[],
        "正印":[],
        "偏财":[],
        "正财":[],
        "七杀":[],
        "正官":[],
        "食神":[],
        "伤官":[]
    }
    # 同我，比肩
    data = get_item(day_gan_data[1])
    for j in range(len(data)):
        data_item = data[j].split("*")
        result[shishenguize["比肩"][day_gan_data[0]+data_item[1]]].append(data_item[0])
    
    for i in range(len(shengke_data)):
        data = get_item(shengke_data[i])
        if i == 0:
            # 我生，食伤
            fuhao = "食伤"
        elif i == 1:
            # 我克，财星
            fuhao = "财星"
        elif i == 2:
            # 生我，印星
            fuhao = "印星"
        elif i == 3:
            # 克我，官杀
            fuhao = "官杀"
        for j in range(len(data)):
            data_item = data[j].split("*")
            result[shishenguize[fuhao][day_gan_data[0]+data_item[1]]].append(data_item[0])
    
    return {
        "bijian":",".join(result["比肩"]),
        "bijie":",".join(result["比劫"]),
        "pianyin":",".join(result["偏印"]),
        "zhengyin":",".join(result["正印"]),
        "piancai":",".join(result["偏财"]),
        "zhengcai":",".join(result["正财"]),
        "qisha":",".join(result["七杀"]),
        "zhengguan":",".join(result["正官"]),
        "shishen":",".join(result["食神"]),
        "shangguan":",".join(result["伤官"])
    }

def get_xun(ganzhi="甲辰"):
    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 计算干支所处旬的初始年
    tiangan_ = ganzhi[0]
    dizhi_ = ganzhi[1]
    tiangan_index_ = tiangan.index(tiangan_)
    dizhi_index_ = dizhi.index(dizhi_)
    back_step = 0
    while True:
        if tiangan[tiangan_index_-back_step] == "甲":
            break
        back_step = (back_step+1)%10
    # 地支减去back_step，另外减1=加11，减2等于加10，依此类推
    chushi_dizhi = dizhi[(dizhi_index_+(12-back_step))%12]

    chushi_xun = "甲"+chushi_dizhi

    # 指定干支对应的空亡（旬空，也叫空亡。由于十天干和十二地支搭配，每旬总会多出来两个地支。这两个地支就叫旬空。）
    kongwang1 = dizhi[(dizhi.index(chushi_dizhi)+9+1)%12]
    kongwang2 = dizhi[(dizhi.index(chushi_dizhi)+9+2)%12]
    kongwang = kongwang1+kongwang2
    return chushi_xun,kongwang

def get_liunian(input_time):
    # 可以以input_time为中心算出前后十年的流年
    # input_time格式为 "2024-11-12 10:19:00"，为str格式
    # 以甲辰年为锚点
    base_nian = 2024
    base_niangan = "甲"
    base_nianzhi = "辰"
    base_shengxiao = "龙"
    tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    shengxiao = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

    target_nian = int(input_time.split("-")[0])
    if target_nian >= base_nian:
        forward_steps = target_nian-base_nian
        target_niangan = tiangan[(tiangan.index(base_niangan)+forward_steps)%10]
        target_nianzhi = dizhi[(dizhi.index(base_nianzhi)+forward_steps)%12]
        target_shengxiao = shengxiao[(shengxiao.index(base_shengxiao)+forward_steps)%12]
        return target_niangan+target_nianzhi,target_shengxiao
    else:
        back_steps = base_nian-target_nian
        # 往回退1相当于往前走9，往回退2相当于往前走8；若退21，先用21对10取余然后余数再按前面的走.
        niangan_forward_steps = 10-back_steps%10
        target_niangan = tiangan[(tiangan.index(base_niangan)+niangan_forward_steps)%10]
        # 往回退1相当于往前走11，往回退2相当于往前走10；若退21，先用21对12取余然后余数再按前面的走.
        nianzhi_forward_steps = 12-back_steps%12
        target_nianzhi = dizhi[(dizhi.index(base_nianzhi)+nianzhi_forward_steps)%12]
        # 生肖同地支
        target_shengxiao = shengxiao[(shengxiao.index(base_shengxiao)+nianzhi_forward_steps)%12]
        return target_niangan+target_nianzhi,target_shengxiao

def get_liuyue(input_time):
    # input_time格式为 "2024-11-12 10:19:00"，为str格式
    yuezhu_chaxun = {
    "甲己": ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"],
    "乙庚": ["戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑"],
    "丙辛": ["己寅", "庚卯", "辛辰", "壬巳", "癸午", "甲未", "乙申", "丙酉", "丁戌", "戊亥", "己子", "庚丑"],
    "丁壬": ["庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑"],
    "戊癸": ["甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥", "甲子", "乙丑"]
}

    liunian,_ = get_liunian(input_time)
    for item in list(yuezhu_chaxun.keys()):
        if liunian[0] in item:
            print(yuezhu_chaxun[item])
            return yuezhu_chaxun[item]


def get_liuri_liushi(input_time=None):
    from lunar_python import Lunar,EightChar
    from lunar_python.util import HolidayUtil
    from datetime import datetime 

    if input_time:
        target_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    else:
        target_time = datetime.now()
    lunar = Lunar.fromDate(datetime.now())
    d = lunar.getEightChar()
    return d.toString().split(" ")[2:]

def get_yangren(bazi):
    # 计算是否有羊刃
    # 键为日干，值为地支
    rangren = {
        "甲":"卯",
        "丙":"午",
        "戊":"午",
        "庚":"酉",
        "壬":"子",
    }
    # 计算是否有羊刃
    if rangren[bazi[0][2]] in bazi[1]:
        return True
        # # 计算有几个羊刃
        # yangren_num = bazi[1].count(rangren[bazi[0][2]])
        # if yangren_num == 1:
        #     return True, "羊刃成单"
        # elif yangren_num == 2:
        #     return True, "羊刃配双"
        # else:
        #     return True, "羊刃群党"
    else:
        False

def get_luwei(bazi):
    # 计算日干所在禄位
    lu = {"甲":"寅","乙":"卯","丙":"巳","丁":"午","戊":"巳","己":"午","庚":"申","辛":"酉","壬":"亥","癸":"子"}
    return lu[bazi[0][2]]

def get_zhengguan(bazi):
    # 计算是否有正官
    result = get_mingzhu_shishen(bazi)
    zhengguan = result["zhengguan"].split(",")
    bazi_ = bazi[0][::]
    del bazi_[2]
    for item in zhengguan:
        if item in bazi_ or item in bazi[1]:
            return True
    return False

def get_zhengyin(bazi):
    # 计算是否有正印
    result = get_mingzhu_shishen(bazi)
    zhengyin = result["zhengyin"].split(",")
    bazi_ = bazi[0][::]
    del bazi_[2]
    for item in zhengyin:
        if item in bazi_ or item in bazi[1]:
            return True
    return False


