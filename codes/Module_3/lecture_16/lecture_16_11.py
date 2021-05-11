# -*- coding: utf-8 -*-

import asyncio
import time
import aiohttp

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}


def test(number):
    """

    :param number:
    :return:
    """
    start = time.time()

    async def get(url: str):
        """

        :param url:
        :return:
        """
        session = aiohttp.ClientSession()
        response = await session.get(url, headers=headers)
        await response.text()
        await session.close()
        return response

    async def request():
        """

        :return:
        """
        url = 'https://www.baidu.com/'
        await get(url)

    tasks = [
        asyncio.ensure_future(request()) for _ in range(number)
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('Number:', number, 'Cost time:', end - start)


for number in [1, 3, 5, 10, 15, 30, 50, 75, 100, 200, 500]:
    test(number)
