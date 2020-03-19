# -*- coding: utf-8 -*-

import re

content = "https://weibo.com/comment/kEraCN"
result1 = re.match("https.*?comment/(.*?)", content)
result2 = re.match("https.*?comment/(.*)", content)
print("result1: ", result1.group(1))
print("result2: ", result2.group(1))
