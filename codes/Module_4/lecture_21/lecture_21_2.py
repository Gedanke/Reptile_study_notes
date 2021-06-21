# -*- coding: utf-8 -*-


import requests

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():
    """

    :return:
    """
    try:
        response = requests.get(PROXY_POOL_URL, headers=headers)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


proxy = get_proxy()

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

try:
    response = requests.get('http://httpbin.org/get', proxies=proxies, headers=headers)
    print(response.text)
except  requests.exceptions.ConnectionError  as  e:
    print('Error', e.args)
