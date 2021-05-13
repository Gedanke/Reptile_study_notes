# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch


async def main():
    """

    :return:
    """
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.center/')
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
