# -*- coding: utf-8 -*-


import re
import time
import random
import requests
import logging
import pymongo
from pyquery import PyQuery
from urllib.parse import urljoin
import multiprocessing

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

ROOT_URL = "https://static1.scrape.center"
PAGE_NUM = 10
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movies'
MONGO_COLLECTION_NAME = 'movies'

client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client['movies']
collection = db['movies']


def scrape_page(url: str):
    """
    
    :param url: 
    :return: 
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page: int):
    """
    
    :param page: 
    :return: 
    """
    index_url = f'{ROOT_URL}/page/{page}'
    return scrape_page(index_url)


def parse_index(html: str):
    """
    
    :param html: 
    :return: 
    """
    doc = PyQuery(html)
    links = doc(".el-card .name")
    for link in links.items():
        href = link.attr("href")
        detail_url = urljoin(ROOT_URL, href)
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrape_detail(url: str):
    """

    :param url:
    :return:
    """
    return scrape_page(url)


def parse_detail(html: str):
    """

    :param html:
    :return:
    """
    doc = PyQuery(html)
    cover = doc('img.cover').attr('src')
    name = doc('a > h2').text()
    categories = [item.text() for item in doc('.categories button span').items()]
    published_at = doc('.info:contains(上映)').text()
    published_at = re.search('(\d{4}-\d{2}-\d{2})', published_at).group(1) \
        if published_at and re.search('\d{4}-\d{2}-\d{2}', published_at) else None
    drama = doc('.drama p').text()
    score = doc('p.score').text()
    score = float(score) if score else None
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


def save_data(data: dict):
    """

    :param data:
    :return:
    """
    collection.update_one({
        "name": data.get("name")
    }, {
        "$set": data
    }, upsert=True)


# def main():
#     """
#
#     :return:
#     """
#     for page in range(1, PAGE_NUM + 1):
#         time.sleep(random.randint(5, 10) / 10)
#         index_html = scrape_index(page)
#         detail_urls = parse_index(index_html)
#         for detail_url in detail_urls:
#             detail_html = scrape_detail(detail_url)
#             data = parse_detail(detail_html)
#             logging.info('get detail data %s', data)
#             logging.info('saving data to mongodb')
#             save_data(data)
#             logging.info('data saved successfully')


def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to mongodb')
        save_data(data)
        logging.info('data saved successfully')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, PAGE_NUM + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
