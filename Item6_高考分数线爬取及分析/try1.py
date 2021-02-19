import pandas as pd

df = pd.read_csv(open(r"河南.csv",encoding='utf-8'))
data = df.values  # data是数组，直接从文件读出来的数据格式是数组
index1 = list(df.keys())  # 获取原有csv文件的标题，并形成列表
data = list(map(list, zip(*data)))  # map()可以单独列出列表，将数组转换成列表
data = pd.DataFrame(data, index=index1)  # 将data的行列转换
data.to_csv(r"河南2.csv", header=0)
