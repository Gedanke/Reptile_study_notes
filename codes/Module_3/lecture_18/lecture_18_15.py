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
    await page.goto('https://www.bing.com/')
    # 后退
    await page.type('#sb_form_q', 'biying')
    # 关闭
    await asyncio.sleep(10)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
