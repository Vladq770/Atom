import asyncio
from sys import argv


def counter(start: int = 0):
    i = start
    while True:
        yield i
        i += 1


async def robot(start: int = 0):
    for i in counter(start):
        print(i)
        await asyncio.sleep(1)


async def main(start: int = 0):
    robot_task = asyncio.create_task(robot(start))
    await robot_task


arg = 0
if len(argv) > 1:
    arg = int(argv[1])

asyncio.run(main(arg))
