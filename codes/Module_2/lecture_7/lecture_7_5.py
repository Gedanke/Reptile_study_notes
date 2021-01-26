# -*- coding: utf-8 -*-

import requests
import re

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)
pattern_str = "<h2.*?>(.*?)</h2>"
pattern = re.compile(pattern_str, re.S)
title = re.findall(pattern, r.text)
print(title)
