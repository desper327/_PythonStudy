import os,shutil
import csv
import sys,time,re

#f=os.listdir(r'F:\Study\Python\MAYA_PY')
#print(f)

# for root, dirs, files in os.walk(r'F:\Study\Python\MAYA_PY\重命名插件'):  
#     for file in files:
#         full_path = os.path.join(root, file)  # 获取文件的完整路径
#         print(full_path)
def read_genarater(toWaiBao,mayaFile=''):
    with open(mayaFile, 'r') as f:
        line_count = 0
        while True:
            try:
                line = f.readline()
                if line == '':
                    break
                yield line
                if not toWaiBao:
                    line_count += 1
                    if line_count >= 500:
                        print(f'读取到了{line_count}行，不再读了')
                        break
            except Exception as e:
                print(f'读取{mayaFile}文件失败，原因是：'+str(e))
                return []
def getMayaFileRefPaths(toWaiBao,mayaFile=''):
    #print('-----当前在这个maya文件里找引用文件mayaFileeeeeee:',mayaFile)
    RG=read_genarater(toWaiBao,mayaFile)
    refpath=[]
    foundfile=False
    for i,line in enumerate(RG):
        if line.startswith('file -r'):
            foundfile=True
            if line.endswith('";\n'):
                refpath.append(line.split('"')[-2])
                foundfile=False
        if foundfile:
            if line.endswith('";\n'):
                refpath.append(line.split('"')[-2])
                foundfile=False
        if 'setAttr ".ftn"' in line:
            texpath=line.split('"')[-2]
            refpath.append(texpath)
        if "fileTextureName" in line:
            if line.endswith('\""\n'):
                texpath=line.split(':')[0][-1]+':'+line.split(':')[-1][:-4]
                refpath.append(texpath)
            ##print('texpath>>>>>>>>'+ texpath)
    files=list(set(refpath))
    for f in files:
        #print('####找到的引用文件>>>>>>>>'+ f)
        pass
    return files



# files=getMayaFileRefPaths(True,r'G:\project\BINGO\Shot\Animation\生娃\整片\work\SW_shot02.ma')
# print(files)



'''
if 'UnrealEditor.exe' in sys.executable:

    print('UE4')
print(sys.executable)

class Test:
    def __init__(self, name):
        self.name = name
    def test(self):
        print('test')

t1=Test('t1')
a=getattr(t1, 'test')
print(a)

e=os.path.exists('G:\chajian\OtherTools')
print(e)
with open(r'G:\chajian\OtherTools\test.csv', 'w') as f:
    f.write('1,2,3\n')


def check_app_file():
    destPath='C:\\ProgramData\\MT_tray\\OtherApps'
    fromPath='G:\\chajian\\OtherTools\\OtherApps'
    if os.path.exists(fromPath):
        for root, dirs, files in os.walk(fromPath):#root就已经包含了文件的全路径
            for file in files:
                from_path = os.path.join(root, file)
                dest_path=os.path.join(destPath, file)
                try:
                    if os.path.isfile(dest_path):
                        continue
                    else:
                        shutil.copy2(from_path, dest_path)
                except Exception as e:
                    print(e)


check_app_file()'''
'''
import subprocess
def mergeMov():
    full_filename = r'C:/Users/zy/Desktop/aa.ma'
    folder_path = os.path.dirname(full_filename)
    movfolder=os.listdir(os.path.dirname(full_filename))
    movfiles=[mov for mov in movfolder if mov.endswith('.mov')]
    for mov in movfiles:
        if '_temp_front' in mov:
            frontmov=mov
        if '_temp_back' in mov:    
            backmov=mov
        if '_temp_left' in mov:    
            leftmov=mov
        if '_temp_right' in mov:    
            rightmov=mov
    if frontmov and backmov and leftmov and rightmov:
        ffmpeg_path=r'C:\ProgramData\MT_tray\OtherApps\ffmpeg.exe'
        if os.path.exists(ffmpeg_path):
            video_files = [os.path.join(folder_path,frontmov),
                            os.path.join(folder_path,backmov),
                            os.path.join(folder_path,leftmov),
                            os.path.join(folder_path,rightmov)]
            print(video_files)

            with open(folder_path+'input.txt', 'w') as f:
                for video in video_files:
                    f.write("file '{}'\n".format(video))

            # 调用ffmpeg命令
            command = [ffmpeg_path, "-f", "concat", "-safe", "0", "-i", folder_path+"input.txt", "-c", "copy", r"C:/Users/zy/Desktop/output.mov"]
            subprocess.run(command)
mergeMov()'''




