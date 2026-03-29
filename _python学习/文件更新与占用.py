import win32file

def is_file_using(file_name):
    try:
        vHandle = win32file.CreateFile(file_name, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
        return int(vHandle) == win32file.INVALID_HANDLE_VALUE
    except:
        return True
    finally:
        try:
            win32file.CloseHandle(vHandle)
        except:
            pass

#获取文件句柄



import os
import stat

def _remove_read_only_bit(file_path):
    """
    移除文件只读属性，使其可写（Windows/跨平台兼容）。

    Args:
        file_path: 文件路径

    Returns:
        None
    """
    if not file_path or not os.path.exists(file_path):
        return
    file_mode = os.stat(file_path).st_mode
    print(file_mode)
    print(stat.S_IWRITE)
    if file_mode & stat.S_IWRITE:#按位与运算，检查 file_mode 中是否包含写权限位    
    # 如果包含，结果非零 (真)
    # 如果不包含，结果为零 (假)
        return
    os.chmod(file_path, file_mode | stat.S_IWRITE)#按位或运算，添加写权限

_remove_read_only_bit(r"C:\Users\89468\Desktop\MXSPyCOM\hello_world.py")