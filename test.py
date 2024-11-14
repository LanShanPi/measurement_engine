import sys
sys.path.append(r"/Users/hzl/Project/measurement_engine/data/")
from yiji import yiji_

import pandas as pd

yiji1 = list(set(list(yiji_["宜"].keys())+list(yiji_["忌"].keys())))


# 读取 CSV 文件并将其存储为 DataFrame
df = pd.read_csv('/Users/hzl/Desktop/算命/名词解释.csv')

# 输出 DataFrame 内容
yiji2 = df["术语"].tolist()

result = []

for item in yiji2:
    if item not in yiji1:
        result.append(item)
print(result)
