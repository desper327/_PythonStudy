#coding=utf-8

import sys
import maya.standalone
import maya.cmds as cmds

def get_dag_objects():
    dag_objects = cmds.ls(dag=True)
    return dag_objects

def get_root_nodes():
    # 使用 ls 命令与参数来获取所有变换节点，然后通过 listRelatives 命令过滤出没有父节点的节点
    all_transforms = cmds.ls(type='transform')
    root_nodes = []
    for transform in all_transforms:
        if not cmds.listRelatives(transform, parent=True) and transform not in ['persp','side', 'top', 'front']:
            root_nodes.append(transform)
    return root_nodes

if __name__ == "__main__":
    maya.standalone.initialize(name='python')
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            cmds.file(file_path, open=True, force=True)
            print('below is the script output:')# 将结果输出到标准输出（PyQt 界面将捕获该输出）
        root_nodes = get_root_nodes()
        for node in root_nodes:
            print(node)
    except Exception as e:
        print("Error: {}".format(e))
    finally:
        maya.standalone.uninitialize()
