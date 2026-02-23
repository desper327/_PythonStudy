import maya.cmds as cmds
import maya.OpenMaya as om
import numpy as np

# def get_matrix_from_transform(obj_name):
#     """获取指定物体的变换矩阵"""
#     matrix_list = cmds.xform(obj_name, query=True, matrix=True, worldSpace=True)
#     matrix = np.array(matrix_list).reshape(4, 4)
#     return matrix

def get_vertex_positions(obj_name):
    """获取模型的所有顶点位置"""
    selection = om.MSelectionList()
    selection.add(obj_name)
    dag_path = om.MDagPath()
    selection.getDagPath(0, dag_path)
    mesh_fn = om.MFnMesh(dag_path)
    points = om.MPointArray()
    mesh_fn.getPoints(points, om.MSpace.kWorld)
    vertices_pos = np.array([[points[i].x, points[i].y, points[i].z, 1] for i in range(points.length())])
    return vertices_pos

# def apply_mixed_transform(vertices, ctrl1_matrix, ctrl2_matrix, weights):
#     """对每个顶点应用混合的变换矩阵"""
#     transformed_vertices = []
#     for i, vertex in enumerate(vertices):
#         mixed_matrix = ctrl1_matrix * weights[i] + ctrl2_matrix * (1 - weights[i])
#         transformed_vertex = np.dot(mixed_matrix, vertex)
#         transformed_vertices.append(transformed_vertex)
#     return np.array(transformed_vertices)

# def set_vertex_positions(obj_name, transformed_vertices):
#     """设置模型顶点位置"""
#     selection = om.MSelectionList()
#     selection.add(obj_name)
#     dag_path = om.MDagPath()
#     selection.getDagPath(0, dag_path)
#     mesh_fn = om.MFnMesh(dag_path)
#     points = om.MPointArray()
#     for vertex in transformed_vertices:
#         point = om.MPoint(vertex[0], vertex[1], vertex[2])
#         points.append(point)
#     mesh_fn.setPoints(points, om.MSpace.kWorld)

def create_mixed_transform(mesh_name,ctrl1_name,ctrl2_name):
    # 获取控制器的世界矩阵
    #ctrl1_matrix = get_matrix_from_transform(ctrl1_name)
    #ctrl2_matrix = get_matrix_from_transform(ctrl2_name)

    # 获取模型的顶点位置
    vertices_pos = get_vertex_positions(mesh_name)

    # 计算每个顶点到控制器的距离
    ctrl1_pos = np.array(cmds.xform(ctrl1_name, query=True, translation=True, worldSpace=True))
    ctrl2_pos = np.array(cmds.xform(ctrl2_name, query=True, translation=True, worldSpace=True))
    weights1 = []
    #weights2 = []
    for vertex in vertices_pos:
        point_pos = vertex[:3]
        dist1 = np.linalg.norm(point_pos - ctrl1_pos)
        dist2 = np.linalg.norm(point_pos - ctrl2_pos)
        total_dist = dist1 + dist2
        weight1 =  np.cbrt(dist1 / total_dist)#这里修改一下，这个函数还不太清楚怎么使用，这个权重值决定了最后的效果
        #weight2 =  np.cbrt(dist2 / total_dist)
        weights1.append(weight1)
        #weights2.append(weight2)
    #weights = np.array(weights)


    cluster_handle, cluster_node=cmds.cluster(mesh_name,n=ctrl1_name+'_cluster')
    #cmds.cluster(vertices,n='cluster2')

    for i in range(len(vertices_pos)):
        cmds.percent(cluster_handle,mesh_name+'.vtx['+str(i)+']',value=weights1[i])
        #cmds.percent(ctrl2_name,i,value=weights2[i])

    # 对顶点应用混合变换
    #transformed_vertices = apply_mixed_transform(vertices, ctrl1_matrix, ctrl2_matrix, weights)

    # 更新模型顶点位置
    #set_vertex_positions(obj_name, transformed_vertices)
    print("已完成")



# 假设已经有模型和两个控制器
obj_name = "pCube1"  # 模型名称
ctrl1_name = "ctrl1"  # 左侧控制器名称
ctrl2_name = "ctrl2"  # 右侧控制器名称
create_mixed_transform(obj_name,ctrl1_name,ctrl2_name)



# #可以实时更新的，利用节点，这个不好，因为一个节点只存一个点，不如用簇，可以存大量的点和权重值
# import maya.cmds as cmds

# mesh,ctrl1,ctrl2=cmds.ls(selection=True)

# def create_mixed_transform(mesh,ctrl1,ctrl2):
#     vertices = cmds.polyEvaluate(mesh, vertex=True)
#     for i in vertices:
#         cmds.createNode('multiplyPointByMatrix',name='multiplyPointByMatrix'+str(i))