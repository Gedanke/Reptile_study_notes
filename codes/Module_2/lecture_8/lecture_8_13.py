# -*- coding: utf-8 -*-

import re

content1 = "2020-3-19 12:00"
content2 = "2020-3-19 13:10"
content3 = "2020-3-19 14:21"

pattern = re.compile("\d{2}:\d{2}")
result1 = re.sub(pattern, "", content1)
result2 = re.sub(pattern, "", content2)
result3 = re.sub(pattern, "", content3)
print(result1, result2, result3)
