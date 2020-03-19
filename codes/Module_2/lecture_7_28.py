# -*- coding: utf-8 -*-

from requests import Request, Session

url = "http://httpbin.org/post"
data = {
    "name": "germey"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
s = Session()
req = Request("POST", url=url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)

print(r.text)
