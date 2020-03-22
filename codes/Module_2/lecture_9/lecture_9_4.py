# -*- coding: utf-8 -*-

from pyquery import PyQuery

filename = "demo.html"
doc = PyQuery(filename=filename)
print(doc("title"))
