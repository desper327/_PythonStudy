import os
import pathlib
import sys
import time
import tomllib
from tqdm import tqdm

import numpy as np

path=pathlib.Path(os.getenv('USERPROFILE',""),'.forza')
with open(path/'forza_config.toml', 'rb') as f:
    config = tomllib.load(f)

print(config['path_vars']["forza_lib_utils"])
sys.path.append(config['path_vars']["forza_lib_utils"])

from forza_utils import time_it,Yprint








# a=[[1,22],[55,66]]
# a=np.array(a)
# b=a.tolist()
# print(a)
# print(a.shape)
# print(b)
# c=np.random.randint(0,100,size=(3,3))
# print(c.flatten().tolist())

#np数组的遍历速度比较
# aarray=np.random.randint(0,100,size=(100000000))#00000
# barray=np.random.randint(0,100,size=(100000000))#00000
# alist=aarray.flatten().tolist()
# print(type(alist))
# blist=[i for i in range(10000000)]
# a=0
# t1=time.time()
# print(aarray)
# for i,k in enumerate(aarray.flatten()):#展开和转成列表再遍历，都不快
#     a+=i
#     #print(i)
# t2=time.time()
# print(a)
# print("aarray  Time used:",t2-t1)

# a=0.0
# t1=time.time()
# for i,k in enumerate(alist):
#     a+=i
# t2=time.time()
# print(a)
# print("list  Time used:",t2-t1)



#转维度后的计算
# aarray=np.random.randint(0,100,size=(100))
# barray=np.random.randint(0,100,size=(100))
# t1=time.time()
# aarray=aarray.reshape(100,1,1)#使用这个reshape以后，要赋值aarray才能改变aarray的值
# barray=barray.reshape(1,100,1)
# aarray=aarray+barray
# t2=time.time()
# print("aarray+barray Time used:",t2-t1)
# print(aarray)
# print(aarray.shape)



#求每个点之间的距离
# point_num=10000
# a=np.random.rand(point_num,3)
# b=np.random.rand(point_num,3)
# a=a.reshape(point_num,1,3)
# b=b.reshape(1,point_num,3)
# c=a-b
# c=np.linalg.norm(c,axis=2)#沿着最后一个轴计算，即计算每个向量的长度
# min_index=c.argmin(axis=1)#返回每行最小值的索引就是距离最近的点的索引

# print(c)
# print(min_index)
# print(c.shape)

"""
a=[[1,1,1],\
   [1,1,0.9]]

b=[[1,0.95,0.96],\
   [1,0.96,0.97]]

for i,p in enumerate(np.array(a)):
    k=np.isclose(np.array(b), p, atol=0.04)#计算 b 中的每个元素与 p 是否在绝对容差 atol=0.04 范围内接近
    print('k',k)
    U=np.all(np.isclose(np.array(b), p, atol=0.04), axis=1)#同样计算 b 中的每个元素与 p 是否接近，得到一个布尔数组。np.all(..., axis=1) 对这个布尔数组的每一行进行 all 操作，即判断每一行中的所有元素是否都接近 p
    print('U',U)
    if not np.any(np.all(np.isclose(np.array(b), p, atol=0.04), axis=1)):
        print("i",i)
        print("p",p)
"""


#模拟三维模型的对称性检查

# 模拟一个三维点云模型
# 这里假设模型是一个NumPy数组，形状为 (N, 3)，其中N是点的数量
# model = np.array([
#     [1.0, 2.0, 3.0],
#     [-1.0, 2.0, 3.0],
#     [2.0, 3.0, 4.0],
#     [-2.0, 3.0, 4.0],
#     [0.0, 1.0, 2.0]
# ])
model=(np.random.rand(60000,3)-0.5)*10
print(model)

@time_it
def check_symmetry(model, atol=0.01):
    # 将模型根据x轴分成两部分,再按照y轴分成两部分，假设Z轴向上
    # 左半部分的点为model[model[:, 0] < 0 and model[:, 1] < 0]

    left_part_a = model[(model[:, 0] < 0) & (model[:, 1] < 0)]
    left_part_b = model[(model[:, 0] < 0) & (model[:, 1] > 0)]
    Yprint(left_part_a.shape)
    Yprint(left_part_b.shape)
    right_part_a = model[(model[:, 0] > 0) & (model[:, 1] < 0)]
    right_part_b = model[(model[:, 0] > 0) & (model[:, 1] > 0)]
    Yprint(right_part_a.shape)
    Yprint(right_part_b.shape)
    

    def check_symmetry_part(part_a, part_b, atol):
        # 对于part_a中的每个点，在part_b中寻找对应的对称点
        symmetric = []
        for point in tqdm(part_a):
            # 创建一个对称点，x坐标取反
            mirrored_point = np.array([-point[0], point[1], point[2]])
            
            # 检查part_b是否存在对应的对称点
            is_close = np.isclose(part_b, mirrored_point, atol=atol).all(axis=1)
            #print(is_close)
            if is_close.any():
                symmetric.append(True)
            else:
                symmetric.append(False)
        
        # 如果所有part_a中的点都有对应的对称点，则part_a是对称的
        return all(symmetric)

    # 检查左半部分的对称性
    is_left_symmetric = check_symmetry_part(left_part_a, left_part_b, atol)
    Yprint(is_left_symmetric)
    # 检查右半部分的对称性
    is_right_symmetric = check_symmetry_part(right_part_a, right_part_b, atol)
    Yprint(is_right_symmetric)

    # 如果左右两部分都对称，则模型是对称的
    return is_left_symmetric and is_right_symmetric



# 检查模型是否在x轴上左右对称
is_symmetric = check_symmetry(model, atol=0.01)
if is_symmetric:
    print("模型在x轴上左右对称")
else:
    print("模型在x轴上不对称")

