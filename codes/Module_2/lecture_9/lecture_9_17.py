# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    Hello,world
    <p>This is a paragraph.</p>
</div>
'''
doc = PyQuery(html)
wrap = doc(".wrap")
print(wrap.text())
wrap.find("p").remove()
print(wrap.text())
