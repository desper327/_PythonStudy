import os

path=input('请输入任意路径，都会在P盘创建相同的文件夹：')

Ppath='P:'+ path.split(':')[1]
print(Ppath)
if os.path.exists(Ppath):
    print('文件夹已存在')
else:
    try:
        os.makedirs(Ppath,exist_ok=True)
        print('文件夹创建成功')
    except Exception as e:
        print('文件夹创建失败',e)



