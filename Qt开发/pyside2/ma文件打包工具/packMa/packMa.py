# coding:utf-8
#import pymel.core as pm
#import maya.cmds as cmds
#import maya.standalone
#import re
#import zipfile
import sys,os,shutil,time,re
import threading

def getmafiles(file=''):
    mafiles=[]
    otherfiles=[]
    if os.path.isfile(file):
        if file.endswith('.ma'):
            mafiles.append(file)
        else:
            otherfiles.append(file)
    elif os.path.isdir(file):
        for root, dirs, files in os.walk(file):
            for f in files:
                if f.endswith('.ma'):
                    mafiles.append(os.path.join(root, f))
                else:
                    otherfiles.append(os.path.join(root, f))
    mafiles=list(set(mafiles))
    otherfiles=list(set(otherfiles))
    return mafiles,otherfiles


def dictByDisk(pathlist=[]):
    # 创建一个字典，用于存储按盘符拆分后的列表
    path_dict = {}
    for path in pathlist:
        # 获取盘符
        drive = os.path.splitdrive(path)[0]
        #print('drive----------------------:',drive)
        # 检查字典中是否已存在该盘符的键
        if drive not in path_dict:
            # 如果不存在，则创建该键，并将路径添加到对应的列表中
            path_dict[drive] = [path]
        else:
            # 如果存在，则直接将路径添加到对应的列表中
            path_dict[drive].append(path)
    return path_dict



def getMayaFileRefPaths(mayaFile=''):
    print('-----当前在这个maya文件里找引用文件mayaFileeeeeee:',mayaFile)
    with open(mayaFile, 'r') as f:
        try:
            lines=f.readlines()
            #lines=f.read().splitlines()
            refpath=[]
            for i,line in enumerate(lines):
                if line.startswith('file -r') and line.endswith(';\n'):
                    refpath.append(line.split('"')[-2])
                    #print('refpath-----'+ refpath1)
                if line.startswith('file -r') and line.endswith('"\n') and lines[i+1].endswith(';\n'):
                    refpath.append(lines[i+1].split('"')[-2])
                    #print('refpath======'+ refpath2)
                if 'setAttr ".ftn"' in line:
                    texpath=line.split('"')[-2]
                    refpath.append(texpath)
                    #print('texpath>>>>>>>>'+ texpath)
            files=list(set(refpath))
            for f in files:
                print('####找到的引用文件>>>>>>>>'+ f)
            return files
        except Exception as e:
            print(f'读取{mayaFile}文件失败，原因是：'+str(e))
            return []
        



unknownFiles=[]
allmafiles=[]
allothers=[]
def classifyMa(mas=None,targetDir='',dictFileInDisk=None):#这里改成字典，后面的去解析字典的信息即可
    global unknownFiles,allmafiles,allothers
    print('调用一次classifyMa，传入的字典是>>>>>',str(dictFileInDisk))
    if mas==None:
        mas=[]
    if dictFileInDisk==None:
        dictFileInDisk={}

    for disk in dictFileInDisk:
        filePaths=dictFileInDisk[disk]
        #print('disk>>>>>'+ str(disk))
        #print('filePaths>>>>>'+ str(filePaths))
        for f in filePaths:
            #print('&&&&&&&&&&&&&&&&&&&&&'+f)
            if os.path.isfile(f):
                if f.endswith('.ma'):
                    if f not in allmafiles:
                        allmafiles.append(f)
                        mas.append(f)
                else:
                    if f not in allothers:
                        allothers.append(f)
            else:
                if f not in unknownFiles:
                    unknownFiles.append(f)
        if mas:
            for ma in mas:
                refFilePaths=getMayaFileRefPaths(ma)
                dictFileInDisk1=dictByDisk(refFilePaths)
                classifyMa(None,targetDir,dictFileInDisk1)


def copyFiles(targetDir='',files=[]):#只有文件
    if files:
        print('+++++++++++++拷贝一次传入的所有的文件,总共{}个：'.format(len(files))+str(files))
        for f in files:
            disk=f.split(':')[0]
            #print('文件名：'+f)
            targetPath=targetDir+f'\\打包{disk}盘\\'+os.path.dirname(f).split(':')[-1]
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
                #print('创建文件夹'+targetPath)
            shutil.copy2(f,targetPath)
            #print('复制文件到'+targetPath)
                    
            writeAndPackBat(targetDir,disk)
        


