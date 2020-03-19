# -*- coding: utf-8 -*-

import requests

url = "https://github.com/favicon.ico"
r = requests.get(url)
# 存放图片的路径
file_path = "../../images/Module_2/favicon.ico"
with open(file_path, "wb") as f:
    f.write(r.content)
