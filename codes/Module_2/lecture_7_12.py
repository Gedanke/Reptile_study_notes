# -*- coding: utf-8 -*-

import requests

file_path = "../../images/Module_2/favicon.ico"
files = {
    "file": open(file_path, "rb")
}
url = "http://httpbin.org/post"
r = requests.post(url=url, files=files)

print(r.text)
