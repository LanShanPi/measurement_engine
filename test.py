import requests
import json
def update_user_birth_info(user_id, birthdate=None, sex=None):
    """
    更新用户的出生日期和/或性别信息
    如果 birthdate 和 sex 均为 None，则不做任何更新
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

update_user_birth_info(user_id="000001", birthdate="1800-12-03T12:00:00",sex="男")