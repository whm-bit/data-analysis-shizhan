import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号‘-’显示为方块的问题



df = pd.read_csv("data_code.csv",encoding="utf-8")
t1 = df.copy()
# print(t1)
t1["count"]=1
t1_result = t1.groupby("性别")["count"].agg(["count"]) # 可以把性别改成年龄

age = t1_result.index.tolist()
numbers = t1_result.values.tolist()

plt.pie(numbers,labels=age,autopct="%1.2f")
plt.title("未知数据年龄段显示",color="white")
plt.axis("equal")
plt.show()