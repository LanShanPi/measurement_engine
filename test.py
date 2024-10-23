from itertools import combinations

# bazi = [ ['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
bazi = [['甲', '丙', '己', '甲'],
            ['戌', '子', '寅', '卯']]

# 所有地支关系定义
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

def count_earthly_branch_combinations(bazi, all_relationships):
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

# 统计所有地支关系的数量
counts = count_earthly_branch_combinations(bazi, all_relationships)

# 打印结果
for (category, comb, *element), count in counts.items():
    # comb_str = ''.join(comb) if isinstance(comb, tuple) else ''.join(comb)
    # element_str = f" 合化 {element[0]}" if element else ""
    # print(f"地支中有 {count} 个 {category}：{comb_str}{element_str} 的组合。")
    
    if category in ["三合","三会","六合","半三合","半三会","拱合"]:
        print(''.join(comb) if isinstance(comb, tuple) else ''.join(comb))
        print(element)
