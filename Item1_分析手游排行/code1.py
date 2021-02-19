import requests
from lxml import etree
import csv



class Game_Analyse(object):

    def __init__(self):
        self.url = "https://shouyou.gamersky.com/ku/0-0-0-30_{}.html"
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Cookie':'ASP.NET_SessionId=jo5rn3xgh5ex0rxx1pb5mrez; Hm_lvt_dcb5060fba0123ff56d253331f28db6a=1593747320; __gads=ID=74c361a2a5112a15:T=1593759211:S=ALNI_Mbl5NhpIrYKGcTyyAcfcG9Vsevu7A; Hm_lpvt_dcb5060fba0123ff56d253331f28db6a=1593766526'
        }
    def get_html(self,page_number):
        response = requests.get(self.url.format(page_number),headers=self.headers)
        res = response.content.decode()
        # print(res)
        return res

    def analyse_one_page(self,i_url): # 爬取一个游戏页面里面的数据
        response = requests.get(i_url,headers=self.headers)
        res = response.content.decode()
        html = etree.HTML(res)
        game_name = html.xpath("//div[@class='Mid1']/div[@class='box_game']/div[@class='box_con']/div/span/text()")[0]
        box_txt = html.xpath("//div[@class='Mid1']/div[@class='box_game']/div[3]/text()")[0]
        game_tag = "" if len(html.xpath("//div[@class='Mid1']/div[@class='box_game']/div[4]/a/text()")) == 0 else ",".join(html.xpath("//div[@class='Mid1']/div[@class='box_game']/div[4]/a/text()")[:])
        # game_feve = html.xpath("//div[@class='Mid1']/div[@class='box_game']/div[5]/div/c/text()")
        # game_fever = html.xpath("//div[@class='box_ZS']/div[3]/div/text()") # 网页源码里面没有
        game_intro = html.xpath("//div[@class='Mid2']/div/div[2]/div[@class='Intro']/p/text()")
        game_intro =("".join(game_intro)).replace(u'\u3000',u'') # 去除字典中的\u3000   \u3000是全角的空白符

        # print(game_name)
        # print(box_txt)
        # print(game_tag)
        # print(game_intro)
        game_information = {
            'game_name':game_name,
            'box_txt':box_txt,
            'game_tag':game_tag,
            'game_intro':game_intro
        }
        # print(game_information)
        return game_information




    def get_one_page(self,page_number): # 爬取一个页面里面的24个游戏链接
        html = self.get_html(page_number)
        html_str = etree.HTML(html)
        ul = html_str.xpath("//ul[@class='pictxt']/li")
        dict_url_title = {}
        for li_s in ul:
            one_game_url = li_s.xpath("a/@href")[0]
            one_game_title = li_s.xpath("a/@title")[0]
            # print(one_game_title,one_game_url,sep="----") # 输出游戏名和游戏链接
            dict_url_title[one_game_title]=one_game_url
        game_24_information = []
        for i_url in dict_url_title.values():# 遍历所有24个的游戏链接
            # print(i_url)
            game_single = self.analyse_one_page(i_url)# 返回一个字典，字典里面是一个游戏是数据
            game_24_information.append(game_single)
        # for one_game_of_24 in game_24_information:
        #     print(one_game_of_24)
        return game_24_information

    def load_to_csv(self,list_data):

        header=['game_name','box_txt','game_tag','game_intro']
        with open('game_data.csv','a',newline="",encoding='utf-8') as f:
            writer = csv.DictWriter(f,fieldnames=header)
            writer.writeheader()
            writer.writerows(list_data)


    def run(self):

        all_data = []
        for i_page_number in range(1,11):# 一共有576个页面

            # 1,获取一页的数据
            print("正在爬取第{}页的数据...".format(i_page_number))
            one_page_data = self.get_one_page(i_page_number) # 接收一个列表，列表里面是24个字典数据

            # 汇总数据
            all_data = all_data + one_page_data
        # print(all_data)
        print("共{}条数据".format(len(all_data)))

        # 3，数据导出csv
        self.load_to_csv(all_data)


if __name__ == '__main__':
    Ga = Game_Analyse()
    Ga.run()