'''
import unreal

# 获取 SubobjectDataSubsystem
so_subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)

# 使用指定的GUID过滤并获取选中的Actor
# guid = "your-guid-here"  # 你需要替换为实际的GUID
actors = unreal.EditorFilterLibrary.by_id_name(
    unreal.EditorLevelLibrary.get_selected_level_actors(),
    guid, 
    unreal.EditorScriptingStringMatchType.MATCHES_WILDCARD
)

if actors:
    actor = actors[0]
    print("Actor found:", actor)
    root_component = actor.root_component
    children_components=root_component.get_children_components(True)

    print ("children_components",children_components)
    # 检查 GeometryCacheComponent 是否已存在
    has_geometry_cache_component = False
    for subobject in children_components:
        if isinstance(subobject, unreal.GeometryCacheComponent):
            has_geometry_cache_component = True
            break
    print ("has_geometry_cache_component",has_geometry_cache_component)
    # 如果 GeometryCacheComponent 不存在，则添加它
    if not has_geometry_cache_component:
        root_sub_object = so_subsystem.k2_gather_subobject_data_for_instance(actor)[0]
        new_sub_object = so_subsystem.add_new_subobject(unreal.AddNewSubobjectParams(
            parent_handle=root_sub_object,
            new_class=unreal.GeometryCacheComponent,
        ))
        print("Added new GeometryCacheComponent:", new_sub_object)
    else:
        print("GeometryCacheComponent already exists.")

else:
    print("No actor found with the given GUID.")

print("GUID:", guid)


#command=r'C:\ProgramData\MT_tray\OtherApps\ffmpeg.exe'
a=r'G:\chajian\Python310\python.exe'
b=r'G:\chajian\Maya_Plugin\MT_plugin\scripts\MT_tray\mayaCall_MT_main.py'
exec('{} {}'.format(a,b))

'''

#被freetest2.py调用的脚本
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: auto_sync.py <change>")
#         sys.exit(1)
    
#     change_number = int(sys.argv[1])
#     print(change_number)
#     time.sleep(change_number)


# changes=['235\n', '236\n', '237\n', '238\n', '245\n', '246\n', '247\n', '248\n', '245\n', '246\n']
# change='22'
# changes.pop(0)
# print(type(changes))
# print(changes)
# print(type(change))
# changes.append(change+'\n')
# print(changes)



import os
import re

def find_consecutive_files(folder_path):
    # 定义正则表达式模式以匹配4个连续数字
    pattern = re.compile(r'\d{4}')
    # 获取文件夹中所有文件的列表
    files = os.listdir(folder_path)
    # 存储满足条件的文件列表
    result = []
    for file in files:
        # 检查文件名是否包含4个连续数字
        match = pattern.search(file)
        if match:
            # 提取数字并转换为整数
            number = int(match.group())
            # 这里我们简单地将每个匹配的文件和其对应的数字存储在一个字典中
            # 后续可以根据需要对这个字典进行处理
            result.append({'file': file, 'number': number})
    # 根据数字对文件进行排序
    result.sort(key=lambda x: x['number'])
    # 检查数字是否连续，并返回连续的文件列表
    consecutive_files = []
    prev_number = None
    for item in result:
        if prev_number is None or item['number'] == prev_number + 1:
            consecutive_files.append(item['file'])
            prev_number = item['number']
        else:
            # 如果数字不连续，则重置连续文件列表和上一个数字
            if consecutive_files:  # 只有当已经找到连续文件时才重置
                yield consecutive_files  # 返回当前找到的连续文件列表
                consecutive_files = []
            prev_number = item['number']
            consecutive_files.append(item['file'])
    
    # 返回最后一组连续文件（如果有的话）
    if consecutive_files:
        yield consecutive_files

# 使用示例：替换'your_folder_path'为你的文件夹路径
folder_path = r'D:\UEproject\Render\3v3竖版\1-3-4'
#for consecutive_group in find_consecutive_files(folder_path):
#    print(consecutive_group)


# class AA:
#     def __init__(self, name):
#         self.name = name
#         print(self.name)
#     def test(self):
#         print('test')

# class BB(AA):
#     def __init__(self, name):
#         super(BB, self).__init__(name)
#         print('call BB')
#     def test(self):
#         super(BB, self).test()
#         print('test2')

# bb=BB('bb')
# bb.test()
