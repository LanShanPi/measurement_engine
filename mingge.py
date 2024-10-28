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

def get_mingge(bazi):
    # 计算五行占比和身强身弱
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shengfu = bazi_sfzk["生扶"].split("，")
    shengfu_score = round(float(wuxing_scale[shengfu[0]][:-1])+float(wuxing_scale[shengfu[1]][:-1]),3)
    if shengfu_score > 6.25:
        print("不入格")
    
    # 计算入什么格
    # 计算八字各个符号的属性
    


# bazi = [['甲', '甲', '乙', '丙'], ['辰', '戌', '丑', '子']]
# bazi = [['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
# bazi = [["丁","丁","甲","癸"],["亥","未","子","酉"]]
bazi = [["庚","壬","丙","庚"],["戌","子","辰","申"]]
get_mingge(bazi)