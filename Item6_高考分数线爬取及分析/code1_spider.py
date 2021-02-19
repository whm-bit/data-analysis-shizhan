import requests
from lxml import etree
import json
import numpy as np
import pandas as pd

class gaokao():

    def __init__(self):
        self.url = ""
        self.headers = ""

    def get_province(self):
        url = "http://www.gaokao.com/jiangsu/fsx/"
        response = requests.get(url)
        res = response.content.decode('gbk')
        # print(res)
        html_str = etree.HTML(res)
        provinces = html_str.xpath("//div[@class='area_box']/a")
        dict_province = {}
        for province_one in provinces:
            # print(province_one.xpath("@href")[0],province_one.xpath("span/text()")[0])
            dict_province[province_one.xpath("span/text()")[0]] = province_one.xpath("@href")[0]
        # print(dict_province)
        return dict_province

    def province_data(self,url,province_name): # 爬取一个省份的高考数据
        response = requests.get(url)
        res = response.content.decode('gbk')
        html_str = etree.HTML(res)

        table_numbers = html_str.xpath("//div[@class='cjArea tm15']/table")
        wenke=0 # 初始化
        print(len(table_numbers))

        # 文科
        if province_name == '广西':
            wenke = html_str.xpath("//div[@class='cjArea tm15']/table[last()-1]/tbody")[0]  # 选取倒数第二个table 文科
        else:
            wenke = html_str.xpath("//div[@class='cjArea tm15']/table[last()-1]")[0]  # 选取倒数第二个table 文科
        W_years = wenke.xpath('tr[1]/th/text()') # 年份 （列名
        W_one_grade = wenke.xpath('tr[2]/td/text()') # 文科一本 (第一行名)
        W_one_grade = [w_one.strip() for w_one in W_one_grade] # 去掉列表元素中的空格
        W_one_grade = W_one_grade[1:] # 去掉列表第一个元素“一本”
        for wog_index,wog_item in enumerate(W_one_grade):
            if wog_item.isdigit() is False:
                W_one_grade[wog_index]=None
        # print(W_one_grade)
        W_two_grade = wenke.xpath('tr[3]/td/text()')# 文科二本 (第二行名)
        W_two_grade = [w_two.strip() for w_two in W_two_grade]  # 去掉列表元素中的空格
        W_two_grade = W_two_grade[1:]  # 去掉列表第一个元素“二本”
        for wtg_index,wtg_item in enumerate(W_two_grade):
            if wtg_item.isdigit() is False:
                W_two_grade[wtg_index]=None
        # print(W_two_grade)

        # 理科
        if province_name == '广西':
            like = html_str.xpath("//div[@class='cjArea tm15']/table[last()]/tbody")[0]  # 选取倒数第一个table 理科
        else:
            like = html_str.xpath("//div[@class='cjArea tm15']/table[last()]")[0]  # 选取倒数第一个table 理科
        L_years = like.xpath('tr[1]/th/text()')  # 年份 （列名）
        # print(L_years)
        L_one_grade = like.xpath('tr[2]/td/text()') # 理科一本 (第一行名)
        L_one_grade = [l_one.strip() for l_one in L_one_grade]
        L_one_grade = L_one_grade[1:]
        for log_index,log_item in enumerate(L_one_grade):
            if log_item.isdigit() is False:
                L_one_grade[log_index]=None
        # print(L_one_grade)
        L_two_grade = like.xpath('tr[3]/td/text()')# 理科二本 (第二行名)
        L_two_grade = [l_two.strip() for l_two in L_two_grade]
        L_two_grade = L_two_grade[1:]
        for ltg_index,ltg_item in enumerate(L_two_grade):
            if ltg_item.isdigit() is False:
                L_two_grade[ltg_index]=None
        # print(L_two_grade)

        list_data = [W_one_grade,W_two_grade,L_one_grade,L_two_grade]
        list_columns = W_years
        list_columns = list_columns[:len(list_columns)-(len(list_columns)-len(W_one_grade))]
        # list_columns.insert[0]="年份"
        print("W_one_grade={},list_columns={}".format(len(W_one_grade),len(list_columns)))
        print("**********************{}".format("\n"))
        list_index = ['文科一本','文科二本','理科一本','理科二本']
        df_data = pd.DataFrame(list_data,index=list_index,columns=list_columns)
        # print(df_data)
        return df_data

    def run(self):
        # 爬取各个省份的链接
        dict_province = self.get_province() # 字典的键是各个省份的名字，值是各个省份的链接

        # 爬取每个省份里面的高考数据
        for province_name,province_url in dict_province.items():
            print(province_name,province_url,sep=",")
            if province_name == "广东": # 因为广东省的数据不干净
                continue

            df_data = self.province_data(province_url,province_name)
            df_data.to_csv("{}.csv".format(province_name))


        # 数据入库
        return None
if __name__ == '__main__':
    gaok = gaokao()
    gaok.run()