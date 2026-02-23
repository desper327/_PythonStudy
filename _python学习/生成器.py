#yield
#yield是生成器，生成器是一个特殊的迭代器，迭代器是可迭代对象的一种
#生成器函数，生成器函数返回的是一个生成器对象，生成器对象是迭代器的一种
#生成器函数使用yield关键字，每次调用yield会暂停函数的执行，并返回yield后面的值，下次调用生成器函数会从上次暂停的地方继续执行
#生成器函数中可以包含多个yield关键字，每次调用生成器函数都会返回一个值，直到最后一个yield
#生成器函数中可以包含return关键字，但只能返回一次，如果生成器函数中包含return关键字，则生成器函数会抛出StopIteration异常
#生成器函数中可以包含yield from关键字，yield from后面跟的是一个可迭代对象，生成器函数会依次返回可迭代对象的值
#生成器函数中可以包含yield from关键字，但只能使用一次，如果生成器函数中包含多个yield from关键字，则抛出SyntaxError异常
'''
def readFile(file):
    file = open(file, 'r', encoding='utf-8')
    while True:
        line = file.readline()
        if line == '':
            break
        yield line

file=r'f:\Study\BaiduSyncdisk\MyStudy\python高级特性.py'
for i,line in enumerate(readFile(file)):
    print(i,line)
'''



'''
#主程序中间使用以下方法，可以间隔一段时间执行函数，并且不阻塞主程序，不同于sleep，sleep会阻塞主程序
import threading
stop_event = threading.Event()

def repeat_function():
    while not stop_event.is_set():
        print("Function executed#####################################")
        stop_event.wait(0.1)  # 每隔0.1秒执行一次

# Start the timer in a separate thread
timer_thread = threading.Thread(target=repeat_function)
timer_thread.start()

# 模拟主程序
i = 0
while i < 50000:
    print('hhhhhhhhhhhhhhhhhhhhhhhhhhhuh')
    i += 1

# Stop the timers by setting the event
stop_event.set()

# Wait for the timer thread to finish
#timer_thread.join()
'''
#不去修改类，而是给类的实例动态增加方法
import types
class A:
    def __init__(self):
        pass
    def bb(self):
        print('bb')

def c(fun):
    def d():
        print('CC')
        fun()
    return d

a=A()
def e():
    print('ee')

a.cc=e()
c(a.cc)()


a.cc()

setattr(a, 'cc', e)