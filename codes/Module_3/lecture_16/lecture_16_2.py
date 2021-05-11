# -*- coding: utf-8 -*-

import asyncio


async def excute(x):
    """

    :param x:
    :return:
    """
    print("Number: ", x)


coroutine = excute(1)
print('Coroutine:', coroutine)
print('After calling execute')
# asyncio.get_event_loop().run_until_complete(coroutine)
loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)
print('After calling loop')
