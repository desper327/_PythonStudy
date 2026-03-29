def decorator1(func):
    def wrapper():
        print("before Decorator 1")
        func()
        print("after Decorator 1")
    return wrapper

def decorator2(func):
    def wrapper():
        print("before Decorator 2")
        func()
        print("after Decorator 2")
    return wrapper


@decorator1
@decorator2
def hello():
    print("Hello")


#hello()
decorator1(decorator2(hello()))



import subprocess

env_vars={'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\wb.zhangyang21\\AppData\\Roaming', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'GIH-D-26309', 'COMSPEC': 'C:\\windows\\system32\\cmd.exe', 'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 'FRONT': 'launcher', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\wb.zhangyang21', 'LOCALAPPDATA': 'C:\\Users\\wb.zhangyang21\\AppData\\Local', 'LOGONSERVER': '\\\\GZDC1', 'LOG_DIR': 'C:\\Users\\wb.zhangyang21\\AppData\\Roaming\\Shotgun\\Logs', 'LOG_FILE': 'C:\\Users\\wb.zhangyang21\\AppData\\Roaming\\Shotgun\\Logs\\Launcher.bat.log', 'NUMBER_OF_PROCESSORS': '16', 'OS': 'Windows_NT', 'PATH': 'C:\\ProgramData\\TitanToolkit\\titan_sgtoolkit\\python\\lib\\site-packages\\pywin32_system32;C:\\windows\\system32;C:\\windows;C:\\windows\\System32\\Wbem;C:\\windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\windows\\System32\\OpenSSH\\;C:\\Program Files\\TortoiseSVN\\bin;D:\\software\\WinMerge;C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\;C:\\Program Files\\Git\\cmd;C:\\Users\\wb.zhangyang21\\.pyenv\\pyenv-win\\bin;C:\\Users\\wb.zhangyang21\\.pyenv\\pyenv-win\\shims;C:\\Users\\wb.zhangyang21\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\wb.zhangyang21\\AppData\\Local\\Programs\\Microsoft VS Code\\bin;C:\\Users\\wb.zhangyang21\\AppData\\Local\\Programs\\Windsurf\\bin;C:\\ProgramData\\PCGM_Apps\\APPs\\Autodesk\\3ds Max 2022.3', 'PATHEXT': '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 165 Stepping 5, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': 'a505', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PROMPT': '$P$G', 'PSMODULEPATH': '%ProgramFiles%\\WindowsPowerShell\\Modules;C:\\windows\\system32\\WindowsPowerShell\\v1.0\\Modules', 'PUBLIC': 'C:\\Users\\Public', 'PYENV': 'C:\\Users\\wb.zhangyang21\\.pyenv\\pyenv-win\\', 'PYENV_HOME': 'C:\\Users\\wb.zhangyang21\\.pyenv\\pyenv-win\\', 'PYENV_ROOT': 'C:\\Users\\wb.zhangyang21\\.pyenv\\pyenv-win\\', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\windows', 'TEMP': 'C:\\Users\\WB5124~1.ZHA\\AppData\\Local\\Temp', 'TITAN_SGTOOLKIT_ROOT': 'C:\\ProgramData\\TitanToolkit\\titan_sgtoolkit', 'TMP': 'C:\\Users\\WB5124~1.ZHA\\AppData\\Local\\Temp', 'UNICLOUD_PATH': 'C:/ProgramData/PCGM_Apps/APPs/unicloud-dcc-launcher', 'USERDNSDOMAIN': 'GAME.NTES', 'USERDOMAIN': 'GAME', 'USERDOMAIN_ROAMINGPROFILE': 'GAME', 'USERNAME': 'wb.zhangyang21', 'USERPROFILE': 'C:\\Users\\wb.zhangyang21', 'WINDIR': 'C:\\windows', 'ZES_ENABLE_SYSMAN': '1', 'SSL_CERT_FILE': 'C:\\ProgramData\\TitanToolkit\\titan_sgtoolkit\\python\\lib\\site-packages\\certifi\\cacert.pem', 'SHOTGUN_ENTITY_TYPE': 'Project', 'SHOTGUN_ENTITY_ID': '1145', 'SHOTGUN_SCRIPT_NAME': 'authentication_script', 'SHOTGUN_SCRIPT_KEY': 'ioiiq2qcbdcuPvmgxltoiqe#m', 'SHOTGUN_SITE': 'https://pipeline-rpc-g18.titan.nie.netease.com', 'TOOLBOX_USERNAME': '', 'LOGIN_USERNAME': 'wb.zhangyang21', 'ArtSVN': 'D:\\T-Hub\\g18art', 'TITAN_3DSMAX_PACKAGES_ROOT': 'C:\\ProgramData\\TitanToolkit\\TitanTAUtils\\max_packages', 'G18_3DSMAX_OVERPASS_PACKAGES_ROOT': 'C:\\ProgramData\\TitanToolkit\\TitanTAUtils\\overpass\\plugin\\OverpassMaxPlugin', 'G18_3DSMAX_OVERPASS_STARTUP_ROOT': 'C:\\ProgramData\\TitanToolkit\\TitanTAUtils\\overpass\\plugin\\OverpassMaxPlugin\\SourceCode\\startup'}
app_script='C:\\ProgramData\\TitanToolkit\\titan_sgtoolkit_dev\\launcher\\application\\3dsmax.bat'
subprocess.call([app_script], shell=True, env=env_vars)