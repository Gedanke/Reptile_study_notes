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
    await page.goto('https://dynamic2.scrape.center/')
    await page.waitForSelector('.item .name')
    await page.click(
        '.item .name', options={
            'button': 'right',
            'clickCount': 1,  # 1 or 2
            'delay': 3000,  # 毫秒
        }
    )
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
