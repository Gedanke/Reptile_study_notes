# -*- coding: utf-8 -*-


import re
import requests
import logging
import pymongo
from pyquery import PyQuery
from sklearn.cluster import KMeans
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

ROOT_URL = "https://static1.scrape.cuiqingcai.com"
PAGE_NUM = 10
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
}


def scrape_page(url: str):
    """
    
    :param url: 
    :return: 
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url, headers=headers, verify=False)
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


def main():
    """
    
    :return: 
    """
    for page in range(1, PAGE_NUM + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        logging.info('detail urls %s', list(detail_urls))


if __name__ == '__main__':
    """"""
    # main()
