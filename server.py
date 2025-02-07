from fastapi import FastAPI
from pydantic import BaseModel
from qiangruo import wuxingliliang, get_qiangruo
from guiqi import guiqi_level
from mingge import get_mingge
from function_tools import get_bazi, get_dayun, get_changsheng, get_shensha
import uvicorn

app = FastAPI()

# 定义请求数据模型
class BaziRequest(BaseModel):
    input_time: str  # 时间格式 YYYY-MM-DD HH:MM:SS
    sex: str  # 性别，男或女

@app.post("/calculate")
def calculate(request: BaziRequest):
    bazi = get_bazi(request.input_time)
    bazi_sfzk, wuxing_scale, wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shensha = get_shensha(bazi, request.sex)
    dayun_data = get_dayun(request.input_time, request.sex)
    changsheng = get_changsheng(bazi, dayun_data)
    guiqi_ = guiqi_level(bazi)
    mingge = get_mingge(bazi)

    return {
        "八字": bazi,
        "五行占比": wuxing_scale,
        "五行得分": wuxing_score,
        "强弱": qiangruo,
        "神煞": shensha,
        "大运年": dayun_data,
        "长生": changsheng,
        "贵气程度": guiqi_,
        "命格": mingge
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)