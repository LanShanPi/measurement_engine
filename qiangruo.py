# 八字天干：['甲', '丙', '己', '甲']，八字地支: ['戌', '子', '卯', '戌']
# 生日1994-12-19T19:00:00-男
# 相生：木 -> 火 -> 土 -> 金 -> 水，水 -> 木循环
# 相克：木 -> 土 -> 水 -> 火 -> 金，金 -> 木循环


from itertools import combinations

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

def count_earthly_branch_combinations(bazi):

    all_relationships = {
        "六冲": [
            ("子", "午"), ("丑", "未"), ("寅", "申"),
            ("卯", "酉"), ("辰", "戌"), ("巳", "亥")
        ],
        "三刑": [
            (("寅", "巳", "申"), "无恩之刑"),
            (("未", "戌", "丑"), "恃势之刑"),
            (("子", "卯"),"无礼之刑")
        ],
        "半三刑": [
            ("寅", "巳"), ("巳", "申")
        ],
        "害": [
            ("子", "未"), ("丑", "午"), ("寅", "巳"),
            ("卯", "辰"), ("申", "亥"), ("酉", "戌")
        ],
        "破": [
            ("子", "酉"), ("丑", "辰"), ("寅", "亥"),
            ("卯", "午"), ("戌", "未"), ("巳", "申")
        ],
        "自刑": [
            ("辰", "辰"), ("午", "午"), ("酉", "酉"), ("亥", "亥")
        ],
        "三合": [
            (("申", "子", "辰"), "水局"),
            (("寅", "午", "戌"), "火局"),
            (("巳", "酉", "丑"), "金局"),
            (("亥", "卯", "未"), "木局"),
            (("辰","戌","丑","未"),"土局")
        ],
        "三会": [
            (("寅", "卯", "辰"), "木局"),
            (("巳", "午", "未"), "火局"),
            (("亥", "子", "丑"), "水局"),
            (("申", "酉", "戌"), "金局")
        ],
        "六合": [
            (("子", "丑"), "土局"),
            (("卯", "戌"), "火局"),
            (("辰", "酉"), "金局"),
            (("巳", "申"), "水局"),
            (("午", "未"), "火或土局")
        ],
        "半三合": [
            (("申", "子"), "半合水局"),
            (("子", "辰"), "半合水局"),
            (("寅", "午"), "半合火局"),
            (("午", "戌"), "半合火局"),
            (("巳", "酉"), "半合金局"),
            (("酉", "丑"), "半合金局"),
            (("亥", "卯"), "半合木局"),
            (("卯", "未"), "半合木局")
        ],
        "半三会": [
            (("寅", "卯"), "半会木局"),
            (("卯", "辰"), "半会木局"),
            (("巳", "午"), "半会火局"),
            (("午", "未"), "半会火局"),
            (("亥", "子"), "半会水局"),
            (("子", "丑"), "半会水局"),
            (("申", "酉"), "半会金局"),
            (("酉", "戌"), "半会金局")
        ],
        "拱合": [
            (("寅", "戌"), "拱火局"),
            (("申", "辰"), "拱水局"),
            (("巳", "丑"), "拱金局"),
            (("亥", "未"), "拱木局")
        ],
        "暗合": [
            ("丑", "午"), ("卯", "辰"), ("亥", "戌"),("子","戌")
        ]
    }
    
    count_dict = {}  # 存储所有组合的计数
    branches = bazi[1]  # 取出地支部分

    # 遍历所有类型的关系
    for category, relationships in all_relationships.items():
        for comb in relationships:
            if isinstance(comb[0], tuple):  # 三字组合（三合、三会、三刑等）
                comb_set = set(comb[0])
                # 检查是否匹配三字组合
                for subset in combinations(branches, len(comb[0])):
                    if set(subset) == comb_set:
                        key = (category, comb[0], comb[1])
                        count_dict[key] = count_dict.get(key, 0) + 1
            else:  # 二字组合（六合、六冲、相刑等）
                comb_set = set(comb)
                # 检查是否匹配二字组合
                for subset in combinations(branches, len(comb)):
                    if set(subset) == comb_set:
                        key = (category, comb)
                        count_dict[key] = count_dict.get(key, 0) + 1

    return count_dict


def compute_bazisfkx(bazi_wuxing):
    sfkx_dict = {
        "金":{"生扶":"金，土","克泄":"火，木，水"},
        "木":{"生扶":"木，水","克泄":"金，土，火"},
        "水":{"生扶":"水，金","克泄":"土，火，木"},
        "火":{"生扶":"火，木","克泄":"水，金，土"},
        "土":{"生扶":"土，火","克泄":"木，水，金"},
    }
    return sfkx_dict[bazi_wuxing]

