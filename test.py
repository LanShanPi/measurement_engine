
# from lunar_python import Lunar,EightChar
# from lunar_python.util import HolidayUtil
# from datetime import datetime 
# lunar = Lunar.fromDate(datetime.now())
# d = lunar.getEightChar()
# print(d)


import requests
import json

# 请求URL
url = "http://117.147.213.226:8000/insert_data/"

# 请求数据
data = {
    "db_name": "mingli",
    "table_name": "birthdate",
    "columns": "id,birthdate,sex,time",
    "values": "000002,1994-12-17T19:30:00,男"
}

# 发送POST请求
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

# 打印返回结果
print(response.status_code)
print(response.json())