import asyncio
from time import time

import aiohttp
import requests


def get_response(url):
    r = requests.get(url)
    return r


def write_picture(response):
    filename = '{}.jpg'.format(int(time()))
    with open(filename, 'wb') as file:
        file.write(response.content)


def main2():
    url = 'https://loremflickr.com/320/240'
    for i in range(10):
        write_picture(get_response(url))


async def fetch_content(url: str, session):
    async with session.get(url) as response:
        data = await response.read()
        write_file(data)


def write_file(data):
    filename = '{}.jpg'.format(int(time()))
    with open(filename, 'wb') as file:
        file.write(data)


async def main():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    # main2()
    print(str(t0 - time()))
