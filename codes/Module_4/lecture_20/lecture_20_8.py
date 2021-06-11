# -*- coding: utf-8 -*-


import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

connector = ProxyConnector.from_url('socks5://127.0.0.1:1089')


async def main():
    """

    :return:
    """
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get('https://httpbin.org/get', headers=headers) as response:
            print(await response.text())


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
