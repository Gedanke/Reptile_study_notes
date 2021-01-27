# -*- coding: utf-8 -*-

import requests
import logging

logging.captureWarnings(True)
url = "https://static1.scrape.cuiqingcai.com/"
response = requests.get(url, verify=False)
print(response.status_code)
