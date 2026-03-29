from tree_sitter import Language, Parser
import re

# 加载 Lua 语言
LUA_LANGUAGE = Language('./tree-sitter-lua.wasm', 'lua')
parser = Parser()
parser.set_language(LUA_LANGUAGE)

def find_value_node(tree, target_path):
    """
    根据路径查找值节点，例如：
    target_path = ['datas.info3dnpc.Fashioned3dNpcAnim', 4, 'attack']
    """
    root = tree.root_node
    
    def walk(node, path):
        if not path:
            return node
        
        key = path[0]
        rest = path[1:]
        
        # 当前层是 table 构造器 { ... }
        if node.type == 'table_constructor':
            for field in node.children:
                if field.type == 'field':
                    # 解析 field 的 key
                    key_node = field.child_by_field_name('key')
                    value_node = field.child_by_field_name('value')
                    
                    if key_node and value_node:
                        # 处理 ["key"] 形式的 key
                        if key_node.type == 'bracket_index_expression':
                            inner = key_node.child_by_field_name('child')
                            if inner and inner.type == 'string':
                                # 提取字符串内容（去掉引号）
                                key_str = inner.text.decode('utf8')[1:-1]
                                if str(key) == key_str:
                                    return walk(value_node, rest)
                            elif inner and inner.type == 'number':
                                key_num = int(inner.text.decode('utf8'))
                                if key == key_num:
                                    return walk(value_node, rest)
        elif node.type == 'number' or node.type == 'true' or node.type == 'false':
            # 到达叶子值
            if not rest:
                return node
        return None
    
    # 从最外层 return {...} 开始
    if root.type == 'chunk':
        for child in root.children:
            if child.type == 'return_statement':
                table_node = child.child_by_field_name('argument')
                if table_node and table_node.type == 'table_constructor':
                    return walk(table_node, target_path)
    return None

def patch_lua_file(file_path, target_path, new_value):
    """
    修改 Lua 文件中的指定值
    :param file_path: Lua 文件路径
    :param target_path: 路径列表，如 ['datas.info3dnpc.Fashioned3dNpcAnim', 4, 'attack']
    :param new_value: 新值（int/bool/string）
    """
    # 读取原始文件（必须用 bytes）
    with open(file_path, 'rb') as f:
        source_code = f.read()
    
    # 解析 AST
    tree = parser.parse(source_code)
    
    # 查找目标节点
    value_node = find_value_node(tree, target_path)
    if not value_node:
        raise ValueError(f"未找到路径: {target_path}")
    
    # 将新值转为 Lua 字面量
    if isinstance(new_value, bool):
        new_str = 'true' if new_value else 'false'
    elif isinstance(new_value, str):
        new_str = f'"{new_value}"'
    else:  # int/float
        new_str = str(new_value)
    
    # 获取原值在源码中的位置（字节偏移）
    start = value_node.start_byte
    end = value_node.end_byte
    
    # 原地替换
    patched_code = source_code[:start] + new_str.encode('utf8') + source_code[end:]
    
    # 写回文件
    with open(file_path, 'wb') as f:
        f.write(patched_code)




file = r"D:\param_2024.lua"
# 示例：将 Fashioned3dNpcAnim[4]["attack"] 改为 15
patch_lua_file(
    file,
    ['datas.info3dnpc.Fashioned3dNpcAnim', 4, 'attack'],
    15
)

# 示例：将 SEPARATE_BODY_FASHION[5] 改为 false
patch_lua_file(
    file,
    ['datas.info3dnpc.SEPARATE_BODY_FASHION', 5],
    False
)