import maya.OpenMaya as om
import maya.cmds as cmds
import numpy as np
import time



#方法一：只能实现对X轴的对称检查  3万顶点耗时6s,12万顶点爆内存
def get_mesh_vertices_as_numpy(mesh_name):
    # 创建 MSelectionList 并选择模型
    sel = om.MSelectionList()
    sel.add(mesh_name)
    
    # 获取 MDagPath
    dag_path = om.MDagPath()
    sel.getDagPath(0, dag_path)
    
    # 获取 MFnMesh 函数集
    mesh_fn = om.MFnMesh(dag_path)
    
    # 获取顶点位置
    points = om.MPointArray()
    mesh_fn.getPoints(points, om.MSpace.kWorld)
    
    # 将顶点转换为 NumPy 数组
    vertex_array = np.zeros((points.length(), 3))
    print(points.length())
    for i in range(points.length()):
        #print(i)
        vertex_array[i, 0] = points[i].x
        vertex_array[i, 1] = points[i].y
        vertex_array[i, 2] = points[i].z

    return vertex_array

def is_symmetric_on_x_axis_optimized(mesh_name, tolerance=0.01):
    # 获取顶点坐标的 NumPy 数组
    vertices = get_mesh_vertices_as_numpy(mesh_name)
    print(vertices.shape)
    
    # 将 X 轴上的顶点划分为正 X 和负 X
    positive_x = vertices[vertices[:, 0] > 0]
    negative_x = vertices[vertices[:, 0] < 0]
    print(positive_x.shape)
    
    # 对负 X 坐标的点进行镜像反转 (负 X -> 正 X)
    negative_x_mirrored = negative_x.copy()
    negative_x_mirrored[:, 0] = -negative_x_mirrored[:, 0]
    print(negative_x_mirrored.shape)
    
    # 为每个正 X 轴顶点，寻找与其距离小于 tolerance 的负 X 轴镜像顶点
    # for pos_vertex in positive_x:
    #     # 计算所有镜像点与当前正 X 轴顶点的欧氏距离
    #     distances = np.linalg.norm(negative_x_mirrored - pos_vertex, axis=1)
    vecters=negative_x_mirrored[None]-positive_x[:,None]
    print('vecters',vecters)
    print(vecters.shape)
    distances = np.linalg.norm(vecters, axis=2)
    print(distances.shape)
    print(distances)
    print(distances[1])
    
    
    min=np.argmin(distances,axis=1)
        
    # 如果没有一个点的距离小于 tolerance，则返回 False
    for i,m in enumerate(min):
        if not distances[i,m] < tolerance:
            print(distances[i,m])
            return False
    
    return True



t1=time.time()

mesh_name = cmds.ls(selection=True)[0]  # 选择要检查的模型
ps=get_mesh_vertices_as_numpy(mesh_name)
#print(ps)
iss=is_symmetric_on_x_axis_optimized(mesh_name)
print(iss)

t2=time.time()
print("aarray  Time used:",t2-t1)



#方法二：可以实现对任意平面的对称检查,可以是2个模型，也可以是1个模型和1个平面，12万顶点耗时6s，50万顶点21s
import maya.OpenMaya as om
import maya.cmds as cmds
import numpy as np
import time
def get_mesh_vertices_as_numpy(mesh_name):
    # 创建 MSelectionList 并选择模型
    sel = om.MSelectionList()
    sel.add(mesh_name)
    
    # 获取 MDagPath
    dag_path = om.MDagPath()
    sel.getDagPath(0, dag_path)
    
    # 获取 MFnMesh 函数集
    mesh_fn = om.MFnMesh(dag_path)
    
    # 获取顶点位置
    points = om.MPointArray()
    mesh_fn.getPoints(points, om.MSpace.kWorld)
    
    # 将顶点转换为 NumPy 数组
    vertex_array = np.zeros((points.length(), 3))
    print(points.length())
    for i in range(points.length()):
        #print(i)
        vertex_array[i, 0] = points[i].x
        vertex_array[i, 1] = points[i].y
        vertex_array[i, 2] = points[i].z

    return vertex_array

