# -*- coding: utf-8 -*-

import time
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
TOTAL_NUMBER = 100
BASE_URL = 'https://static4.scrape.center/detail/{id}'
start_time = time.time()
for id in range(1, TOTAL_NUMBER + 1):
    url = BASE_URL.format(id=id)
    logging.info('scraping %s', url)
    response = requests.get(url, headers)
end_time = time.time()
logging.info('total time %s seconds', end_time - start_time)
