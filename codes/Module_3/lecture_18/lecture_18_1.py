# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch
from pyquery import PyQuery


async def main():
    """

    :return:
    """
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.center/')
    await page.waitForSelector('.item .name')
    doc = PyQuery(await page.content())
    names = [item.text() for item in doc('.item .name').items()]
    print('Names:', names)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
