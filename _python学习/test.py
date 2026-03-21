import os


def print_test():
    青青= True
    打印=print
    打印(青青)



def dataclass_test():
    from dataclasses import dataclass, asdict, field
    @dataclass
    class P4LoginInfo:
        Access: str
        AuthMethod: int
        Email: str
        FullName: str
        Type: str

    a=P4LoginInfo("123456", 1, "123@123.com", "张三", "P4")
    print(a)
    print(asdict(a))
    print(field(default=123))

def subprocess_test():
    import subprocess
    import os
    script_path = r"A:\TD\CGTW\Plugin\sync_model_mat_to_rig\export_mat.py"
    mayapy_path=r"D:/Software/Maya 2020/Maya2020/bin/mayapy.exe"
    mod_file_path=r"G:/commonTemplate/Asset/Character/character1/for_Assts_Data/Shader_Tex_scenes/Version/character1_Shader.ma"             

    cmd = [mayapy_path, script_path, mod_file_path]

    print(f"执行命令: {cmd}")
    #process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(mod_file_path))
    os.system("cmd.exe /k "+" ".join(cmd))
    # process.wait()
    # print(process.stdout.read().decode('GBK'))
    # print(process.stderr.read().decode('GBK'))

def test():
    mayapy_path=r"D:/Software/Maya 2020/Maya2020/bin/mayapy.exe"
    print(os.path.basename(mayapy_path).split(".")[0])

def test_env():
    import os
    env={"LUGWITAPPDIR": "D:\\TD_Depot\\Software\\Lugwit_syncPlug\\lugwit_insapp",
    "LUGWITLIBDIR": "D:\\TD_Depot\\Software\\Lugwit_syncPlug\\lugwit_insapp\\trayapp\\Lib",
    "LUGWITPATH": "D:\\TD_Depot\\plug_in\\Lugwit_plug",
    "LUGWITTOOLDIR": "D:\\TD_Depot\\Software\\Lugwit_syncPlug\\lugwit_insapp\\trayapp",
    "LUGWIT_MAYAPLUGINPATH": "D:\\TD_Depot\\plug_in\\Lugwit_plug\\mayaPlug",
    "LUGWIT_PUBLICPATH": "A:\\TD",
    "MAYA_MODULE_PATH": "C:\\Program Files\\Epic Games\\MetaHumanForMaya\\",
    "MAYA_UI_LANGUAGE": "en_US",
    "YPLUG": "D:\\TD_Depot\\plug_in\\Yplug",
    }
    env["PATH"] = os.getenv("PATH","") + ';"D:\\TD_Depot\\plug_in\\Lugwit_plug\\mayaPlug\\plug-ins"'
    os.environ.update(env)
    print(os.environ)

def test_str():
    a="C:\\Program Files\\Epic Games\\MetaHumanForMaya\\".find("ile",13,15)
    print(a)
    print("HHHoooOO".lower())


import sys
sys.path.append(r"D:\code_dev\TitanTAUtils\max_packages\python\public_mode_utils")
try:
    from print_public_mode import Tprint
except:
    Tprint = print

def check_repeat_maps1(map_files):
    is_success = True
    file_info = {}
    target_file = ""
    clean_map_files = list(set(map_files))
    Tprint(clean_map_files,file_info)
    
    for file in clean_map_files:
        Tprint(file)
        file_full_name = os.path.basename(file)#1214.psd
        file_name = file_full_name.split(".")[0]# 1214
        file_type = file_full_name.split(".")[-1]# psd

        if file_name in file_info.keys():
            Tprint(file,file_name,file_info)
            suffix = file_info[file_name]["file_type"].split(".")[-1]
            Tprint(suffix)
            if file_type != suffix:
                if os.path.dirname(file) == os.path.dirname(file_info[file_name]["file_path"]) and file_type in  ["tga","psd"] and suffix in  ["tga","psd"]: #同文件夹下的psd和tga同名忽略
                    Tprint("同文件夹下的psd和tga同名忽略: " + file_full_name + " -- " + file_name+suffix)
                    pass
                else:
                    Tprint("存在命名重复的贴图文件: " + file_full_name + " -- " + file_name + "." + str(file_info[file_name]))
                    target_file = file
                    is_success = False
        else:
            file_info[file_name] = {"file_type":file_type,"file_path":file}

    if not is_success:
        msg = "       检测到贴图文件命名重复，请修改后重新导出！\n"
        msg += "        不同格式的贴图文件不可重名！因为 PSD 文件会转换为 tga\n"
        msg += "        如：123.psd 和 123.tga 需要修改为 123.psd 和 abc.tga\n"
        for f in map_files:
            msg += "        " + f + "\n"
        return is_success, msg
    return is_success, None


