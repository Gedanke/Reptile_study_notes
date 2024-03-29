# -*- coding: utf-8 -*-


import json
import requests

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
url = 'https://api.diffbot.com/v3/article'
params = {
    'token': '77b41f6fbb24496d5113d528306528fa',
    'url': 'https://news.ifeng.com/c/7kQcQG2peWU',
    'fields': 'meta'
}
response = requests.get(url, params=params, headers=headers)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
