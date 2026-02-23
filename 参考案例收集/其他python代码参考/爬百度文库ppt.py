#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Time   :2022/12/6 16:04
@Author :tisugou
@DESC   :
'''


import requests
import os
from lxml import etree


# 创建目录方法
def create_file(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

url = 'https://wenku.baidu.com/view/9231c80c5b8102d276a20029bd64783e09127dc7?aggId=6d791c27a4e9856a561252d380eb6294dd882217&fr=catalogMain_text_ernie_recall_backup_new%3Awk_recommend_main1&_wkts_=1689872856758&wkQuery=python%E6%AD%A3%E5%88%99'

resp = requests.get(url)

# print(resp.text)
text = resp.text

html = etree.HTML(text)

img_list = html.xpath('//div[@class="mod flow-ppt-mod"]/div/div/img')

# 计数
cnt = 1

# 文件保存路径
file_path = './wendang/'
create_file(file_path)

# 获取图片
for i in img_list:
    try:
        img_url = i.xpath('./@src')[0]
    except:
        img_url = i.xpath('./@data-src')[0]

    # 文件名称
    file_name = f'{file_path}page_{cnt}.jpg'
    print(file_name, img_url)
    # 下载保存图片
    resp = requests.get(img_url)
    with open(file_name, 'wb') as f:
        f.write(resp.content)

    cnt += 1