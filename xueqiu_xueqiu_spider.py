

import requests
import pymysql
import scrapy
from scrapy import Field
import time
import logging
from utils import time_cycle

# 新股申购 xingushengou
class Stock1(scrapy.Item):
    Name = scrapy.Field()
    OnlSubcode = scrapy.Field()
    OnlSubbegDate = scrapy.Field()
    PlanIssMaxQTY = scrapy.Field()
    OnlPlanIssMaxQTY = scrapy.Field()
    OnlSubMaxQTY = scrapy.Field()
    IssPrice = scrapy.Field()
    OnlLotwinerStpubDate = scrapy.Field()
    Leaduwer = scrapy.Field()
    OnlDistrDate = scrapy.Field()
    OnlDrawlotsDate = scrapy.Field()
    OnlRdshowbegDate = scrapy.Field()

# 新股行情 xinguhangqing
class Stock2(scrapy.Item):
    Name = scrapy.Field()
    OnlSubbegDate = scrapy.Field()
    ListDate = scrapy.Field()
    ActIssQTY = scrapy.Field()
    IssPrice = scrapy.Field()
    Napsaft = scrapy.Field()
    FirstOpenPrice = scrapy.Field()
    FirstPercent = scrapy.Field()
    FirstTurnrate = scrapy.Field()
    PeTtm = scrapy.Field()
    Pb = scrapy.Field()
    Current = scrapy.Field()
    Percent = scrapy.Field()
    StockIncome = scrapy.Field()
    ListedPercent = scrapy.Field()

# 打新收益 daxinshouyi
class Stock3(scrapy.Item):
    Name = scrapy.Field()
    ListDate = scrapy.Field()
    IssPrice = scrapy.Field()
    FirstPercent = scrapy.Field()
    Current = scrapy.Field()
    ListedPercent = scrapy.Field()
    StockIncome = scrapy.Field()
    PlanIssMaxQTY = scrapy.Field()
    Napsaft = scrapy.Field()
    PeTtm = scrapy.Field()
    Pb = scrapy.Field()
    OnlLotWinRT = scrapy.Field()
    OnlEffSubQTY = scrapy.Field()
    OnlOnversubRT = scrapy.Field()


