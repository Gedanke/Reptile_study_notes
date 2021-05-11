# -*- coding: utf-8 -*-

import aiohttp
import asyncio

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}


async def main():
    """

    :return:
    """
    data = {
        'name': 'germey', 'age': 25
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://httpbin.org/post', headers=headers, data=data) as response:
            print('status:', response.status)
            print('headers:', response.headers)
            print('body:', await response.text())
            print('bytes:', await response.read())
            print('json:', await response.json())


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
