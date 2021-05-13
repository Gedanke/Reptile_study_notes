# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch


async def main():
    """

    :return:
    """
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport(
        {'width': 1920, 'height': 1080}
    )
    await page.goto('https://dynamic2.scrape.center/')
    await page.waitForSelector('.item .name')
    await asyncio.sleep(2)
    await page.screenshot(path='example.png')
    dimensions = await page.evaluate(
        '''() => { return { width: document.documentElement.clientWidth, height:
        document.documentElement.clientHeight, deviceScaleFactor: window.devicePixelRatio, } }'''
    )
    print(dimensions)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
