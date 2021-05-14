# -*- coding: utf-8 -*-

import asyncio
from pyppeteer import launch, launcher


async def gain_driver():
    """

    :return:
    """
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport(
        {'width': 1920, 'height': 1080}
    )
    with open('stealth.min.js') as f:
        js = f.read()
    await page.evaluateOnNewDocument(js)
    # await page.evaluateOnNewDocument(
    #     'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    # )
    # return page
    # page = await gain_driver()
    '''test'''
    url = "https://bot.sannysoft.com/"
    await page.goto(url)
    source = await page.content()
    with open('result.html', 'w') as f:
        f.write(source)


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(gain_driver())
