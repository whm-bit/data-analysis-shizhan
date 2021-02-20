import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False


def CL1_data():
    """
    获取CL1的指定日期和close数据
    :return:
    """
    sql_cl1_trade_code ="select TRADE_CODE from globalcommodityinfo where SEC_NAME like '%纽交所轻质低硫原油期货%'"
    df_cl1_trade_code = pd.read_sql(sql_cl1_trade_code,con=db)
    cl1_trade_code = np.array(df_cl1_trade_code).tolist()[0][0]


    cl1_global_CLOSE = "select CLOSE from globalcommodity where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(cl1_trade_code)

    cl1_global_DT = "select DT from globalcommodity where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(cl1_trade_code)


    df_CLOSE = pd.read_sql(cl1_global_CLOSE,con=db)
    df_DT = pd.read_sql(cl1_global_DT,con=db)

    df_CLOSE_list = np.array(df_CLOSE).tolist()
    df_DT_list = np.array(df_DT).tolist()


    cl1_date=[]
    cl1_close=[]


    for dt,cl in zip(df_DT_list,df_CLOSE_list):
        # print(dt[0],cl[0])
        cl1_date.append(dt[0])
        cl1_close.append(cl[0])

    return cl1_date,cl1_close


def CL60_data():
    """
    获取CL60的指定日期和close数据
    :return:
    """
    sql_cl60_trade_code ="select TRADE_CODE from globalcommodityinfo where SEC_NAME like '%WTI:连六十%'"
    df_cl60_trade_code = pd.read_sql(sql_cl60_trade_code,con=db)
    cl60_trade_code = np.array(df_cl60_trade_code).tolist()[0][0]
    # print(cl60_trade_code)


    cl60_global_CLOSE = "select CLOSE from globalcommodity where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(cl60_trade_code)

    cl60_global_DT = "select DT from globalcommodity where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(cl60_trade_code)


    df_CLOSE = pd.read_sql(cl60_global_CLOSE,con=db)
    df_DT = pd.read_sql(cl60_global_DT,con=db)

    df_CLOSE_list = np.array(df_CLOSE).tolist()
    df_DT_list = np.array(df_DT).tolist()


    cl60_date=[]
    cl60_close=[]


    for dt,cl in zip(df_DT_list,df_CLOSE_list):
        # print(dt[0],cl[0])
        cl60_date.append(dt[0])
        cl60_close.append(cl[0])

    return cl60_date,cl60_close


def USGG10YR_data():
    """
    获取美国10年国债收益率指数数据和指定日期
    :return:
    """
    sql_usgg10_trade_code ="select TRADE_CODE from globalrateinfo where SEC_NAME like '%美国国债收益率:10%'"
    df_usgg10_trade_code = pd.read_sql(sql_usgg10_trade_code,con=db)
    usgg10_trade_code = np.array(df_usgg10_trade_code).tolist()[0][0]
    # print(usgg10_trade_code)


    usgg10_global_CLOSE = "select CLOSE from globalrate where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(usgg10_trade_code)

    usgg10_global_DT = "select DT from globalrate where TRADE_CODE = '{}' and DT between '2019-04-01' and '2020-04-01'".format(usgg10_trade_code)


    df_CLOSE = pd.read_sql(usgg10_global_CLOSE,con=db)
    df_DT = pd.read_sql(usgg10_global_DT,con=db)

    df_CLOSE_list = np.array(df_CLOSE).tolist()

    df_DT_list = np.array(df_DT).tolist()


    usgg10_date=[]
    usgg10_close=[]


    for dt,cl in zip(df_DT_list,df_CLOSE_list):
        # print(dt[0],cl[0])
        usgg10_date.append(dt[0])
        usgg10_close.append(cl[0])

    return usgg10_date,usgg10_close

def Remove_redundant_data(cl1_date,cl1_close,cl60_date,cl60_close):

    """
    去除CL1和CL60中多余的数据
    :param cl1_date:
    :param cl1_close:
    :param cl60_date:
    :param cl60_close:
    :return:
    """
    cl1_date_df = dict(zip(cl1_date,cl1_close))
    cl60_date_df = dict(zip(cl60_date,cl60_close))

    # print(cl1_date_df)
    var_index=0
    var_index2=0
    for date_cl1,close_cl1 in cl1_date_df.items():
        # print(date_cl1,close_cl1)
        if date_cl1 in cl60_date_df:
            var_index = var_index + 1
        else:
            # print(date_cl1)
            del cl1_date[var_index]
            del cl1_close[var_index]
            var_index = var_index + 1
    # print(len(cl1_date),len(cl1_close))

    for date_cl60,close_cl60 in cl60_date_df.items():
        # print(date_cl60,close_cl60)
        if date_cl60 in cl1_date_df:
            var_index2 = var_index2 + 1
        else:
            # print(date_cl60)
            del cl60_date[var_index]
            del cl60_close[var_index]
            var_index2 = var_index2 + 1
    # print(len(cl60_date),len(cl60_close))
    return cl1_date,cl1_close,cl60_date,cl60_close


if __name__ == '__main__':
    db = pymysql.connect(host="rm-uf6c8yi6zdq6ea7p1qo.mysql.rds.aliyuncs.com", user="temp_intern",
                         password="temp_intern", db="stock", port=3306)
    cur = db.cursor()

    cl1_date,cl1_close = CL1_data()
    cl60_date,cl60_close = CL60_data()

    cl1_date_new,cl1_close_new,cl60_date_new,cl60_close_new = Remove_redundant_data(cl1_date,cl1_close,cl60_date,cl60_close)

    # print("*"*30)
    cl1_sub_cl60_close = []

    # CL1 - CL60
    for cl1,cl60 in zip(cl1_close_new,cl60_close_new):
        cl1_sub_cl60_close.append(cl1-cl60)
    # print(cl1_sub_cl60_close)

    usgg10_date, usgg10_close = USGG10YR_data()
    # print(len(usgg10_date))

    # 画图
    fig, ax1 = plt.subplots(1,1,figsize=(10,7))
    ax2 = ax1.twinx()
    ax1.plot(cl1_date_new, cl1_sub_cl60_close,'g-')
    ax2.plot(usgg10_date, usgg10_close,'b-')

    ax1.set_xlabel("时间")

    ax1.set_ylabel("WTI升贴水", color='green')
    ax2.set_ylabel("美国10y国债收益率", color='blue')

    plt.title("CL1/CL60价差与美国国债收益率")

    plt.show()

    db.close()


"""
由图可得以下信息：
1，CL1/CL60价差与美国国债收益率的整体走势和波动相似度很高
2，从2019年8月到2019年9月下旬，CL1/CL60价差呈上升趋势，美国国债收益率呈下降趋势
3，从2020年1月份开始，CL1/CL60价差与美国国债收益率均开始大幅下降，说明美国流感和疫情造成的严峻局势对此影响很大
4，在2019年6月到7月中旬的时间里，美国国债收益率大致呈先上升后下降的趋势，而CL1/CL60价差呈先下降后上升的趋势，两者趋势截然相反
"""