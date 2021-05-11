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

CONCURRENCY = 5
URL = 'https://www.baidu.com'
semaphore = asyncio.Semaphore(CONCURRENCY)
session = aiohttp.ClientSession()


async def scrape_api():
    """

    :return:
    """
    async with semaphore:
        print('scraping', URL)
        async with session.get(URL, headers=headers) as response:
            await asyncio.sleep(1)
            return await response.text()


async def main():
    """

    :return:
    """
    global session
    session = aiohttp.ClientSession()
    scrape_index_tasks = [
        asyncio.ensure_future(scrape_api()) for _ in range(10000)
    ]
    await asyncio.gather(*scrape_index_tasks)


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
