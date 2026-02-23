#print(super(str, 'hello').upper())

class A:
    def __init__(self, x):
        self.x = x

class B(A):
    def __init__(self, x, y):
        super(B,self).__init__(x)
        self.y = y
    @staticmethod
    def static_method():
        #self.y = 3
        print("static method")#无法访问到实例属性
    @classmethod
    def class_method(cls):
        cls.x = 4
        print("class method",cls.x is B.x)#无法访问到实例属性


b = B(1, 2)
print(b.x, b.y)
# Output: 1 2
b.static_method()#实例可以访问静态方法
# Output: static method
B.class_method()#类可以访问类方法
# Output: class method True
b.class_method()#实例可以访问类方法
B.static_method()#类可以访问静态方法


print("==="*50)


# from concurrent.futures import ThreadPoolExecutor
# import time
# from concurrent.futures import ProcessPoolExecutor


# def task(n):
#     time.sleep(1)
#     return n
# def task2(n):
#     time.sleep(2)
#     return n*2
# def task3(n):
#     time.sleep(3)
#     return n*3
# if __name__ == '__main__':
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         # results = executor.map(task, range(10))
#         # for result in results:
#         #     print(result)
#         a=executor.submit(task, 1)
#         b=executor.submit(task2, 2)
#         c=executor.submit(task3, 3)
#         print(type(a),dir(a))
#         print(a.result())
#         print(b.result())
#         print(c.result())

    # with ProcessPoolExecutor(max_workers=2) as executor:
    #     results = executor.map(task, range(10))
    #     for result in results:
    #         print(result)


from collections import defaultdict
a=defaultdict(list)
print(a["b"])  #打印结果[]   如果获取不到就返回默认的


def set_dict(d, keys, value):
    for key in keys[:-1]:
        d.setdefault(key, {})
        print(d)
    d[keys[-1]] = value
    return d


print(set_dict({}, ["path", "to", "key"], "value"))
# Output: {'path': {'to': {'key': 'value'}}}

cc={}
cc.setdefault("a",{}).setdefault("b",{}).setdefault("c",1)
print(cc)


from typing import List,Dict,Tuple,Set,Union,Optional

a: Union[int,float] = 1.0

d :Optional[str] = None#可选类型,可以为None或者指定的类型

a: List[float] = [1.0, 2.0, 3.0]

b: Dict[str,int] = {"a":1,"b":2}

c: Tuple[str,int,float] = ("a",1,2.0)

d: Set[str] = {"a","b"}


print(set(["ff",1]))




from dataclasses import dataclass,asdict,astuple

@dataclass
class student:
    name:str ="wang"
    id:int = 123
    age:int = 90
    address:str = "beijing"

a=student("张三",19111,"20","北京")
print(a.id)
print(asdict(a))
print(astuple(a))
print(student.name)



from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str
    is_active: bool = True  # 默认值

# 类型检查器会捕获这些错误
bad_user: User = {
    "name": "Dave",
    "age": "forty",  # 错误：应该是int
    "emial": "dave@example.com"  # 错误：拼写错误
}  



import csv
def read_csv():
    with open(r"C:\Users\Desper\Desktop\文职.csv", 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row

# for row in read_csv():
#     pass#print(row)

def func2():
    with open(r"C:\Users\Desper\Desktop\文职.csv", 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pass#print(row)

#func2()



def func3():
    print(3)
    return 3
print(type(eval("1+2.1")))
print(type(eval("{1:2}")))
#print(type(eval("func3()")))


def func4():
    print(4)
    print(type(eval("func3()")))
    return 44
print(type(eval("func4()")))


s="{1:1,2:2,\
3:3}"

s2="""
for i in range(3):
    print(f'Count: {i}')
"""
# eval(s2)



def flatten_dict(d, items={}):

    if isinstance(d, dict):
        for k, v in d.items():
            if not isinstance(v, dict):
                items[k]=v
            else:
                flatten_dict(v, items)
    elif isinstance(d, list):
        for v in enumerate(d):
            if isinstance(v, dict):
                for k, v in v.items():
                    if not isinstance(v, dict):
                        items[k]=v
                    else:
                        flatten_dict(v, items)
    return items

dict1 = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}
print(flatten_dict(dict1))#{'c': 1, 'd': 2, 'e': 3, 'f': 4}