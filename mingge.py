from mingge_domain import get_congge,get_zhengbage,get_jianluge,get_biange

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
# bazi = [["庚","壬","甲","甲"],["巳","寅","子","子"]]
# bazi = [['甲', '丙', '己', '甲'],['戌', '子', '卯', '戌']]
# bazi = [["丁","乙","丙","己"],["丑","巳","子","丑"]]
# bazi = [["丁","癸","癸","甲"],["卯","丑","未","寅"]]
# bazi = [["丙","己","丙","乙"],["子","亥","子","未"]]
bazi = [["丙","癸","丙","戊"],["子","巳","午","戌"]]
get_mingge(bazi)


# 从格小于6.25，专旺大于93