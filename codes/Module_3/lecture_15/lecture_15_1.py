# -*- coding: utf-8 -*-

import time
import random
import json
import logging
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urljoin


def gain_driver():
    """

    :return:
    """
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features-AutomationControlled")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
    )
    driver = Chrome('chromedriver', options=chrome_options)
    driver.set_window_size(1366, 768)
    with open('stealth.min.js') as f:
        js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    return driver


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://dynamic2.scrape.center/page/{page}'
TIME_OUT = 10
TOTAL_PAGE = 10
browser = gain_driver()
wait = WebDriverWait(browser, TIME_OUT)


def scrape_page(url: str, condition, locator):
    """

    :param url:
    :param condition:
    :param locator:
    :return:
    """
    logging.info('scraping %s', url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """

    :param page:
    :return:
    """
    url = INDEX_URL.format(page=page)
    scrape_page(
        url, condition=EC.visibility_of_all_elements_located,
        locator=(By.CSS_SELECTOR, '#index .item')
    )


def parse_index():
    """

    :return:
    """
    elements = browser.find_elements_by_css_selector('#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(INDEX_URL, href)


# def main():
#     """
#
#     :return:
#     """
#     try:
#         for p in range(1, TOTAL_PAGE + 1):
#             scrape_index(p)
#             detail_urls = parse_index()
#             logging.info('details urls %s', list(detail_urls))
#     finally:
#         browser.close()


def scrape_detail(url: str):
    """

    :param url:
    :return:
    """
    scrape_page(
        url, condition=EC.visibility_of_element_located,
        locator=(By.TAG_NAME, 'h2')
    )


def parse_detail():
    """

    :return:
    """
    url = browser.current_url
    name = browser.find_element_by_tag_name('h2').text
    categories = [
        element.text for element in browser.find_elements_by_css_selector('.categories button span')
    ]
    cover = browser.find_element_by_css_selector('.cover').get_attribute('src')
    score = browser.find_element_by_class_name('score').text
    drama = browser.find_element_by_css_selector('.drama p').text
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


def save_data(data):
    """

    :param data:
    :return:
    """
    name = data.get('name')
    data_path = str(name) + ".json"
    json.dump(
        data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2
    )


def main():
    """

    :return:
    """
    try:
        for page in range(1, TOTAL_PAGE + 1):
            time.sleep(random.randint(5, 8))
            scrape_index(page)
            detail_urls = parse_index()
            for detail_url in list(detail_urls):
                time.sleep(random.randint(3, 5) / 2)
                logging.info('get detail url %s', detail_url)
                scrape_detail(detail_url)
                detail_data = parse_detail()
                save_data(detail_data)
                logging.info('detail data %s', detail_data)
    finally:
        browser.close()


if __name__ == '__main__':
    """"""
    main()
