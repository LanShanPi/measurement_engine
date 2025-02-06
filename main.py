from qiangruo import wuxingliliang,get_qiangruo
from guiqi import guiqi_level
from mingge import get_mingge
from function_tools import get_bazi,get_dayun,get_changsheng,get_shensha




def main(input_time,sex):
    bazi = get_bazi(input_time)
    print("八字：",bazi)

    # 计算五行占比
    bazi_sfzk,wuxing_scale,wuxing_score = wuxingliliang(bazi)
    print("五行占比：",wuxing_scale)
    print("五行得分：",wuxing_score)

    # 计算身强身弱
    qiangruo = get_qiangruo(bazi)
    print("强弱：",qiangruo)

    shensha = get_shensha(bazi,sex)
    print("神煞：",shensha)

    # 计算大运
    dayun_data = get_dayun(input_time,sex)
    print("大运年：",dayun_data)

    # 获取八字和大运的长生
    changsheng = get_changsheng(bazi, dayun_data)
    print(changsheng)


    # 计算贵气程度
    guiqi_ = guiqi_level(bazi)
    print("贵气程度：",guiqi_)

    # 计算命格
    mingge = get_mingge(bazi)
    print("命格：",mingge)

if __name__ == "__main__":
    # bazi = [["丙","癸","丙","戊"],["子","巳","午","戌"]]
    # 农历生日
    # input_time = "1997-10-10 23:30:00"
    # input_time = "1994-11-17 19:30:00"
    input_time = "2022-10-12 08:00:00"
    main(input_time,"男")