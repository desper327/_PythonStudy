# import subprocess
# a=subprocess.call("NotePad.exe")
# print(a)

import threading
import subprocess
import time
from Y_utils import *


#@time_it
def cul1():
    num = 0
    for i in range(500):
        num += i
        time.sleep(0.01)
    print("第一个函数")

#@time_it
def cul2():
    num = 0
    for i in range(100000000):
        num += i
    print("第二个函数")



def run_1():
    start_time=time.time()
    t1=threading.Thread(target=cul1, daemon=True)
    t2=threading.Thread(target=cul2)
    t1.start()
    t2.start()
    #t2.join()#加入主线程，等待t2线程结束
    print(time.time()-start_time)


    start_time=time.time()
    cul1()
    cul2()
    print(time.time()-start_time)
    """运行结果：
    0.01738572120666504
    第二个函数
    第一个函数
    第一个函数
    第二个函数
    9.271392583847046"""



def run_2():
    start_time=time.time()
    t1=threading.Thread(target=cul1, daemon=True)#或者使用t1.daemon=True
    t2=threading.Thread(target=cul2)
    t1.start()
    t2.start()
    t2.join()#加入主线程，等待t2线程结束
    print(time.time()-start_time)#等待t2线程结束才


    start_time=time.time()
    cul1()
    cul2()
    print(time.time()-start_time)
    """运行结果：
    2.7601561546325684
    第一个函数
    第一个函数
    第二个函数
    7.944104909896851"""






from concurrent.futures import ThreadPoolExecutor
import requests

def fetch(url):
    try:
        return requests.get(url, timeout=3).text[:50]
    except Exception as e:
        return f"Error: {e}"



def run_3():
    with ThreadPoolExecutor(max_workers=5) as executor:  # 最多5个并发
        results = executor.map(fetch, ["https://www.baidu.com/"]*110)
        for res in results:
            print(res)




 
def task(n):
    time.sleep(1)
    return f"Task {n} completed"
 
def run_4():
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务
        futures = [executor.submit(task, i) for i in range(5)]
        
        # 获取结果
        for future in futures:
            print(future.result())
 
# 输出：
# Task 0 completed
# Task 1 completed
# Task 2 completed
# Task 3 completed
# Task 4 completed



#线程之间通信
import queue

def producer(q):
    for i in range(10):
        q.put(i)
        print(f"生产者生产了{i}")
        time.sleep(1)
 
def consumer(q):
    while True:
        if not q.empty():
            item = q.get()
            print(f"消费者消费了{item}")
        else:
            print("队列为空，等待生产者生产")
            time.sleep(1)
 
def run_5():
    q = queue.Queue()
    t1 = threading.Thread(target=producer, args=(q,))
    t2 = threading.Thread(target=consumer, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()




import csv
found=False
def read_csv(call):
    global found
    with open(r"C:\Users\Desper\Desktop\文职.csv", 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #yield row
            if "电磁信息安全检测" in row:
                print(row)
                found=True
                call()
                #break

def callback():
    # while not found:
    #     print("等待中")
    time.sleep(1)
    print("找到了")
    
def run_6():
    global found
    t1=threading.Thread(target=read_csv,args=(callback,))
    t1.daemon=True
    t1.start()
    #t1.join()
    time.sleep(10)










if __name__ == '__main__':
    # run_1()
    # run_2()
    # run_3()
    # run_4()
    # run_5()
    run_6()