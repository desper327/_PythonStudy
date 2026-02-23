# coding:utf-8
import os
import sys



for path in sys.path:
    if 'PYTHON' in path:
        print(path)





















'''

import time

getcwd=os.getcwd()
#print(getcwd)  #F:\Study\Python/NORMAL_PY
b=os.path.relpath('F:/Users/89468/Desktop')
print(b*10)
a=os.path.abspath('.')
print(a)
a=os.path.abspath('..')
print(a)
a=os.path.abspath('..\..')
print(a)
os.makedirs('C:/Users/89468/Desktop/haha/kk/ff/ss/myJson')
time.sleep(6)
os.removedirs('C:/Users/89468/Desktop/haha/kk/ff/ss/myJson')


# 打印所有环境变量及其对应的值
for key in os.environ:
    print(f"{key}: {os.getenv(key)}")
'''


'''
a=[1,2,3,4,5,5,5,5,5]
b=list(set(a))
print(b)


curentPath=os.getcwd().replace('\\','/')  
print(curentPath)
'''



""" # -*- coding: utf-8 -*-
import json
dict1={'钢背兽':1,'PA':2}
dict2={'斯文':3,'花仙子':4}
dict2.update(dict1)
dict3={**dict1,**dict2}
#print(dict2)
del dict3['PA']
#print(dict3)

dir='C:/Users/89468/Desktop/myJson.json'

# 打开文件并读取内容
# with open(dir, 'r', encoding='utf-8') as file:
#    data = json.load(file)

# 打印数据
# print(data)
#  bb=data['a']
# print(bb)
# for a in data:
#    print(a,data[a])

with open(dir, 'r', encoding='utf-8') as file:
    #file.write(json.dumps(dict3, ensure_ascii=False))
    a=file.read(6)
    print(type(a))
    print(a)

#格式化字符串
aa='sShot02'
bb='Project'
cc=30
dd=str(cc)+'这是项目名{1}这是镜头号{0}'.format(aa,bb)
print(dd)
#结果  30这是项目名Project这是镜头号shot02
ccc=dd.replace('shot','FFF')
print(ccc)

"""

