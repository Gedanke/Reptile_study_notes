# -*- coding: utf-8 -*-

from pyquery import PyQuery

url = "https://dogedoge.com"
doc = PyQuery(url=url)
print(doc("title"))
