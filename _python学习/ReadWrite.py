# -*- coding: utf-8 -*-

import json
import sys

#从命令行获取参数
# 检查命令行参数的数量
if len(sys.argv) < 2:
    print("请提供参数")
    sys.exit(1)

# 获取命令行参数
arg1 = sys.argv[1]
arg2 = sys.argv[2] if len(sys.argv) >= 3 else None

# 打印命令行参数
print("first arg    "+ arg1)
print("second arg    "+ arg2)



string1='''三、写json文件
1.导入json模块

import json

2.用只写方式打开文件

open(json文件,'w',encoding='utf8')

3.用dump方法把字典内容写入到json文件中

ensure_ascii = False 代表中文不转义

4.关闭文件

file.close()'''

file=open('myJson.json', 'w')
file.write(string1)
file.close()

dic1={'a':'李白','b':'杜甫','c':'陆游'}
file=open('myJson.json', 'w')
json.dump(dic1,file,ensure_ascii=False)
file.close()


FileRead=open('myJson.json', 'r',encoding='utf8')
File2data=json.load(FileRead)
FileRead.close()


FileWrite=open('myJson.json', 'w',encoding='utf8')
File2data['a']='王昌龄'
json.dump(File2data,FileWrite,ensure_ascii=False)
FileWrite.close()
