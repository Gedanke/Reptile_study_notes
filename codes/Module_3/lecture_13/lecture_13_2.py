# -*- coding: utf-8 -*-

import random
import time
import json
import requests
import logging

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://dynamic1.scrape.center/api/movie/?limit={limit}&offset={offset}'


def scrape_api(url: str):
    """
    :param url:
    :return:
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url, headers)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


LIMIT = 10


def scrape_index(page: int):
    """
    :param page:
    :return:
    """
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


DETAIL_URL = 'https://dynamic1.scrape.center/api/movie/{id}'


def scrape_detail(id: str):
    """
    :param id:
    :return:
    """
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


TOTAL_PAGE = 10


def save_data(data):
    """

    :param data:
    :return:
    """
    name = data.get('name')
    data_path = str(name) + ".json"
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def main():
    """
    :return:
    """
    for page in range(1, TOTAL_PAGE + 1):
        time.sleep(random.randint(3, 5))
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            time.sleep(random.randint(6, 10) / 10)
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data %s', detail_data)
            save_data(detail_data)


if __name__ == '__main__':
    """"""
    main()
