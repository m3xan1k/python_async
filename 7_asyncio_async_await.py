import asyncio


async def count_nums():
    count = 0
    while True:
        print(count)
        await asyncio.sleep(1)
        count += 1


async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print('{} seconds have passed'.format(count))
        await asyncio.sleep(1)
        count += 1


async def main():
    task1 = asyncio.create_task(count_nums())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    asyncio.run(main())
