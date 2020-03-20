# -*- coding: utf-8 -*-

import re

content = "Hello 1234567 World_This is a Regex Demo"
pattern_str = "^Hello.*Demo$"
pattern = re.compile(pattern_str)
result = re.match(pattern, content)
print(result)
print(result.group())
print(result.span())
