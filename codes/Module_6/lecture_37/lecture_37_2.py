# -*- coding: utf-8 -*-


from client import DiffbotClient, DiffbotCrawl

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

diffbot = DiffbotClient()
token = 'your_token'
url = 'http://shichuan.github.io/javascript-patterns/'
api = 'article'
response = diffbot.request(url, token, api, headers=headers)
