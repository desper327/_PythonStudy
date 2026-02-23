import requests
import pandas as pd
import time

def fetch_all_stocks():
    """获取全市场股票列表（排除科创板）"""
    url = "http://80.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "10000",  # 获取足够大的数量
        "po": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23",  # 沪深A股
        "fields": "f12,f14",
        "_": int(time.time() * 1000)
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    all_stocks = []
    for item in data['data']['diff']:
        code = item['f12']
        # 排除科创板（688开头）
        if code.startswith('688'):
            continue
        # 生成secid（沪市1.代码，深市0.代码）
        exchange = '1' if code.startswith('6') else '0'
        secid = f"{exchange}.{code}"
        all_stocks.append({
            '股票代码': code,
            'secid': secid,
            '股票名称': item['f14']
        })
    return all_stocks

def fetch_finance_data(secid):
    """获取个股财务数据（同原函数）"""
    url = "http://push2.eastmoney.com/api/qt/stock/get"
    fields = "f58,f162,f167,f100,f169,f170,f171,f113,f86,f84,f85"
    params = {
        'secid': secid,
        'fields': fields,
        'invt': 2,
        '_': int(time.time() * 1000)
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'http://quote.eastmoney.com/'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json().get('data', {})
        
        return {
            '市盈率(PE)': data.get('f162', 'N/A'),
            '市净率(PB)': data.get('f167', 'N/A'),
            '所属行业': data.get('f100', 'N/A'),
            '股息率': data.get('f169', 'N/A'),
            'ROE': data.get('f170', 'N/A'),
            '每股收益': data.get('f171', 'N/A'),
            '总市值(亿)': round(data.get('f113', 0)/1e8, 2),
            '流通市值(亿)': round(data.get('f86', 0)/1e8, 2),
            '52周最高': data.get('f84', 'N/A'),
            '52周最低': data.get('f85', 'N/A')
        }
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def main(max_stocks=100):
    # 获取全市场股票列表
    print("正在获取股票列表（排除科创板）...")
    all_stocks = fetch_all_stocks()
    
    # 截取前N只股票
    selected_stocks = all_stocks[:max_stocks]
    print(f"准备获取前{max_stocks}只股票数据...")
    
    # 获取财务数据
    financial_data = []
    
    for idx, stock in enumerate(selected_stocks, 1):
        time.sleep(0.5)  # 增加延时防止封IP
        data = fetch_finance_data(stock['secid'])
        
        if data:
            merged_data = {
                '股票代码': stock['股票代码'],
                '股票名称': stock['股票名称'],
                **data
            }
            financial_data.append(merged_data)
            print(f"进度：{idx}/{max_stocks} | 已获取 {stock['股票名称']} 数据")
    
    # 创建DataFrame并保存
    df = pd.DataFrame(financial_data)
    print(df.columns)
    columns_order = [
        '股票代码', '股票名称', '所属行业', '市盈率(PE)', '市净率(PB)', 
        '股息率', 'ROE', '每股收益', '总市值(亿)', '流通市值(亿)',
        '52周最高', '52周最低'
    ]
    df = df[columns_order]
    filename = f'A股财务数据_前{max_stocks}只.csv'
    df.to_csv(filename, index=False, encoding='utf_8_sig')
    print(f"数据已保存到 {filename}")

if __name__ == '__main__':
    # 在此处修改需要爬取的股票数量
    main(max_stocks=10)