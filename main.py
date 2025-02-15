from qiangruo import wuxingliliang,get_qiangruo
from guiqi import guiqi_level
from mingge import get_mingge
from function_tools import get_bazi,get_dayun,get_changsheng,get_shensha,get_canggan,get_age,get_shishen
import pytz
from datetime import datetime



def main(input_time,sex):
    bazi = get_bazi(input_time)
    print("八字：",bazi)

    canggan = get_canggan(bazi)
    print("地支藏干：",canggan)

    shishen = get_shishen(bazi)
    print("十神：",shishen)

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

    # 获取当前时间八字
    beijing_tz = pytz.timezone("Asia/Shanghai")
    beijing_time = datetime.now(beijing_tz)
    now_bazi = get_bazi(beijing_time.strftime("%Y-%m-%d %H:%M:%S"),mark=False)
    print("当前时间八字：",now_bazi)

    # 获取年纪
    age = get_age(input_time)
    print("当前命主年纪：",age)

if __name__ == "__main__":
    # bazi = [["丙","癸","丙","戊"],["子","巳","午","戌"]]
    # 农历生日
    # input_time = "1997-10-10 23:30:00"
    input_time = "1994-11-17 19:30:00"
    # input_time = "1993-08-25 23:35:00"
    main(input_time,"男")