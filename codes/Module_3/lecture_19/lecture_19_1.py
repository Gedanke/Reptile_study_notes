# -*- coding: utf-8 -*-

import time
import random
import json
import logging
import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://dynamic2.scrape.center/page/{page}'
TIMEOUT = 10
TOTAL_PAGE = 10
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
HEADLESS = True

browser, tab = None, None


async def init():
    """

    :return:
    """
    global browser, tab
    browser = await launch(
        headless=HEADLESS,
        args=[
            '--disable-infobars',
            f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'
        ]
    )
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})


async def scrape_page(url: str, selector: str):
    """

    :param url:
    :param selector:
    :return:
    """
    logging.info('scraping %s', url)
    try:
        await tab.goto(url)
        await tab.waitForSelector(
            selector, options={
                'timeout': TIMEOUT * 1000
            })
    except TimeoutError:
        logging.error('error occurred while scraping %s', url, exc_info=True)


async def scrape_index(page):
    """

    :param page:
    :return:
    """
    url = INDEX_URL.format(page=page)
    await scrape_page(url, '.item .name')


async def parse_index():
    """

    :return:
    """
    return await tab.querySelectorAllEval(
        '.item .name', 'nodes => nodes.map(node => node.href)'
    )


async def scrape_detail(url: str):
    """

    :param url:
    :return:
    """
    await scrape_page(url, 'h2')


async def parse_detail():
    """

    :return:
    """
    url = tab.url
    name = await tab.querySelectorEval('h2', 'node => node.innerText')
    categories = await tab.querySelectorAllEval('.categories button span', 'nodes => nodes.map(node => node.innerText)')
    cover = await tab.querySelectorEval('.cover', 'node => node.src')
    score = await tab.querySelectorEval('.score', 'node => node.innerText')
    drama = await tab.querySelectorEval('.drama p', 'node => node.innerText')

    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


async def save_data(data):
    """

    :param data:
    :return:
    """
    name = data.get('name')
    data_path = str(name) + ".json"
    json.dump(
        data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2
    )


async def main():
    """

    :return:
    """
    await init()
    try:
        for page in range(1, TOTAL_PAGE + 1):
            time.sleep(random.randint(3, 5))
            await scrape_index(page)
            detail_urls = await parse_index()
            for detail_url in detail_urls:
                time.sleep(random.randint(3, 5) / 2)
                await scrape_detail(detail_url)
                detail_data = await parse_detail()
                logging.info('data %s', detail_data)
                await save_data(detail_data)
    finally:
        await browser.close()


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