def compute_shengkexie(item1,item2):
    # item1表示日柱的五行
    # item2表示八字中其他位置的五行
    sheng = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
    ke = {"木":"土","土":"水","水":"火","火":"金","金":"木"}
    if sheng[item2] == item1:
        return "生"
    elif ke[item2] == item1:
        return "克"
    elif sheng[item1] == item2:
        return "泄"
    elif item1 == item2:
        return "扶"

def get_shengfukexie(bazi):
    # 计算八字中各个位置跟日柱的生、扶、克、泄的关系
    # 计算八字中的五行属性
    # 月令可能为None，此时要看旺相休囚死
    # [[{'甲': ['阳', '木', '克', 5]}, {'丙': ['阳', '火', '生', 10]}, {'己': ['阴', '土', 'S', 'S']}, {'甲': ['阳', '木', '克', 10]}], 
    # [{'戌': ['阳', '土', '扶', 5]}, {'子': ['阳', '水', 'Y',50]}, {'卯': ['阴', '木', '克', 10]}, {'戌': ['阳', '土', '扶', 7.5]}]]
    bazi_wuxing = []
    for i in range(len(bazi)):
        item = []
        for j in range(len(bazi[i])):
            if i == 0 and j == 2 :
                # 日柱不用算
                item.append({bazi[i][j]:[tiangan_dizhi[bazi[i][j]][0],tiangan_dizhi[bazi[i][j]][1],"S",12.5]})
                continue 
            if i == 1 and j == 1:
                item.append({bazi[i][j]:[tiangan_dizhi[bazi[i][j]][0],tiangan_dizhi[bazi[i][j]][1],"Y",50]})
                continue
            # 添加生扶克泄，五行属性
            sfkx = compute_shengkexie(tiangan_dizhi[bazi[0][2]][1],tiangan_dizhi[bazi[i][j]][1])
            item.append({bazi[i][j]:[tiangan_dizhi[bazi[i][j]][0],tiangan_dizhi[bazi[i][j]][1],sfkx]})
            # 添加位置分
            if (i == 0 and j == 0) or (i == 1 and j == 0):
                item[-1][bazi[i][j]].append(7.5)
            elif (i == 1 and j == 3):
                item[-1][bazi[i][j]].append(10)
            elif (i == 0 and j == 1) or (i == 0 and j == 3) or (i == 1 and j == 2):
                item[-1][bazi[i][j]].append(12.5)
        #     elif (i == 1 and j == 1):
        #         item[-1][bazi[i][j]].append(50)

        bazi_wuxing.append(item[::])
    return bazi_wuxing

def get_yueling_wangxiangxiuqiusi(yueling,rizhu_wuxing):
    wxxqs = {
        "寅卯":{"木":1,"火":0.8,"水":0.6,"金":0.8,"土":1},
        "巳午":{"火":1,"土":0.8,"木":0.6,"水":0.8,"金":1},
        "申酉":{"金":1,"水":0.8,"土":0.6,"火":0.8,"木":1},
        "亥子":{"水":1,"木":0.8,"金":0.6,"土":0.8,"火":1},
        "辰未戌丑":{"土":1,"金":0.8,"火":0.6,"木":0.8,"水":1}
    }
    for item in wxxqs.keys():
        if yueling in item:
            # print(f"月令为:{yueling},日柱五行为：{rizhu_wuxing},月令分为：{wxxqs[item][rizhu_wuxing]*50}")
            return wxxqs[item][rizhu_wuxing]*50

            
def get_yueling_score(bazi):
    rizhu = bazi[0][2]
    yueling = bazi[1][1]
    rizhu_wuxing = tiangan_dizhi[rizhu][1]
    yueling_wuxing = tiangan_dizhi[yueling][1]
    yueling_score = get_yueling_wangxiangxiuqiusi(yueling,rizhu_wuxing)
    return yueling_wuxing,yueling_score

