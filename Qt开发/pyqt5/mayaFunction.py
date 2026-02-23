# -*- coding: utf-8 -*-
import sys
import os

MAYA_LOCATION = "C:/Program Files/Autodesk/Maya2020"
PYTHON_LOCATION = MAYA_LOCATION + "/Python/Lib/site-packages"

os.environ["MAYA_LOCATION"] = MAYA_LOCATION
os.environ["PYTHONPATH"] = PYTHON_LOCATION

sys.path.append(MAYA_LOCATION)
sys.path.append(PYTHON_LOCATION)
sys.path.append(MAYA_LOCATION+"/bin")
sys.path.append(MAYA_LOCATION+"/lib")
sys.path.append(MAYA_LOCATION+"/Python")
sys.path.append(MAYA_LOCATION+"/Python/DLLs")
sys.path.append(MAYA_LOCATION+"/Python/Lib")
sys.path.append(MAYA_LOCATION+"/Python/Lib/plat-win")
sys.path.append(MAYA_LOCATION+"/Python/Lib/lib-tk")
#print('\n'.join(sys.path))

import maya.standalone
'''
try:
    import maya.standalone
except Exception as e:
    print(f"Error initializing Maya standalone: {e}")
'''
maya.standalone.initialize(name='python')

import maya.cmds as cmds
ma_file_path = "C:/Users/89468/Desktop/testExport/aaa.mb"
cmds.file(ma_file_path, open=True, force=True)


# 获取当前打开的 Maya 文件中的引用文件
reference_files = cmds.file(query=True, reference=True)

#保存清理后的文件：
cleaned_file_path = 'C:/Users/89468/Desktop/testexport/BBB.ma'
cmds.file(rename=cleaned_file_path)
cmds.file(save=True)

#关闭Maya：
maya.standalone.uninitialize()




