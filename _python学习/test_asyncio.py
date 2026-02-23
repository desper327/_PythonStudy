import asyncio
import time

async def say_hello():
    print("Hello")
    await asyncio.sleep(1.5)
    print("World1")
    return "Hello World"

async def say_goodbye():
    print("Goodbye")
    await asyncio.sleep(1)
    print("World2")
    return "Goodbye World"


async def main():
    tasks = [asyncio.create_task(say_hello()), asyncio.create_task(say_goodbye())]
    results = await asyncio.gather(*tasks)# asyncio.gather 会确保最终返回的 results 列表中的结果顺序与你创建 tasks 时的顺序完全一致
    print(results)


async def main2():
    # 顺序执行：但是实际是阻塞了
    result_a = await say_hello()
    result_b = await say_goodbye()
    print(result_a, result_b)


if __name__ == '__main__':
    start_time = time.time()  
    #asyncio.run(main())
    asyncio.run(main2())
    end_time = time.time()
    print("Time used:", end_time - start_time)
    
# 运行异步函数
#asyncio.run(say_hello())