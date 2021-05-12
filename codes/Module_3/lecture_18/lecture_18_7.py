# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch

width, height = 1366, 768


async def main():
    """

    :return:
    """
    browser = await launch(headless=False, args=['--disable-infobars', f'--window-size={width},{height}'])
    page = await browser.newPage()
    await page.setViewport(
        {'width': width, 'height': height}
    )
    await page.evaluateOnNewDocument(
        'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    )
    await page.goto('https://antispider1.scrape.center/')
    await asyncio.sleep(10)


asyncio.get_event_loop().run_until_complete(main())