def removeDubble(PackLog,filePaths=[]):
    with open(PackLog, 'a+') as f:
        f.seek(0)
        lines=f.readlines()
        for filePath in filePaths:
            if filePath  in lines:
                filePaths.remove(filePath)
            if filePath not in lines:
                f.write(filePath+'\n')
    return filePaths


def writeLog(PackLog,unknownFiles=[],path=''):
    if unknownFiles:
        with open(PackLog, 'a+') as f:
            f.write('打包{}文件中丢失的文件：\n'.format(path.split('\\')[-1]))            
            for unknownFile in unknownFiles:
                f.write(unknownFile+'\n')

def writeNote(PackLog):
    note='双击运行映射bat文件，即可创建对应盘符。\n\n'
    if not os.path.exists(PackLog):
        with open(PackLog, 'w') as f:
            f.write(note)
    else:
        with open(PackLog, 'r') as f:
            content=f.read()
            if '双击' in content:
                return
            else:
                with open(PackLog, 'w') as f:
                    f.write(note)
                    f.write(content)


def writeAndPackBat(targetDir='',disk=''):
    batFile=targetDir+f'打包{disk}盘\\'+f'映射{disk}盘.bat'
    if not os.path.exists(batFile):
        with open(batFile,'w') as f:
            f.write('subst {0}:  %CD%'.format(disk[0])+'\n')

def filterFile(filePaths=[]):
    pattern = r'^[A-Z]:'  
    notMatchFiles=[]
    for filePath in filePaths:
        # 使用re.match()函数进行匹配，如果匹配成功则返回Match对象，否则返回None  
        match = re.match(pattern, filePath) 
        if not match:
            notMatchFiles.append(filePath)
    newFilePaths=[]
    for filePath in filePaths:
        if filePath not in notMatchFiles:
            newFilePaths.append(filePath)
    print('++++合格的文件：》》》》》》》》》》》》》',newFilePaths,'++++不合格文件：》》》》》》》》》》',notMatchFiles)
    return newFilePaths,notMatchFiles


def removeAlreadyCopied(targetDir,paths):
    newPaths=[]
    for path in paths:
        path=path.replace('\\', '\\').replace('/', '\\')
        newPaths.append(path)

    repeatfiles=[]
    needPaths=[]
    print('——————————————————检查是否有重复的文件：',newPaths)   
    for root, dirs, files in os.walk(targetDir):
        files=[(root+'\\'+file).split(':')[1] for file in files]
        for file in files:
            for path in newPaths:
                if path.split(':')[1].replace('\\','')  in  file.replace('\\',''):         #先比较一下被拷贝文件是否在目标文件夹中，如果不在，再单独进行拷贝和记录进度
                    print('——————————————————匹配上了————————————————————————'*10,file,path.split(':')[1])
                    if path not in repeatfiles:
                        repeatfiles.append(path) 
                print('——————————————————全局变量文件路径里处理后的文件路径',path.split(':')[1].replace('\\',''))
                print('——————————————————目标路径里处理后的文件路径：',file.replace('\\',''))
    for new in newPaths:
        if new not in repeatfiles:
            needPaths.append(new)
    needPaths=list(set(needPaths))#如果在，就移出列表，或者设置一个bool，再界面选择是否覆盖文件
    print('——————————————————剩下来没有重复的文件：',needPaths)
    return needPaths


def fakeProgressing(targetDir):
    fakeProgress=0    
    for fake in range(8):############--------------
        fakeProgress=fake
        if os.path.exists(targetDir+'/进度.txt'):
            with open(targetDir+'/进度.txt', 'r+') as f:
                p=f.read().strip()
                if int(p)>fakeProgress:
                    print('^^^^^^^^^^fake进度小，不写入进度')
                    return
                else:
                    f.seek(0)
                    f.write(str(fakeProgress))
                    print('^^^^^^^^^写入fake进度：'+str(fakeProgress))
        else:
            with open(targetDir+'/进度.txt', 'w') as f:
                f.write(str(fakeProgress))
                print('^^^进度文件不存在，第一次写入进度：'+str(fakeProgress))
        time.sleep(0.5)


