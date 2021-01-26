# -*- coding: utf-8 -*-

import requests

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)

if not r.status_code == requests.codes.ok:
    exit()
else:
    print("Request Successfully")
