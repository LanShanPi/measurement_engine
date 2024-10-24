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





from itertools import combinations


def count_earthly_branch_combinations(bazi):
    print(bazi)
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

def main(arg1) -> dict:
    print(arg1)
    bazi = [list(arg1[:4]),list(arg1[4:])]
    counts = count_earthly_branch_combinations(bazi)
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
            
    return {
        "result": str(xchhp),
    }


print(main("甲丙己甲戌子卯戌"))