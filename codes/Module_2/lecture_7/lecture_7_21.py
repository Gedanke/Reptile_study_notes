# -*- coding: utf-8 -*-

import requests
import logging

logging.captureWarnings(True)
url = "https://static2.scrape.cuiqingcai.com/"
response = requests.get(url, verify=False)
print(response.status_code)
