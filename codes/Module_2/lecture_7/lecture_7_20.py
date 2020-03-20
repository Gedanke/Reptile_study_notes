# -*- coding: utf-8 -*-

import requests
import urllib3

urllib3.disable_warnings()
url = "https://static2.scrape.cuiqingcai.com/"
response = requests.get(url, verify=False)
print(response.status_code)
