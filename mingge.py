from qiangruo import get_qiangruo,wuxingliliang
from guiqi import count_earthly_branch_combinations_with_scores
from function_tools import get_yangren,get_luwei,get_zhengguan,get_zhengyin
from data.nayin import nayin_

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

wuxing = {
    "金": ["庚", "辛", "申", "酉"],
    "木": ["甲", "乙", "寅", "卯"],
    "水": ["壬", "癸", "子", "亥"],
    "火": ["丙", "丁", "巳", "午"],
    "土": ["戊", "己", "丑", "辰", "未", "戌"]
}

jijiewuxing = {
        "春":["寅卯","木"],
        "夏":["巳午","火"],
        "秋":["申酉","金"],
        "冬":["亥子","水"],
        "长夏":["辰未戌丑","土"]
    }

three_combinations = {
    "三合": {
        frozenset(["申", "子", "辰"]): "水局",
        frozenset(["寅", "午", "戌"]): "火局",
        frozenset(["巳", "酉", "丑"]): "金局",
        frozenset(["亥", "卯", "未"]): "木局",
        frozenset(["辰", "戌", "丑", "未"]): "土局"
    },
    "三会": {
        frozenset(["寅", "卯", "辰"]): "木局",
        frozenset(["巳", "午", "未"]): "火局",
        frozenset(["亥", "子", "丑"]): "水局",
        frozenset(["申", "酉", "戌"]): "金局"
    }
}


def get_shengke(yuansu):
    # 计算元素对应的我克，克我，我生，生我，同我
    # 列表中的顺序是我克，克我，我生，生我，同我
    shengke = {
        "金":["木","火","水","土","金"],
        "木":["土","金","火","水","木"],
        "水":["火","土","木","金","水"],
        "火":["金","水","土","木","火"],
        "土":["水","木","金","火","土"],
    }
    return shengke[yuansu]

# 定义一个函数来检查地支中是否包含三合或三会组合
def check_three_combinations(branches, combinations):
    result = {"三合": [], "三会": []}
    for combo_type, combo_dict in combinations.items():
        for combo_set, ju in combo_dict.items():
            # 判断组合是否为地支的子集
            if combo_set.issubset(branches):
                result[combo_type].append((combo_set, ju))
    return result

def get_dizhi_lianru(bazi):
    #####检过#####
    earthly_branches = bazi[1]
    # 地支顺序列表
    dizhi_order = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 获取地支在顺序列表中的索引
    indices = [dizhi_order.index(eb) for eb in earthly_branches]
    # 检查是否连续相连
    if indices == list(range(indices[0], indices[0] + 4)):
        return True
    # 检查是否隔位相连
    if indices == list(range(indices[0], indices[0] + 7, 2)):
        return True
    return False


def get_tiangan_lianzhu(bazi):
    #####检过（judge_tiangan_lianzhu函数有更详细的判断）#####
    heavenly_stems = bazi[0]
    # 天干顺序列表
    tiangan_order = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 获取天干在顺序列表中的索引
    indices = [tiangan_order.index(hs) for hs in heavenly_stems]
    # 检查是否连续相连
    if indices == list(range(indices[0], indices[0] + 4)):
        return True
    return False

