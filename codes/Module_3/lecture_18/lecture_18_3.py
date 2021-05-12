# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch


async def main():
    """

    :return:
    """
    await launch(headless=False)
    await asyncio.sleep(10)


asyncio.get_event_loop().run_until_complete(main())