def progressing(maFiles,otherFiles,targetDir):
    #print(maFiles,otherFiles,targetDir)
    progress=0
    loop=True
    lenOfAll=len(maFiles+otherFiles)
    # pattern = re.compile(r'映射[A-Z]盘.bat')  # 匹配"映射"后跟一个大写字母和"盘.txt" 
    if maFiles or otherFiles:
        alreadyExists=0
        setAlreadyExists=False
        while loop:
            copied=0
            n=len(os.listdir(targetDir))
            for root, dirs, files in os.walk(targetDir):  
                copied=len(files)+copied

            copied=copied-n
            print('!!!!!!!!!!!!!!!copied',copied)
            if setAlreadyExists==False:
                alreadyExists=copied  
                setAlreadyExists=True
            print('!!!!!!!!!!!alreadyExists',alreadyExists)
            if (copied-alreadyExists)<lenOfAll:
                loop=True
            else:
                loop=False
            print('已经拷贝文件数：'+str(copied-alreadyExists))
            print('计划拷贝总文件数：'+str(lenOfAll))
            progress1=(copied-alreadyExists)/lenOfAll*100
            progress=int(progress1)
            if os.path.exists(targetDir+'/进度.txt'):
                with open(targetDir+'/进度.txt', 'r+') as f:
                    p=f.read().strip()
                    if int(p)==progress:
                        print('^^^^^^^^^^进度相同，不写入进度')
                    elif int(p)>progress:
                        print('^^^^^^^^^^进度小，不写入进度')
                    else:
                        f.seek(0)
                        f.write(str(progress))
                        print('^^^^^^^^^写入进度：'+str(progress))
            else:
                with open(targetDir+'/进度.txt', 'w') as f:
                    f.write(str(progress))
                    print('^^^进度文件不存在，第一次写入进度：'+str(progress))
            time.sleep(0.5)
    else:
        progress=100
        with open(targetDir+'/进度.txt', 'w') as f:
            f.write(str(progress))
            print('^^^强制写入写入进度：'+str(progress))



def main(paths=[],targetPackDir = r'D:\\打包\\'):

    global allmafiles,allothers,unknownFiles

    if not paths or  not targetPackDir:
        return print('没有传入文件路径参数')
    if targetPackDir[-1]!='\\':
        targetPackDir+='\\'

    packLog=targetPackDir+'打包文档.txt'

    def fakeprocess():
        fakeProgressing(targetPackDir)
    ft=threading.Thread(target=fakeprocess,daemon=True)
    ft.start()


    if not os.path.exists(targetPackDir):
        os.makedirs(targetPackDir)
    if paths: 
        mafiles=[]
        otherfiles=[]
        for path in paths:
            mafiles.extend(getmafiles(path)[0])
            otherfiles.extend(getmafiles(path)[1])
            #('ma文件：'+str(mafiles))
            #print('其他文件：'+str(otherfiles))
        #time.sleep(100000)
        allmafiles.extend(mafiles)
        allothers.extend(otherfiles)

    if allmafiles:

        for mafile in allmafiles:
            refFilePaths=getMayaFileRefPaths(mafile)

            a,b=filterFile(refFilePaths)
            unknownFiles.extend(b)

            dictFileInDisk=dictByDisk(a)
            # print(dictFileInDisk)
            classifyMa([],targetPackDir,dictFileInDisk)

    allmafiles=list(set(allmafiles))
    allothers=list(set(allothers))

    allmafiles=removeAlreadyCopied(targetPackDir,allmafiles)
    allothers=removeAlreadyCopied(targetPackDir,allothers)

    def process():
        progressing(allmafiles,allothers,targetPackDir)
    t=threading.Thread(target=process,daemon=True)
    t.start()

    copyFiles(targetPackDir,allothers)
    copyFiles(targetPackDir,allmafiles)
    print(u'所有文件复制完成---------------------------------------------'*100)
    

    if unknownFiles:
        writeLog(packLog,unknownFiles,mafile)
    writeNote(packLog)



#ma文件中引用ma文件的问题，已实现
#文件太大时候的性能问题
#重复文件的问题，已实现
#空的zip文件不应存在，已实现
#要加右键文件夹打包，打包的所有文件路径都记录，然后去里面对是否存在，防止重复
#log文件提示安装方法，已实现
#打包加入自动映射工具