def judge_tiangan_lianzhu(eight_char):
    # 纳音五行相生关系
    nayin_wuxing = {
        '金': '水', '水': '木', '木': '火', '火': '土', '土': '金'
    }
    # 天干顺序表
    tiangan_order = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

    tiangan = eight_char[0]  # 天干
    dizhi = eight_char[1]    # 地支
    
    indices = [tiangan_order.index(t) for t in tiangan]
    
    # 倒垂连珠
    def is_daocui_lianzhu():
        return indices == sorted(indices, reverse=True)

    # 正印连珠
    def is_zhengyin_lianzhu():
        return indices == sorted(indices)
    
    # 悬印连珠
    def is_xuanyin_lianzhu():
        return all((indices[i] - indices[i + 1]) == 1 for i in range(len(indices) - 1))
    
    # 天干连珠（必须要4位顺行或逆行）
    def is_tiangan_lianzhu():
        return (indices == sorted(indices) or indices == sorted(indices, reverse=True)) and len(indices) == 4

    # 判断纳音连珠
    def is_nayin_lianzhu():
        # 纳音列表生成，若组合不存在则返回None
        nayin_list = [nayin_[tiangan[i] + dizhi[i]] if (tiangan[i] + dizhi[i]) in nayin_ else None for i in range(4)]
        
        # 如果存在None，说明组合中有非法天干地支，直接返回False
        if None in nayin_list:
            return False
        wuxing = [nayin[-1] for nayin in nayin_list]

        def is_shunsheng():
            return all(nayin_wuxing[wuxing[i]] == wuxing[i + 1] for i in range(len(wuxing) - 1))

        def is_nisheng():
            reversed_wuxing = list(nayin_wuxing.keys())[::-1]
            return all(reversed_wuxing[reversed_wuxing.index(wuxing[i])] == wuxing[i + 1] for i in range(len(wuxing) - 1))

        return is_shunsheng() or is_nisheng()
    
    result = {
        "倒垂连珠": is_daocui_lianzhu(),
        "正印连珠": is_zhengyin_lianzhu(),
        "悬印连珠": is_xuanyin_lianzhu(),
        "天干连珠": is_tiangan_lianzhu(),
        "纳音连珠": is_nayin_lianzhu()
    }
    return result

def get_die_lian_fang(bazi):
    """
    检查是否符合“棣萼联芳”格局
    :param heavenly_stems: 天干列表 [年干, 月干, 日干, 时干]
    :return: True 如果符合，否则 False
    """
    heavenly_stems = bazi[0]
    # 检查年月天干相同，日时天干相同
    if heavenly_stems[0] == heavenly_stems[1] and heavenly_stems[2] == heavenly_stems[3]:
        return True
    # 检查年日天干相同，月时天干相同
    if heavenly_stems[0] == heavenly_stems[2] and heavenly_stems[1] == heavenly_stems[3]:
        return True
    # 检查四柱天干相同
    if len(set(heavenly_stems)) == 1:
        return True
    return False


def get_huojin_zhuyin(bazi):
    """
    检查是否符合“火金铸印”格
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为金
    if heavenly_stems[2] not in ["庚", "辛"]:
        return False
    # 检查是否有火金相遇，火金力量需均衡
    fire_elements = {"丙", "丁", "巳", "午"}
    metal_elements = {"庚", "辛", "申", "酉"}
    fire_count = sum(elem in fire_elements for elem in heavenly_stems + earthly_branches)
    metal_count = sum(elem in metal_elements for elem in heavenly_stems + earthly_branches)
    # 火和金的数量应当均衡，假设1到2个为适中
    if fire_count < 1 or fire_count > 2 or metal_count < 1 or metal_count > 2:
        return False
    # 检查是否有丑字，丑为金库
    if "丑" in earthly_branches:
        return False
    return True


def get_muhuo_jiaohui(bazi):
    """
    检查是否符合“木火交辉”格
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    
    # 检查日干是否为木或火
    if heavenly_stems[2] not in ["甲", "乙", "丙", "丁"]:
        return False
    
    # 检查月份是否为春月或夏月
    spring_months = ["寅", "卯", "辰"]
    summer_months = ["巳", "午", "未"]
    if earthly_branches[1] not in spring_months + summer_months:
        return False
    
    # 检查是否无金和水的克制
    metal_elements = {"庚", "辛", "申", "酉"}
    water_elements = {"壬", "癸", "亥", "子"}
    if any(elem in metal_elements for elem in heavenly_stems + earthly_branches) or \
       any(elem in water_elements for elem in heavenly_stems + earthly_branches):
        return False
    
    # 检查时柱是否为木或火
    wood_fire_elements = {"甲", "乙", "丙", "丁", "寅", "卯", "巳", "午"}
    if heavenly_stems[3] not in wood_fire_elements and earthly_branches[3] not in wood_fire_elements:
        return False

    # 检查特定日柱
    specific_days = [("甲", "戌"), ("甲", "午"), ("甲", "寅"), 
                     ("丙", "午"), ("丙", "寅"), ("丙", "戌")]
    if (heavenly_stems[2], earthly_branches[2]) not in specific_days:
        return False
    
    return True


