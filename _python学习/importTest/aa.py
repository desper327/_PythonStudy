# coding:utf-8

import bb


print(u'我是aa')

def funA():
    bb.funB()
    return 'gg'

g=funA()


import sys

print(sys.path)

# for path in sys.path:
#     #if 'PYTHON' in path:
#     print(path)
