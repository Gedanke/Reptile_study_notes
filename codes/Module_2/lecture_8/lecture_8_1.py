# -*- coding: utf-8 -*-

import re

content = "Hello 123 4567 World_This is a Regex Demo"
print(len(content))
pattern_str = "^Hello\s\d\d\d\s\d{4}\s\w{10}"
pattern = re.compile(pattern_str)
result = re.match(pattern, content)
print(result)
print(result.group())
print(result.span())
