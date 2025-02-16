import dashscope
from http import HTTPStatus
import logging
import uvicorn
from config import qianwen_key
from fastapi import FastAPI
from pydantic import BaseModel
from qiangruo import wuxingliliang, get_qiangruo
from guiqi import guiqi_level
from mingge import get_mingge
from function_tools import get_bazi, get_dayun, get_changsheng, get_shensha, get_age, get_canggan, get_shishen
import pytz
from datetime import datetime
from prompts import all_prompt, question_prompt, ask_birthdate_prompt
from file_process import write_to_markdown
import requests
import json
import asyncio

# ======================= 日志系统配置 =======================
# 创建 logger 对象
logger = logging.getLogger("bazi_app")
logger.setLevel(logging.DEBUG)  # 设置最低日志级别为 DEBUG

# 创建控制台 handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台只输出 INFO 级别及以上
console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# 创建文件 handler，保存详细日志
file_handler = logging.FileHandler("bazi_app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s')
file_handler.setFormatter(file_formatter)

# 将 handler 添加到 logger 中
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("日志系统初始化完成。")

# ======================= FastAPI 应用实例 =======================
app = FastAPI()

# ======================= 请求数据模型 =======================
class BaziRequest(BaseModel):
    input_time: str  # 格式：YYYY-MM-DD HH:MM:SS
    sex: str         # 性别，例如：男 或 女

class AskRequest(BaseModel):
    question: str    # 用户提问的问题
    user_id: str     # 用户ID

class AskRequest_Load(BaseModel):
    input_time: str  # 格式：YYYY-MM-DD HH:MM:SS
    sex: str         # 性别，例如：男 或 女
    question: str    # 用户提问的问题

# ======================= 数据库操作相关函数 =======================
def insert_user_birthdate(user_id, birthdate, sex):
    """
    向远程服务器插入用户的出生年月日时和性别信息
    """
    logger.debug(f"进入 insert_user_birthdate: user_id={user_id}, birthdate={birthdate}, sex={sex}")
    url = "http://117.147.213.226:8000/insert_data/"
    data = {
        "db_name": "mingli",
        "table_name": "birthdate",
        "columns": "id,birthdate,sex,time",
        "values": f"{user_id},{birthdate},{sex}"
    }
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        logger.info(f"插入用户({user_id})出生信息成功，响应码：{response.status_code}")
    except Exception as e:
        logger.error(f"插入用户({user_id})出生信息出错：{str(e)}")

def update_user_birth_info(user_id, birthdate=None, sex=None):
    """
    更新用户的出生日期和/或性别信息
    """
    logger.debug(f"进入 update_user_birth_info: user_id={user_id}, birthdate={birthdate}, sex={sex}")
    
    # 构造更新子句
    clauses = []
    if birthdate is not None:
        clauses.append(f'birthdate = "{birthdate}"')
    if sex is not None:
        clauses.append(f'sex = "{sex}"')

    set_clause = ", ".join(clauses)
    url = "http://117.147.213.226:8000/update_data/"
    data = {
        "db_name": "mingli",
        "table_name": "birthdate",
        "set_clause": set_clause,
        "condition": f'id={user_id}'
    }
    try:
        response = requests.put(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        logger.info(f"更新用户({user_id})信息成功，响应码：{response.status_code}")
    except Exception as e:
        logger.error(f"更新用户({user_id})信息出错：{str(e)}")

def get_user_birthdate(user_id):
    """
    从远程服务器查询用户的出生年月日时和性别信息
    """
    logger.debug(f"进入 get_user_birthdate: user_id={user_id}")
    url = "http://117.147.213.226:8000/select_data/"
    data = {
        "db_name": "mingli",
        "table_name": "birthdate",
        "condition": f'id="{user_id}"'
    }
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        result = response.json()
        logger.info(f"查询用户({user_id})出生信息成功，结果：{result}")
        if "data" in result and result["data"]:
            return result["data"][0]
        else:
            logger.info(f"查询用户({user_id})无数据。")
            return "None"
    except Exception as e:
        logger.error(f"查询用户({user_id})出生信息出错：{str(e)}")
        return "None"

# ======================= 与大模型交互相关函数 =======================
def ask_birthdate(question):
    """
    当查询不到用户出生信息时，调用此函数构造提醒用户提供出生年月日时和性别的对话。
    提示语模板中要求用户按照指定格式“%Y-%m-%d %H:%M:%S#sex”提供数据。
    """
    logger.debug(f"进入 ask_birthdate，问题：{question}")
    prompt = ask_birthdate_prompt.format(question=question)
    logger.info(f"生成 ask_birthdate 的 Prompt: {prompt}")
    try:
        response = dashscope.Generation.call(
            "deepseek-r1",
            messages=[{'role': 'user', 'content': prompt}],
            result_format='message',
            stream=False,
            incremental_output=False
        )
        if response.status_code == HTTPStatus.OK:
            response_text = response.output.choices[0]['message']['content']
            logger.info("ask_birthdate 调用大模型接口成功。")
            return response_text
        else:
            error_msg = (f"请求ID: {response.request_id}, 状态码: {response.status_code}, "
                         f"错误码: {response.code}, 错误信息: {response.message}")
            logger.error(f"ask_birthdate 大模型接口返回错误: {error_msg}")
            return error_msg
    except Exception as e:
        logger.error(f"ask_birthdate 出错：{str(e)}")
        return f"ask_birthdate 出错：{str(e)}"

def get_ai_response_stream(prompt):
    """
    调用大模型接口，采用流式响应获取回答内容
    """
    logger.debug(f"进入 get_ai_response_stream，Prompt: {prompt[:50]}...")  # 仅显示前50字符
    response_text = ""
    try:
        response_generator = dashscope.Generation.call(
            "deepseek-r1",
            messages=[{'role': 'user', 'content': prompt}],
            result_format='message',
            stream=True,
            incremental_output=True
        )
        for message in response_generator:
            if hasattr(message, "output") and message.output.choices:
                response_text += message.output.choices[0]['message']['content']
        logger.info("get_ai_response_stream 大模型接口流式调用成功。")
    except Exception as e:
        logger.error(f"流式响应处理出错：{str(e)}")
        return f"流式响应处理出错：{str(e)}"
    # write_to_markdown(content=response_text)
    if response_text:
        logger.debug(f"get_ai_response_stream 返回结果: {response_text[:50]}...")
        return response_text
    else:
        logger.warning("get_ai_response_stream 未能获取有效响应。")
        return "未能获取有效响应"

async def async_get_ai_response_stream(prompt: str):
    """
    异步包装 get_ai_response_stream，避免阻塞事件循环
    """
    logger.debug("进入 async_get_ai_response_stream。")
    return await asyncio.to_thread(get_ai_response_stream, prompt)

# ======================= 提取八字及生成 prompt 的函数 =======================
def build_question_prompt(birthdate: str, sex: str, question: str) -> str:
    """
    根据出生时间、性别和用户问题生成用于大模型回答的 prompt，
    包含八字、五行、神煞等命理信息以及当前时间等。
    """
    logger.debug(f"生成 question_prompt，birthdate={birthdate}, sex={sex}, question={question}")
    bazi = get_bazi(birthdate)
    bazi_sfzk, wuxing_scale, wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shensha = get_shensha(bazi, sex)
    dayun_data = get_dayun(birthdate, sex)
    changsheng = get_changsheng(bazi, dayun_data)
    guiqi_ = guiqi_level(bazi)
    mingge = get_mingge(bazi)
    canggan = get_canggan(bazi)
    shishen = get_shishen(bazi)
    age = get_age(birthdate)
    beijing_tz = pytz.timezone("Asia/Shanghai")
    beijing_time = datetime.now(beijing_tz)
    now_bazi = get_bazi(beijing_time.strftime("%Y-%m-%d %H:%M:%S"), mark=False)
    prompt = question_prompt.format(
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
        sex=sex,
        question=question,
        current_time=beijing_time.strftime("%Y-%m-%d %H:%M:%S"),
        current_hour_pillar=now_bazi
    )
    logger.info(f"生成的 question_prompt 完成。")
    return prompt

def build_calculate_prompt(birthdate: str, sex: str) -> str:
    """
    根据出生时间和性别生成用于计算八字等命理信息的 prompt，
    使用 all_prompt 模板。
    """
    logger.debug(f"生成 calculate_prompt，birthdate={birthdate}, sex={sex}")
    bazi = get_bazi(birthdate)
    bazi_sfzk, wuxing_scale, wuxing_score = wuxingliliang(bazi)
    qiangruo = get_qiangruo(bazi)
    shensha = get_shensha(bazi, sex)
    dayun_data = get_dayun(birthdate, sex)
    changsheng = get_changsheng(bazi, dayun_data)
    guiqi_ = guiqi_level(bazi)
    mingge = get_mingge(bazi)
    canggan = get_canggan(bazi)
    shishen = get_shishen(bazi)
    age = get_age(birthdate)
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
        sex=sex,
    )
    logger.info("生成的 calculate_prompt 完成。")
    return prompt

async def process_question(birthdate: str, sex: str, question: str) -> str:
    """
    根据出生信息和用户问题生成 prompt，并调用大模型接口返回回答。
    """
    logger.debug("进入 process_question。")
    prompt = build_question_prompt(birthdate, sex, question)
    logger.debug("调用 async_get_ai_response_stream 获取大模型回答。")
    ai_response = await async_get_ai_response_stream(prompt)
    logger.debug("process_question 返回结果。")
    return ai_response

# ======================= API 路由 ======================
@app.post("/ask")
async def ask_bazi_question(request: AskRequest):
    """
    提供问答服务：
    1. 根据用户ID查询用户出生信息，如果查询不到则调用 ask_birthdate 提示用户提供出生信息；
    2. 如果收到符合格式的出生信息，则将信息写入数据库，并基于出生信息生成命理数据后调用大模型回答问题。
    """
    logger.info(f"接收到 /ask 请求，用户ID: {request.user_id}，问题: {request.question}")
    user_id = request.user_id
    # 首先查询用户出生信息
    user_inf = await asyncio.to_thread(get_user_birthdate, user_id)
    # 如果查不到（此时用户的话里可能已有出生年月日时，也可能没有）
    if user_inf == "None":
        logger.info(f"用户({user_id})出生信息未查询到，调用 ask_birthdate。")
        response = await asyncio.to_thread(ask_birthdate, request.question)
        # 如果用户说的话中有出生信息，此时大模型的回复会有体现，直接提取出生信息和回答，并将数据插入数据库
        if "&&" in response:
            # 用户提供了正确格式的信息(下面处理response的格式的原因跟prompt有关)
            user_birthdate = response.split("&&")[0]
            answer = response.split("&&")[1]
            birthdate_part = user_birthdate.split("#")[0]
            sex_part = user_birthdate.split("#")[1]
            await asyncio.to_thread(insert_user_birthdate, user_id, birthdate_part, sex_part)
            logger.info(f"用户({user_id})的出生信息已保存，返回回答。")
            return {"answer": answer}
        else:
            # 如果用户说的话中没有出生信息，直接返回提示。
            logger.info(f"用户({user_id})未提供有效的出生信息，返回提示。")
            return {"answer": response}
    else:
        # 如果查询到了用户的出生信息则会直接回复
        try:
            # 从数据库中取出的出生信息格式： [id, birthdate, sex, time]
            birthdate = user_inf[1].replace("T", " ")
            sex = user_inf[2]
            logger.debug(f"用户({user_id})查询到的出生信息：birthdate={birthdate}, sex={sex}")
            ai_response = await process_question(birthdate, sex, request.question)
            logger.info(f"用户({user_id})/ask 请求处理完成。")
            return {"answer": ai_response}
        except Exception as e:
            logger.error(f"处理用户({user_id}) /ask 请求时出错：{str(e)}")
            return {"answer": f"内部错误：{str(e)}"}

@app.post("/ask_load")
async def ask_bazi_question_load(request: AskRequest_Load):
    """
    本地测试接口：
    根据请求中提供的出生时间、性别和问题，生成命理信息并调用大模型回答问题。
    """
    logger.info(f"接收到 /ask_load 请求，输入时间: {request.input_time}, 性别: {request.sex}")
    try:
        ai_response = await process_question(request.input_time, request.sex, request.question)
        logger.info("/ask_load 请求处理完成。")
        return {"answer": ai_response}
    except Exception as e:
        logger.error(f"/ask_load 请求处理出错：{str(e)}")
        return {"answer": f"内部错误：{str(e)}"}

@app.post("/calculate")
async def calculate(request: BaziRequest):
    """
    计算命理信息接口：
    根据请求中的出生时间和性别，生成所有命理数据并调用大模型接口返回结果。
    """
    logger.info(f"接收到 /calculate 请求，输入时间: {request.input_time}, 性别: {request.sex}")
    try:
        prompt = build_calculate_prompt(request.input_time, request.sex)
        logger.debug("调用 async_get_ai_response_stream 获取 calculate 回答。")
        ai_response = await async_get_ai_response_stream(prompt)
        logger.info("/calculate 请求处理完成。")
        return {"answer": ai_response}
    except Exception as e:
        logger.error(f"/calculate 请求处理出错：{str(e)}")
        return {"answer": f"内部错误：{str(e)}"}

# ======================= 启动应用 =======================
if __name__ == "__main__":
    dashscope.api_key = qianwen_key
    logger.info("启动 FastAPI 应用，监听端口 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)