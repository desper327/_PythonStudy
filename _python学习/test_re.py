import re
import sys,os

#sys.path.append(os.getenv("USERPROFILE","") + r"\.forza")
sys.path.append(r"F:\BaiduSyncSpace\BaiduSyncdisk\ForzaPipeline\Forza_Lib\utils")
from forza_utils import Yprint




text = "123aaer*%&^%$#@qq.com!tgbaaaBBBb_+****@@\nsdf886ppqq1\r2=!@#$"


"""
a=re.findall(r"\d+", text)  #查找所有数字
Yprint(a)

b=re.findall(r"129",text)  #查找所有包含12的字符串
Yprint(b)

b2=re.findall("[p-z]+",text)  #查找所有包含p-z的字符串
Yprint(b2)

c=re.search(r"12",text).group()  #查找第一个包含129的字符串
Yprint(c)  


d=re.sub(r"12","RR",text)  #替换所有包含12的字符串为RR
Yprint(d)


e=re.match(r"2",text).group()  #查找第一个以12开头的字符串
Yprint(e)


"""

p=r"[a-b]+"
a=re.sub(p,"YYYYY",text,flags=re.IGNORECASE)  #查找所有小写字母
Yprint(a)