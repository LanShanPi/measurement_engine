from qiangruo import get_qiangruo,wuxingliliang

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

def get_lurenge(bazi):
    pass

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


def get_mingge(bazi):
    # 计算五行占比和身强身弱
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shengfu = bazi_sfzk["生扶"].split("，")
    shengfu_score = round(float(wuxing_scale[shengfu[0]][:-1])+float(wuxing_scale[shengfu[1]][:-1]),3)
    if shengfu_score > 6.25:
        return "不入格"
    # 开始计算命格
    rigan_wuxing = tiangan_dizhi[bazi[0][2]][1]
    # 计算日干克的属性和克日干的属性(位置1为我克，位置2为克我)
    shengke = get_shengke(rigan_wuxing)
    rigan_caisha = [[shengke[0]]*7,[shengke[1]]*7]

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
        return "弃命从财格"
    elif bazi_wuxing == rigan_caisha[1]:
        return "弃命从杀格"
    else:
        return "不入格"




# bazi = [['甲', '甲', '乙', '丙'], ['辰', '戌', '丑', '子']]
# bazi = [['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
# bazi = [["丁","丁","甲","癸"],["亥","未","子","酉"]]
bazi = [["庚","壬","丙","庚"],["戌","子","辰","申"]]
get_mingge(bazi)


# 从格小于6.25，专旺大于93