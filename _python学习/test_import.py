import test_import_package.package2.module3 as module3
print(module3)
print(type(module3))

from test_import_package.package2 import module2
print(module2)
print(type(module2))
print(module2.module1.__file__)
print(module2.os.__file__)



#from .test_Enum import Color    入口文件中不能使用相对导入，会报错
"""报错 ImportError: attempted relative import with no known parent package，没有找到父包，无法导入。"""