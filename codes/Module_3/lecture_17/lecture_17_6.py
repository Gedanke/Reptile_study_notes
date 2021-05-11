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
    timeout = aiohttp.ClientTimeout(total=1)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url='https://httpbin.org/get', headers=headers) as response:
            print('status:', response.status)


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
