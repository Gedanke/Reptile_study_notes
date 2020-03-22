# -*- coding: utf-8 -*-

from pyquery import PyQuery
import requests

url = "https://dogedoge.com"
doc = PyQuery(requests.get(url=url).text)
print(doc("title"))
