from itertools import combinations
from collections import defaultdict, Counter
import math

def count_earthly_branch_combinations_with_scores(bazi):
    # 定义所有可能的关系及其组合（直接附带分数）
    all_relationships = {
        "六冲": ([
            ("子", "午"), ("丑", "未"), ("寅", "申"),
            ("卯", "酉"), ("辰", "戌"), ("巳", "亥")
        ], 1),
        "半三刑": ([
            ("寅", "巳"), ("巳", "申"),("子", "卯")
        ], 0.66),
        "自刑": ([
            ("辰", "辰"), ("午", "午"), ("酉", "酉"), ("亥", "亥")
        ], 0.66),
        "害": ([
            ("子", "未"), ("丑", "午"), ("寅", "巳"),
            ("卯", "辰"), ("申", "亥"), ("酉", "戌")
        ], 0.5),
        "破": ([
            ("子", "酉"), ("丑", "辰"), ("寅", "亥"),
            ("卯", "午"), ("戌", "未"), ("巳", "申")
        ], 0.33),
        "六合": ([
            ("子", "丑"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未")
        ], 1),
        "半三合": ([
            ("申", "子"), ("子", "辰"), ("寅", "午"), ("午", "戌"),
            ("巳", "酉"), ("酉", "丑"), ("亥", "卯"), ("卯", "未")
        ], 0.66),
        "拱合": ([
            ("寅", "戌"), ("申", "辰"), ("巳", "丑"), ("亥", "未")
        ], 0.33)
    }

    count_dict = defaultdict(float)  # 使用 defaultdict 来简化计数逻辑
    branches = bazi[1]  # 取出地支部分

    # 遍历所有类型的关系
    for category, (relationships, base_score) in all_relationships.items():
        for comb in relationships:
            # 生成所有可能的索引子集，长度为组合长度
            for subset in combinations(range(len(branches)), len(comb)):
                subset_branches = [branches[i] for i in subset]  # 保留重复元素
                if Counter(subset_branches) == Counter(comb):  # 比较元素及其出现次数
                    position_score = calculate_position_score(list(subset))  # 计算位置系数
                    score = base_score * position_score  # 计算总得分
                    key = (category, tuple(comb), subset)  # 使用包含位置的键，以区分不同的组合实例
                    count_dict[key] += score  # 累加相同关系的得分

    return count_dict

def calculate_position_score(indices):
    # 计算位置系数
    indices.sort()  # 对索引进行排序
    gaps = [j - i - 1 for i, j in zip(indices, indices[1:])]  # 计算相邻地支之间的实际间隔数量
    max_gap = max(gaps, default=0)  # 获取最大间隔

    if max_gap == 0:
        return 1  # 相邻（间隔为 0），位置系数为 1
    elif max_gap == 1:
        return 2 / 3  # 间隔为 1，位置系数为 2/3
    elif max_gap == 2:
        return 1 / 3  # 间隔为 2，位置系数为 1/3
    else:
        return 0  # 超过两个间隔不计算分数

def normal_cdf(z):
    """计算标准正态分布的累积分布函数 (CDF)。"""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

def get_guiqi(group1_score,group2_score):
    """
    根据正面和负面关系的比值和差值来计算命格评级。
    - group1_score: 负面关系总分（刑冲害破）
    - group2_score: 正面关系总分（六合、三合、拱合）
    """
    score = group1_score+group2_score
    if score <= -3 or score >= 3:
        return "天赐"
    elif score > -3 and score <= -2.175:
        return "初绽"
    elif score > -2.175 and score <= -1.35:
        return "含光"
    elif score > -1.35 and score <= -0.525:
        return "清扬"
    elif score > -0.525 and score <= 0.3:
        return "明华"
    elif score > 0.3 and score <= 0.975:
        return "属泽"
    elif score > 0.975 and score <= 1.65:
        return "灵瑞"
    elif score > 1.65 and score <= 2.325:
        return "煊耀"
    elif score > 2.325 and score < 3:
        return "辉煌"

def main(bazi):
    # 计算八字中地支的所有关系及其得分
    counts = count_earthly_branch_combinations_with_scores(bazi)
    group1_score = 0  # 用于存储【六冲，三刑，半三刑，自刑，害，破】的总得分
    group2_score = 0  # 用于存储【六合，半三合、拱合】的总得分

    # 遍历所有关系及其得分
    for (category, comb, subset), score in counts.items():
        comb_str = ''.join(comb)  # 组合的字符串表示
        subset_str = ', '.join(str(i) for i in subset)  # 位置的字符串表示
        print(f"地支中有 {category}：{comb_str} 的组合，位置为：{subset_str}，总分为：{score:.2f}")
        
        # 根据类别分配得分到不同组
        if category in ["六冲", "三刑", "半三刑", "自刑", "害", "破"]:
            group1_score += score
        elif category in ["六合", "半三合", "拱合"]:
            group2_score += score
    
    # 计算贵气程度
    guiqi_dengji = get_guiqi(group1_score,group2_score)

    return {
        "he":round(group2_score,2),
        "chongxinghaipo":round(group1_score, 2),
        "guiqichengdu":guiqi_dengji
    }

    

    

if __name__ == "__main__":
    # 示例八字，包含天干和地支
    bazi = [['甲', '丙', '己', '甲'],['戌', '子', '卯', '戌']]
    # bazi = [ ['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
    # bazi = [["庚","癸","庚","丙"],["午","未","辰","子"]]
    # bazi = [["癸","壬","甲","甲"],["酉","戌","子","子"]]
    # bazi = [["丁","丁","甲","癸"],["亥","未","子","酉"]]
    # bazi = [ ['丙', '庚', '癸', '戊'],['午', '午', '午', '午']]
    main(bazi)
