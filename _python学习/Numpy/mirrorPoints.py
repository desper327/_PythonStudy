
#传统方式 可行，测试6s
import maya.cmds as cmds
import time

def mirror_points():
    # 获取选中的物体
    selection = cmds.ls(selection=True)

    # 确保选中两个模型
    if len(selection) < 2:
        cmds.warning("请选中两个模型")
        return

    source_model = selection[0]
    target_model = selection[1]

    # 获取源模型的所有点坐标
    points = cmds.xform(f'{source_model}.vtx[*]', query=True, translation=True, worldSpace=True)

    # 将点坐标转换为二维列表, 每三个值为一个点的坐标
    mirrored_points = []
    for i in range(0, len(points), 3):
        # 获取当前点的坐标
        x = points[i]
        y = points[i + 1]
        z = points[i + 2]

        # 根据 x 轴进行镜像
        mirrored_x = -x
        mirrored_points.extend([mirrored_x, y, z])  # 添加镜像后的坐标

    # 设置目标模型的点坐标
    for i in range(len(mirrored_points) // 3):
        cmds.xform(f'{target_model}.vtx[{i}]', worldSpace=True, translation=mirrored_points[i*3:(i+1)*3])


t1=time.time()
# 调用函数
mirror_points()

t2=time.time()

print("traditional Time used:",t2-t1)





#numpy方式  cmds  可行  测试14s
import maya.cmds as cmds
import numpy as np

def mirror_points():
    # 获取选中的物体
    selection = cmds.ls(selection=True)

    # 确保选中两个模型
    if len(selection) < 2:
        cmds.warning("请选中两个模型")
        return

    source_model = selection[0]
    target_model = selection[1]

    # 获取源模型的所有点坐标
    points = cmds.xform(f'{source_model}.vtx[*]', query=True, translation=True, worldSpace=True)

    # 将点坐标转换为 NumPy 数组
    points_array = np.array(points).reshape(-1, 3)  # 将一维数组重塑为二维数组 (N, 3)

    # 根据 x轴进行镜像
    mirrored_points_array = points_array * np.array([-1, 1, 1])

    # 设置目标模型的点坐标
    for i in range(len(mirrored_points_array)):
        cmds.xform(f'{target_model}.vtx[{i}]', worldSpace=True, translation=mirrored_points_array[i].tolist())

# 调用函数

t1=time.time()
# 调用函数
mirror_points()

t2=time.time()

print("numpy Time used:",t2-t1)



#api方式 numpy 可行  测试0.06s
import maya.OpenMaya as om
import maya.cmds as cmds
import numpy as np

def get_mesh_points_as_numpy(mesh_name):
    """
    获取指定模型的点坐标并转换为 numpy 数组
    """
    # 选择 mesh 对象
    selection_list = om.MSelectionList()
    selection_list.add(mesh_name)
    
    # 获取 mesh dag path
    dag_path = om.MDagPath()
    selection_list.getDagPath(0, dag_path)
    
    # 获取 mesh 的 MFnMesh 对象
    mesh_fn = om.MFnMesh(dag_path)
    
    # 获取点数据
    points = om.MPointArray()
    mesh_fn.getPoints(points, om.MSpace.kWorld)
    
    # 转换为 numpy 数组
    points_np = np.zeros((points.length(), 3))
    for i in range(points.length()):
        points_np[i, 0] = points[i].x
        points_np[i, 1] = points[i].y
        points_np[i, 2] = points[i].z
        
    return points_np

def set_mesh_points_from_numpy(mesh_name, points_np):
    """
    将 numpy 数组中的点坐标设置为指定模型的点坐标
    """
    # 选择 mesh 对象
    selection_list = om.MSelectionList()
    selection_list.add(mesh_name)
    
    # 获取 mesh dag path
    dag_path = om.MDagPath()
    selection_list.getDagPath(0, dag_path)
    
    # 获取 mesh 的 MFnMesh 对象
    mesh_fn = om.MFnMesh(dag_path)
    
    # 创建一个新的 MPointArray
    points = om.MPointArray()
    for i in range(points_np.shape[0]):
        point = om.MPoint(points_np[i, 0], points_np[i, 1], points_np[i, 2])
        points.append(point)
    
    # 将修改后的点设置回 mesh
    mesh_fn.setPoints(points, om.MSpace.kWorld)

def mirror_points_along_x(points_np):
    """
    沿 X 轴镜像点坐标
    """
    mirrored_points = np.copy(points_np)
    mirrored_points[:, 0] = -mirrored_points[:, 0]  # 镜像 X 轴坐标
    return mirrored_points

def main():
    # 获取当前选择的模型
    selected_objects = cmds.ls(selection=True)
    
    if len(selected_objects) != 2:
        cmds.error("请选中两个模型，第一个是源模型，第二个是目标模型")
        return
    
    source_mesh = selected_objects[0]
    target_mesh = selected_objects[1]
    
    # 获取第一个模型的点坐标
    source_points = get_mesh_points_as_numpy(source_mesh)
    
    # 镜像点坐标
    mirrored_points = mirror_points_along_x(source_points)
    
    # 将镜像后的点坐标设置给第二个模型
    set_mesh_points_from_numpy(target_mesh, mirrored_points)
    print(f"已将 {source_mesh} 的镜像坐标应用到 {target_mesh}")

# 运行
t1=time.time()
# 调用函数
main()
t2=time.time()

print("API numpy Time used:",t2-t1)








#api方式无numpy 测试0.05s
import maya.OpenMaya as om
import maya.cmds as cmds
import time

def get_mesh_points(mesh_name):
    """
    获取指定模型的点坐标并存储在一个 Python 列表中
    """
    # 选择 mesh 对象
    selection_list = om.MSelectionList()
    selection_list.add(mesh_name)
    
    # 获取 mesh dag path
    dag_path = om.MDagPath()
    selection_list.getDagPath(0, dag_path)
    
    # 获取 mesh 的 MFnMesh 对象
    mesh_fn = om.MFnMesh(dag_path)
    
    # 获取点数据
    points = om.MPointArray()
    mesh_fn.getPoints(points, om.MSpace.kWorld)
    
    # 将点数据转换为 Python 列表 (3D 点的列表)
    points_list = []
    for i in range(points.length()):
        point = (points[i].x, points[i].y, points[i].z)
        points_list.append(point)
    
    return points_list

def set_mesh_points(mesh_name, points_list):
    """
    将点坐标列表设置到指定的模型
    """
    # 选择 mesh 对象
    selection_list = om.MSelectionList()
    selection_list.add(mesh_name)
    
    # 获取 mesh dag path
    dag_path = om.MDagPath()
    selection_list.getDagPath(0, dag_path)
    
    # 获取 mesh 的 MFnMesh 对象
    mesh_fn = om.MFnMesh(dag_path)
    
    # 创建一个新的 MPointArray
    points = om.MPointArray()
    for point in points_list:
        points.append(om.MPoint(point[0], point[1], point[2]))
    
    # 将修改后的点设置回 mesh
    mesh_fn.setPoints(points, om.MSpace.kWorld)

def mirror_points_along_x(points_list):
    """
    沿 X 轴镜像点坐标
    """
    mirrored_points_list = []
    for point in points_list:
        # 将 X 坐标镜像（即取负）
        mirrored_point = (-point[0], point[1], point[2])
        mirrored_points_list.append(mirrored_point)
    
    return mirrored_points_list

def main():
    # 获取当前选择的模型
    selected_objects = cmds.ls(selection=True)
    
    if len(selected_objects) != 2:
        cmds.error("请选中两个模型，第一个是源模型，第二个是目标模型")
        return
    
    source_mesh = selected_objects[0]
    target_mesh = selected_objects[1]
    
    # 获取第一个模型的点坐标
    source_points = get_mesh_points(source_mesh)
    
    # 镜像点坐标
    mirrored_points = mirror_points_along_x(source_points)
    
    # 将镜像后的点坐标设置给第二个模型
    set_mesh_points(target_mesh, mirrored_points)
    print(f"已将 {source_mesh} 的镜像坐标应用到 {target_mesh}")

# 运行
t1=time.time()

main()
t2=time.time()

print("aarray  Time used:",t2-t1)
