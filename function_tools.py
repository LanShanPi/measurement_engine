def get_xun(ganzhi="甲辰"):
    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 计算干支所处旬的初始年
    tiangan_ = ganzhi[0]
    dizhi_ = ganzhi[1]
    tiangan_index_ = tiangan.index(tiangan_)
    dizhi_index_ = dizhi.index(dizhi_)
    back_step = 0
    while True:
        if tiangan[tiangan_index_-back_step] == "甲":
            break
        back_step = (back_step+1)%10
    # 地支减去back_step，另外减1=加11，减2等于加10，依此类推
    chushi_dizhi = dizhi[(dizhi_index_+(12-back_step))%12]

    chushi_xun = "甲"+chushi_dizhi

    # 指定干支对应的空亡（旬空，也叫空亡。由于十天干和十二地支搭配，每旬总会多出来两个地支。这两个地支就叫旬空。）
    kongwang1 = dizhi[(dizhi.index(chushi_dizhi)+9+1)%12]
    kongwang2 = dizhi[(dizhi.index(chushi_dizhi)+9+2)%12]
    kongwang = kongwang1+kongwang2
    return chushi_xun,kongwang
