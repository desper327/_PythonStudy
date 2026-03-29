import getpass,os,sys,importlib
try:
    sys.path.append(os.getenv("forza",""))
    forza_utils = importlib.import_module("forza_utils")
    Yprint=forza_utils.Yprint 
except:
    Yprint=print 

"""
def my_print(name: str) -> None:
    print("Hello, " + name + "!")

my_print("Alice")


import PySide2.QtWidgets as QtWidgets
from PySide2.QtCore import Qt,Signal,Slot

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ad_signal = Signal(str)


w=MyWidget()
w.ad_signal.connect(my_print)
"""


import getpass,os,sys
print(getpass.getuser())
print(os.environ.get('USERNAME'))
print(os.environ.get("ArtSVN"))
# print(sys.modules.keys())
# print(os.path.normpath(__file__))

# a=(1,3)
# b=4
# print(list(*a),list(*b))


# d = {'spam': 1, 'eggs': 2, 'cheese': 3}
# e = {'cheese': 'cheddar', 'aardvark': 'Ethel'}
# #d.update(e)
# print(d|e)
# d|=e
# print(d)


preset_name="555ddd"  #  "56-df*d_rr"
print(preset_name.isalnum())
print("".join([c for c in preset_name if c.isalnum() or c in "_- "]))

print(os.path.expanduser("~"))



error_msg=[]
file_name="你好hhh.txt"
error_msg.extend(
    "ds" for char in file_name if '\u4e00' <= char <= '\u9fff' 
)
print(error_msg)


call_line='Tprint("hahaha")'
b=call_line.split('Tprint')[1].strip()[1:].strip()[:-1]
print(b)

print("-\n"*10)


_a={
    "active": True,
    "title": "武器_初阶",
    "skeleton_parent1_file": "",
    "skeleton_parent2_file": "",
    "order": 2
}

if _a["skeleton_parent1_file"]:
    print("aaa")

print(not _a["skeleton_parent1_file"])

aa={"a":1,"b":2,"c":3}
bb={"b":5,"c":3,"d":4}
print(aa.items() & bb.items())



path="Users//ArtSVN\\Desktop"
print(os.path.normpath(path))


import sys
sys.path.append(r"D:\code_dev\TitanTAUtils\max_packages\python\public_mode_utils")
from print_public_mode import Tprint
Tprint({})



# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Dict, List, Optional
import re


