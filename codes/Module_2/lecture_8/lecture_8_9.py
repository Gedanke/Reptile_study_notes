# -*- coding: utf-8 -*-

import re

content = "Extra strings Hello 1234567 World_This is a Regex Demo Extra strings"
pattern_str = "Hello.*?(\d+).*?Demo"
result = re.match(pattern_str, content)
# result = re.search(pattern_str, content)
print(result)
# print(result.group(1))
