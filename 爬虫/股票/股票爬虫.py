'''
import requests
import openpyxl

url = 'http://27.push2.eastmoney.com/api/qt/clist/get'
wb = openpyxl.Workbook()
ws = wb.active

header = ['代码', '名称', '现价', '动态市盈率', '市净率', '总市值(亿)', '流通市值(亿)']
ws.append(header)

for i in range(1, 10):
    data = {
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        'pz': 1000,         # 每页条数
        'pn': i,            # 页码
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048'
    }
    response = requests.get(url, data)
    response_json = response.json()
    print(i, response_json)
    # 返回数据为空时停止循环
    if response_json['data'] is None:
        break
    for j, k in response_json['data']['diff'].items():
        code = k['f12']         # 代码
        name = k['f14']         # 名称
        price = k['f2']         # 股价
        pe = k['f9']            # 动态市盈率
        pb = k['f23']           # 市净率
        total_value = k['f20']          # 总市值
        currency_value = k['f21']       # 流通市值
        price = round(price/100, 2)     # 价格转换为正确值（保留2位小数）
        pe = round(pe/100, 2)           # 市盈率转换为正确值（保留2位小数）
        pb = round(pb/100, 2)           # 市净率转换为正确值（保留2位小数）
        total_value = round(total_value / 100000000, 2)         # 总市值转换为亿元（保留2位小数）
        currency_value = round(currency_value / 100000000, 2)   # 流通市值转换为亿元（保留2位小数）
        print('代码: %s, 名称: %s, 现价: %s, 动态市盈率: %s, 市净率: %s, 总市值: %s亿, 流通市值: %s亿' % (code, name, price, pe, pb, total_value, currency_value))
        row_data = [code, name, price, pe, pb, total_value, currency_value]
        ws.append(row_data)

wb.save("stock_info.xlsx")





import requests
import openpyxl

url = 'http://27.push2.eastmoney.com/api/qt/clist/get'
wb = openpyxl.Workbook()
ws = wb.active

header = ['代码', '名称', '现价', '动态市盈率', '市净率', '总市值(亿)', '流通市值(亿)', '最近6个季度净利润增长率', '净利润率', '毛利率', '净利率', '分红率', '扣非净利润同比增长', '资产负债率', '所处行业', '最新流动比率', '最新速动比率']
ws.append(header)

def get_stock_info(code):
    # 根据股票代码发送请求获取更多信息
    # 这里需要替换为您相应的API请求和数据解析逻辑
    stock_info = {
        '净利润增长率': 10.5,
        '净利润率': 20.1,
        '毛利率': 30.2,
        '净利率': 25.5,
        '分红率': 1.5,
        '扣非净利润同比增长': 8.7,
        '资产负债率': 40.3,
        '所处行业': '科技',
        '流动比率': 1.8,
        '速动比率': 1.2
    }
    return stock_info

for i in range(1, 10):
    data = {
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        'pz': 1000,         # 每页条数
        'pn': i,            # 页码
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048'
    }
    response = requests.get(url, data)
    response_json = response.json()
    print(i, response_json)
    # 返回数据为空时停止循环
    if response_json['data'] is None:
        break
    for j, k in response_json['data']['diff'].items():
        code = k['f12']         # 代码
        name = k['f14']         # 名称
        price = k['f2']         # 股价
        pe = k['f9']            # 动态市盈率
        pb = k['f23']           # 市净率
        total_value = k['f20']          # 总市值
        currency_value = k['f21']       # 流通市值
        price = round(price/100, 2)     # 价格转换为正确值（保留2位小数）
        pe = round(pe/100, 2)           # 市盈率转换为正确值（保留2位小数）
        pb = round(pb/100, 2)           # 市净率转换为正确值（保留2位小数）
        total_value = round(total_value / 100000000, 2)         # 总市值转换为亿元（保留2位小数）
        currency_value = round(currency_value / 100000000, 2)   # 流通市值转换为亿元（保留2位小数）
        print('代码: %s, 名称: %s, 现价: %s, 动态市盈率: %s, 市净率: %s, 总市值: %s亿, 流通市值: %s亿' % (code, name, price, pe, pb, total_value, currency_value))
        stock_info = get_stock_info(code)
        row_data = [code, name, price, pe, pb, total_value, currency_value, stock_info['净利润增长率'], stock_info['净利润率'], stock_info['毛利率'], stock_info['净利率'], stock_info['分红率'], stock_info['扣非净利润同比增长'], stock_info['资产负债率'], stock_info['所处行业'], stock_info['流动比率'], stock_info['速动比率']]
        ws.append(row_data)

wb.save("stock_info.xlsx")

'''


