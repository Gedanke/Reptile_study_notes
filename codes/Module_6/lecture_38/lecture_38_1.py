# -*- coding: utf-8 -*-


import requests
from readability import Document

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

url = 'https://tech.163.com/19/0909/08/EOKA3CFB00097U7S.html'
html = requests.get(url, headers=headers).content
doc = Document(html)
print('title:', doc.title())
print('content:', doc.summary(html_partial=True))
