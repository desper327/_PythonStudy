

import subprocess,os,csv

# PYTHON_PATH = r'C:\ProgramData\python310\python'
# SCRIPT_PATH = r'D:\ZYfiles\BaiduSyncdisk\MyStudy\FreeTest.py'
# change_numbers=['4', '5', '6', '7', '8', '9', '10']

# for change_number in change_numbers:
#     change_number = change_number.strip()
#     if change_number == '':
#         continue
#     print(f'change_number{change_number}')
#     try:
#         #subprocess.Popen([PYTHON_PATH, SCRIPT_PATH, change_number])
#         result = subprocess.run([PYTHON_PATH, SCRIPT_PATH, change_number], check=True)
#         print(f'子进程输出: {result.stdout}')
#     except Exception as e:
#         print(f'执行脚本时出错: {e}')



def shareInfo():
    if os.path.exists(r'C:\ProgramData\Python310'):
        pyInfo=r'本地python310已存在'
    else:
        pyInfo=r'本地python310不存在'

    mayaMod=os.getenv("USERPROFILE")+"\\Documents\\maya\\modules\\MT_plugin.mod"
    if os.path.exists(mayaMod):
        mayaPluginInfo=r'mayaModule正常安装在用户文档路径下'
    else:
        mayaPluginInfo=r'mayaModule非正常安装，用户文档路径下不存在'

    otherAppPath='C:\\ProgramData\\MT_tray\\OtherApps'
    otherAppInfo=[]
    if os.path.exists(otherAppPath):
        for root, dirs, files in os.walk(otherAppPath):
            for file in files:
                otherAppInfo.append(file)
    

    def writeFirstRow():
        try:
            with open(shareInfoFile, 'w', encoding='utf-8') as f:
                writer=csv.writer(f)
                writer.writerow(['群晖用户名', 'IP地址', 'python310信息', 'p4用户名','maya插件信息','其他app信息'])            
        except Exception as e:
            print(f"写入第一行失败: {str(e)}")
        
    shareInfoFile=r'G:\chajian\OtherTools\shareInfo\shareInfo'
    if os.path.exists(shareInfoFile):
        UserInfoExists=False
        with open(shareInfoFile, 'r', encoding='utf-8') as f:
            reader=csv.DictReader(f)
            for line in reader:
                print(line)
                print('line群晖用户名',line['群晖用户名'])
                if 'zhangyang' in line['群晖用户名']:
                    UserInfoExists=True
                    return
        if not UserInfoExists:
            with open(shareInfoFile, 'a+', encoding='utf-8') as f:
                writer=csv.writer(f)
                writer.writerow(['username', 'ip_address', pyInfo, 'P4username', mayaPluginInfo,otherAppInfo])
    else:
        writeFirstRow()

shareInfo()