import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体



def Glod_data():

    sql_gold_trade_code ="select TRADE_CODE from globalcommodityinfo where CATEGORY='黄金'"   # 从globalcommodityinfo表中查询黄金的trade_code
    df_gold_trade_code = pd.read_sql(sql_gold_trade_code,con=db) # 转化为DataFrame数据
    gold_trade_code = np.array(df_gold_trade_code).tolist()[0][0] #黄金的trade_code字符串


    sql_global_CLOSE = "select CLOSE from globalcommodity where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(gold_trade_code)

    sql_global_DT = "select DT from globalcommodity where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(gold_trade_code)


    df_CLOSE = pd.read_sql(sql_global_CLOSE,con=db) # DataFrame数据
    df_DT = pd.read_sql(sql_global_DT,con=db)

    df_CLOSE_list = np.array(df_CLOSE).tolist() # 将数据转换为矩阵再转化为列表

    df_DT_list = np.array(df_DT).tolist()


    gold_date=[]
    gold_close=[]


    for dt,cl in zip(df_DT_list,df_CLOSE_list):
        # print(dt[0],cl[0])
        gold_date.append(dt[0])
        gold_close.append(cl[0])

    return gold_date,gold_close

def Nird_data():

    sql_nird_trade_code = "select TRADE_CODE from globalindexinfo where SEC_NAME like '%负利率债规模%'"
    df_nird_trade_code = pd.read_sql(sql_nird_trade_code,con=db)
    nird_trade_code = np.array(df_nird_trade_code).tolist()[0][0]
    # print(nird_trade_code)

    sql_nird_CLOSE = "select CLOSE from globalindex where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(nird_trade_code)

    sql_nird_DT = "select DT from globalindex where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(nird_trade_code)

    df_CLOSE = pd.read_sql(sql_nird_CLOSE,con=db) # DataFrame数据
    df_DT = pd.read_sql(sql_nird_DT,con=db)

    df_CLOSE_list = np.array(df_CLOSE).tolist()

    df_DT_list = np.array(df_DT).tolist()


    nird_date=[]
    nird_close=[]


    for dt,cl in zip(df_DT_list,df_CLOSE_list):
        # print(dt[0],cl[0])
        nird_date.append(dt[0])
        nird_close.append(cl[0])

    return nird_date,nird_close

if __name__ == '__main__':
    db = pymysql.connect(host="rm-uf6c8yi6zdq6ea7p1qo.mysql.rds.aliyuncs.com", user="temp_intern",
                         password="temp_intern", db="stock", port=3306)
    cur = db.cursor()

    nird_date,nird_close = Nird_data()
    gold_date,gold_close = Glod_data()

    # plt.plot(gold_date,gold_close,color="red")
    # plt.plot(nird_date,nird_close,color="black")
    # plt.show()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(nird_date,nird_close, 'g-')
    ax2.plot(gold_date,gold_close, 'b-')

    ax1.set_xlabel("时间")

    ax1.set_ylabel("负利率债", color='green')
    ax2.set_ylabel("黄金", color='blue')

    plt.show()

    db.close()

"""
由图可知：在2019年4月到2020年4月，黄金和负利率债规模指数的整体趋势和波动大致相同，两者息息相关。
"""