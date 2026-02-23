import unreal
import os
i='Ani_XXX_SC01_Hc_05-1.fbx'
a= i.split(".")[0]
b=a.split("_")[-1]
c=a.split("_")
d=""
if '-' in b:
    if len(c)==5:
        d=c[3]+"_"+c[4][:-2]
    if len(c)==4:
        d=c[3][:-2]
else:
    if len(c)==5:
        d=c[3]+"_"+c[4]
    if len(c)==4:
        d=c[3]

'''

import os
import re
ProjectFolders=['BP','CHA','Prop','Project_','Developers','Collections','VFX','Scene','Other']
#content_path='from UE param'

dirs=os.listdir(content_path)
paths=[]
files=[]

for i in dirs:
    if os.path.isdir(content_path+i) and not i.startswith('__') :
        check=False
        for folder in ProjectFolders:
            if re.search(folder, i, re.IGNORECASE):#folder in i:
                check=True
                break
        if not check:
            p='/Game/'+i
            paths.append(p)
    elif os.path.isfile(content_path+i):
        f='/Game/'+ i.split('.')[0]
        files.append(f)





# for i in range(5):
#     for j in range(5):
#         print(i, j)
#         if i == 2 and j == 2:
#             break
#     print("Outside loop")

'''

'''
import win32file
def is_used(file_name):
    try:
        vHandle = win32file.CreateFile(file_name, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
        #return int(vHandle) ==  win32file.INVALID_HANDLE_VALUE 
        win32file.CloseHandle(vHandle)
        print("Close Handle")
        '''
'''
    except:
        return True
    # finally:
    #     try:
    #         print("Close Handle")
    #     except:
    #         print("can't Close Handle")

'''
'''
print(is_used(file))
'''
'''
import win32file  
import win32con  

def is_used2(file_name):  
    try:  
        # 使用共享模式打开文件，以检查是否可以被其他进程访问  
        vHandle = win32file.CreateFile(  
            file_name,  
            win32con.GENERIC_READ,  
            win32con.FILE_SHARE_READ,  
            None,  
            win32con.OPEN_EXISTING,  
            win32con.FILE_ATTRIBUTE_NORMAL,  
            None  
        )  
        # 如果成功打开，则认为文件没有被独占使用  
        return False  
    except win32file.error:  
        # 如果因为其他进程独占文件而失败，则返回True  
        return True  
    finally:  
        # 尝试关闭句柄，但只在它已被定义时  
        if 'vHandle' in locals() and vHandle is not None:  
            win32file.CloseHandle(vHandle)

#print(is_used2(file2))

'''

#import UAssetAPI
unreal.MaterialEditingLibrary.set_material_instance_parent(instance, new_parent)