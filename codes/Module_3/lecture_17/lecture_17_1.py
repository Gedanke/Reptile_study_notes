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


async def fetch(session, url):
    """

    :param session:
    :param url:
    :return:
    """
    async with session.get(url, headers=headers) as response:
        return await response.text(), response.status


async def main():
    """

    :return:
    """
    async with aiohttp.ClientSession() as session:
        html, status = await fetch(session, 'https://weibo.com/')
        print(f'html: {html[:100]}...')
        print(f'status: {status}')


if __name__ == '__main__':
    """"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
