# -*- coding: utf-8 -*-

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, headers=headers)
print(r.text)
