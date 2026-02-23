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

mayapy_path=r"D:/Software/Maya 2020/Maya2020/bin/mayapy.exe"
print(os.path.basename(mayapy_path).split(".")[0])


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