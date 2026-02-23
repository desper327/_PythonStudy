import asyncio,time

async def hello():
    print("Hello1",time.time())
    await asyncio.sleep(2)
    print("Hello2",time.time())


async def haha():
    print("haha1",time.time())
    await asyncio.sleep(2)
    print("haha2",time.time())



async def main():
    await asyncio.gather(hello(), haha())


if __name__ == '__main__':
    asyncio.run(main())