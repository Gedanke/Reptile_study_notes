# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch


async def main():
    """

    :return:
    """
    browser = await launch(headless=False, args=['--disable-infobars'])
    page = await browser.newPage()
    await page.setViewport(
        {'width': 1920, 'height': 1080}
    )
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    await page.goto('https://antispider1.scrape.center/')
    await asyncio.sleep(10)


asyncio.get_event_loop().run_until_complete(main())