class Share:
    def __init__(self):
        self.conn = pymysql.Connect(host='x',port=3306,user='x',password='x',db='spider_finance')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

        self.cookies1 = {
            'aliyungf_tc': 'AQAAAKjWEktyzQsAuV7IfJX8q9iFJCZi',
            's': 'cc11kdi8u3',
            'xq_a_token': '8e5aeb2767487283b3c63763bac31b974deff1df',
            'xq_r_token': '722038f2a7439aa4dbdf02fb017d402da34be38c',
            'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1563896561',
            'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1563896561',
            '__utmt': '1',
            '__utma': '1.1504805370.1563896561.1563896561.1563896561.1',
            '__utmb': '1.1.10.1563896561',
            '__utmc': '1',
            '__utmz': '1.1563896561.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'u': '681563896561351',
            'device_id': 'b4a317f4cb4dd32056398ec9d9936106',
        }

        self.headers1 = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://xueqiu.com/hq',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache',
        }
        self.cookies2 = {
            'device_id': 'f660ce0e000b7c85bfe6a35f5dae2a1e',
            's': 'de11ozc4rv',
            'u': '351563863577456',
            '__utmz': '1.1563863577.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'aliyungf_tc': 'AQAAAEUOv2BY6wQAI5rd3ZgrmhYiTgaF',
            'xq_a_token': '8e5aeb2767487283b3c63763bac31b974deff1df',
            'xq_r_token': '722038f2a7439aa4dbdf02fb017d402da34be38c',
            '__utmc': '1',
            'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1563863577,1563934111',
            'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1563938210',
            '__utma': '1.554930563.1563863577.1563934111.1563938210.4',
            '__utmt': '1',
            '__utmb': '1.1.10.1563938210',
        }

        self.headers2 = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://xueqiu.com/hq',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }
        self.params1 = (
            ('page', '1'),
            ('size', '30'),
            ('order', 'asc'),
            ('order_by', 'onl_subbeg_date'),
            ('type', 'subscribe'),
            ('_', '1563896839656'),
        )


    def xingushengou(self):
        response = requests.get('https://xueqiu.com/service/v5/stock/preipo/cn/query', headers=self.headers1, params=self.params1,
                                cookies=self.cookies1)
        results_li = response.json()['data']['items']
        for results in results_li:
            Name = results['name']  # 股票简称
            OnlSubcode = results['onl_subcode']  # 申购代码

            OnlSubbegDate = time_cycle(results['onl_subbeg_date'] / 1000)  # 申购日期

            PlanIssMaxQTY = results['planissmaxqty']  # 预计发行量(万)
            OnlPlanIssMaxQTY = results['onl_planissmaxqty']  # 网上发行量
            OnlSubMaxQTY = results['onl_sub_maxqty']  # 申购上限
            IssPrice = results['iss_price']  # 发行价

            OnlLotwinerStpubDate = time_cycle(results['onl_lotwiner_stpub_date'] / 1000)  # 中签号公布日

            # zhongqianlv = results['']   #中签率
            # zhongqianhao = results['onl_lorwin_code']    #中签号
            # shijimuzizonge = results[]     #实际募资总额
            # dangqianjia = results[]    #当前价
            Leaduwer = results['leaduwer']  # 主承销商
            OnlDistrDate = time_cycle(results['onl_distr_date'] / 1000)  # 网上配号日
            OnlDrawlotsDate = time_cycle(results['onl_drawlots_date'] / 1000)  # 网上摇号抽签日
            OnlRdshowbegDate = time_cycle(results['onl_rdshowbeg_date'] / 1000)  # 网上路演日期
            print(Name)

            sql = 'insert into xingushengou values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                Name, OnlSubcode, OnlSubbegDate, PlanIssMaxQTY, OnlPlanIssMaxQTY, OnlSubMaxQTY, IssPrice,
                OnlLotwinerStpubDate, Leaduwer, OnlDistrDate, OnlDrawlotsDate, OnlRdshowbegDate)

            print(sql)
            # 执行SQL语句
            xx = self.cursor.execute(sql)
            print(111, xx)
            self.conn.commit()
    def xinguhangqing(self):
        for page in range(1, 11):
            params = (
                ('page', page),
                ('size', '30'),
                ('order', 'desc'),
                ('order_by', 'list_date'),
                ('type', 'quote'),
                ('_', '1563938638327'),
            )

            response = requests.get('https://xueqiu.com/service/v5/stock/preipo/cn/query', headers=self.headers2,
                                    params=params, cookies=self.cookies2)

            results_li = response.json()['data']['items']
            print(results_li)
            for results in results_li:
                Name = results['name']  # 股票名称
                OnlSubbegDate = results['onl_subbeg_date']  # 申购日期
                ListDate = results['list_date']  # 上市日期
                ActIssQTY = results['actissqty']  # 发行量
                IssPrice = results['iss_price']  # 发行价
                Napsaft = results['napsaft']  # 发行后每股净资产
                FirstOpenPrice = results['first_open_price']  # 首日开盘价
                FirstPercent = results['first_percent']  # 首日涨跌幅
                FirstTurnrate = results['first_turnrate']  # 换手率

                PeTtm = results['pe_ttm']  # 市盈率
                Pb = results['pb']  # 市净率
                Current = results['current']  # 当前价
                Percent = results['percent']  # 今日涨跌幅
                StockIncome = results['stock_income']  # 每签获利

                ListedPercent = (Current-IssPrice)/IssPrice  # 上市后涨跌幅  (当前价-发行价)/发行价
                print(Name)

                sql = 'insert into xinguhangqing values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    Name, OnlSubbegDate, ListDate, ActIssQTY, IssPrice, Napsaft, FirstOpenPrice,
                    FirstPercent, FirstTurnrate, PeTtm, Pb, Current, Percent, StockIncome, ListedPercent
                )
                # 执行SQL语句
                self.cursor.execute(sql)
                self.conn.commit()
            time.sleep(0.5)

    def daxinshouyi(self):
        for page in range(1, 11):
            params = (
                ('page', page),
                ('size', '30'),
                ('order', 'desc'),
                ('order_by', 'list_date'),
                ('type', 'income'),
                ('_', '1563938851950'),
            )

            response = requests.get('https://xueqiu.com/service/v5/stock/preipo/cn/query', headers=self.headers2,
                                    params=params, cookies=self.cookies2)

            results_li = response.json()['data']['items']
            print(results_li)
            for results in results_li:
                Name = results['name']  # 股票名称
                ListDate = time_cycle(results['list_date'] / 1000)  # 上市日期
                IssPrice = results['iss_price']  # 发行价
                FirstPercent = results['first_percent']  # 首日涨跌幅
                Current = results['current']  # 当前价
                ListedPercent = format(results['listed_percent'], '.2f')  # 上市后涨跌幅

                try:
                    StockIncome = format(results['stock_income'], '.0f')  # 每签获利
                except Exception as e:
                    logging.error("Get Stock Income Failed" )
                    StockIncome = ""

                PlanIssMaxQTY = results['planissmaxqty']  # 发行量
                Napsaft = results['napsaft']  # 发行后每股净资产
                PeTtm = format(results['pe_ttm'], '.2f')  # 市盈率
                Pb = results['pb']  # 市净率

                try:
                    OnlLotWinRT = format((results['onl_lotwinrt']) * 1000, '.2f')  # 中签率
                except Exception as e:
                    logging.error("Get OnlLotWinRT Failed")
                    OnlLotWinRT = ""

                try:
                    OnlEffSubQTY = results['onl_effsubqty']  # 网上有效申购股数
                except Exception as e:
                    logging.error("Get OnlEffSubQTY Failed")
                    OnlEffSubQTY = ""

                try:
                    OnlOnversubRT = format(results['onl_onversubrt'], '.2f')  # 网上超额认购倍数
                except Exception as e:
                    logging.error("Get OnlOnversubRT Failed")
                    OnlOnversubRT = ""

                print(Name,StockIncome)
                sql = 'insert into daxinshouyi values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    Name, ListDate, IssPrice, FirstPercent, Current, ListedPercent, StockIncome,
                    PlanIssMaxQTY, Napsaft, PeTtm, Pb, OnlLotWinRT, OnlEffSubQTY, OnlOnversubRT)

                # 执行SQL语句
                self.cursor.execute(sql)
                self.conn.commit()
            time.sleep(0.5)

    def close_mysql(self):
        self.cursor.close()
        self.conn.close()


def main():
    xueqiu_spider = Share()
    xueqiu_spider.xingushengou()
    xueqiu_spider.xinguhangqing()
    xueqiu_spider.daxinshouyi()

if __name__ == '__main__':
    main()
