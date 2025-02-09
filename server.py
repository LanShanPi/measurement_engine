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
from file_process import write_to_markdown


app = FastAPI()

# 定义请求数据模型
class BaziRequest(BaseModel):
    input_time: str  # 时间格式 YYYY-MM-DD HH:MM:SS
    sex: str  # 性别，男或女


def get_ai_response(prompt):
    response = dashscope.Generation.call(
        "deepseek-r1",
        messages=[{'role': 'user', 'content': prompt}],
        result_format='message',  # 设定返回格式
        stream=False,  # 关闭流式输出
        incremental_output=False  # 关闭增量输出
    )

    if response.status_code == HTTPStatus.OK:
        response_text = response.output.choices[0]['message']['content']
        write_to_markdown(content=response_text)
        return response_text
    else:
        return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        )

def get_ai_response_stream(prompt):
    response_generator = dashscope.Generation.call(
        "deepseek-r1",
        messages=[{'role': 'user', 'content': prompt}],
        result_format='message',
        stream=True,  # 开启流式输出
        incremental_output=True  # 允许增量输出
    )

    # 由于 stream=True，返回的是生成器，无法直接获取 status_code
    response_text = ""

    try:
        for message in response_generator:  # 遍历流式返回的数据
            if hasattr(message, "output") and message.output.choices:
                response_text += message.output.choices[0]['message']['content']
    except Exception as e:
        return f"Error during stream processing: {str(e)}"
    write_to_markdown(content=response_text)

    return response_text if response_text else "未能获取有效响应"

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
    prompt = all_prompt.format(
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
                    sex=request.sex,
                )
    response = get_ai_response_stream(prompt)
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

