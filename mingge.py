from qiangruo import get_qiangruo,wuxingliliang
from guiqi import count_earthly_branch_combinations_with_scores

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

def get_biange(bazi):
    # 井栏斜义：清奇显贵 (天干必须有三个庚，日柱必须为庚申，庚子，庚辰中的一个，地支必须三合出水局)
    if bazi[0].count("庚") >= 3 and bazi[0][2] == "庚" and bazi[1][2] in ["申","子","辰"]:
        # 获取地支部分
        earthly_branches = set(bazi[1])  # 将地支部分转换为集合以便检查
        # 检查八字中的三合和三会
        result = check_three_combinations(earthly_branches, three_combinations)
        if result["三合"]:
            if result["三会"][0][1] == "水局":
                return "井栏斜义"
    
    # 壬骑龙背：主大富贵 (日干必须为壬，地支中必须有辰，且地支中辰+寅的数量大于等于3，另外日柱为壬辰最优)
    if bazi[0][2] == "壬":
        if (bazi[1].count("辰") >= 1) and (bazi[1].count("辰")+bazi[1].count("寅") >= 3):
            return "壬骑龙背"
    
    # 子遥巳禄：登科及第（日柱为甲子，时柱也必须为甲子，然后在年支或者月支必须出现巳吗）
    if bazi[0][2] == "甲" and bazi[0][3] == "甲" and bazi[1][2] == "子" and bazi[1][3] == "子" and "巳" in bazi[1][:2]:
        return "子遥巳禄"
    
    # 六阴朝阳格：稳坐朝堂（日柱为辛丑、辛卯、辛巳、辛未、辛酉、辛亥其中之一，时支为子）
    if bazi[0][2]+bazi[1][2] in ["辛丑","辛卯","辛巳","辛未","辛酉","辛亥"] and bazi[1][3] == "子":
        return "六阴朝阳"

    # 六乙鼠贵：贵命（日干为乙，日支为子，六乙指的是表示六种不同的乙日，也就是以乙日为日干的六种组合）
    if bazi[0][2] == "乙" and bazi[1][2] == "子":
        return "六乙鼠贵"
    
    # 日禄归时：大富大贵（日干的在时支得到自己的禄位）
    # 列表中每个元素的第一个符号为日干，第二个符号为时支
    lu = ["甲寅","乙卯","丙巳","丁午","戊巳","己午","庚申","辛酉","壬亥","癸子"]
    if bazi[0][2]+bazi[1][3] in lu:
        return "日禄归时"
    # 官星坐禄（天干中出现日干的官星，且官星所在位置的地支正好是官星的禄位）
    # 字典中的值第一个符号为正官第二个为七杀
    guanxingzuolu = {"甲":"辛庚","乙":"庚辛","丙":"癸壬","丁":"壬癸","戊":"乙甲","己":"甲乙","庚":"丁丙","辛":"丙丁","壬":"己戊","癸":"戊己",}
    guanxing = guanxingzuolu[bazi[0][2]][0]
    if guanxing in bazi[0] and guanxing+bazi[1][bazi[0].index(guanxing)] in lu:
        return "官星坐禄"
    
    # 拱禄拱贵：王侯贵命（拱出的禄位不能填实，即不能出现在地支中）
    # 每个元素前两个字是日柱，后两个字是时柱
    gonglu = {"癸亥癸丑":"拱出子禄","癸丑癸亥":"拱出子禄","丁巳丁未":"拱出午禄","己未己巳":"拱出午禄","戊辰戊午":"拱出已禄"}
    gonggui = {"甲申甲戌":"拱出酉中辛金为贵","乙未乙酉":"拱出申中庚金为官","甲寅甲子":"拱出丑中辛金","戊申戊午":"可拱出未中乙木","辛丑辛卯":"拱出寅中丙火"}
    rizhushizhu = bazi[0][2]+bazi[1][2]+bazi[0][3]+bazi[1][3]
    if rizhushizhu in list(gonglu) or rizhushizhu in list(gonggui):
        return "拱禄拱贵"
    
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
        return "冲禄"
        
    # 六壬趋艮（六壬日遇到甲寅时,合出亥中壬水即有了禄）
    # 六壬日中的地支
    liuren = ["子","寅","辰","午","申","戌"]
    if bazi[0][2] == "壬" and bazi[1][2] in liuren and (bazi[0][3]+bazi[1][3] == "甲寅") and "亥" not in bazi[1]:
        return "六壬趋艮"
    
    # 六甲趋乾(六甲日遇见亥时)
    # 六甲日中的地支
    liujia = ["子","寅","辰","午","申","戌"]
    if bazi[0][2] == "甲" and bazi[1][2] in liujia and bazi[1][3] == "亥" and "寅" not in bazi[1]:
        return "六甲趋乾"
    
    # 财官双美
    lumatongxiang = ["壬午","癸巳"]
    if bazi[0][2]+bazi[1][2] in lumatongxiang:
        return "财官双美"
    
    # 金神格
    shizhu = ["癸酉","己巳","乙丑"]
    rizhu = ["甲子","甲辰"]
    # pass

    # 魁罡格
    kuigang = ["庚辰","庚戌","壬辰","戊戌"]
    if bazi[0][2]+bazi[1][2] in kuigang:
        return "魁罡格"
    
    # 子午双包
    # 待写
    

 
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
        print(f"地支中有 {category}：{comb_str} 的组合，位置为：{subset_str}，总分为：{score:.2f}")

    return f"{rigan}日干，生于{yueling}月，农历{jianlu_dict[rigan][0]}，入建禄格"

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
    
def get_mingge(bazi):
    # 获取从格
    congge = get_congge(bazi)
    print(congge)
    # 获取正八格
    zhengbage = get_zhengbage(bazi)
    print(zhengbage)
    # 获取建禄格
    jianluge = get_jianluge(bazi)
    print(jianluge)
    # 获取变格
    biange = get_biange(bazi)
    print(biange)


# bazi = [['甲', '甲', '乙', '丙'], ['辰', '戌', '丑', '子']]
# bazi = [['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
# bazi = [["丁","丁","甲","癸"],["亥","未","子","酉"]]
bazi = [["庚","壬","甲","甲"],["巳","寅","子","子"]]
get_mingge(bazi)


# 从格小于6.25，专旺大于93