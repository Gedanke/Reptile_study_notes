# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<ul class="list">
    <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
</ul>
'''
doc = PyQuery(html)
li = doc(".item-0.active")
print(li)
li.attr("name", "link")
print(li)
li.text("changed item")
print(li)
li.html("<span>changed item</span>")
print(li)