def get_jinbai_shuiqing(bazi):
    """
    检查是否符合“金白水清”格
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为金或癸水
    if heavenly_stems[2] not in ["庚", "辛", "癸"]:
        return False
    # 检查时干是否为金或水
    if heavenly_stems[3] not in ["庚", "辛", "壬", "癸"]:
        return False
    # 检查是否符合特定日子
    main_days = [("庚", "申"), ("辛", "酉")]
    other_days = [("庚", "辰"), ("庚", "子"), ("癸", "巳"), ("癸", "酉"), ("癸", "丑")]
    if (heavenly_stems[2], earthly_branches[2]) not in main_days + other_days:
        return False
    # 检查月份
    autumn_months = ["申", "酉", "戌"]
    spring_months = ["寅", "卯"]
    summer_months = ["巳", "午", "未"]
    winter_months = ["亥", "子", "丑"]
    if earthly_branches[1] in summer_months:
        return False  # 生于夏月不符合
    # 检查秋季出生的条件
    if (heavenly_stems[2], earthly_branches[2]) in main_days and earthly_branches[1] in autumn_months:
        # 如果生于秋月，且时支为亥、子
        if earthly_branches[3] in ["亥", "子"]:
            return True
    # 检查春季和冬季出生的条件
    if (heavenly_stems[2], earthly_branches[2]) in other_days:
        if earthly_branches[1] in autumn_months + winter_months:
            # 没有火伤金、土制水
            if not any(branch in earthly_branches for branch in ["巳", "午", "辰", "丑"]):
                return True
    return False


def get_jiase_ge(bazi):
    """
    检查是否符合“稼穑格”
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为戊或己
    if heavenly_stems[2] not in ["戊", "己"]:
        return False
    # 定义土局的地支组合
    earth_combination = {"辰", "戌", "丑", "未"}
    # 检查地支是否形成土局
    if not earth_combination.issubset(set(earthly_branches)):
        return False
    # 检查木的数量
    wood_elements = {"甲", "乙"}
    wood_count = sum(elem in wood_elements for elem in heavenly_stems + earthly_branches)
    # 木的数量应适中，假设1到2个为适中
    if wood_count > 2:
        return False
    # 检查火的数量
    fire_elements = {"巳", "午"}
    fire_count = sum(elem in fire_elements for elem in heavenly_stems + earthly_branches)
    # 火的数量也应适中，假设1到2个为适中
    if fire_count > 2:
        return False
    # 检查是否有金
    metal_elements = {"庚", "辛", "申", "酉"}
    if any(elem in metal_elements for elem in heavenly_stems + earthly_branches):
        return False
    return True

def get_runxia_ge(bazi):
    """
    检查是否符合“润下格”
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为壬或癸
    if heavenly_stems[2] not in ["壬", "癸"]:
        return False
    # 定义水局的地支组合
    water_combination = {"申", "子", "辰"}
    # 检查地支是否形成水局
    if not water_combination.issubset(set(earthly_branches)):
        return False
    # 检查是否有水绝之地
    water_absent_places = {"卯", "巳"}
    if any(elem in earthly_branches for elem in water_absent_places):
        return False
    # 检查是否有刑冲（这里假设一个简单的地支刑冲检测规则）
    # 忌见辰戌相冲，子午相冲等
    opposing_branches = [("辰", "戌"), ("子", "午")]
    for a, b in opposing_branches:
        if a in earthly_branches and b in earthly_branches:
            return False
    return True


def get_congge_ge(bazi):
    """
    检查是否符合“从革格”
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为庚或辛
    if heavenly_stems[2] not in ["庚", "辛"]:
        return False
    # 定义金局的地支组合
    gold_combination = {"巳", "酉", "丑"}
    # 检查地支是否形成金局
    if not gold_combination.issubset(set(earthly_branches)):
        return False
    # 检查火的数量
    fire_elements = {"丙", "丁", "巳", "午"}
    fire_count = sum(elem in fire_elements for elem in heavenly_stems + earthly_branches)
    # 火的数量应适中，假设1到2个为适中
    if fire_count < 1 or fire_count > 2:
        return False
    return True
    