def parse_anim_filename(filename: str) -> Dict:
    """
    解析动画文件名
    
    文件名格式：
    
    【单武器格式】
    - {4位角色ID}_{动作名}.max                        → 导出 100 和 101
    - {4位角色ID}_{动作名}_{假位}.max                 → 导出 100 和 101  (假位: 1位数字)
    - {4位角色ID}_{动作名}_{等级}_{假位}.max          → 导出 100        (等级: 任意位, 假位: 1位)
    - {4位角色ID}_{动作名}_{等级}_{皮肤}_{假位}.max   → 导出 101        (等级: 任意位, 皮肤: 1位, 假位: 1位)
    
    【双武器格式】
    - [c]{4位角色ID}_{4位角色ID}_{动作名}.max
    - [c]{4位角色ID}_{4位角色ID}_{动作名}_{假位}.max
    - [c]{4位角色ID}_{4位角色ID}_{动作名}_{等级}_{假位}.max
    - [c]{4位角色ID}_{4位角色ID}_{动作名}_{等级}_{皮肤}_{假位}.max
    
    双武器说明：
    - 可以以 'c' 或 'C' 开头（可选）
    - 第一个4位数字是角色ID
    - 第二个4位数字是引用角色ID
    - 其他规则与单武器相同
    
    规则：
    - 角色ID：必须是4位数字
    - 引用角色ID：必须是4位数字（仅双武器）
    - 假位：必须是1位数字
    - 皮肤：必须是1位数字
    - 等级：可以是任意位数字
    
    Args:
        filename: 文件名（可以带路径）
        
    Returns:
        {
            'success': bool,                # 是否解析成功
            'errors': List[str],            # 错误信息列表（如果有）
            'is_dual_weapon': bool,         # 是否为双武器
            'has_c_prefix': bool,           # 是否有C前缀（仅双武器有效）
            'character_id': str,            # 角色ID（4位数字）
            'ref_character_id': Optional[str],  # 引用角色ID（仅双武器，4位数字）
            'action_name': str,             # 动作名
            'level': Optional[int],         # 等级（如果有）
            'skin': Optional[int],          # 皮肤（如果有，1位数字）
            'fake_pos': Optional[int],      # 假位（如果有，1位数字）
            'export_types': List[int],      # 要导出的类型 [100] 或 [101] 或 [100, 101]
            'original_name': str,           # 原始文件名
            'full_path': str,               # 完整路径
        }
    
    Examples:
        >>> # 单武器
        >>> result = parse_anim_filename("0001_Throne.max")
        >>> result['is_dual_weapon']
        False
        
        >>> # 双武器（带C前缀）
        >>> result = parse_anim_filename("c0001_0002_attack_22_3_1.max")
        >>> result['is_dual_weapon']
        True
        >>> result['has_c_prefix']
        True
        >>> result['character_id']
        '0001'
        >>> result['ref_character_id']
        '0002'
        
        >>> # 双武器（不带C前缀）
        >>> result = parse_anim_filename("0001_0002_attack.max")
        >>> result['is_dual_weapon']
        True
        >>> result['has_c_prefix']
        False
    """
    # 初始化返回值
    result = {
        'success': False,
        'errors': [],
        'is_dual_weapon': False,
        'has_c_prefix': False,
        'character_id': None,
        'ref_character_id': None,
        'action_name': None,
        'level': None,
        'skin': None,
        'fake_pos': None,
        'export_types': [],
        'original_name': '',
        'full_path': str(Path(filename)),
    }
    
    # 提取文件名（去除路径和扩展名）
    path = Path(filename)
    name_without_ext = path.stem
    result['original_name'] = name_without_ext
    
    # 检查是否有C前缀
    has_c_prefix = False
    working_name = name_without_ext
    
    if working_name.lower().startswith('c'):
        # 检查c后面是否紧跟4位数字
        if len(working_name) > 5 and working_name[1:5].isdigit() and len(working_name[1:5]) == 4:
            has_c_prefix = True
            result['has_c_prefix'] = True
            working_name = working_name[1:]  # 去掉C前缀
    
    # 分割各部分
    parts = working_name.split('_')
    
    # 验证基本格式
    if len(parts) < 2:
        result['errors'].append(f"文件名格式错误，至少需要2个部分，当前只有 {len(parts)} 个部分")
        return result
    
    # 判断是否为双武器（第一个和第二个部分都是恰好4位数字）
    is_dual_weapon = False
    character_id = parts[0]
    ref_character_id = None
    action_name_index = 1  # 动作名的索引位置
    
    # 验证第一个角色ID（必须恰好是4位数字）
    if not re.match(r'^\d{4}$', character_id):
        result['errors'].append(f"角色ID必须是4位数字，当前: {character_id} (长度: {len(character_id)})")
    else:
        result['character_id'] = character_id
    
    # 检查是否为双武器格式（第二部分必须恰好是4位数字）
    if len(parts) >= 3:
        potential_ref_id = parts[1]
        # 必须恰好是4位数字（长度为4且全是数字）
        if len(potential_ref_id) == 4 and potential_ref_id.isdigit():
            # 确认是双武器
            is_dual_weapon = True
            result['is_dual_weapon'] = True
            ref_character_id = potential_ref_id
            result['ref_character_id'] = ref_character_id
            action_name_index = 2  # 动作名在第3个位置
            
            # 验证引用角色ID格式
            if not re.match(r'^\d{4}$', ref_character_id):
                result['errors'].append(f"引用角色ID必须是4位数字，当前: {ref_character_id} (长度: {len(ref_character_id)})")
        else:
            # 第二部分不是恰好4位数字，判定为单武器
            # 如果是数字但不是4位，记录为错误
            if potential_ref_id.isdigit() and len(potential_ref_id) != 4:
                # 这可能是用户想写双武器但格式错误
                result['errors'].append(f"第二部分是数字但不是4位({len(potential_ref_id)}位): {potential_ref_id}，无法判定为双武器")
    
    # 验证至少有动作名
    if action_name_index >= len(parts):
        result['errors'].append(f"缺少动作名")
        return result
    
    # 提取动作名
    action_name = parts[action_name_index]
    
    # 提取参数部分（动作名之后的所有数字）
    params = []
    for i in range(action_name_index + 1, len(parts)):
        part = parts[i]
        if part.isdigit():
            params.append(part)  # 先保存为字符串，后面验证位数
        else:
            # 如果遇到非数字，可能是动作名的延续
            action_name += '_' + part
    
    result['action_name'] = action_name
    
    # 根据参数数量解析
    param_count = len(params)
    
    if param_count == 0:
        # 无参数：导出 100 和 101
        result['export_types'] = [100, 101]
        
    elif param_count == 1:
        # 1个参数：假位，导出 100 和 101
        # 验证假位必须是1位数字
        if len(params[0]) != 1:
            result['errors'].append(f"假位必须是1位数字，当前: {params[0]} (长度: {len(params[0])})")
        else:
            result['fake_pos'] = int(params[0])
        result['export_types'] = [100, 101]
        
    elif param_count == 2:
        # 2个参数：等级 + 假位，导出 100
        # 等级可以是任意位数
        result['level'] = int(params[0])
        
        # 验证假位必须是1位数字
        if len(params[1]) != 1:
            result['errors'].append(f"假位必须是1位数字，当前: {params[1]} (长度: {len(params[1])})")
        else:
            result['fake_pos'] = int(params[1])
        
        result['export_types'] = [100]
        
    elif param_count == 3:
        # 3个参数：等级 + 皮肤 + 假位，导出 101
        # 等级可以是任意位数
        result['level'] = int(params[0])
        
        # 验证皮肤必须是1位数字
        if len(params[1]) != 1:
            result['errors'].append(f"皮肤必须是1位数字，当前: {params[1]} (长度: {len(params[1])})")
        else:
            result['skin'] = int(params[1])
        
        # 验证假位必须是1位数字
        if len(params[2]) != 1:
            result['errors'].append(f"假位必须是1位数字，当前: {params[2]} (长度: {len(params[2])})")
        else:
            result['fake_pos'] = int(params[2])
        
        result['export_types'] = [101]
        
    else:
        # 超过3个参数
        result['errors'].append(f"参数过多，最多3个参数（等级_皮肤_假位），当前有 {param_count} 个参数")
    
    # 判断是否成功
    result['success'] = len(result['errors']) == 0
    
    return result


