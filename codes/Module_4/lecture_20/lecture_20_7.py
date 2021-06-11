# -*- coding: utf-8 -*-


import asyncio
import aiohttp

proxy = 'http://127.0.0.1:8889'

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}


async def main():
    """

    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get', headers=headers, proxy=proxy) as response:
            print(await response.text())


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
