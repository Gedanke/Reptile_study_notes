# -*- coding: utf-8 -*-

import asyncio


async def execute(x):
    """

    :param x:
    :return:
    """
    print('Number:', x)
    return x


coroutine = execute(1)
print('Coroutine:', coroutine)
print('After calling execute')
task = asyncio.ensure_future(coroutine)
print('Task:', task)
# asyncio.get_event_loop().run_until_complete(task)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:', task)
print('After calling loop')
