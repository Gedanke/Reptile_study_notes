# -*- coding: utf-8 -*-

import requests
import socks
import socket

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1089)
socket.socket = socks.socksocket
try:
    response = requests.get('https://httpbin.org/get', headers=headers)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
