from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import List
import uvicorn
from qiangruo import get_qiangruo,wuxingliliang
from guiqi import guiqi_level
from yunshi import tiaoxi
from datetime import datetime
from lunar_python import Lunar

app = FastAPI()

# 定义异步 POST 路由来处理八字分析
@app.post("/bazi")
async def bazi(request: Request):
    # 示例 bazi = [['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']]
    data = await request.json()
    bazi = data["bazi"]  # 获取八字嵌套列表
    _,wuxing_liliang = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    guiqi_dengji = guiqi_level(bazi)
    return {
        "message": "八字分析完成",
    }

# 生成调喜
@app.post("/tiaoxi")
async def tiaoxi(request: Request):
    # tiaoxi([['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']],"2024-10-28T11:04:54")
    # tiaoxi([['丙', '庚', '癸', '戊'],['子', '寅', '酉', '午']],"")
    # 从请求体中解析 JSON 数据
    data = await request.json()
    bazi = data["bazi"]  # 获取八字嵌套列表
    date = data["date"]  # 获取日期字符串并解析为 datetime 对象
    current_shichen,current_shichen_tiaoxi,all_shichen_tiaoxi = tiaoxi(bazi,date)
    yiji = Lunar.fromDate(datetime.now())
    # 宜
    yi = yiji.getDayYi()
    # 忌
    ji = yiji.getDayJi()
    return {
        "message": "八字分析完成",
    }


# 启动 FastAPI 服务
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
