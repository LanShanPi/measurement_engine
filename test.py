# # 定义八字和地支关系




# # 定义一个函数来判断给定的两个地支是否属于某种关系
# def check_relationship(pair, relationships):
#     for relationship, (pairs, score) in relationships.items():
#         if (pair[0], pair[1]) in pairs or (pair[1], pair[0]) in pairs:
#             return relationship, score
#     return None, 0

# def get_struction(bazi):
#     # 定义地支关系及其对应分数
#     all_relationships = {
#         "六冲": ([("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")], 1),
#         "半三刑": ([("寅", "巳"), ("巳", "申"), ("子", "卯"), ("丑", "戌"), ("戌", "未")], 0.67),
#         "自刑": ([("辰", "辰"), ("午", "午"), ("酉", "酉"), ("亥", "亥")], 0.67),
#         "害": ([("子", "未"), ("丑", "午"), ("寅", "巳"), ("卯", "辰"), ("申", "亥"), ("酉", "戌")], 0.5),
#         "破": ([("子", "酉"), ("丑", "辰"), ("寅", "亥"), ("卯", "午"), ("戌", "未"), ("巳", "申")], 0.33),
#         "六合": ([("子", "丑"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未"), ("寅", "亥")], 1),
#         "半三合": ([("申", "子"), ("子", "辰"), ("寅", "午"), ("午", "戌"), ("巳", "酉"), ("酉", "丑"), ("亥", "卯"), ("卯", "未")], 0.67),
#         "拱合": ([("寅", "戌"), ("申", "辰"), ("巳", "丑"), ("亥", "未")], 0.33)
#     }
#     # 记录有结构且可以冲合对消的情况，键为rel1的组合，值为rel2应该是的组合
#     rule1 = {
#         "六合":"六冲",
#         "六冲":"六合",
#         "半三刑":"半三合",
#         "半三合":"半三刑",
#     }
#     # 记录有结构但是无法冲合对消的组合，键为rel1的组合，值为rel2不能是的组合
#     rule2 = {
#         "六合":["六合","六冲","半三合","拱合"],
#         "半三合":["六合","拱合","半三刑","半三合"],
#         "拱合":["六合","半三合"],
#         "六冲":["六冲","六合","害","破","自刑","半三刑"],
#         "半三刑":["六冲","半三合","半三刑","害","破","自刑"],
#         "害":["害","破","自刑","半三刑","六冲"],
#         "破":["害","破","自刑","半三刑","六冲"],
#         "自刑":["害","破","自刑","半三刑","六冲"],
#     }
#     # 更新位置对，包含所有组合
#     position_pairs = [
#         [(0, 1), (2, 3)],
#         [(0, 2), (1, 3)],
#         [(0, 3), (1, 2)],
#         [(0, 1), (1, 3)],
#         [(1, 2), (2, 3)]
#     ]
#     # 计算有效组合的数量
#     valid_combinations = 0

#     num1 = [0]
#     num2 = [0]

#     # 遍历所有位置对组合
#     for pos1, pos2 in position_pairs:
#         branch1 = (bazi[1][pos1[0]], bazi[1][pos1[1]])
#         branch2 = (bazi[1][pos2[0]], bazi[1][pos2[1]])
        
#         # 检查每个位置对是否符合地支关系
#         rel1, score1 = check_relationship(branch1, all_relationships)
#         rel2, score2 = check_relationship(branch2, all_relationships)
        
        
#         # 判断是否符合“冲合对消”或“半三刑半三合”条件(有结构且能对消)
#         if (rel1 and rel2) and (rel2 == rule1[rel1]):
#             num1[0] = num1[0] + 1
#             print(f"对消组合: {pos1} 和 {pos2} -> 元素 {branch1} ({rel1}), {branch2} ({rel2})")
#         # 有结构，但是不能对消
#         if (rel1 and rel2) and (rel2 not in rule2[rel1]):
#             num2[0] = num2[0] + 1
#             print(f"不对消组合: {pos1} 和 {pos2} -> 元素 {branch1} ({rel1}), {branch2} ({rel2})")
            
#     print(f"对消组合为{num1[0]}对")
#     print(f"不对消组合为{num2[0]}对")


# bazi = [['丙', '甲', '丙', '甲'], ['子', '午', '子', '丑']]
# get_struction(bazi)



import requests
import json
from datetime import datetime

# def test_bazi_get():
#     """测试根据日期获取八字的接口"""
#     url = "http://42.123.114.119:8595/bazi_get"
    
#     # 测试不同的日期时间
#     test_dates = [
#         "2011-11-04T00:05:23",
#         "1994-12-19T19:00:00",
#         "2024-03-15T08:30:00",
#         "1988-06-25T15:45:00"
#     ]
    
#     for date_str in test_dates:
#         print(f"\n测试日期: {date_str}")
#         payload = {
#             "date_time": date_str
#         }
        
#         try:
#             print("发送请求...")
#             response = requests.post(url, json=payload)
#             print(f"状态码: {response.status_code}")
            
#             if response.status_code == 200:
#                 result = response.json()
#                 print("\n八字信息:")
#                 print(json.dumps(result, ensure_ascii=False, indent=2))
#             else:
#                 print(f"请求失败: {response.text}")
                
#         except requests.exceptions.ConnectionError:
#             print("错误: 无法连接到服务器，请确保服务器已启动")
#         except Exception as e:
#             print(f"错误: {str(e)}")
        
#         print("-" * 50)

# if __name__ == "__main__":
#     test_bazi_get()


def test_bazi_api():
    """测试八字分析接口"""
    # API地址
    url = "http://42.123.114.119:8595/wuxing_analysis_get"
    
    # 测试数据
    payload = {
        "tiangan": "甲,丙,己,甲",
        "dizhi": "戌,子,卯,戌"
    }
    
    try:
        # 发送POST请求
        print("\n正在发送请求...")
        response = requests.post(url, json=payload)
        
        # 检查响应状态
        print(f"状态码: {response.status_code}")
        
        # 打印响应结果
        print("\n响应结果:")
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请确保服务器已启动")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    test_bazi_api()
