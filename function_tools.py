from lunar_python import Lunar,EightChar
from datetime import datetime 
from zhdate import ZhDate as lunar_date
import re
import cnlunar
from jieqi import ershisijieqi_v1
from lunar_python import Lunar, Solar

import json
def get_changsheng(bazi=None, dayun_data=None ):
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
        '丙': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '戊': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '庚': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
        '壬': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'],
        '癸': ['卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰'],
        '乙': ['午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未'],
        '丁': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
        '己': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
        '辛': ['子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑'],
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
    for i in range(2,len(dayun_data)):
        dayun_changsheng.append(get_longsheng_state(day_gan,dayun_data[i][2][-1]))
    
    #'time_year_changsheng': get_longsheng_state(day_gan, time_year_zhi),
    # 'time_month_changsheng': get_longsheng_state(day_gan, time_month_zhi),
    # 'time_day_changsheng': get_longsheng_state(day_gan, time_day_zhi),
    # 'time_hour_changsheng': get_longsheng_state(day_gan, time_hour_zhi),

    # 计算长生状态
    # result存储的长生状态顺序为[八字年，八字月，八字日，八字时，大运]

    # result = []
    # result.append(get_longsheng_state(day_gan, bazi_year_zhi)),
    # result.append(get_longsheng_state(day_gan, bazi_month_zhi))
    # result.append(get_longsheng_state(day_gan, bazi_day_zhi))
    # result.append(get_longsheng_state(day_gan, bazi_hour_zhi))
    # result.append(dayun_changsheng)

    result = {}
    result["年柱十二长生"] = get_longsheng_state(day_gan, bazi_year_zhi)
    result["月柱十二长生"] = get_longsheng_state(day_gan, bazi_month_zhi)
    result["日柱十二长生"] = get_longsheng_state(day_gan, bazi_day_zhi)
    result["时柱十二长生"] = get_longsheng_state(day_gan, bazi_hour_zhi)
    result["大运年十二长生"] = dayun_changsheng
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
        "比肩":",".join(result["比肩"]),
        "比劫":",".join(result["比劫"]),
        "偏印":",".join(result["偏印"]),
        "正印":",".join(result["正印"]),
        "偏财":",".join(result["偏财"]),
        "正财":",".join(result["正财"]),
        "七杀":",".join(result["七杀"]),
        "正官":",".join(result["正官"]),
        "食神":",".join(result["食神"]),
        "伤官":",".join(result["伤官"])
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

