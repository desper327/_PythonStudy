import maya.cmds as cmds
import maya.OpenMaya as om

def get_soft_selection_vertices_and_weights():
    # 创建一个空的 MSelectionList，用于获取软选择
    selection_list = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection_list)

    # 获取 MRichSelection 来获取软选择的权重数据
    rich_selection = om.MRichSelection()
    om.MGlobal.getRichSelection(rich_selection)
    
    soft_selection = om.MSelectionList()
    rich_selection.getSelection(soft_selection)
    
    dag_path = om.MDagPath()
    component = om.MObject()

    vertices = []
    weights = []
    
    # 遍历选择的组件，获取软选择权重
    iter = om.MItSelectionList(soft_selection, om.MFn.kMeshVertComponent)
    while not iter.isDone():
        iter.getDagPath(dag_path, component)
        fn_comp = om.MFnSingleIndexedComponent(component)
        
        # 获取顶点索引和权重
        for i in range(fn_comp.elementCount()):
            vertex_index = fn_comp.element(i)
            weight = fn_comp.weight(i).influence()  # 权重值
            
            vertices.append(f"{dag_path.fullPathName()}.vtx[{vertex_index}]")
            weights.append(weight)
        
        iter.next()
    
    return vertices, weights


def create_cluster_from_soft_selection():
    # 获取软选择的顶点和权重
    vertices, weights = get_soft_selection_vertices_and_weights()
    
    if not vertices:
        cmds.warning("没有找到软选择的顶点，请启用软选择并选择顶点")
        return

    # 创建簇变形器
    cluster_handle, cluster_node = cmds.cluster(vertices)#注意此处要加进去顶点，这些顶点要在簇里才能设置权重
    
    # 为簇应用权重
    for vertex, weight in zip(vertices, weights):
        print(vertex, weight)
        cmds.percent(cluster_handle, vertex, value=weight)

    print("簇已创建，并应用了软选择权重")


# 运行函数
create_cluster_from_soft_selection()