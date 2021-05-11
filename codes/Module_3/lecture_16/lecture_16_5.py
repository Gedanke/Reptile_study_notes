# -*- coding: utf-8 -*-

import asyncio
import requests

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}


async def request():
    """

    :return:
    """
    url = "https://www.baidu.com"
    status = requests.get(url, headers)
    return status


def callback(task):
    """

    :param task:
    :return:
    """
    print('Status:', task.result())


coroutine = request()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)
print('Task:', task)

# asyncio.get_event_loop().run_until_complete(task)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:', task)
