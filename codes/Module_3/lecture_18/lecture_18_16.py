# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch


async def main():
    """

    :return:
    """
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://www.bing.com/')
    print('HTML:', await page.content())
    print('Cookies:', await page.cookies())
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
