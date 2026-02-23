
#https://pan.baidu.com/s/1wsK-G7aYGhbiS6_cr_vbzA提取码：mzkk

import re
import time
import pymongo
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}


def get_page(url):
    """获取网页源码"""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('Error', e.args)


def get_stock_data(text):
    """获取股票代码、名称、PE"""
    com = re.compile('"f2":(?P<end>.+?),.*?"f6":(?P<volume>.+?),.*?"f12":"(?P<number>.+?)",.*?"f14":"(?P<name>.+?)"'
                    ',.*?"f15":(?P<max>.+?),.*?"f16":(?P<min>.+?),.*?"f17":(?P<start>.+?),', re.S)
    ret = com.finditer(text)
    for i in ret:
        yield {
            'number': i.group('number'),
            'name': i.group('name'),
            'start': i.group('start'),
            'max': i.group('max'),
            'min': i.group('min'),
            'end': i.group('end'),
            'volume': i.group('volume')
        }


def save_data(number=None, name=None, start_price=None, max_price=None, min_price=None, end_price=None, volume=None):
    """存进MongoDB"""
    client = pymongo.MongoClient("localhost", 27017)
    db = client.stock
    collection = db.stock_data7
    shijian = time.strftime('%Y-%m-%d', time.localtime())  # '2020-05-25'
    data = {"time": shijian, "number": number, "name": name, "start_price": start_price, "max_price": max_price,
            "min_price": min_price, "end_price": end_price, "volume": volume}
    collection.insert_one(data)


def main(start=1, end=1):
    for i in range(start, end+1):
        url = 'http://60.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408744624686429123_1578798932591&pn=' \
            '%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:' \
            '0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,' \
            'f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1586266306109' % i
        content = get_page(url=url)
        data = get_stock_data(text=content)
        for j in data:
            number = j.get('number')
            name = j.get('name')
            start = j.get('start')
            max_price = j.get('max')
            min_price = j.get('min')
            end = j.get('end')
            volume = j.get('volume')
            if start == '"-"':
                start, max_price, min_price, end, volume = '0', '0', '0', '0', '0'
            save_data(number=number, name=name, start_price=eval(start), max_price=eval(max_price),
                      min_price=eval(min_price), end_price=eval(end), volume=round(eval(volume) / 10 ** 8, 2))
        time.sleep(2)


if __name__ == '__main__':
    main(start=1, end=2)