"""


a=120
b=36

c=a-b*3
print(b)

print(50*10/5)  #这儿一行没用



#hjgfhgfhfhgf
print(int('6')+int('9'))

print(0.5+6)
print(int(True))

print(8>10)
print(30%2)
print(3*'我爱我的祖国')
print("wupeiqi"=="alex")#单引号报错
print(666==666)
print('666'==666)

"""
"""
v1=1 or 2
print(v1)

v2 = 4 and 8
print(v2)

1 > 1 or 3<4 or 4>5 and 2>1 and 9>8 or 7<6
#False or T or F and T and T or F
#False or T or T and T or F
#False or T or T or F
#F or T or F
#F or F
#F
print(1 > 1 or 3 < 4 or 4 > 5 and 2 > 1 and 9 > 8 or 7 < 6)
print(False or True or False and True and True or False)
print(True)
'''
not 2 >1 and 3<4 or 4>5 and 2>1 and 9>8 or 7<6
not T and T or F and T and T or False
F and T or F and T and T or False
f or F and T and T or False
f or F and T or False
f or F or False
F or False
f
'''
print(not 2 >1 and 3<4 or 4>5 and 2>1 and 9>8 or 7<6)
'''
8 or 3 and 4 or 2 and 0 or 9 and 7
8 or 4 or 0 or 7
8 or 0 or 7
8 or 7
8
'''
print(8 or 3 and 4 or 2 and 0 or 9 and 7)

# 0 or 2 and 3 and 4 or 6 and 0 or 3
# 0 or 4 or 0 or 3
# 4 or 0 or 3
# 4 or 3
# 4
# print(0 or 2 and 3 and 4 or 6 and 0 or 3)
# print(2>1 or 6)




from os import name


answer=True
while answer:
    num=1
    while num<4:
        info=input('猜年龄')
        a=3-num
        if info !="22":
            print('还剩'+str(a)+'次')
        else:
            print('猜对了！')
        break
        num=num+1
    print('还玩吗？Y or N？')
print('退出程序')


#带参数的函数
def ppp(x,y):
    x=x+y
    y=y**3
    return x,y

a,b=ppp(5,9)
print(a,b)



#打印3行字
def printline(num):
    for i in range(num):
        print("-"*30)
printline(3)



#求3个数的平均数
def sum3(a,b,c):
    print((a+b+c)/3.0) 

sum3(15,18,1)




f=open("123.txt","w")








a=3#全局变量
def TP():
    #global a 修改了啊为全局变量
    a=20  #局部变量
    print(a)

TP()#打印出来的是局部变量
print(a)#打印出来全局变量

#格式化字符串
b="{0}and{1}".format(a,"快快快")  #占位是0和1
print(b)


# 另一种方式 f'{}'

def sayhi(name):
    print(f'I am {name}')

sayhi("zy")



def tianxie():
    chart={
        name:input("name:"),
        "age":input("age="),
        "phone":input("phonenum=")
    }
    flag=True
    for i in chart.items():
        if len(i)==0:
            flag=False
            print("有空没填")
    return flag,chart

tianxie()












mm=lambda n,k:n+2*k           #lambda函数 匿名函数
f=mm  #变量可以指向函数名,其他函数使用这个变量,高阶函数
def add(o,p):
    return f(o,p)+f(2*o,2*p)
print(add(3,4))


'''

def aloop(s,d):
    for a in range(d):
        if s==1:
            f=cmds.polyCube()
        elif s==2:
            f=cmds.polySphere()
        else:
            f=cmds.polyCone()
        
aloop(2,3)

'''

password = input ("请输入密码：")
print(password)

import maya.mel as aa
from maya import cmds






class human:
    def __init__(self,name):
        self.firstname=name.split()[0]
        self.lastname=name.split()[1]
    def greet(self):
        print('hallo,I am {}'.format(self.lastname))

bob=human('bob ll')
bob.greet()

class chinese(human):
    def __init__(self,name,city):
        super().__init__(name)#chinese,self
        self.city=city
    def greety(self):
        print('nihao,I am from {}'.format(self.city))


zhang=chinese("zhang yang","beijing")
zhang.greet()




#爬虫程序
from bs4 import BeautifulSoup
import re


"""
"""
birth_year=input("birth year?")
age=2023-int(birth_year)
print(age)
"""
'''
from ctypes.wintypes import HHOOK
from re import split


name="asdfd"
name.upper()

number=[1,2,3,4,5,6,7,8,9,10]
number.insert(2,555)

number.append(120)
a=type(number)
print(a,number)


#字典，字典里面包含了不同数据类型
dictA={'a':33,0.99999:55,6:('kkk','III')}
g=dictA.get(6)
print(g)

#字典操作
a = {'数学':95}
print(a)
#添加新键值对
a['语文'] = 89
#再次添加新键值对
a['英语'] = 90
print(a)

#字符串的操作，split分割
stringA='www.cctv.com'
rr=stringA.split('.')
print(rr[0])


str="网站名称：{}   网址：{}"
print(str.format("C语言中文网","c.biancheng.net"))


#两个帮助函数
#print(dir(int))
#help(split)



for gg in stringA:
    print(gg,end='')#这里end=是print函数的一个参数


for i in range(10):
    for p in range(5):
        print('i=',i,'p=',p)

        

cc=reversed(stringA)
print(cc)


#查看所有的path值
import  sys
print(sys.path)




#写一个动物类，写5个实例，实现类的构造函数
class Animal:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def eat(self):
        print('吃')

dog=Animal('dog',1)
cat=Animal('cat',2)

#写一个载具类，实现5个实例，实现类的构造函数
class Car:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def run(self):
        print('跑')

car1=Car('car1',1)
car2=Car('car2',2)



import os
# 定义路径
path='C:\\Users\\89468\\Desktop\\卡牌 翻卡翻牌 抽卡抽牌 道具卡 属性卡 棋牌卡 随机\\yx_pai01\\yxal'
# 获取文件列表
filelist=os.listdir(path)
# 定义第一个文件名
firstname='图片'
# 定义索引变量
i=30
# 遍历文件列表
for file in filelist:
    # 获取文件路径
    
    olddir=os.path.join(path,file)
    # 判断是否是文件夹
    if os.path.isdir(olddir):
        # 如果是文件夹，则跳过
        continue#
    # 判断文件后缀
    if os.path.splitext(file)[1]=='.png':
        # 如果是png文件，则设置新文件名
        newname=firstname+str(i)+'.png'
        # 获取文件后缀
        print(newname)
        # 获取文件后缀
        filetype=os.path.splitext(file)[1]
        # 获取新文件路径
        newdir=os.path.join(path,newname)
        # 执行重命名操作
        os.rename(olddir,newdir)
        # 更新索引变量
        i+=1

'''
