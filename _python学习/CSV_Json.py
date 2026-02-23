# -*- coding: utf-8 -*-
import csv
import os
import json
#import configparser as config


data=[['姓名','年龄','性别','班级'],['小明','18','男','1班'],['小红','19','女','2班'],['小亮','20','男','3班']]

with open('config.csv', 'w+',encoding='utf-8-sig') as csv_file:
    csv.writer(csv_file).writerows(data)

list=[]
with open('config.csv', 'r+',encoding='utf-8-sig') as csv_file2:
    csv_reader = csv.DictReader(csv_file2) #使用dictReader读成字典
    csv_reader2=csv.reader(csv_file2)#使用 reader 读成

    for item in csv_reader:
        print('DictReader读出来的是'+str(item))
        list.append(item)
    csv_file2.seek(0)
    for item in csv_reader2:
        print('Reader读出来的是'+str(item))



with open('设备登记.json', 'w+',encoding='utf-8-sig') as json_file:
    json.dump(list, json_file)
    json.load(json_file)