import csv
import json
import requests
from lxml import etree


class DataScraper:
    def __init__(self):
        self.pagename_type = {
            "业绩报表": "RPT_LICO_FN_CPD",
            "业绩快报": "RPT_FCI_PERFORMANCEE",
            "业绩预告": "RPT_PUBLIC_OP_NEWPREDICT",
            "预约披露时间": "RPT_PUBLIC_BS_APPOIN",
            "资产负债表": "RPT_DMSK_FN_BALANCE",
            "利润表": "RPT_DMSK_FN_INCOME",
            "现金流量表": "RPT_DMSK_FN_CASHFLOW"
        }

        self.pagename_en = {
            "业绩报表": "yjbb",
            "业绩快报": "yjkb",
            "业绩预告": "yjyg",
            "预约披露时间": "yysj",
            "资产负债表": "zcfz",
            "利润表": "lrb",
            "现金流量表": "xjll"
        }

        self.en_list = []

        self.url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'closed',
            'Referer': 'https://data.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

    def get_table(self, page):
        params = {
            'sortTypes': '-1,-1',
            'reportName': self.table_type,
            'columns': 'ALL',
            'filter': f'(REPORT_DATE=\'{self.timePoint}\')'
        }

        if self.table_type in ['RPT_LICO_FN_CPD']:
            params['filter'] = f'(REPORTDATE=\'{self.timePoint}\')'
        params['pageNumber'] = str(page)
        response = requests.get(url=self.url, params=params, headers=self.headers)
        data = json.loads(response.text)
        if data['result']:
            return data['result']['data']
        else:
            return

    def get_header(self, all_en_list):
        ch_list = []
        url = f'https://data.eastmoney.com/bbsj/{self.pagename_en[self.pagename]}.html'
        response = requests.get(url)
        res = etree.HTML(response.text)
        for en in all_en_list:
            ch = ''.join(
                [i.strip() for i in res.xpath(f'//div[@class="dataview"]//table[1]//th[@data-field="{en}"]//text()')])
            if ch:
                ch_list.append(ch)
                self.en_list.append(en)
        return ch_list

    def write_header(self, table_data):
        with open(self.filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            headers = self.get_header(list(table_data[0].keys()))
            writer.writerow(headers)

    def write_table(self, table_data):
        with open(self.filename, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item in table_data:
                row = []
                for key in item.keys():
                    if key in self.en_list:
                        row.append(str(item[key]))
                print(row)
                writer.writerow(row)

    def get_timeList(self):
        headers = {
            'Referer': 'https://data.eastmoney.com/bbsj/202206.html',
        }
        response = requests.get('https://data.eastmoney.com/bbsj/202206.html', headers=headers)
        res = etree.HTML(response.text)
        return res.xpath('//*[@id="filter_date"]//option/text()')

    def run(self):
        self.timeList = self.get_timeList()
        for index, value in enumerate(self.timeList):
            if (index + 1) % 5 == 0:
                print(value)
            else:
                print(value, end=' ; ')

        self.timePoint = str(input('\n请选择时间（可选项如上）:'))
        self.pagename = str(
            input('请输入报表类型（业绩报表;业绩快报;业绩预告;预约披露时间;资产负债表;利润表；现金流量表）:'))
        assert self.timePoint in self.timeList, '时间输入错误'
        assert self.pagename in list(self.pagename_type.keys()), '报表类型输入错误'
        self.table_type = self.pagename_type[self.pagename]
        self.filename = f'{self.pagename}_{self.timePoint}.csv'
        self.write_header(self.get_table(1))
        page = 1
        while True:
            table = self.get_table(page)
            if table:
                self.write_table(table)
            else:
                break
            page += 1


if __name__ == '__main__':
    scraper = DataScraper()
    scraper.run()
