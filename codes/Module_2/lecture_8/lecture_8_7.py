# -*- coding: utf-8 -*-

import re

content = '''Hello 1234567 World_This 
is a Regex Demo
'''
# result = re.match("^He.*?(\d+).*?Demo$", content)
result = re.match("^He.*?(\d+).*?Demo$", content, re.S)
print(result.group(1))
