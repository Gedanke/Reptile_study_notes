# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth

url = "https://static3.scrape.cuiqingcai.com/"
r = requests.get(url, auth=HTTPBasicAuth("admin", "admin"))
print(r.status_code)
