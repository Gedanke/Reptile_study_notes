# -*- coding: utf-8 -*-

import requests

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)
print(r.text)
