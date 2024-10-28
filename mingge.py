from qiangruo import get_qiangruo,wuxingliliang

def get_mingge(bazi):
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    print(bazi_sfzk,wuxing_scale,wuxing_score,qiangruo)


# bazi = [['甲', '甲', '乙', '丙'], ['辰', '戌', '丑', '子']]
# bazi = [['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
# bazi = [["丁","丁","甲","癸"],["亥","未","子","酉"]]
bazi = [["庚","壬","丙","庚"],["戌","子","辰","申"]]
get_mingge(bazi)