def check_repeat_maps(map_files):
    """
    检查贴图文件是否重复命名
    
    逻辑：
    1. 先按文件夹分组
    2. 在每个文件夹内检查是否有重复文件名
    3. 保留原有的全局重复检查逻辑（跨文件夹检查）
    
    Args:
        map_files: 贴图文件路径列表
        
    Returns:
        tuple: (is_success, error_message)
    """
    is_success = True
    error_messages = []
    
    # 去重
    clean_map_files = list(set(map_files))
    Tprint(clean_map_files)
    
    folder_groups = {}
    for file in clean_map_files:
        folder_path = os.path.dirname(file)
        if folder_path not in folder_groups:
            folder_groups[folder_path] = []
        folder_groups[folder_path].append(file)
    
    Tprint(f"检测到 {len(folder_groups)} 个文件夹")
    
    for folder_path, files_in_folder in folder_groups.items():
        Tprint(f"\n检查文件夹: {folder_path}")
        Tprint(f"文件数: {len(files_in_folder)}")
        
        folder_file_info = {}
        
        for file in files_in_folder:
            file_full_name = os.path.basename(file)  # 1214.psd
            file_name = file_full_name.split(".")[0]  # 1214
            file_type = file_full_name.split(".")[-1]  # psd
            
            if file_name in folder_file_info.keys():
                # 在同一个文件夹内发现重复文件名
                existing_file_type = folder_file_info[file_name]["file_type"]
                existing_file_path = folder_file_info[file_name]["file_path"]
                
                # 同文件夹下的psd和tga同名忽略
                if file_type in ["tga", "psd"] and existing_file_type in ["tga", "psd"]:
                    Tprint(f"  ✓ 同文件夹下的psd和tga同名忽略: {file_full_name} -- {file_name}.{existing_file_type}")
                    continue
                else:
                    # 其他情况视为重复错误
                    error_msg = f"  ✗ 同文件夹内存在重复文件名:\n"
                    error_msg += f"    文件夹: {folder_path}\n"
                    error_msg += f"    文件1: {os.path.basename(existing_file_path)}\n"
                    error_msg += f"    文件2: {file_full_name}\n"
                    Tprint(error_msg)
                    error_messages.append(error_msg)
                    is_success = False
            else:
                folder_file_info[file_name] = {
                    "file_type": file_type,
                    "file_path": file
                }
    
    if not is_success:
        msg = "检测到贴图文件命名重复，请修改后重新导出！\n\n"
        msg += "规则说明：\n"
        msg += "  1. 同文件夹内，PSD和TGA可以同名（PSD会转换为TGA）\n"
        msg += "  2. 同文件夹内，其他格式不可同名\n"
        msg += "错误详情：\n"
        msg += "\n".join(error_messages)
        msg += "\n所有检测的文件：\n"
        for f in clean_map_files:
            msg += f"  {f}\n"
        Tprint(msg)
        return is_success, msg
    
    return is_success, None



_files=[r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\1214.psd",
        r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\1214.tga",
        r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\1214.tga",
        r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\1214.tga",
        r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\1214.tga",
        r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\05\1214.psd",
        r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\05\1214.tga"]
#print(list(set(_files)))

#check_repeat_maps(_files)

def convert_to_absolute_path(path, base_path=None):
    """判断路径是否为相对路径，如果是则转换为绝对路径"""
    if not path:
        return path
    
    if os.path.isabs(path):
        if base_path and not os.path.exists(path):#尝试自动转换到本地的p4映射路径
            if "G18项目美术资源" in path and "G18项目美术资源" in base_path:
                path = base_path.split("G18项目美术资源")[0] + "G18项目美术资源" + path.split("G18项目美术资源")[1]
                print(path)
        return os.path.normpath(path)
    
    if base_path:
        absolute_path = os.path.join(base_path, path)
    else:
        absolute_path = os.path.abspath(path)
    
    return os.path.normpath(absolute_path)
p1=r"E:\PerforceWork\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\5NPC（3D）\1214布雨神君\模型换装004\01\1214.tga"
p2=r"D:\P4WorkSpace\Z\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\1主角（3D端游）\时装蒙皮文件\276\jxk_276_skin.max"
p3=r"F:/inner01/guangzhou/G18项目美术资源/P4V目录/2)美术资源制作目录/2)制作资源/角色/1主角（3D端游）/时装蒙皮文件/276/01/276_1_1.tga"
print(p2.split("G18项目美术资源")[0])
a=convert_to_absolute_path(p3,base_path=p2)
print(a)
print(os.path.exists(a))