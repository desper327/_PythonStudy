# coding=utf-8
import os
import maya.cmds as cmds
def clear_maya_file(path):
    u"""删除所有未知节点与插件，删除多余script节点"""
    path = path.replace('\\', '/')
    folder_path = path.rsplit('/', 1)[0]
    file_name = path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    results = []
    with open(path, 'r') as file_obj:
        need_write = True
        for line in file_obj.readlines():
            if line.startswith('createNode') or line.startswith('select'):
                need_write = True
                if line.startswith('createNode script'):
                    if not line.startswith('createNode script -n "sceneConfigurationScriptNode"') not line.startswith('createNode script -n "uiConfigurationScriptNode"'):
                        need_write = False
            if need_write:
                results.append(line)
    with open(path, "w") as file_obj:
        file_obj.writelines(results)
    return True

def list_maya_file(dir_path):
    all_file_list = []
    for foldername, subfolders, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.rsplit('.', 1)[-1] == 'ma':
                file_path = os.path.join(foldername, filename)
                all_file_list.append(file_path)
    cmds.progressBar(progress_bar, edit=True, maxValue=len(all_file_list))
    cmds.refresh()
    return all_file_list

def start_clean(*arg):
    folder_path = cmds.textField(folder_path_filed, q=True, text=True)
    if not os.path.isdir(folder_path):
        cmds.text(feed_back, e=True, label=u'请在上方输入文件夹路径')
    else:
        maya_file_list = list_maya_file(folder_path)
        if maya_file_list:
            cmds.text(feed_back, e=True, label=u'开始清理maya文件')
            for each_file in maya_file_list:
                clear_maya_file(each_file)
                cmds.progressBar(progress_bar, edit=True, step=1)
                cmds.refresh()
                cmds.text(feed_back, e=True, label=u'开始清理{}'.format(each_file))
            cmds.text(feed_back, e=True, label=u'全部清理完毕')
        else:
            cmds.text(feed_back, e=True, label=u'已完全清理完毕')
            

try:
    if cmds.window(maya_file_clean_win, exists=True):
        cmds.deleteUI(maya_file_clean_win)
except:
    pass
maya_file_clean_win = cmds.window(title=u'maya文件清理', widthHeight=(300, 200))
cmds.columnLayout(adjustableColumn=True)
cmds.text( label='这个脚本可以批量清除所有ma文件中所有非常规的脚本节点' )
cmds.text( label='文件夹路径(请勿带有中文路径)' )
folder_path_filed = cmds.textField()
cmds.button(label=u'开始清理', c=start_clean)
feed_back = cmds.text(label=u'_(:з」∠)_')
progress_bar = cmds.progressBar(maxValue=100, width=300)
cmds.setParent('..')
cmds.showWindow(maya_file_clean_win)