def get_yanzhang_ge(bazi):
    """
    检查是否符合“炎上格”
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为丙或丁
    if heavenly_stems[2] not in ["丙", "丁"]:
        return False
    # 定义火局的地支组合
    fire_combination = {"寅", "午", "戌"}
    # 检查地支是否形成火局
    if not fire_combination.issubset(set(earthly_branches)):
        return False
    # 检查是否有寅木印星
    if "寅" not in earthly_branches:
        # 如果没有寅木印星，检查是否有亥水相济
        if "亥" not in earthly_branches:
            return False
    # 检查是否有戊己土和辰丑湿土
    unfavorable_elements = {"戊", "己", "辰", "丑"}
    if any(elem in heavenly_stems + earthly_branches for elem in unfavorable_elements):
        return False
    return True

def get_quzhi_ge(bazi):
    """
    检查是否符合“曲直格”
    :param bazi: 八字列表，格式为 [(年干, 月干, 日干, 时干), (年支, 月支, 日支, 时支)]
    :return: True 如果符合，否则 False
    """
    # 提取天干和地支
    heavenly_stems = bazi[0]
    earthly_branches = bazi[1]
    # 检查日干是否为甲或乙
    if heavenly_stems[2] not in ["甲", "乙"]:
        return False
    # 定义木局的地支组合
    wood_combinations = [
        {"寅", "卯", "辰"},  # 东方木局
        {"亥", "卯", "未"}   # 木局
    ]
    # 检查地支是否形成木局
    if set(earthly_branches) not in wood_combinations:
        return False
    # 检查四柱中是否有金
    gold_elements = {"庚", "辛", "申", "酉"}
    if any(elem in heavenly_stems + earthly_branches for elem in gold_elements):
        return False
    return True

def get_zhengbage(bazi):
    rigan_wuxing = tiangan_dizhi[bazi[0][2]][1]
    yuezhi_wuxing = tiangan_dizhi[bazi[1][1]][1]
    sheng = {
        "金":"水",
        "木":"火",
        "水":"木",
        "火":"土",
        "土":"金",
    }
    ke = {
        "金":"木",
        "木":"土",
        "水":"火",
        "火":"金",
        "土":"水",
    }
    
    if sheng[rigan_wuxing] == yuezhi_wuxing:
        # 日柱生月支
        return "伤官局"
    elif ke[rigan_wuxing] == yuezhi_wuxing:
        # 日柱克月支
        return "财旺局"
    elif rigan_wuxing == yuezhi_wuxing:
        # 日柱同月支
        return "命旺局"
    elif sheng[yuezhi_wuxing] == rigan_wuxing:
        # 月支生日柱
        return "印重局"
    elif ke[yuezhi_wuxing] == rigan_wuxing:
        # 月支克日柱
        return "煞重局"

def get_jianluge(bazi):
    # 需要老师确定
    # 需要计算八字中的冲合以判断入格的深浅
    jianlu_dict = {
        "甲":["寅","正月"],
        "乙":["卯","二月"],
        "丙":["巳","四月"],
        "丁":["午","五月"],
        "戊":["巳","四月"],
        "己":["午","五月"],
        "庚":["申","七月"],
        "辛":["酉","八月"],
        "壬":["亥","十月"],
        "癸":["子","十一月"],
    }
    rigan = bazi[0][2]
    yueling = bazi[1][1]
    # 判断是否入建禄格
    if yueling != jianlu_dict[rigan][0]:
        return "不入建禄格"
    
    # 入建禄格，根据冲合判断入的深浅
    counts = count_earthly_branch_combinations_with_scores(bazi)
    # 首先计算八字地支中冲合分数，遍历所有关系及其得分
    for (category, comb, subset), score in counts.items():
        comb_str = ''.join(comb)  # 组合的字符串表示
        subset_str = ', '.join(str(i) for i in subset)  # 位置的字符串表示
        # print(f"地支中有 {category}：{comb_str} 的组合，位置为：{subset_str}，总分为：{score:.2f}")

    return "入建禄格"

def get_zhuanwangge(bazi):
    # 需要跟老师确认
    # 计算五行占比和身强身弱
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shengfu = bazi_sfzk["生扶"].split("，")
    shengfu_score = round(float(wuxing_scale[shengfu[0]][:-1])+float(wuxing_scale[shengfu[1]][:-1]),3)
    # 必须是生扶日元的元素比占93.5以上才行
    if shengfu_score < 93.5:
        return "不入专旺格"
    # 不知道还需不需要计算各个元素对日元的生克关系
    return "专旺格"

def get_congge(bazi):
    # 计算五行占比和身强身弱
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shengfu = bazi_sfzk["生扶"].split("，")
    shengfu_score = round(float(wuxing_scale[shengfu[0]][:-1])+float(wuxing_scale[shengfu[1]][:-1]),3)
    
    if shengfu_score > 6.25:
        return "不入从格"
    # 开始计算命格
    rigan_wuxing = tiangan_dizhi[bazi[0][2]][1]
    # 计算日干克的属性和克日干的属性(位置0为我克，位置1为克我，位置2为我生)
    shengke = get_shengke(rigan_wuxing)
    rigan_caisha = [[shengke[0]]*7,[shengke[1]]*7,[shengke[2]]*7]
    # 删除日干
    bazi_copy = bazi[::]
    del bazi_copy[0][2]
    # 计算八字各个符号的属性
    bazi_wuxing = []
    for i in range(len(bazi_copy)):
        for j in range(len(bazi_copy[i])):
            bazi_wuxing.append(tiangan_dizhi[bazi_copy[i][j]][1])
    # 计算入什么格
    if bazi_wuxing == rigan_caisha[0]:
        return "从财格"
    elif bazi_wuxing == rigan_caisha[1]:
        return "从杀格"
    elif bazi_wuxing == rigan_caisha[2]:
        return "从儿格"
    else:
        return "不入从格"


def get_jinglanxieyige(bazi):
    # 井栏斜义：清奇显贵 (天干必须有三个庚，日柱必须为庚申，庚子，庚辰中的一个，地支必须三合出水局)
    if bazi[0].count("庚") >= 3 and bazi[0][2] == "庚" and bazi[1][2] in ["申","子","辰"]:
        # 获取地支部分
        earthly_branches = set(bazi[1])  # 将地支部分转换为集合以便检查
        # 检查八字中的三合和三会
        result = check_three_combinations(earthly_branches, three_combinations)
        if result["三合"]:
            if result["三会"][0][1] == "水局":
                return True
    return False

def get_renqilongbeige(bazi):
    # 壬骑龙背：主大富贵 (日干必须为壬，地支中必须有辰，且地支中辰+寅的数量大于等于3，另外日柱为壬辰最优)
    if bazi[0][2] == "壬":
        if (bazi[1].count("辰") >= 1) and (bazi[1].count("辰")+bazi[1].count("寅") >= 3):
            return True
    return False

def get_ziyaosiluge(bazi):
    # 子遥巳禄：登科及第（日柱为甲子，时柱也必须为甲子，然后在年支或者月支必须出现巳吗）
    if bazi[0][2] == "甲" and bazi[0][3] == "甲" and bazi[1][2] == "子" and bazi[1][3] == "子" and "巳" in bazi[1][:2]:
        return True
    return False

def get_liuyinchaoyangge(bazi):
    # 六阴朝阳格：稳坐朝堂（日柱为辛丑、辛卯、辛巳、辛未、辛酉、辛亥其中之一，时支为子）
    if bazi[0][2]+bazi[1][2] in ["辛丑","辛卯","辛巳","辛未","辛酉","辛亥"] and bazi[1][3] == "子":
        return True
    return False

def get_liuyishuguige(bazi):
    # 六乙鼠贵：贵命（日干为乙，日支为子，六乙指的是表示六种不同的乙日，也就是以乙日为日干的六种组合）
    if bazi[0][2] == "乙" and bazi[1][2] == "子":
        return True
    return False

def get_riluguishige(bazi):
    # 日禄归时：大富大贵（日干的在时支得到自己的禄位）
    # 列表中每个元素的第一个符号为日干，第二个符号为时支
    lu = ["甲寅","乙卯","丙巳","丁午","戊巳","己午","庚申","辛酉","壬亥","癸子"]
    if bazi[0][2]+bazi[1][3] in lu:
        return True
    return False

def get_guanxingzuoluge(bazi):
    lu = ["甲寅","乙卯","丙巳","丁午","戊巳","己午","庚申","辛酉","壬亥","癸子"]
    # 官星坐禄（天干中出现日干的官星，且官星所在位置的地支正好是官星的禄位）
    # 字典中的值第一个符号为正官第二个为七杀
    guanxingzuolu = {"甲":"辛庚","乙":"庚辛","丙":"癸壬","丁":"壬癸","戊":"乙甲","己":"甲乙","庚":"丁丙","辛":"丙丁","壬":"己戊","癸":"戊己",}
    guanxing = guanxingzuolu[bazi[0][2]][0]
    if guanxing in bazi[0] and guanxing+bazi[1][bazi[0].index(guanxing)] in lu:
        return True
    return False

def get_gonglugongguige(bazi):
    # 拱禄拱贵：王侯贵命（拱出的禄位不能填实，即不能出现在地支中）
    # 每个元素前两个字是日柱，后两个字是时柱
    gonglu = {"癸亥癸丑":"拱出子禄","癸丑癸亥":"拱出子禄","丁巳丁未":"拱出午禄","己未己巳":"拱出午禄","戊辰戊午":"拱出已禄"}
    gonggui = {"甲申甲戌":"拱出酉中辛金为贵","乙未乙酉":"拱出申中庚金为官","甲寅甲子":"拱出丑中辛金","戊申戊午":"可拱出未中乙木","辛丑辛卯":"拱出寅中丙火"}
    rizhushizhu = bazi[0][2]+bazi[1][2]+bazi[0][3]+bazi[1][3]
    if rizhushizhu in list(gonglu) or rizhushizhu in list(gonggui):
        return True
    return False

def get_chongluge(bazi):
    # 冲禄：贵命（首先计算日干所在禄位，然后计算禄位对应的六冲符号，日支必须是该六冲符号，且年，月，时支必须存在该六冲符号，且禄位必须不能存在于地支中）
    liuchong = ["子午", "丑未","寅申","卯酉", "辰戌", "巳亥"]
    # 计算日干所在的禄位
    lu = {"甲":"寅","乙":"卯","丙":"巳","丁":"午","戊":"巳","己":"午","庚":"申","辛":"酉","壬":"亥","癸":"子"}
    lu_wei = lu[bazi[0][2]]
    # 计算禄位对应的六冲符号
    for item in liuchong:
        if lu_wei in item:
            chonglu = item.replace(item,"")
    # 计算地支中禄位对应的六冲符号是否大于2，且日支是否为禄位对应的六冲符号，且禄位符号不存在于地支中
    chonglu_num = bazi[1].count(chonglu)
    if lu_wei not in bazi[1] and chonglu_num >= 2 and bazi[1][2] == chonglu:
        return True
    return False

def get_liurenqugenge(bazi):
    # 六壬趋艮（六壬日遇到甲寅时,合出亥中壬水即有了禄）
    # 六壬日中的地支
    liuren = ["子","寅","辰","午","申","戌"]
    if bazi[0][2] == "壬" and bazi[1][2] in liuren and (bazi[0][3]+bazi[1][3] == "甲寅") and "亥" not in bazi[1]:
        return True
    return False

def get_liujiaquqiange(bazi):
    # 六甲趋乾(六甲日遇见亥时)
    # 六甲日中的地支
    liujia = ["子","寅","辰","午","申","戌"]
    if bazi[0][2] == "甲" and bazi[1][2] in liujia and bazi[1][3] == "亥" and "寅" not in bazi[1]:
        return True
    return False

def get_caiguanshuangmeige(bazi):
    # 财官双美
    lumatongxiang = ["壬午","癸巳"]
    if bazi[0][2]+bazi[1][2] in lumatongxiang:
        return True
    return False

def get_jinshenge(bazi):
    # 金神格
    shizhu = ["癸酉","己巳","乙丑"]
    rigan = ["甲","己"]
    rizhu = ["甲子","甲辰"]
    if bazi[0][3]+bazi[1][3] in shizhu and bazi[0][2] in rigan:
        return True
    return False

def get_kuigangge(bazi):
    # 魁罡格
    kuigang = ["庚辰","庚戌","壬辰","戊戌"]
    if bazi[0][2]+bazi[1][2] in kuigang:
        return True
    return False

def get_ziwushuangbaoge(bazi):
    # 子午双包
    dizhi_str = "".join(bazi[1])
    if "子午子" in dizhi_str or "午子午" in dizhi_str:
        if get_yangren(bazi) and get_luwei(bazi) and get_zhengguan(bazi) and get_zhengyin(bazi):
            return True
    return False

def get_bazhuanwangluge(bazi):
    # 八专禄旺
    # 计算日干的五行属性
    if tiangan_dizhi[bazi[0][2]][1] == tiangan_dizhi[bazi[1][2]][1]:
        return True
    return False

def get_ganzhichiwangge(bazi):
    # 干支持旺
    conditions = [
        (["甲", "乙"], ["亥", "卯", "未"], ["寅", "卯"]),
        (["丙", "丁"], ["寅", "午", "戌"], ["巳", "午"]),
        (["戊", "己"], ["巳", "午"], ["辰", "戌", "丑", "未"]),
        (["庚", "辛"], ["巳", "酉", "丑"], ["申", "酉"]),
        (["壬", "癸"], ["申", "子", "辰"], ["亥", "子"]),
    ]
    for day_stems, month_branches, time_branches in conditions:
        if bazi[0][2] in day_stems and bazi[1][2] in month_branches and bazi[1][3] in time_branches:
            return True
    return False

def get_biange(bazi):
    if get_jinglanxieyige(bazi):
        return "井栏斜仪"
    
    if get_renqilongbeige(bazi):
        return "壬骑龙背"
    
    if get_ziyaosiluge(bazi):
        return "子遥巳禄"
    
    if get_liuyinchaoyangge(bazi):
        return "六阴朝阳"
    
    if get_liuyishuguige(bazi):
        return "六乙鼠贵"
    
    if get_riluguishige(bazi):
        return "日禄归时"
    
    if get_guanxingzuoluge(bazi):
        return "官星坐禄"
    
    if get_gonglugongguige(bazi):
        return "拱禄拱贵"
    
    if get_chongluge(bazi):
        return "冲禄"
    
    if get_liurenqugenge(bazi):
        return "六壬趋艮"
    
    if get_liujiaquqiange(bazi):
        return "六甲趋乾"
    
    if get_caiguanshuangmeige(bazi):
        return "财官双美"
    
    if get_jinshenge(bazi):
        return "金神格"
    
    if get_kuigangge(bazi):
        return "魁罡格"

    if get_ziwushuangbaoge(bazi):
        return "子午双包"
    
    if get_bazhuanwangluge(bazi):
        return "八专禄旺"
    
    if get_ganzhichiwangge(bazi):
        return "干支持旺"
    
    # 曲直格
    if get_quzhi_ge(bazi):
        return "曲直格"
    
    # 炎上格
    if get_yanzhang_ge(bazi):
        return "炎上格"
    
    # 从革格
    if get_congge_ge(bazi):
        return "从革格"
    
    # 润下格
    if get_runxia_ge(bazi):
        return "润下格"
    
    # 稼穑格
    if get_jiase_ge(bazi):
        return "稼穑格"
    
    # 金白水清
    if get_jinbai_shuiqing(bazi):
        return "金白水清"

    # 木火交辉
    if get_muhuo_jiaohui(bazi):
        return "木火交辉"

    # 火金铸印
    if get_huojin_zhuyin(bazi):
        return "火金铸印"
    
    # 棣萼联芳
    if get_die_lian_fang(bazi):
        return "棣萼联芳"
    
    # 天干连珠
    if get_tiangan_lianzhu(bazi):
        return "天干连珠"
    
    # 地支连茹
    if get_dizhi_lianru(bazi):
        return "地支连茹"

    return "不入变格"



def get_mingge(bazi):
    mingge = {
        "变格":"",
        "建禄格":"",
        "从格":"",
        "正八格":"",
        }
    # 获取变格
    biange = get_biange(bazi)
    mingge["变格"] = biange
    # 获取建禄格
    jianluge = get_jianluge(bazi)
    mingge["建禄格"] =  jianluge
    # 获取从格
    congge = get_congge(bazi)
    mingge["从格"] =  congge
    # 获取正八格
    zhengbage = get_zhengbage(bazi)
    mingge["正八格"] =  zhengbage

    return mingge
    
    
    




    