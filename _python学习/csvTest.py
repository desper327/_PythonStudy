import csv
import json
import sys
import os
#reload(sys)
#sys.setdefaultencoding('utf8') 

# with open("F:\Study\BaiduSyncdisk\MyStudy\mayaToUE.csv", 'r') as f:
#     # for read in csv.DictReader(f):
#     #     print(read)
#     reader = csv.DictReader(f)
#     for row in reader:
#         print(row)


'''
path1=r"F:\Study\BaiduSyncdisk\MyStudy\mayaToUE.csv"
path2=r"F:\Study\BaiduSyncdisk\MyStudy\mayaToUE2.csv"

path3=r"F:\Study\BaiduSyncdisk\MyStudy\MMT2.json"
with open(path1, "r") as read,open(path2, 'w') as csvfile,open(path3, 'w') as f:
    fieldnames = ['id','model', 'material', 'plug','texture', 'path']
    writer=csv.writer(csvfile)
    #writer.writerow(fieldnames)    
    for read in csv.reader(read):
        print(read)
        pass
        writer.writerow(read)
        json.dump(read, f, indent=4, ensure_ascii=False)
    
'''

shareInfoFile=r'G:\chajian\OtherTools\shareInfo\shareInfo'
if os.path.exists(shareInfoFile):
    with open(shareInfoFile, 'r', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        reader2=reader
        print(len(list(reader2)))
        f.seek(0)
        for line in reader:
            print(line)
            if 'zhangyang' in line['群晖用户名']:
                print('2')

