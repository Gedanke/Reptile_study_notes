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
BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

response_login = requests.post(
    LOGIN_URL, json={
        'username': USERNAME,
        'password': PASSWORD
    }, headers=headers
)

data = response_login.json()
print('Response JSON', data)

jwt = data.get('token')
print('JWT', jwt)

headers['Authorization'] = f'jwt {jwt}'

response_index = requests.get(
    INDEX_URL, params={
        'limit': 18,
        'offset': 0
    }, headers=headers
)

print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
print('Response Data', response_index.json())
