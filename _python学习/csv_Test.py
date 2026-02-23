# coding:utf-8
import csv

# path=r"F:\Study\BaiduSyncdisk\MyStudy\mayaToUE.csv"



# def read():
#     with open(path, "r") as read:
#         for dictData in csv.DictReader(read):#得到的是一行一个字典的数组，不包括首行
#             if dictData["group"]=='rig':
#                 if dictData['name']=='rivet':
#                     print(dictData['label'])
#                 yield dictData
        


# # for d in read:
# #     print(d['icon'])
#         #dictData["functions"] = [fun for fun in dictData["functions"].split("\n") if fun]

#         # if not dictData["icon"]:
#         #     dictData["icon"] = "lush.jpg"
#         #yield cls(dictData)

# path2=r'F:\Study\Python\NORMAL_PY\test.csv'
# rows = [
#     ['Name', 'Age', 'City'],
#     ['Alice', 30, 'New York'],
#     ['鲍勃', 25, 'Los Angeles'],
#     ['查理', 35, 'Chicago']
# ]
# def write():
#     with open(path2, "w",newline='') as write:
#         writer = csv.writer(write)
#         for i in rows:
#             writer.writerow(i)
# write()

path=r"F:\Study\BaiduSyncdisk\MyStudy\mayaToUE.csv"
with open(path, "r",newline='',encoding='utf-8') as read:
    for read in csv.DictReader(read):
        print(read)