def get_liunian(input_time=None):
    # 默认输入是农历
    # 可以以input_time为中心算出前后十年的流年
    # input_time格式为 "2024-11-12 10:19:00"，为str格式
    # 以甲辰年为锚点

    if input_time:
        target_time = str(datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S"))
    else:
        target_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 转成农历
        target_time = convert_yangli_to_nongli(target_time)

    base_nian = 2024
    base_niangan = "甲"
    base_nianzhi = "辰"
    base_shengxiao = "龙"
    tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    shengxiao = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

    target_nian = int(target_time.split("-")[0])
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

def get_liuyue(input_time=None):
    print(input_time)
    # 默认输入是农历
    # input_time格式为 "2024-11-12 10:19:00"，为str格式
    if input_time:
        # datetime型
        target_time = str(datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S"))
    else:
        # 字符串型，获取的时间是阳历，要转成农历
        target_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 转成农历
        target_time = convert_yangli_to_nongli(target_time)
    
    

def get_liuri_liushi(input_time=None):
    # 默认输入是农历
    if input_time:
        target_time = str(datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S"))
    else:
        # 获取的是阳历时间
        target_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 转成农历
        target_time = convert_yangli_to_nongli(target_time)
    lunar = Lunar.fromDate(datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S'))
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

def convert_yangli_to_nongli(input_time):
    # 阳历转农历
    dt_date = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    date = str(lunar_date.from_datetime(dt_date)) # 农历2020年7月7日 , 从阳历日期转换成农历日期
    # 正则表达式提取年份、月份和日期
    pattern = r"农历(\d{4})年(\d{1,2})月(\d{1,2})日"

    match = re.search(pattern, date)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return year+"-"+month+"-"+day+" "+input_time.split(" ")[1]

def convert_nongli_to_yangli(input_time):
    #农历转阳历
    year = int(input_time.split(" ")[0].split("-")[0])
    month = int(input_time.split(" ")[0].split("-")[1])
    day = int(input_time.split(" ")[0].split("-")[2])
    date = lunar_date(year,month,day) 
    # 字符串类型
    date = str(date.to_datetime()).split(" ")[0]+" "+input_time.split(" ")[1]
    return date

def get_bazi(input_time,mark=True):
    # 获取用户八字
    # mark标记是否为农历，若为False则不是农历，否则为农历,默认为True，即农历
    if mark:
        # 转阳历
        input_time = convert_nongli_to_yangli(input_time)
    # print(input_time)
    # 需要把日期转成阳历再进行计算
    date = cnlunar.Lunar(datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S"), godType='8char')  # 常规算法
    nianzhu = date.year8Char
    yuezhu = date.month8Char
    rizhu = date.day8Char
    shizhu = date.twohour8Char
    bazi = []
    bazi.append([nianzhu[0],yuezhu[0],rizhu[0],shizhu[0]])
    bazi.append([nianzhu[1],yuezhu[1],rizhu[1],shizhu[1]])
    return bazi

def get_time_dif(time_str1,time_str2):######################
    print(time_str1,time_str2)

    # 定义时间格式
    time_format = '%Y-%m-%d %H:%M:%S.%f'

    # 将时间字符串转换为 datetime 对象
    time_obj1 = datetime.strptime(time_str1, '%Y-%m-%d %H:%M:%S')
    time_obj2 = datetime.strptime(time_str2, '%Y-%m-%d %H:%M:%S.%f')

    # 计算时间差
    time_diff = time_obj2 - time_obj1

    # 提取天数和小时数
    days = time_diff.days
    seconds = time_diff.seconds
    hours = seconds // 3600  # 将秒数转换为小时
    minutes = (seconds % 3600) // 60  # 剩余秒数转换为分钟
    remaining_seconds = (seconds % 3600) % 60  # 剩余秒数
    print(f"时间差: {days}天 {hours}小时 {minutes}分钟 {remaining_seconds}秒")
    return [days,hours,minutes,remaining_seconds]
    

def get_dayun(birthday,sex):
    # 生日要转成阳历
    birthday = convert_nongli_to_yangli(birthday)
    year = int(birthday.split("-")[0])
    month = int(birthday.split("-")[1])
    day = int(birthday.split("-")[2].split(" ")[0])
    hour = int(birthday.split("-")[2].split(" ")[1].split(":")[0])
    minutes = int(birthday.split("-")[2].split(" ")[1].split(":")[1])
    second = int(birthday.split("-")[2].split(" ")[1].split(":")[2])

    solar = Solar(year,month,day,hour,minutes,second)
    lunar = solar.getLunar()
    baZi = lunar.getEightChar()
    # 八字
    # print(baZi.getYear() + ' ' + baZi.getMonth() + ' ' + baZi.getDay() + ' ' + baZi.getTime())
    if sex == "男":
        yun = baZi.getYun(1)
    else:
        yun = baZi.getYun(0)

    dayun_list = []
    dayun_list.append('出生' + str(yun.getStartYear()) + '年' + str(yun.getStartMonth()) + '个月' + str(yun.getStartDay()) + '天后起运')
    dayun_list.append('阳历' + yun.getStartSolar().toYmd() + '后起运')

    # 大运
    daYunArr = yun.getDaYun()
    # 出生当年为1岁
    for i in range(1, len(daYunArr)):
        daYun = daYunArr[i]
        dayun_list.append([str(daYun.getStartYear()) + '年 ', str(daYun.getStartAge()) + '岁 ', daYun.getGanZhi()])
    # ['出生4年0个月20天后起运', '阳历1999-01-08后起运', ['1999年 ', '6岁 ', '乙亥'], ['2009年 ', '16岁 ', '甲戌'], ['2019年 ', '26岁 ', '癸酉'], ['2029年 ', '36岁 ', '壬申'], ['2039年 ', '46岁 ', '辛未'], ['2049年 ', '56岁 ', '庚午'], ['2059年 ', '66岁 ', '己巳'], ['2069年 ', '76岁 ', '戊辰'], ['2079年 ', '86岁 ', '丁卯']]
    return dayun_list


def get_shishen(bazi):
    result = {
        "比肩":0,
        "比劫":0,
        "偏印":0,
        "正印":0,
        "偏财":0,
        "正财":0,
        "七杀":0,
        "正官":0,
        "食神":0,
        "伤官":0
    }
    shishen = get_mingzhu_shishen(bazi)
    for i in range(len(bazi)):
        for j in range(len(bazi[i])):
            if i == 0 and j == 2:
                continue
            for item in list(shishen.keys()):
                if bazi[i][j] in shishen[item]:
                    result[item] += 1
    return result

def get_canggan(bazi):
    canggan_ = {
        "子":"癸",
        "丑":"己癸辛",
        "寅":"甲丙戊",
        "卯":"乙",
        "辰":"辰乙癸",
        "巳":"丙庚戊",
        "午":"丁己",
        "未":"己丁乙",
        "申":"庚壬戊",
        "酉":"辛",
        "戌":"戊辛丁",
        "亥":"壬甲",
    }

    dizhicanggan = []
    for item in bazi[1]:
        dizhicanggan.append(canggan_[item])
    return dizhicanggan

def get_shensha(bazi,gender):
    # gender格式为字符串“男”，“女”
    # 神煞中的键是年支，值是月、日、时 的地支
    nianzhudizhi_shensha = {
        "孤辰":{"子":"寅","丑":"寅","寅":"巳","卯":"巳","辰":"巳","巳":"申","午":"申","未":"申","申":"亥","酉":"亥","戌":"亥","亥":"寅"},
        "寡宿":{"子":"戌","丑":"戌","寅":"丑","卯":"丑","辰":"丑","巳":"辰","午":"辰","未":"辰","申":"未","酉":"未","戌":"未","亥":"戌"},
        "大耗":{
            "阳男阴女":{"子":"未","丑":"申","寅":"酉","卯":"戌","辰":"亥","巳":"子","午":"丑","未":"寅","申":"卯","酉":"辰","戌":"巳","亥":"午"},
            "阴男阳女":{"子":"巳","丑":"午","寅":"未","卯":"申","辰":"酉","巳":"戌","午":"亥","未":"子","申":"丑","酉":"寅","戌":"卯","亥":"辰"}
        }
    }
    # 对于天德贵人“地支”中的巳要从年日时的地支查，“天干”中的值从年月日时的天干中查
    # 对于月德贵人键为月支，值为年月日时德天干
    yuezhudizhi_shensha = {
        "天德贵人":{
            "地支":{"子":"巳","卯":"申","午":"亥","酉":"寅",},
            "天干":{"丑":"庚","寅":"丁","辰":"壬","巳":"辛","未":"甲","申":"癸","戌":"丙","亥":"乙"}
        },
        "月德贵人":{"寅":"丙","午":"丙","戌":"丙","申":"壬","子":"壬","辰":"壬","亥":"甲","卯":"甲","未":"甲","巳":"庚","酉":"庚","丑":"庚"}
    }
    # 键为日干，值为年月日时的地支
    rizhutiangan_shensha = {
        "天乙贵人":{"甲":["丑","未"],"戊":["丑","未"],"庚":["丑","未"],"乙":["子","申"],"己":["子","申"],"丙":["亥","酉"],"丁":["亥","酉"],"辛":["寅","午"],"壬":["巳","卯"],"癸":["巳","卯"]},
        "文昌贵人":{"甲":"巳","乙":"午","丙":"申","丁":"酉","戊":"申","己":"酉","庚":"亥","辛":"子","壬":"寅","癸":"丑"},
        "羊刃":{"甲":"卯","丙":"午","戊":"午","庚":"酉","壬":"子"},
        "红艳煞":{"甲":"午","乙":"午","丙":"寅","丁":"未","戊":"辰","己":"辰","庚":"戌","辛":"酉","壬":"子","癸":"申"},
        "干禄":{"甲":"寅","乙":"卯","丙":"巳","丁":"午","戊":"巳","己":"午","庚":"申","辛":"酉","壬":"亥","癸":"子"}
    }
    # 键为日柱的地支，值为年月时的地支
    rizhudizhi_shensha = {
        "将星":{"子":"子","丑":"酉","寅":"午","卯":"卯","辰":"子","巳":"酉","午":"午","未":"卯","申":"子","酉":"酉","戌":"午","亥":"卯"},
        "华盖":{"子":"辰","丑":"丑","寅":"戌","卯":"未","辰":"辰","巳":"丑","午":"戌","未":"未","申":"辰","酉":"丑","戌":"戌","亥":"未"},
        "驿马":{"子":"寅","丑":"亥","寅":"申","卯":"巳","辰":"寅","巳":"亥","午":"申","未":"巳","申":"寅","酉":"亥","戌":"申","亥":"巳"},
        "劫煞":{"子":"巳","丑":"寅","寅":"亥","卯":"申","辰":"巳","巳":"寅","午":"亥","未":"申","申":"巳","酉":"寅","戌":"亥","亥":"申"},
        "亡神":{"子":"亥","丑":"申","寅":"巳","卯":"寅","辰":"亥","巳":"申","午":"巳","未":"寅","申":"亥","酉":"申","戌":"巳","亥":"寅"},
        "桃花":{"子":"酉","丑":"午","寅":"卯","卯":"子","辰":"酉","巳":"午","午":"卯","未":"子","申":"酉","酉":"午","戌":"卯","亥":"子"}
    }

    wuxing = {
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



    result = []
    # 计算是否有孤辰，寡宿，大耗
    yuerishi_zhi = "".join(bazi[1][1:])
    for item in list(nianzhudizhi_shensha.keys()):
        if item == "大耗":
            yinyang_nannv = wuxing[bazi[0][2]][0]+gender
            for yynn in list(nianzhudizhi_shensha[item].keys()):
                if yinyang_nannv in yynn:
                    if nianzhudizhi_shensha[item][yynn][bazi[1][0]] in yuerishi_zhi:
                        result.append(item)
        else:
            if nianzhudizhi_shensha[item][bazi[1][0]] in yuerishi_zhi:
                result.append(item)

    # 计算是否有天德贵人，月德贵人
    nianrishi_zhi = "".join([bazi[1][0],bazi[1][2],bazi[1][3]])
    nianyuerishi_gan = "".join(bazi[0])
    for item in list(yuezhudizhi_shensha.keys()):
        if item == "天德贵人":
            for td in list(yuezhudizhi_shensha[item].keys()):
                if td == "地支":
                    if bazi[1][1] not in "子卯午酉":
                        continue
                    if yuezhudizhi_shensha[item][td][bazi[1][1]] in nianrishi_zhi:
                        result.append(item)
                else:
                    if bazi[1][1] not in "丑寅辰巳未申戌亥":
                        continue
                    if yuezhudizhi_shensha[item][td][bazi[1][1]] in nianyuerishi_gan:
                        result.append(item)
        else:
            if yuezhudizhi_shensha[item][bazi[1][1]] in nianyuerishi_gan:
                result.append(item)

    # 计算是否有天乙贵人，文昌贵人，羊刃，红艳煞，干禄
    nianyuerishi_zhi = "".join(bazi[1])
    for item in list(rizhutiangan_shensha.keys()):
        if item == "天乙贵人":
            for dz in rizhutiangan_shensha[item][bazi[0][2]]:
                if dz in nianyuerishi_zhi:
                    result.append(item)
        elif item == "羊刃":
            if bazi[0][2] in "甲丙戊庚壬":
                if rizhutiangan_shensha[item][bazi[0][2]] in nianyuerishi_zhi:
                    result.append(item)
        else:
            if rizhutiangan_shensha[item][bazi[0][2]] in nianyuerishi_zhi:
                result.append(item)

    # 计算是否有将星，华盖，驿马，劫煞，亡神，桃花
    nianyueshi_zhi = "".join([bazi[1][0],bazi[1][1],bazi[1][3]])
    for item in list(rizhudizhi_shensha.keys()):
        if rizhudizhi_shensha[item][bazi[1][2]] in nianyueshi_zhi:
            result.append(item)
    
    return result

def get_age(birthdate_str):
    """
    根据出生日期计算周岁
    :param birthdate_str: str, 格式 "YYYY-MM-DD HH:MM:SS"
    :return: int, 计算出的年龄
    """
    # 解析出生日期
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d %H:%M:%S").date()
    
    # 获取当前日期
    today = datetime.today().date()
    
    # 计算周岁
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    
    return age


def get_current_time():
    import pytz
    beijing_tz = pytz.timezone("Asia/Shanghai")
    beijing_time = datetime.now(beijing_tz)
    # 阳历时间
    time = str(beijing_time.strftime("%Y-%m-%d %H:%M:%S"))
    yangli_year = time.split(" ")[0].split("-")[0]
    yangli_month = time.split(" ")[0].split("-")[1]
    yangli_day = time.split(" ")[0].split("-")[2]
    yangli_hour = time.split(" ")[1].split(":")[0]
    yangli_min = time.split(" ")[1].split(":")[1]
    yangli_sec = time.split(" ")[1].split(":")[2]
    # 农历时间
    nongli = convert_yangli_to_nongli(time)
    nongli_year = nongli.split(" ")[0].split("-")[0]
    nongli_month = nongli.split(" ")[0].split("-")[1]
    nongli_day = nongli.split(" ")[0].split("-")[2]
    nongli_hour = time.split(" ")[1].split(":")[0]
    nongli_min = time.split(" ")[1].split(":")[1]
    nongli_sec = time.split(" ")[1].split(":")[2]
    # 计算星期
    result = datetime.now().isocalendar()

    current_time = f"当前日期是：阳历{yangli_year}年{yangli_month}月{yangli_day}日，农历{nongli_year}年{nongli_month}月{nongli_day}日，本年第{result[1]}周的周{result[2]}，当前时间是（24小时制）：{yangli_hour}时{yangli_min}分{yangli_sec}秒"

    return current_time
# print(get_current_time())

# bazi = [['甲', '丙', '己', '甲'], ['戌', '子', '卯', '戌']]
# bazi = [["丙","己","丙","乙"],["子","亥","子","未"]]
# bazi = [["丁","癸","癸","甲"],["卯","丑","未","寅"]]

# bazi = [['丁', '辛', '丙', '戊'], ['丑', '亥', '辰', '子']]
# print(get_shensha(bazi,"女"))
