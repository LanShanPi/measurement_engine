# 24节气计算方法：https://zhuanlan.zhihu.com/p/101273758

from ephem import *
import math
import datetime


def ershisijieqi_v1(num,date):#从当前时间开始连续输出未来n个节气的时间
    #24节气
    jieqi=["春分","清明","谷雨","立夏","小满","芒种",\
        "夏至","小暑","大暑","立秋","处暑","白露",\
        "秋分","寒露","霜降","立冬","小雪","大雪",\
        "冬至","小寒","大寒","立春","雨水","惊蛰"]
    #计算黄经
    def ecliptic_lon(jd_utc):
        s=Sun(jd_utc)#构造太阳
        equ=Equatorial(s.ra,s.dec,epoch=jd_utc)#求太阳的视赤经视赤纬（epoch设为所求时间就是视赤经视赤纬）
        e=Ecliptic(equ)#赤经赤纬转到黄经黄纬
        return e.lon#返回黄纬
    #根据时间求太阳黄经，计算到了第几个节气，春分序号为0
    def sta(jd):
        e=ecliptic_lon(jd)
        n=int(e*180.0/math.pi/15)
        return n
    #根据当前时间，求下个节气的发生时间
    def iteration(jd,sta):#jd：要求的开始时间，sta：不同的状态函数
        s1=sta(jd)#初始状态(太阳处于什么位置)
        s0=s1
        dt=1.0#初始时间改变量设为1天
        while True:
            jd+=dt
            s=sta(jd)
            if s0!=s:
                s0=s
                dt=-dt/2#使时间改变量折半减小
            if abs(dt)<0.0000001 and s!=s1:
                break
        return jd

    # 输出的时间是阳历时间
    # jd=now()#获取当前时间的一个儒略日和1899/12/31 12:00:00儒略日的差值
    given_time_str = date
    # 将给定的时间字符串转换为 ephem.Date 格式
    jd = Date(given_time_str)
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)+1

    
    result = []
    # 存储指定日期前后的1个节气时间
    # 计算出来的月日时分秒都是小于10的时候都是一个数字
    for i in range(num):
        # 第一个位置存储指定日期后的第一个节气的日期，第二个位置存储节气名字
        temp = []
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=Date(jd+1/3).tuple()
        temp.append(str(d[0])+"-"+str(d[1])+"-"+str(d[2])+" "+str(d[3])+":"+str(d[4])+":"+str(d[5]))
        temp.append(jieqi[n])
        n+=1
        result.append(temp[::])
        temp.clear()
    # 返回格式：[['2024-1-6 4:49:9.657441', '小寒']] 
    return result

# result = ershisijieqi_v1(24,"2024-01-01 00:00:00")
# print(result)