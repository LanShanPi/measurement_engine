from config import qianwen_key
from fastapi import FastAPI
from pydantic import BaseModel
from qiangruo import wuxingliliang, get_qiangruo
from guiqi import guiqi_level
from mingge import get_mingge
from function_tools import get_bazi, get_dayun, get_changsheng, get_shensha,get_age,get_canggan,get_shishen
import uvicorn
from http import HTTPStatus
import dashscope
import pytz
from datetime import datetime
from prompts import all_prompt

app = FastAPI()

# 定义请求数据模型
class BaziRequest(BaseModel):
    input_time: str  # 时间格式 YYYY-MM-DD HH:MM:SS
    sex: str  # 性别，男或女

def get_ai_response(prompt):
    messages = [
        {'role': 'user', 'content': prompt}]
    responses = dashscope.Generation.call("deepseek-r1", #调用的模型接口
                                messages=messages,
                                result_format='message',  # set the result to be "message"  format.
                                stream=True, # 是否开启流式输出，不开启设置False
                                incremental_output=True  # 是否开启流式输出，不开启设置False
                                )
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0]['message']['content']
        else:
            return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            )


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
    canggan = get_canggan(bazi)
    shishen = get_shishen(bazi)
    beijing_tz = pytz.timezone("Asia/Shanghai")
    beijing_time = datetime.now(beijing_tz)
    now_bazi = get_bazi(beijing_time.strftime("%Y-%m-%d %H:%M:%S"),mark=False)
    age = get_age(request.input_time)
    all_prompt = all_prompt.prompt.format(
                    bazi=bazi,
                    wuxing_scale=wuxing_scale,
                    wuxing_score=wuxing_score,
                    qiangruo=qiangruo,
                    shensha=shensha,
                    dayun_data=dayun_data,
                    changsheng=changsheng,
                    guiqi_=guiqi_,
                    mingge=mingge,
                    canggan=canggan,
                    shishen=shishen,
                    age=age,
                    sex=request.sex
                )
    response = get_ai_response(all_prompt)
    return response

    # return {
    #     "八字": bazi,
    #     "五行占比": wuxing_scale,
    #     "五行得分": wuxing_score,
    #     "强弱": qiangruo,
    #     "神煞": shensha,
    #     "大运年": dayun_data,
    #     "长生": changsheng,
    #     "贵气程度": guiqi_,
    #     "命格": mingge,
    #     "地支藏干": canggan,
    #     "十神": shishen,
    #     "性别": request.sex,
    #     "当前命主年纪": age,
    #     "当前时间八字": now_bazi,
    # }

if __name__ == "__main__":
    dashscope.api_key = qianwen_key
    uvicorn.run(app, host="0.0.0.0", port=8001)

