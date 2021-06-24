# -*- coding: utf-8 -*-


import requests
from urllib.parse import urljoin

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'
session = requests.Session()

response_login = session.post(
    LOGIN_URL, data={
        'username': USERNAME,
        'password': PASSWORD
    }, headers=headers
)

cookies = session.cookies
print('Cookies', cookies)

response_index = session.get(INDEX_URL, headers=headers)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
