# -*- coding: utf-8 -*-

import requests

s = requests.Session()
s.get("http://httpbin.org/cookies/set/number/123456789")
r = s.get("http://httpbin.org/cookies")
