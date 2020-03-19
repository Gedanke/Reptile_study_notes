# -*- coding: utf-8 -*-

import re

content = "(百度)www.baidu.com"
result = re.match("\(百度\)www\.baidu\.com", content)
print(result)
print(result.group())
