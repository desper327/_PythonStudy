#coding:utf-8
import shutil
import os
import time
#import schedule


if os.path.exists(r'E:\最终交片与工程打包'):
    try:
        os.system('subst P: E:\最终交片与工程打包')
    except:
        pass



txtFile=r'G:\待迁移至P盘文件.txt'
currenttime=time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
mainFolders=[]

def readTxt():
    with open(txtFile, 'r',encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines:
            path=i.strip('\n')
            if os.path.exists(path):
                mainFolders.append(path)
    return mainFolders


def copyFile(path):
    error=''
    source_paths=[]
    Ppaths=[]
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):#root就已经包含了文件的全路径
            for file in files:
                source_path = os.path.join(root, file)
                Ppath='P:'+ source_path.split(':')[1]
                source_paths.append(source_path)
                Ppaths.append(Ppath)
                try:
                    print('ppath文件夹是：',os.path.dirname(Ppath))
                    if not os.path.exists(os.path.dirname(Ppath)):
                        os.makedirs(os.path.dirname(Ppath))
                        print('ppath不存在 ,创建文件夹：',os.path.dirname(Ppath))
                    shutil.copy2(source_path, Ppath)#原来已存在的被覆盖，不存在的添加
                except Exception as e:
                    error+=f'文件{path}复制失败，原因是{e}'+'\n'
    
        with open(txtFile, 'a',encoding='utf-8') as f:
            if error:
                f.write('\n'+'复制完成'+currenttime+'\n'+error)
            else:
                f.write('\n'+'复制完成'+currenttime)
    return source_paths,Ppaths

def deleteFile(source_paths):
    log=''
    DeleteMainFolder=True
    for i,spath in enumerate(source_paths):
        if os.path.exists(spath):
            Ppath='P:'+ spath.split(':')[1]
            if not os.path.exists(Ppath):
                log+=f'文件{spath}删除失败，原因是文件在P盘中不存在'+'\n'
                DeleteMainFolder=False
            else:
                try:
                    os.remove(spath)
                except Exception as e:
                    log+=f'文件{spath}删除失败，原因是{e}'+'\n'
    if DeleteMainFolder:
        for path in source_paths:
            dir=os.path.dirname(path)
            try:
                os.rmdir(dir)
            except:
                pass
    with open(txtFile, 'a+',encoding='utf-8') as f:
        f.write('\n'+'原文件删除完成'+currenttime+'\n'+log)


def remove_empty_folders(path):
    if not os.path.isdir(path):
        return
    is_empty = True
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            if not remove_empty_folders(full_path):
                is_empty = False
        else:
            is_empty = False
    if is_empty:
        os.rmdir(path)
        print(f"Removed empty folder: {path}")
        return True
    return is_empty


'''        
def main():
    schedule.every().day.at("06:00").do(mainFunc)
    while True:
        schedule.run_pending()
        time.sleep(59)
'''

def mainFunc():
    mainFolders=readTxt()
    for p in mainFolders:
        s,d=copyFile(p)
        deleteFile(s)
        remove_empty_folders(p)


if __name__ == '__main__':
    mainFunc()

