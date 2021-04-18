# -*- coding: utf-8 -*-

from requests import Request, Session

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
url = "http://httpbin.org/post"
data = {
    "name": "germey"
}
s = Session()
req = Request("POST", url=url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)

print(r.text)
