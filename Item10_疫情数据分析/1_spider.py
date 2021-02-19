import requests
from lxml import etree
import re
import json
import ast
import pandas as pd

class Yiqing():
    def __init__(self):
        self.url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
        self.headers = {

        }

    def get_html(self):
        response = requests.get(self.url,headers = self.headers)
        res_html = response.content.decode()
        res = etree.HTML(res_html)
        return res

    def get_content(self,res):
        body = res.xpath("//body/script[1]/text()")
        headd = "try { window.getListByCountryTypeService2true = "
        endd = "}catch(e){}"
        # print(body[0])
        # print(type(body[0]))    # <class 'lxml.etree._ElementUnicodeResult'>
        body = body[0]
        body = body[len(headd):-len(endd)]
        # print(body)
        # print(type(body))   # 是str类型 一个以[开头，以]结束的str型


        json_body = json.loads(body)
        # print(json_body)
        # for i_body in json_body:
        #     print(i_body) # 是一个字典
        # print(len(json_body)) # 215
        # print(type(json_body)) # list
        all_country_list = []
        for i_body in json_body:
            single_dict = {}
            single_dict["国家名称"] = i_body["provinceName"]
            single_dict["现存确诊"] = i_body["currentConfirmedCount"] # 现存确诊
            single_dict["累计确诊"] = i_body["confirmedCount"] # 累计确诊
            single_dict["死亡人数"] = i_body["deadCount"] # 死亡
            single_dict["治愈人数"] = i_body["curedCount"] # 治愈
            all_country_list.append(single_dict)
        # print(all_country_list)
        # for i_country in all_country_list:
        #     print(i_country)
        a = pd.DataFrame(all_country_list)
        print(a)
        a.to_csv("counts_for_country.csv",index=False) # index=False是把第一列多余的索引去掉
    def run(self):
        # 获取源码
        res = self.get_html()

        # 提取数据
        self.get_content(res)

        # 数据入库

        pass
if __name__ == '__main__':
    yq = Yiqing()
    yq.run()