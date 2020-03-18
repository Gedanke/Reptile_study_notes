# -*- coding: utf-8 -*-

import requests

url = "https://static3.scrape.cuiqingcai.com/"
r = requests.get(url, auth=("admin", "admin"))
print(r.status_code)