def split_point_cloud(point_cloud, plane_point, plane_normal):
    # 确保法向量单位化
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    
    # 计算每个点到平面的距离
    distances = np.dot(point_cloud - plane_point, plane_normal)
    
    # 根据距离分割点云
    right_plane = point_cloud[distances > 0]  # 在平面上方的点
    left_plane = point_cloud[distances < 0]  # 在平面下方的点
    
    return right_plane, left_plane


def is_symmetric(point_cloud_1, point_cloud_2, plane_point, plane_normal, tolerance):
    # 确保法向量单位化
    plane_normal = plane_normal / np.linalg.norm(plane_normal)

    # 计算镜像点
    mirrored_points = []
    
    for p in point_cloud_1:
        # 计算到平面的距离
        distance = np.dot(plane_normal, p - plane_point)
        # 计算镜像点
        mirrored_point = p - 2 * distance * plane_normal
        mirrored_points.append(mirrored_point)

    mirrored_points = np.array(mirrored_points)
    unmatched_points = []
    # 转换为 numpy 数组并检查对称性
    for i,p in enumerate(mirrored_points):#np.nd
        if not np.any(np.all(np.isclose(point_cloud_2, p, atol=tolerance), axis=1)):
            #这里使用NumPy的isclose函数来比较point_cloud_2（一个点云，假设是一个二维或三维的NumPy数组，其中每一行代表一个点）和单个点p。atol=tolerance指定了绝对容差，即两个值之间的最大绝对差异，若在此容差范围内，则认为它们是“接近”的。np.isclose会返回一个布尔数组，其形状与point_cloud_2相同，每个元素表示对应位置的点是否与p接近。
            #使用np.all沿着第一个轴（axis=1）进行归约操作。只有当一行中的所有元素（即一个点的所有坐标）都与p接近时，结果才是True
            #np.any被用来检查上一步得到的布尔数组中是否有任何True值。如果有任何点p在point_cloud_2中有与之接近的对应点（考虑到容差），np.any的结果就是True，否则是False。
            unmatched_points.append(i)#list(i)[0]#i没有意义，不是顶点索引

    return unmatched_points == [] , unmatched_points

#——————————————————————————————————————————————————————————————————————————————————————————
#转成了np数组以后，就不能再获取顶点索引了，这个列表的索引不是顶点索引，可以在尝试下，把获取的点全部存到np数组里，即使被平面分割2部分，也保留着占位，这样点的序号就还能对应上了
#————————————————————————————————————————————————————————————————————————————————————————————————
def select_unmatched_points(unmatched_points,mesh_name_1,mesh_name_2=None):
    indexes=list(set(unmatched_points))
    selection_list = ['{}.vtx[{}]'.format(mesh_name_1, index) for index in indexes]
    if mesh_name_2:
        selection_list.extend(['{}.vtx[{}]'.format(mesh_name_2, index) for index in indexes])
    cmds.select(selection_list, replace=True)



#轴和平面
plane_point = np.array([0, 0, 0])
plane_normal = np.array([1, 0, 0])#x轴
tolerance=0.01
#选择模型
if len(cmds.ls(sl=1))==2:
    mesh_name_1 = cmds.ls(sl=1)[0]
    mesh_name_2 = cmds.ls(sl=1)[1]
    point_cloud_1 = get_mesh_vertices_as_numpy(mesh_name_1)
    point_cloud_2 = get_mesh_vertices_as_numpy(mesh_name_2)
elif len(cmds.ls(sl=1))==1:
    mesh_name_1 = cmds.ls(sl=1)[0]
    point_cloud_1 = get_mesh_vertices_as_numpy(mesh_name_1)
    point_cloud_1,point_cloud_2=split_point_cloud(point_cloud_1, plane_point, plane_normal)


t1=time.time()

check,unmatched_points=is_symmetric(point_cloud_1, point_cloud_2, plane_point, plane_normal, tolerance)
select_unmatched_points(unmatched_points,mesh_name_1,mesh_name_2)
print(check)

t2=time.time()
print("aarray  Time used:",t2-t1)