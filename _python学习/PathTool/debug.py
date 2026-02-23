import os,shutil

# source_path =r'G:\工程打包\2024\4399\摔下楼救狗\Maya工程.rar'
# Ppath='P:'+ source_path.split(':')[1]
'''
try:
    print('ppath文件夹是：',os.path.dirname(Ppath))
    if not os.path.exists(os.path.dirname(Ppath)):
        print('ssss')
        os.mkdir(os.path.dirname(Ppath))
        print('创建的文件夹是：',os.path.dirname(Ppath))
    #shutil.copy2(source_path, Ppath)#原来已存在的被覆盖，不存在的添加
except Exception as e:

    print(e)
'''


#p=r'P:\工程打包\2024\4399\摔下楼救狗'
#os.makedirs(p)
# path=r'G:\AAA外包\又跑了\渲染\8.28\02\02.0309.png'
# #path=r'C:\pcwlenv'
# for root, dirs, files in os.walk(path):#root就已经包含了文件的全路径   walk的参数必须是文件夹，不能是文件，但不会报错
#     for file in files:
#         print(os.path.join(root, file))

# shutil.copy2(path,r'D:\dabao\打包G盘\\AAA外包\又跑了\渲染\8.27\02')

# os.makedirs('D:\\打包\\打包C盘')

# with open('D:\\打包\\打包C盘\\映射C盘.bat','w') as f:
#     f.write('C:\\pcwlenv')#

# a=r'G:/project/4399/Asset/角色Chars/Zhanan/Texture/Texture/T_黄头发版/zhanan_C001_shenti_BaseColor.png'
# print(os.path.exists(a))
# print(os.path.isfile(a))

# l=os.listdir(r'D:\打包')
# print(l)



def copyFiles(targetDir='',files=[]):#只有文件
    if files:
        print('拷贝一次传入的所有的文件：'+str(files))
        for f in files:
            disk=f.split(':')[0]
            #print('文件名：'+f)
            targetPath=targetDir+f'\\打包{disk}盘\\'+os.path.dirname(f).split(':')[-1]
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
                #print('创建文件夹'+targetPath)
            shutil.copy2(f,targetPath)
            #print('复制文件到'+targetPath)


#copyFiles(r'D:\打包',[r'G:\\project\\4399\\Asset\\角色Chars\\Nanzhu\\Rig\\approve\\Nanzhu_Rig.ma'])
'''
a=r'\\打包\\打包G盘\\project\\iGame\\Asset\\道具Props\\crtm\\Rig\\approve\\SK_TW.fbx'
b=r'\project\iGame/Asset\\道具Props\/crtm\\Rig/approve\\SK_TW.fbx'
b=os.path.commonpath(b)
#print(b in a ,'hhhhhhhhhhhhhhh')
print(b)

'''

os.system('cmd.exe')


# import subprocess
# subprocess.Popen('cmd.exe')