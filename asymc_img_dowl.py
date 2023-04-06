import asyncio
from time import time
import os
import aiofiles
import aiohttp


async def write_image(data: bytes) -> None:
    name = int(time() * 1000)
    filename = f'file{name}.jpeg'
    filepath = os.path.join('img', filename)
    if not os.path.exists('img'):
        os.makedirs('img')

    async with aiofiles.open(filepath, 'wb') as file:
        await file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        await write_image(data)


async def main():

    url = 'https://loremflickr.com/320/240/paris,girl/all'
    tasks = []
    async with  aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for i in range(11):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    asyncio.run(main())
