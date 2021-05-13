# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch


async def main():
    """

    :return:
    """
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.setViewport(
        {'width': 1920, 'height': 1080}
    )
    await page.goto('https://www.baidu.com')
    page = await browser.newPage()
    await page.setViewport(
        {'width': 1920, 'height': 1080}
    )
    await page.goto('https://www.bing.com')
    pages = await browser.pages()
    print('Pages:', pages)
    page1 = pages[1]
    await page1.bringToFront()
    await asyncio.sleep(100)


asyncio.get_event_loop().run_until_complete(main())