if __name__ == "__main__":
    test_files = [
        ("单武器-无参数", "0001_Throne.max"),
        ("单武器-假位", "0001_piano_4.max"),
        ("单武器-等级假位", "0001_ridesit5_4.max"),
        ("单武器-等级假位2", "0001_ridestand24.max"),
        ("单武器-等级皮肤假位", "0001_piano_22_3_1.max"),
        
        ("双武器C-无参数", "c0001_0002_attack.max"),
        ("双武器C-假位", "c0001_0002_attack_5.max"),
        ("双武器C-等级假位", "c0001_0002_attack_25_3.max"),
        ("双武器C-等级皮肤假位", "c0001_0002_attack_22_3_1.max"),
        ("双武器C大写", "C0001_0002_walk.max"),
        
        ("双武器-无参数", "0001_0002_defend.max"),
        ("双武器-假位", "0001_0002_defend_7.max"),
        ("双武器-等级假位", "0001_0002_defend_30_2.max"),
        ("双武器-等级皮肤假位", "0001_0002_defend_15_2_4.max"),
        
        ("错误-角色ID不是4位", "1_Throne.max"),
        ("错误-角色ID5位", "00001_Throne.max"),
        ("错误-假位2位", "0001_piano_44.max"),
        ("错误-皮肤2位", "0001_piano_22_33_1.max"),
        ("错误-假位2位", "0001_piano_22_3_11.max"),
        ("错误-缺少动作名", "0001.max"),
        ("错误-参数过多", "0001_piano_1_2_3_4.max"),
        ("错误-双武器引用ID 3位", "c0001_002_attack.max"),
        ("错误-双武器引用ID 5位", "c0001_00002_attack.max"),
        ("错误-双武器引用ID 2位", "0001_02_attack.max"),
        ("正确-双武器引用ID 2位","c0001_0002_ridestand10_start_22_3_1.max"),
    ]
    
    print("=" * 120)
    print("动画文件名解析测试（支持单武器和双武器）")
    print("=" * 120)
    
    for desc, filename in test_files:
        print(f"\n【{desc}】 📁 {filename}")
        print("-" * 120)
        
        result = parse_anim_filename(filename)
        
        if result['success']:
            print(f"  ✅ 解析成功")
            print(f"     武器类型:     {'双武器' if result['is_dual_weapon'] else '单武器'}")
            
            if result['is_dual_weapon']:
                print(f"     C前缀:        {'是' if result['has_c_prefix'] else '否'}")
                print(f"     角色ID:       {result['character_id']}")
                print(f"     引用角色ID:   {result['ref_character_id']}")
            else:
                print(f"     角色ID:       {result['character_id']}")
            
            print(f"     动作名:       {result['action_name']}")
            
            if result['level'] is not None:
                print(f"     等级:         {result['level']}")
            if result['skin'] is not None:
                print(f"     皮肤:         {result['skin']} (1位)")
            if result['fake_pos'] is not None:
                print(f"     假位:         {result['fake_pos']} (1位)")
            
            print(f"     导出类型:     {result['export_types']}")
        else:
            print(f"  ❌ 解析失败")
            print(f"     错误信息:")
            for i, error in enumerate(result['errors'], 1):
                print(f"       {i}. {error}")
            
            # 显示部分解析成功的字段
            if result['is_dual_weapon']:
                print(f"     武器类型:     双武器 ✓")
                if result['has_c_prefix']:
                    print(f"     C前缀:        是 ✓")
            else:
                if result['action_name'] and '_' in result['action_name']:
                    print(f"     武器类型:     单武器（第二部分不是4位数字，作为动作名）")
            
            if result['character_id']:
                print(f"     角色ID:       {result['character_id']} ✓")
            if result['ref_character_id']:
                print(f"     引用角色ID:   {result['ref_character_id']} ✓")
            if result['action_name']:
                print(f"     动作名:       {result['action_name']} ✓")
    
    print("\n" + "=" * 120)
    print("统计信息")
    print("=" * 120)
    
    success_count = sum(1 for _, f in test_files if parse_anim_filename(f)['success'])
    total_count = len(test_files)
    single_weapon_count = sum(1 for _, f in test_files if not parse_anim_filename(f)['is_dual_weapon'] and parse_anim_filename(f)['success'])
    dual_weapon_count = sum(1 for _, f in test_files if parse_anim_filename(f)['is_dual_weapon'] and parse_anim_filename(f)['success'])
    
    print(f"总文件数:     {total_count}")
    print(f"成功数:       {success_count}")
    print(f"  - 单武器:   {single_weapon_count}")
    print(f"  - 双武器:   {dual_weapon_count}")
    print(f"失败数:       {total_count - success_count}")
    print(f"成功率:       {success_count / total_count * 100:.1f}%")