def get_bazi_score(wuxing_score,bazi,tiangan_dizhi):
    # 计算八字位置所得分数,只需要计算天干即可，因为地支通过藏干来算
    bazi_wuxing = get_shengfukexie(bazi)
    for j in range(len(bazi_wuxing[0])):
        if list(bazi_wuxing[0][j].values())[0][2] not in ["Y"]:
            # 去掉月令
            # print(f"八字位置:{list(bazi_wuxing[0][j].values())[0][1]},得分：{list(bazi_wuxing[0][j].values())[0][3]}")
            wuxing_score[list(bazi_wuxing[0][j].values())[0][1]] += list(bazi_wuxing[0][j].values())[0][3]
    
    # 藏干表
    canggan = {
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
    for i in range(len(bazi[1])):
        dizhicanggan.append(canggan[bazi[1][i]])
    # 计算藏干得分
    for i in range(len(dizhicanggan)):
        if i == 1:
            continue
        if len(dizhicanggan[i]) == 1:
            wuxing_score[tiangan_dizhi[dizhicanggan[i]][1]] += list(bazi_wuxing[1][i].values())[0][3]
        elif len(dizhicanggan[i]) == 2:
            canggan_list = list(dizhicanggan[i])
            for index,item in enumerate(canggan_list):
                if index == 0:
                    wuxing_score[tiangan_dizhi[item][1]] += list(bazi_wuxing[1][i].values())[0][3]*0.7
                elif index == 1:
                    wuxing_score[tiangan_dizhi[item][1]] += list(bazi_wuxing[1][i].values())[0][3]*0.3
        else:
            canggan_list = list(dizhicanggan[i])
            for index,item in  enumerate(canggan_list):
                if index == 0:
                    # print(f"藏干：{tiangan_dizhi[item][1]},得分{list(bazi_wuxing[1][i].values())[0][3]*0.65}")
                    wuxing_score[tiangan_dizhi[item][1]] += list(bazi_wuxing[1][i].values())[0][3]*0.65
                elif index == 1:
                    # print(f"藏干：{tiangan_dizhi[item][1]},得分{list(bazi_wuxing[1][i].values())[0][3]*0.25}")
                    wuxing_score[tiangan_dizhi[item][1]] += list(bazi_wuxing[1][i].values())[0][3]*0.25
                else:
                    # print(f"藏干：{tiangan_dizhi[item][1]},得分{list(bazi_wuxing[1][i].values())[0][3]*0.10}")
                    wuxing_score[tiangan_dizhi[item][1]] += list(bazi_wuxing[1][i].values())[0][3]*0.10
    return wuxing_score,dizhicanggan

def get_hehua_score(wuxing_score,bazi):
    yueling = bazi[1][1]
    wxxqs = {
        "寅卯":{"木":1,"火":0.8,"水":0.6,"金":0.4,"土":0.2},
        "巳午":{"火":1,"土":0.8,"木":0.6,"水":0.4,"金":0.2},
        "申酉":{"金":1,"水":0.8,"土":0.6,"火":0.4,"木":0.2},
        "亥子":{"水":1,"木":0.8,"金":0.6,"土":0.4,"火":0.2},
        "辰未戌丑":{"土":1,"金":0.8,"火":0.6,"木":0.4,"水":0.2}
    }
    hehua = {
        "三合":["申子辰三合水局","寅午戌三合火局","巳酉丑三合金局","亥卯未三合木局","辰戌丑未三合土局",2],
        "三会":["寅卯辰三会木局","巳午未三会火局","亥子丑三会水局","申酉戌三会金局",2],
        "六合":["子丑合化土","卯戌合化火","辰酉合化金","巳申合化水","午未合化火或土",1],
        "半三合":["申子、子辰半合水局","寅午、午戌半合火局","巳酉、酉丑半合金局","亥卯、卯未半合木局",0.65],
        "半三会":["寅卯、卯辰半会木局","巳午、午未半会火局","亥子、子丑半会水局","申酉、酉戌半会金局",0.35],
        "拱合":["寅午戌拱火局","申子辰拱水局","巳酉丑拱金局","亥卯未拱木局",0.0075],
    }

    hehua_name = []
    hehuayuansu = []
    hehua_num = []

    # 统计所有地支关系的数量
    counts = count_earthly_branch_combinations(bazi)
    for (category, comb, *element), count in counts.items():
        if category in ["三合","三会","六合","半三合","半三会","拱合"]:
            # print(''.join(comb) if isinstance(comb, tuple) else ''.join(comb),category,element,count)
            hehua_name.append(category)
            hehuayuansu.append(element[0][-2])
            hehua_num.append(int(count))

    for item in wxxqs.keys():
        if yueling in item:
            for i in range(len(hehua_name)):
                wuxing_score[hehuayuansu[i]] += wxxqs[item][hehuayuansu[i]]*50*hehua[hehua_name[i]][-1]*hehua_num[i]
                # if hehuayuansu[i] == "金":
                #     print(wxxqs[item][hehuayuansu[i]]*50*hehua[hehua_name[i]][-1]*hehua_num[i])
            break


    # 记录所有的刑冲合害破
    xchhp = []
    for (category, comb, *element), count in counts.items():
        comb_str = ''.join(comb) if isinstance(comb, tuple) else ''.join(comb)
        if category in ["害","破"]:
            xchhp.append(f"{comb_str}相{category}")
        elif category in ["三刑","半三刑","自刑"]:
            xchhp.append(f"{comb_str}相刑")
        elif category in ["六冲"]:
            xchhp.append(f"{comb_str}相冲")
        elif category == "暗合":
            xchhp.append(f"{comb_str}暗合")
        elif category in ["六合"]:
            xchhp.append(f"{comb_str}合化{element[0][-2]}局")
        elif category in ["三合"]:
            xchhp.append(f"{comb_str}三合{element[0][-2]}局")
        elif category in ["半三合"]:
            xchhp.append(f"{comb_str}半合{element[0][-2]}局")
        elif category in ["半三会"]:
            xchhp.append(f"{comb_str}半会{element[0][-2]}局")
        elif category in ["拱合"]:
            xchhp.append(f"{comb_str}拱合{element[0][-2]}局")
    return wuxing_score,xchhp


def get_qiangruo(bazi):
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    shengfu = bazi_sfzk["生扶"].split("，")
    kexie = bazi_sfzk["克泄"].split("，")
    shengfu_scale = 0
    kexie_scale = 0
    for item in shengfu:
        shengfu_scale += float(wuxing_scale[item].strip("%"))
    for item in kexie:
        kexie_scale += float(wuxing_scale[item].strip("%"))
    if shengfu_scale >=0 and shengfu_scale < 6.25:
        return "极至弱"
    elif shengfu_scale >=6.25 and shengfu_scale < 12.5:
        return "极弱"
    elif shengfu_scale >= 12.5 and shengfu_scale < 18.75:
        return "太弱"
    elif shengfu_scale >= 18.75 and shengfu_scale < 25:
        return "过弱"
    elif shengfu_scale >= 25 and shengfu_scale < 31.25:
        return "很弱"
    elif shengfu_scale >= 31.25 and shengfu_scale < 37.5:
        return "弱"
    elif shengfu_scale >= 37.5 and shengfu_scale < 43.75:
        return "偏弱"
    elif shengfu_scale >= 43.75 and shengfu_scale < 50:
        return "稍弱"
    elif shengfu_scale >= 50 and shengfu_scale < 56.25:
        return "中和"
    elif shengfu_scale >= 56.25 and shengfu_scale < 62.5:
        return "稍强"
    elif shengfu_scale >= 62.5 and shengfu_scale < 68.75:
        return "偏强"
    elif shengfu_scale >= 68.75 and shengfu_scale < 75:
        return "强"
    elif shengfu_scale >= 75 and shengfu_scale < 81.25:
        return "很强"
    elif shengfu_scale >= 81.25 and shengfu_scale <= 87.5:
        return "过强"
    elif shengfu_scale >= 87.5 and shengfu_scale <= 93.75:
        return "太强"
    elif shengfu_scale >= 93.75 and shengfu_scale < 100:
        return "极强"
    elif shengfu_scale > 100:
        return "极至强"


def wuxingliliang(bazi):
        wuxing_score = {
                "金":0,
                "木":0,
                "水":0,
                "火":0,
                "土":0,
                        }
        # 计算月令五行得分
        yueling_wuxing,yueling_score = get_yueling_score(bazi)
        wuxing_score[yueling_wuxing] += yueling_score
        # 计算八字五行力量
        wuxing_score,dizhicanggan = get_bazi_score(wuxing_score,bazi,tiangan_dizhi)
        # 计算合化力量
        wuxing_score,xchhp = get_hehua_score(wuxing_score,bazi)
        # 计算总和
        total = sum(wuxing_score.values())
        # 计算占比
        percentage_data = {k: (v / total) * 100 for k, v in wuxing_score.items()}
        wuxing_scale = {k: str(round(v, 3))+"%" for k, v in percentage_data.items()}
        # 计算日元的生扶克泄
        bazi_wuxing = tiangan_dizhi[bazi[0][2]][1]
        bazi_sfzk = compute_bazisfkx(bazi_wuxing)
        return bazi_sfzk,wuxing_scale,wuxing_score



# bazi = [['甲', '丙', '己', '甲'],['戌', '子', '卯', '戌']]
# bazi = [ ['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
# bazi = [["庚","癸","庚","丙"],["午","未","辰","子"]]
# bazi = [["癸","壬","甲","甲"],["酉","戌","子","子"]]
# bazi = [["丁","丁","甲","癸"],["亥","未","子","酉"]]
# bazi = [['丙', '甲', '丙', '甲'],['寅', '午', '午', '午']]
# bazi = [['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
# bazi = [['甲', '甲', '乙', '丙'], ['辰', '戌', '丑', '子']]

# bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
# print(wuxing_score)
# # 计算身强身弱
# qiangruo = get_qiangruo(bazi)
# print(qiangruo)
