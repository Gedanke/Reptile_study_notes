# Requests 库使用

爬虫，可以说是用程序模拟浏览器向服务器发出请求，从服务器处得到响应并解析处理的过程。这其中发生很复杂的过程，通信协议，服务器响应和应答等等。

如果这些过程需要我们手动完成，工作量太大了。Python 的强大之处就是有很多封装好了的“轮子”可以直接使用， 比如这节要讲的 Requests 库，有了它，我们可以很简单地完成一个请求和应答过程，而不需要关心太多的底层细节。

---
---

## 安装

如果你已经安装了 Python3 ，使用 pip3 就可以安装了。

在命令行里输入：

```shell
pip3 install requests
```

或者使用Pycharm自带的工具：

![](../../images/Module_2/lecture_7_1.jpg)

---

## 实例

当我们在浏览器中输入一个 URL 并回车，浏览器就发出来了一个 GET 请求，浏览器得到响应，解析源代码得到网页内容。

如果我们想模拟这个过程的话，使用 ```requests``` 库的 ```get``` 方法，传入 URL，就可以得到网页源代码了。

以 [https://static1.scrape.cuiqingcai.com/](https://static1.scrape.cuiqingcai.com/) 为实例网站：

![](../../images/Module_2/lecture_7_2.jpg)

使用 ```requests``` 库来爬取网站的源代码，[实例](../../codes/Module_2/lecture_7/lecture_7_1.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)
print(r.text)
```

部分结果为：

```html

<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="icon" href="/static/img/favicon.ico">
    <title>Scrape | Movie</title>
    <link href="/static/css/app.css" type="text/css" rel="stylesheet">
    <link href="/static/css/index.css" type="text/css" rel="stylesheet">
</head>
<body>
<div id="app">
    ...
</div>
</body>
```

由于网页内容多，这里只截取了部分。

从运行结果可以看出，我们已经得到了网页的源代码，里面包含了电影的标题，类型，上映时间等等，之后我们会从中提取相应的信息。

---

## 请求

接下来，我们将使用 ```requests``` 来构造 GET 请求和 POST 请求。

---

## GET 请求

以 [http://httpbin.org/get](http://httpbin.org/get) 为例，如果客户端发起了 GET 请求，该网站会判断并返回相应的请求信息，包括 Headers，IP 等。

[示例](../../codes/Module_2/lecture_7/lecture_7_2.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
r = requests.get(url=url)
print(r.text)
```

结果如下：

```json
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.18.4",
    "X-Amzn-Trace-Id": "Root=1-5e71a091-dddec6cc677846b05c4e05f8"
  },
  "origin": "117.178.93.51",
  "url": "http://httpbin.org/get"
}
```

网站返回了请求所携带的信息，包括 Headers，URL，IP 等等。

我们知道，对于 GET 请求，URL 后面可以跟一些参数，如果我们现在想添加两个参数，其中 name 是 germey，age 是 25，URL 就可以写成如下内容：

[http://httpbin.org/get?name=germey&age=25](http://httpbin.org/get?name=germey&age=25)

构造这个请求连接，可以写成这样：

```python
r = requests.get("http://httpbin.org/get?name=germey&age=25")
```

更方便的写法是 [下面](../../codes/Module_2/lecture_7/lecture_7_3.py) 这样的：

```python
# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
data = {
    "name": "germey",
    "age": 25
}
r = requests.get(url=url, params=data)
print(r.text)
```

结果为：

```json
{
  "args": {
    "age": "25",
    "name": "germey"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.18.4",
    "X-Amzn-Trace-Id": "Root=1-5e71c90d-bb2daf48b3597b920f434f08"
  },
  "origin": "117.178.93.51",
  "url": "http://httpbin.org/get?name=germey&age=25"
}
```

在这里我们把 URL 参数通过字典的形式传给 ```get``` 方法的 ```params```
参数，请求的链接便自动变为 [http://httpbin.org/get?name=germey&age=25](http://httpbin.org/get?name=germey&age=25)
，这一点从返回的信息 args 也可以看出。

我们可以看出，网页返回的类型是 str 类型的，JSON 格式的，如果想得到 JSON 格式的数据，使用 json 方法即可。

[示例](../../codes/Module_2/lecture_7/lecture_7_4.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
r = requests.get(url=url)
print(type(r.text))
print(r.json())
print(type(r.json()))
```

结果为：

```text
<class 'str'>
{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4', 
'X-Amzn-Trace-Id': 'Root=1-5e71cb6e-b13fd4d8862a8338ce169e80'}, 'origin': '117.178.93.51', 'url': 'http://httpbin.org/get'}
<class 'dict'>
```

调用 json 方法，就可以将返回结果是 JSON 格式的字符串转化为字典。

如果返回结果不是 JSON 格式，便会出现解析错误，抛出 ```json.decoder.JSONDecodeError``` 异常。

---

## 抓取网页

我们对得到的网页源代码进行一个简单的提取。

[示例](../../codes/Module_2/lecture_7/lecture_7_5.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests
import re

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)
pattern_str = "<h2.*?>(.*?)</h2>"
pattern = re.compile(pattern_str, re.S)
title = re.findall(pattern, r.text)
print(title)
```

结果为：

```text
['霸王别姬 - Farewell My Concubine', '这个杀手不太冷 - Léon', '肖申克的救赎 - The Shawshank Redemption', 
'泰坦尼克号 - Titanic', '罗马假日 - Roman Holiday', '唐伯虎点秋香 - Flirting Scholar', '乱世佳人 - Gone with the Wind', 
'喜剧之王 - The King of Comedy', '楚门的世界 - The Truman Show', '狮子王 - The Lion King']
```

我们使用了正则表达式匹配出所有的标题，关于正则表达式会在下一节消息介绍。

从运行结果可知，我们提取出了所有的电影标题，一个最基本的抓取并提取网页内容流程就完成了。

---

## 抓取二进制数据

之前例子抓取的是网页页面，返回了一个HTML文档，对于图片，视频，音频等等，它们都是由二进制根据特定的编码格式组成的，由特定的解析格式就可以得到它们。

来看一个 [示例](../../codes/Module_2/lecture_7/lecture_7_6.py) ：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://github.com/favicon.ico"
r = requests.get(url)
print(r.text)
print(r.content)
```

结果为：

```text
:�������O                                L������                                      ������                                        ������!                                ������4                                @���8���          
��������333                                                ���t�������+R������t                                                                `������R����������                                                                    �������������\                                                                        G������������                                                                          ������������                                                                                ������������                                                                                ���������������                                                                            ������������%                                                                           ������������v                                                                        a������G������                                                                ������G+++������]                                                                I������+++    ������3                                                                ������         �����5            +*���                ���&            !�����             �����f    @@@b����������l+++    R�����                $$$��������������������������$$$                     ������������������������                             .����������������������.                                     ��������������������                                             $$$������������������$$$                                                         ��������������                                                                         +++G��������G+++                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
b'\x00\x00\x01\x00\x02\x00\x10\x10\x00\x00\x01\x00 \x00(\x05\x00\x00&\x00\x00\x00  \x00\x00\x01\x00 \x00(\x14\x00\x00N\x05\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00 \x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x13v\x13\x13\x13\xc5\x0e\x0e\x0e\x12\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x0f\x0f\x11\x11\x11\x14\xb1\x13\x13\x13i\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x14\x14\x96\x13\x13\x14\xfc\x13\x13\x14\xed\x00\x00\x00\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x15\x15\x17\xff\x15\x15\x17\xff\x11\x11\x13\x85\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x12\xc1\x13\x13\x14\xee\x11\x11\x11\x1e\x10\x10\x10\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x13\x13\x14\xf5\x15\x15\x17\xff\x15\x15\x17\xff\x11\x11\x14\xaf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x14\x14\x99\x15\x15\x17\xff\x06\x06\x11,\x0e\x0e\x0e\\\x0f\x0f\x0f\xc1\x0f\x0f\x0f"\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x0f\x0f4\x10\x10\x10\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x14\x14\x14\x8f\x00\x00\x00\x00\x10\x10\x100\x0f\r\x0f\xff\x00\x00\x00\xf9\x01\x01\x01\xed\x02\x02\x02\xff\x02\x02\x02\xf6\x0e\x0e\x0e8\x00\x00\x00\x00\x00\x00\x00\x00\x08\x08\x08@\x02\x02\x02\xeb\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x11\x11\x11-\x14\x14\x15\x9c\x14\x14\x15\xff\x01\x01\x01\xfc\x0f\x0f\x11\xfb\r\r\x11;\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\r\x12:\x13\x13\x14\xe7\x15\x15\x17\xff\x15\x15\x17\xff\x12\x12\x12\x9a\x13\x13\x13\xd9\x15\x15\x17\xff\x15\x15\x17\xff\x13\x13\x13O\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x11L\x15\x15\x17\xff\x15\x15\x17\xff\x13\x13\x13\xda\x13\x13\x14\xf6\x15\x15\x17\xff\x14\x14\x14\xf0\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x13\x13\x14\xf1\x15\x15\x17\xff\x13\x13\x14\xf6\x13\x13\x14\xf7\x15\x15\x17\xff\x14\x14\x14\xe1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x14\x14\xe1\x15\x15\x17\xff\x13\x13\x14\xf7\x14\x14\x14\xde\x15\x15\x17\xff\x13\x13\x14\xf9\x0f\x0f\x0f!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x1f\x13\x13\x14\xf8\x15\x15\x17\xff\x14\x14\x14\xde\x11\x11\x14\xa2\x15\x15\x17\xff\x15\x15\x17\xff\x0f\x0f\x0f4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10@\x15\x15\x17\xff\x15\x15\x17\xff\x11\x11\x14\xa2\x0e\x0e\x0e8\x15\x15\x17\xff\x15\x15\x17\xff\x12\x12\x12\x98\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x00\x00\x12\x12\x12\x98\x15\x15\x17\xff\x15\x15\x17\xff\x0e\x0e\x0e8\x00\x00\x00\x00\x11\x11\x14\xa4\x15\x15\x17\xff\x11\x11\x12\xc1\x0e\x0e\x0e6\x00\x00\x00\x81\r\r\r\xdc\x12\x12\x14\xd8\x12\x12\x14\xd8\x13\x13\x14\xf7\x00\x00\x00t\x05\x05\x057\x11\x11\x12\xc1\x15\x15\x17\xff\x11\x11\x14\xa4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x13\x13\x13\xc6\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x13\x13\x13\xc6\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x11\x11\x14\xa2\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x11\x11\x14\xa2\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10>\x13\x13\x13\x97\x13\x13\x13\xd9\x12\x12\x14\xf2\x12\x12\x14\xf2\x13\x13\x13\xd9\x13\x13\x13\x97\x10\x10\x10>\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00(\x00\x00\x00 \x00\x00\x00@\x00\x00\x00\x01\x00 \x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15+\x0c\x1e\x1e\x1e\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x1b\x1b\x1c$$$\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x1d#\x17\x17\x18\x92\x15\x15\x17\xf1\x16\x16\x17\xf3@@@\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\xed\x16\x16\x17\xf3\x16\x16\x18\x95\x1c\x1c\x1c%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$$$\x07\x16\x16\x18\x80\x16\x16\x18\xf8\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff   \x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x17\xfe\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf9\x16\x16\x18\x82   \x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x1b\x1b\x1c\x16\x16\x17\xd0\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff+++\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x17\xfd\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x17\xd2\x1a\x1a\x1a\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x1b/\x15\x15\x17\xe6\x15\x15\x17\xff\x15\x15\x17\xfc\x16\x16\x18\xb8\x16\x16\x18t\x16\x16\x19g\x16\x16\x18~UUU\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x17\xfc\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xe6\x16\x16\x1b/\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x1a\x1a\x1d\x15\x15\x17\xe6\x15\x15\x17\xff\x15\x15\x17\xfc\x18\x18\x18I\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x17\xfb\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xe6\x1a\x1a\x1a\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$$$\x07\x16\x16\x17\xd1\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\x9d\x00\x00\x00\x00\x15\x15 \x18\x16\x16\x18s\x15\x15\x17\x90\x17\x17\x19f$$$\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x1c\x1c\x12\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x17\xd1$$$\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\x81\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xf1\x1b\x1b\x1b\x1c\x1c\x1c\x1c%\x16\x16\x18\xeb\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x17\x17\x1aN\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x18\x18@\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x1c$\x16\x16\x18\xf9\x15\x15\x17\xff\x15\x15\x18\xee\x16\x16\x1aE\x15\x15+\x0c\x16\x16\x17\xcf\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x17\xc4\x80\x80\x80\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x18\xbf\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf8\x16\x16\x1d#\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\x94\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x17\x8e\x17\x17\x1aZ\x16\x16\x17\xd1\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xe2\x16\x16\x18\x80\x16\x16\x1aE\x1c\x1c\x1c\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"""\x0f\x17\x17\x17B\x17\x17\x19{\x16\x16\x17\xdb\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x17\x17\x18\x93\x00\x00\x00\x00\'\'\'\r\x15\x15\x17\xf2\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xfe\x16\x16\x18\x82333\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x80\x80\x02\x16\x16\x18t\x15\x15\x17\xfc\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xf2\x15\x15+\x0c\x16\x16\x19R\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x18`\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x19R\x15\x15\x19\x91\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xca\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\xb7\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x19\x91\x16\x16\x18\xc9\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x19\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x19G\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xc8\x16\x16\x18\xe1\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x17\x17\x17\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00   \x08\x16\x16\x18\xf8\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xe0\x16\x16\x18\xf5\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xf2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\xde\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf5\x16\x16\x17\xf3\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x18\xca\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x17\xf3\x15\x15\x18\xd9\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf4\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\xe1\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xd9\x15\x15\x18\xbf\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x1c\x1c\x1c%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00   \x10\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xbf\x16\x16\x18\x95\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18v\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x18a\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\x95\x16\x16\x19G\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf4\x19\x19\x19\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x1b\x1b\x13\x16\x16\x18\xeb\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x19G+++\x06\x15\x15\x17\xf1\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x19]\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x18\x18I\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xf1+++\x06\x00\x00\x00\x00\x16\x16\x18\x97\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x19\x19\x193\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x1a\x1a\x1e\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\x97\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15 \x18\x16\x16\x18\xf4\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x18\x18\x185\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15+\x0c\x18\x18\x18*\x80\x80\x80\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x01\x1b\x1b\x1b&\x1e\x1e\x1e\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x17\x17!\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf4\x15\x15 \x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x18\x82\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x17\x17\x19f\x00\x00\x00\x00@@@\x04\x17\x17\x17b\x16\x16\x17\xe7\x15\x15\x17\xff\x16\x16\x17\xf3\x16\x16\x17\xd2\x15\x15\x18\xc1\x15\x15\x18\xc0\x16\x16\x17\xd1\x15\x15\x17\xf0\x15\x15\x17\xff\x16\x16\x18\xed\x15\x15\x18l+++\x06\x00\x00\x00\x00\x16\x16\x19R\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\x82\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$$$\x07\x16\x16\x18\xc8\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xd6\x15\x15\x18\xa8\x16\x16\x18\xec\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xef\x15\x15\x18\xaa\x15\x15\x18\xcd\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xc8$$$\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15 \x18\x15\x15\x18\xe3\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xe3\x15\x15 \x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x1c.\x15\x15\x18\xe3\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x18\xe3\x16\x16\x1c.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15 \x18\x16\x16\x18\xc8\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xc8\x15\x15 \x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$$$\x07\x16\x16\x18\x82\x16\x16\x18\xf4\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x16\x16\x18\xf4\x16\x16\x18\x82$$$\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15 \x18\x16\x16\x18\x97\x15\x15\x17\xf1\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xff\x15\x15\x17\xf1\x16\x16\x18\x97\x15\x15 \x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00+++\x06\x16\x16\x19G\x16\x16\x18\x95\x15\x15\x18\xbf\x15\x15\x18\xd9\x16\x16\x17\xf3\x16\x16\x17\xf3\x15\x15\x18\xd9\x15\x15\x18\xbf\x16\x16\x18\x95\x16\x16\x19G+++\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

这样打印了 r 的两个属性，```text``` 和 ```content```。

前两行是 ```r.text```，出现了乱码，因为图片是二进制数据，转换为 ```str``` 类型时自然会乱码，最后一行是 ```r.content```，这是 ```bytes``` 类型数据。

这样 URL 实际上是 github 的图标：

![](../../images/Module_2/lecture_7_3.jpg)

我们可以将图片的二进制数据保存起来：

[程序](../../codes/Module_2/lecture_7/lecture_7_7.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://github.com/favicon.ico"
r = requests.get(url)
with open("favicon.ico", "wb") as f:
    f.write(r.content)
```

这里我们将数据以二进制形式写入了当前路径下。

运行后，可以在当前路线下看到 ```favicon.ico``` 的图标：

![](../../images/Module_2/lecture_7_4.jpg)

图片我们就成功保存了，对于视频和音频我们也是类型的方法。

---

## 添加 headers

在一个 HTTP 请求中，请求头是一个重要的组成部分，如果不设置请求头，网站发现它不是一个正常浏览器发起的，很可能会得不到预期结果。

Python 一键构造爬虫请求头，[参考](https://segmentfault.com/a/1190000019926385) 。

如果我们想添加一个 User-Agent 字段，我们可以从浏览器中得到：

![](../../images/Module_2/lecture_7_5.jpg)

之后可以如下操作，[程序](../../codes/Module_2/lecture_7/lecture_7_8.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, headers=headers)
print(r.text)
```

部分结果为：

```html

<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="icon" href="/static/img/favicon.ico">
    <title>Scrape | Movie</title>
    <link href="/static/css/app.css" type="text/css" rel="stylesheet">
    <link href="/static/css/index.css" type="text/css" rel="stylesheet">
</head>
<body>
<div id="app">
    ...
</div>
</body>
```

在 headers 参数中添加其他字段信息也是可以的。

---

## POST 请求

我们使用 POST 请求来访问 [http://httpbin.org/post](http://httpbin.org/post) 。

[示例](../../codes/Module_2/lecture_7/lecture_7_9.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

data = {
    "name": "germey",
    "age": "25"
}
url = "http://httpbin.org/post"
r = requests.post(url=url, data=data)
print(r.text)
```

结果为：

```json5
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "age": "25",
    "name": "germey"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "18",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.18.4",
    "X-Amzn-Trace-Id": "Root=1-5e71dfcd-d55d50bec263dd263752df20"
  },
  "json": null,
  "origin": "117.178.93.51",
  "url": "http://httpbin.org/post"
}
```

form 部分就是提交的数据，这就证明 POST 请求成功发送了。

---

## 响应

发送请求后，得到的是响应，即 Response。

在之前的实例中，我们使用 ```text``` 和 ```content``` 获取了响应的内容。此外，还有很多属性和方法可以用来获取其他信息，比如状态码，响应头，Cookies 等。

[示例](../../codes/Module_2/lecture_7/lecture_7_10.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)

print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)
```

结果为：

```text
<class 'int'> 200
<class 'requests.structures.CaseInsensitiveDict'> {'Server': 'nginx/1.17.8', 'Date': 'Wed, 18 Mar 2020 08:53:19 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Vary': 'Accept-Encoding', 'X-Frame-Options': 'SAMEORIGIN', 'Strict-Transport-Security': 'max-age=15724800; includeSubDomains', 'Content-Encoding': 'gzip'}
<class 'requests.cookies.RequestsCookieJar'> <RequestsCookieJar[]>
<class 'str'> https://static1.scrape.cuiqingcai.com/
<class 'list'> []
```

```status_code``` 属性得到状态码，```headers``` 属性得到响应头，```cookies``` 属性得到 ```Cookies```，```url``` 属性得到 URL，```history```
属性得到请求历史。

可以看出，headers 和 cookies 这两个属性得到的结果分别是 ```CaseInsensitiveDict``` 和 ```RequestsCookieJar``` 类型。

通过状态码，我们可以知道是否爬取成功，而 ```requests``` 提供了一个内置的状态码查询对象 ```requests.codes```。

[示例](../../codes/Module_2/lecture_7/lecture_7_11.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)

if not r.status_code == requests.codes.ok:
    exit()
else:
    print("Request Successfully")
```

结果为：

```text
Request Successfully
```

这里 ```requests.codes.ok``` 表示成功的状态码 200，这样我们就不用直接写数字了，而且使用字符串也更加直观。

对于其他状态码，我们可以查看 ```requests.codes``` 的源码：

```python
    # Informational.
    100: ('continue',),
    101: ('switching_protocols',),
    102: ('processing',),
    103: ('checkpoint',),
    122: ('uri_too_long', 'request_uri_too_long'),
    200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
    201: ('created',),
    202: ('accepted',),
    203: ('non_authoritative_info', 'non_authoritative_information'),
    204: ('no_content',),
    205: ('reset_content', 'reset'),
    206: ('partial_content', 'partial'),
    207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
    208: ('already_reported',),
    226: ('im_used',),

    # Redirection.
    300: ('multiple_choices',),
    301: ('moved_permanently', 'moved', '\\o-'),
    302: ('found',),
    303: ('see_other', 'other'),
    304: ('not_modified',),
    305: ('use_proxy',),
    306: ('switch_proxy',),
    307: ('temporary_redirect', 'temporary_moved', 'temporary'),
    308: ('permanent_redirect',
          'resume_incomplete', 'resume',),  # These 2 to be removed in 3.0

    # Client Error.
    400: ('bad_request', 'bad'),
    401: ('unauthorized',),
    402: ('payment_required', 'payment'),
    403: ('forbidden',),
    404: ('not_found', '-o-'),
    405: ('method_not_allowed', 'not_allowed'),
    406: ('not_acceptable',),
    407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
    408: ('request_timeout', 'timeout'),
    409: ('conflict',),
    410: ('gone',),
    411: ('length_required',),
    412: ('precondition_failed', 'precondition'),
    413: ('request_entity_too_large',),
    414: ('request_uri_too_large',),
    415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
    416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
    417: ('expectation_failed',),
    418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
    421: ('misdirected_request',),
    422: ('unprocessable_entity', 'unprocessable'),
    423: ('locked',),
    424: ('failed_dependency', 'dependency'),
    425: ('unordered_collection', 'unordered'),
    426: ('upgrade_required', 'upgrade'),
    428: ('precondition_required', 'precondition'),
    429: ('too_many_requests', 'too_many'),
    431: ('header_fields_too_large', 'fields_too_large'),
    444: ('no_response', 'none'),
    449: ('retry_with', 'retry'),
    450: ('blocked_by_windows_parental_controls', 'parental_controls'),
    451: ('unavailable_for_legal_reasons', 'legal_reasons'),
    499: ('client_closed_request',),

    # Server Error.
    500: ('internal_server_error', 'server_error', '/o\\', '✗'),
    501: ('not_implemented',),
    502: ('bad_gateway',),
    503: ('service_unavailable', 'unavailable'),
    504: ('gateway_timeout',),
    505: ('http_version_not_supported', 'http_version'),
    506: ('variant_also_negotiates',),
    507: ('insufficient_storage',),
    509: ('bandwidth_limit_exceeded', 'bandwidth'),
    510: ('not_extended',),
    511: ('network_authentication_required', 'network_auth', 'network_authentication'),
```

---

## 高级用法

刚才，我们了解了 ```requests``` 的基本用法，如基本的 GET，POST 请求以及 Response 对象。

这仅仅是冰山一角，```requests``` 几乎可以完成HTPP的所有操作。

接下来，我们将介绍 ```requests``` 库的高级用法，如文件上传，Cookies 设置，代理设置等等

---

### 文件上传

如果一个网站需要上传文件，我们可以使用 POST 请求实现。

[示例](../../codes/Module_2/lecture_7/lecture_7_12.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

file_path = "favicon.ico"
files = {
    "file": open(file_path, "rb")
}
url = "http://httpbin.org/post"
r = requests.post(url=url, files=files)

print(r.text)
```

结果为：

```json5
{
  "args": {},
  "data": "",
  "files": {
    "file": "data:application/octet-stream;base64,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AAAAAAAAKysrBhYWGUcWFhiVFRUYvxUVGNkWFhfzFhYX8xUVGNkVFRi/FhYYlRYWGUcrKysGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
  },
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "6665",
    "Content-Type": "multipart/form-data; boundary=22ee8820c2f949c7a662ade1c3f9b4f6",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.18.4",
    "X-Amzn-Trace-Id": "Root=1-5e71e564-5191e1c012596fb04fcfefe0"
  },
  "json": null,
  "origin": "117.178.93.51",
  "url": "http://httpbin.org/post"
}
```

这里我们上传指定路径下的 ```favicon.ico``` 文件，上传其他文件的操作类似，网站返回响应，里面包含 ```files``` 这个字段，而 ```form字``` 段是空的，这证明文件上传部分会单独有一个 ```files``` 字段来标识。

---

### Cookies

我们如果想用 ```requests``` 获取和设置 Cookies 也非常方便。

[过程](../../codes/Module_2/lecture_7/lecture_7_13.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://www.baidu.com/"
r = requests.get(url=url)

print(r.cookies)
for key, value in r.cookies.items():
    print(key + "=" + value)
```

结果为：

```textmate
<RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>
BDORZ=27315
```

这里我们首先调用 ```cookies``` 属性即可成功得到 Cookies，可以发现它是 ```RequestCookieJar``` 类型。然后用 ```items``` 方法将其转化为元组组成的列表，遍历输出每一个 Cookie 的名称和值，实现 Cookie 的遍历解析。

我们可以使用 Cookie 来维持登陆状态，以 Github 为例。

我们先登陆个人的 GitHub 账号，将 Headers 中的 Cookie 复制下来：

![](../../images/Module_2/lecture_7_6.jpg)

提取个人的 Cookie ，放到请求头 Headers 中，发送请求。

[示例](../../codes/Module_2/lecture_7/lecture_7_14.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

headers = {
    "Cookie": "_octo=GH1.1.1819589382.1584486488; _device_id=099cf2a13524a2c20ad62f0e91191d4d; _ga=GA1.2.813069593.1584486504; tz=Asia%2FShanghai; user_session=ReKP5u5LLH61NGCHZ7Dj4YlpvLt26tHIqIPIK-k9kLWgwp0B; __Host-user_session_same_site=ReKP5u5LLH61NGCHZ7Dj4YlpvLt26tHIqIPIK-k9kLWgwp0B; logged_in=yes; dotcom_user=Gedanke; _gh_sess=bBnIWA4C5jutpcfzayOqVqOHZZvOoX2I9EikNoCNSpNelUcxCvsKTOyKL9n8gjW6cSl08wHzYuEPtDa2NS%2BziQmaxyydldvS22jLFMrOj59jr68j8nDY2IxnTPZsN4rN7vC99Z9ktKubl01LwB%2FroOC3roPhnAabaXbmU1z%2BfF0viOxPDXhw8Su0MdRtVlu8WIEiLwfUdbRABefUVjMxN0OdhRXLOBKyFLLH23Y50wriV47UEy0UuZi0fbcrtW22sFUVk6XCw9tbJ4vCtxD8mScPZCTRyhZE7nGuYLYGsPs8xsZrIkBmEUk1gUXfUlDf%2B1SM5%2BHKhzIDKQkn6%2BSHEfXyMq%2FTJgrUBkFHKy7au%2FYn5zbdeC4aIBQ%2Bdj1U%2FlgaR8pMLiYZGaMPiefoeNdcE1og9jAVOjGG0HF9%2FjGirYVmbgKWReGrbu3Ypm6EXRGrCuCnuLzcjcVDMTl7n5ubq%2F3Le0Io6Wvk4xyIcxeK1OwcGnRtGNfjtGf66C4TTDv3ZLdPJdAxFJxcH2119FRFdXVVN843A%2Fw%2BcsgV6NFbinoXPXtj1ZVznLPD3lj79VwvD1zdgMbqPuuneyTAKWKMPOrZ5w%2B4BHoE0vl%2BHViGVlh07AkdZhfEmSDOPB945z2Z8nOawRjdmybxw%2FDlGGW2y9qHBcLK2BXlgnve0vFCr2bKyj7xPVlHkOFVV032OiiV0eIDsgN5QIsVIgiQwA2R05jO6%2Fu%2F27jerdRSPY72e49sC3ILPo07X%2FogPFnUiD7SNT63CUZHz3V%2FAU0b61esLCMgJjdmNFCTwhLqXGbjdL9tbZpQVr0VmIxOkadO76qK8Wjwl7BYtzctAInrnCS8Z6GTbzvdmO%2FOcmhRjapFANsuw6ma4PtYiScFeJb2NmUwTRJpFIVcOstsrzn2nbvAGp8IsXwn2PTff6XA9E3oca2b%2F71%2Fs3x9ub8EKCzs75%2F2zYnCS1sewoWp9O0ttxo0s0YWdjfSSrMrBhSw4UHgYY43pBFsFpVJetJbfvBCzSo6%2Bmzc8zqE2TqaREdtH73NXTlI%2BAo13VhYVY0%2BaLurI5cKoaGK2iuJrED5xMhtjGhMVbEl9%2BkQMBvca%2FMOVqBUivXcFB9xju7zOauUqQeDMmiXEhyHfMnRnp7LQsi8RuTfi4mXWpGJ6zyiUQS7Bm592jdV77O4oS5gLKdNHcW%2FHv0QAfP81oWPtHMGkB7YzEAaMN06IB%2BXnGYTv2%2Fljuc4Idj3c7A3ALAF5X3HDTIXZZtqM5R%2FvW2tvGNI%2Fr%2FKxKs4%2FmeK6qOoEWS6rDuw0lu9NlyCWGRJxly0QKUUIuhpICSOzg%2FNyurfwZMRdbydfXKo9rh25LbqPxncwxZ1LB81ZBkiclsu%2FwtnjmLmOTpElm4zfB2fPSY2xbsXVyTr07ibNuqCnXJJ5rkJVT773Q5RhOl2LzG7N6oKXEF42UeZUBdJugY31oISUdx8T13nwCtD36QX%2FuEREXzGMQrK%2B8Yt64u%2F6TWJFb9YcYP%2Bdo6eDTcEwgnRBgBgwdDc%2Bg69R2pT2dDn%2B9wi%2BFDIBIuf00yUwzO7WE8skh1b%2FR4ElaEcicPNfmvUX5P9Be4G32WlGCfS0V%2FoQp4QDMt1my47syqBFvrM5RwHfdo9ITwXolR9%2BSsU0r6VTrZWKjvdsaM19AnJ6iCAu7td43YzOf%2BV35hZA2mCi7OePKqRbg%2BWaElXDMJm%2F4R0Fwoie%2B7R1PEPIFpxPcJO%2FpWpbFTziYmgDuOJy%2BWP7L2mIptMe0TZB%2B90TLJejOY4zVWx1FVjZ5qtULq99Ls7%2B%2B0dYQqaTzcCua4FGmXyajMOaOi6T%2FqoIqLFehIDTbNGGvryP4QSC6woVSihpCf7XNC1ALVIfvTu--5lqrnPABlumLAeh2--FIRpm6tm1fHIQ%2FqiVWwqVg%3D%3D",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
url = "https://github.com/"

r = requests.get(url=url, headers=headers)
print(r.text)
```

部分结果如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    ...
</head>
<body class="logged-in env-production page-responsive full-width">
...
<summary class="Header-link"
         aria-label="View profile and more"
         data-ga-click="Header, show menu, icon:avatar">
    <img class="avatar " alt="@Gedanke" width="20" height="20"
         src="https://avatars3.githubusercontent.com/u/47662202?s=60&amp;u=c88f77d663ceb55358e5b1f285b0e45a870f25f8&amp;v=4">
    <span class="feature-preview-indicator js-feature-preview-indicator" hidden></span>
    <span class="dropdown-caret"></span>
</summary>
...
</body>
</html>
```

可以发现返回的结果中包含了登陆后才能显示的内容，如我的用户名，如果你尝试同样的操作也可以得到你的个人信息。

这样，我们用 Cookies 成功模拟登陆了，登陆后的内容都可以访问了。

当然，我们也可以通过 ```cookies``` 参数来设置 Cookies 的信息，这里我们可以构造一个 ```RequestsCookieJar``` 对象，然后把刚才复制的 Cookie 处理下并赋值。

[示例](../../codes/Module_2/lecture_7/lecture_7_15.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests
from requests.cookies import RequestsCookieJar

cookies = "_octo=GH1.1.1819589382.1584486488; _device_id=099cf2a13524a2c20ad62f0e91191d4d; _ga=GA1.2.813069593.1584486504; tz=Asia%2FShanghai; user_session=ReKP5u5LLH61NGCHZ7Dj4YlpvLt26tHIqIPIK-k9kLWgwp0B; __Host-user_session_same_site=ReKP5u5LLH61NGCHZ7Dj4YlpvLt26tHIqIPIK-k9kLWgwp0B; logged_in=yes; dotcom_user=Gedanke; _gh_sess=bBnIWA4C5jutpcfzayOqVqOHZZvOoX2I9EikNoCNSpNelUcxCvsKTOyKL9n8gjW6cSl08wHzYuEPtDa2NS%2BziQmaxyydldvS22jLFMrOj59jr68j8nDY2IxnTPZsN4rN7vC99Z9ktKubl01LwB%2FroOC3roPhnAabaXbmU1z%2BfF0viOxPDXhw8Su0MdRtVlu8WIEiLwfUdbRABefUVjMxN0OdhRXLOBKyFLLH23Y50wriV47UEy0UuZi0fbcrtW22sFUVk6XCw9tbJ4vCtxD8mScPZCTRyhZE7nGuYLYGsPs8xsZrIkBmEUk1gUXfUlDf%2B1SM5%2BHKhzIDKQkn6%2BSHEfXyMq%2FTJgrUBkFHKy7au%2FYn5zbdeC4aIBQ%2Bdj1U%2FlgaR8pMLiYZGaMPiefoeNdcE1og9jAVOjGG0HF9%2FjGirYVmbgKWReGrbu3Ypm6EXRGrCuCnuLzcjcVDMTl7n5ubq%2F3Le0Io6Wvk4xyIcxeK1OwcGnRtGNfjtGf66C4TTDv3ZLdPJdAxFJxcH2119FRFdXVVN843A%2Fw%2BcsgV6NFbinoXPXtj1ZVznLPD3lj79VwvD1zdgMbqPuuneyTAKWKMPOrZ5w%2B4BHoE0vl%2BHViGVlh07AkdZhfEmSDOPB945z2Z8nOawRjdmybxw%2FDlGGW2y9qHBcLK2BXlgnve0vFCr2bKyj7xPVlHkOFVV032OiiV0eIDsgN5QIsVIgiQwA2R05jO6%2Fu%2F27jerdRSPY72e49sC3ILPo07X%2FogPFnUiD7SNT63CUZHz3V%2FAU0b61esLCMgJjdmNFCTwhLqXGbjdL9tbZpQVr0VmIxOkadO76qK8Wjwl7BYtzctAInrnCS8Z6GTbzvdmO%2FOcmhRjapFANsuw6ma4PtYiScFeJb2NmUwTRJpFIVcOstsrzn2nbvAGp8IsXwn2PTff6XA9E3oca2b%2F71%2Fs3x9ub8EKCzs75%2F2zYnCS1sewoWp9O0ttxo0s0YWdjfSSrMrBhSw4UHgYY43pBFsFpVJetJbfvBCzSo6%2Bmzc8zqE2TqaREdtH73NXTlI%2BAo13VhYVY0%2BaLurI5cKoaGK2iuJrED5xMhtjGhMVbEl9%2BkQMBvca%2FMOVqBUivXcFB9xju7zOauUqQeDMmiXEhyHfMnRnp7LQsi8RuTfi4mXWpGJ6zyiUQS7Bm592jdV77O4oS5gLKdNHcW%2FHv0QAfP81oWPtHMGkB7YzEAaMN06IB%2BXnGYTv2%2Fljuc4Idj3c7A3ALAF5X3HDTIXZZtqM5R%2FvW2tvGNI%2Fr%2FKxKs4%2FmeK6qOoEWS6rDuw0lu9NlyCWGRJxly0QKUUIuhpICSOzg%2FNyurfwZMRdbydfXKo9rh25LbqPxncwxZ1LB81ZBkiclsu%2FwtnjmLmOTpElm4zfB2fPSY2xbsXVyTr07ibNuqCnXJJ5rkJVT773Q5RhOl2LzG7N6oKXEF42UeZUBdJugY31oISUdx8T13nwCtD36QX%2FuEREXzGMQrK%2B8Yt64u%2F6TWJFb9YcYP%2Bdo6eDTcEwgnRBgBgwdDc%2Bg69R2pT2dDn%2B9wi%2BFDIBIuf00yUwzO7WE8skh1b%2FR4ElaEcicPNfmvUX5P9Be4G32WlGCfS0V%2FoQp4QDMt1my47syqBFvrM5RwHfdo9ITwXolR9%2BSsU0r6VTrZWKjvdsaM19AnJ6iCAu7td43YzOf%2BV35hZA2mCi7OePKqRbg%2BWaElXDMJm%2F4R0Fwoie%2B7R1PEPIFpxPcJO%2FpWpbFTziYmgDuOJy%2BWP7L2mIptMe0TZB%2B90TLJejOY4zVWx1FVjZ5qtULq99Ls7%2B%2B0dYQqaTzcCua4FGmXyajMOaOi6T%2FqoIqLFehIDTbNGGvryP4QSC6woVSihpCf7XNC1ALVIfvTu--5lqrnPABlumLAeh2--FIRpm6tm1fHIQ%2FqiVWwqVg%3D%3D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
url = "https://github.com/"
jar = RequestsCookieJar()
for cookie in cookies.split(";"):
    key, value = cookie.split("=", 1)
    jar.set(key, value)

r = requests.get(url=url, cookies=jar, headers=headers)
print(r.text)
```

正常登陆。

这里我们首先新建一个 ```RequestCookieJar``` 对象，然后将复制下来的 cookies 利用 ```split``` 方法分割，接着利用 ```set``` 方法设置好每个 Cookie 的 ```key``` 和 ```value```，最后通过调用 ```requests``` 的 ```get``` 方法并传递给 cookies 参数即可。

---

### Session 维持

在之前的案例中，我们用 GET 和 POST 方法模拟请求，实际上两个请求对应 Session 是不同的，那么 Cookies 也是不同的，相对于你用两个浏览器打开了不同的页面。

在用多种请求方式访问网站，我们不希望每次请求都设置 Cookies，所以我们需要维护一个 Session，这便是 Session 对象了。

[示例](../../codes/Module_2/lecture_7/lecture_7_16.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

requests.get("http://httpbin.org/cookies/set/number/123456789")
r = requests.get("http://httpbin.org/cookies")
print(r.text)
```

结果为，运行时间较长：

```json5
{
  "cookies": {}
}
```

这里我们请求了一个测试网址 [http://httpbin.org/cookies/set/number/123456789](http://httpbin.org/cookies/set/number/123456789) 。请求这个网址时，可以设置一个 cookie，名称叫作 number，内容是 123456789，随后又请求了 [http://httpbin.org/cookies](http://httpbin.org/cookies) ，此网址可以获取当前的 Cookies。

没有得到，使用 Session 试试。

[程序](../../codes/Module_2/lecture_7/lecture_7_17.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

s = requests.Session()
s.get("http://httpbin.org/cookies/set/number/123456789")
r = s.get("http://httpbin.org/cookies")
```

结果为，运行时间较长：

```json
{
  "cookies": {
    "number": "123456789"
  }
}
```

利用 Session，可以做到模拟同一个 Session 而不用担心 Cookies 的问题。它通常用于模拟登录成功之后再进行下一步的操作。

---

### SSL 证书验证

之前我们说过，HTTPS 比 HTTP 更安全，如果有些网站没有设置 HTTPS 证书，或者网站的 HTTPS 证书不被 CA 机构认可，在浏览器中打开这些 URL 时就会出现 SSL 证书错误。

以 [https://static2.scrape.cuiqingcai.com/](https://static2.scrape.cuiqingcai.com/) 为例，使用 Chrome 打开它，会出现以下提示。

![](../../images/Module_2/lecture_7_7.jpg)

我们可以在浏览器中通过一些设置来忽略证书的验证。

但是如果我们想用 ```requests``` 来请求这类网站，会遇到什么问题呢？

[示例](../../codes/Module_2/lecture_7/lecture_7_18.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://static2.scrape.cuiqingcai.com/"
response = requests.get(url)
print(response.status_code)
```

报错了：

```textmate
requests.exceptions.SSLError: HTTPSConnectionPool(host='static2.scrape.cuiqingcai.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')])")))
```

抛出了 ```SSLError``` 错误，因为我们请求的 URL 的证书是无效的。

这类网站在浏览器中也是可以访问的，同样的，它也是可以爬取的。

我们可以使用 ```verify``` 参数控制是否验证证书，如果将其设置为 ```False```，在请求时就不会再验证证书是否有效。如果不加 ```verify``` 参数的话，默认值是 ```True```，会自动验证。

稍微改写，[如下](../../codes/Module_2/lecture_7/lecture_7_19.py) ：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://static2.scrape.cuiqingcai.com/"
response = requests.get(url, verify=False)
print(response.status_code)
```

结果为：

```textmate
C:\Users\hasee\AppData\Roaming\Python\Python37\site-packages\urllib3\connectionpool.py:858: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
200
```

请求成功了。

它给出了一个警告，建议我们给它指定证书。我们可以通过设置忽略警告的方式来屏蔽这个警告。

[程序](../../codes/Module_2/lecture_7/lecture_7_20.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests
import urllib3

urllib3.disable_warnings()
url = "https://static2.scrape.cuiqingcai.com/"
response = requests.get(url, verify=False)
print(response.status_code)
```

或者通过捕获警告到日志的方式忽略警告，[如下](../../codes/Module_2/lecture_7/lecture_7_21.py) ：

```python
# -*- coding: utf-8 -*-

import requests
import logging

logging.captureWarnings(True)
url = "https://static2.scrape.cuiqingcai.com/"
response = requests.get(url, verify=False)
print(response.status_code)
```

当然，我们也可以指定一个本地证书用作客户端证书，这可以是单个文件(包含密钥和证书)或一个包含两个文件路径的元组：```crt``` 和 ```key``` 文件，并且指定它们的路径。另外注意，本地私有证书的 ```key``` 必须是解密状态，加密状态的 ```key``` 是不支持的。

---

### 超时设置

有时候会因为网络等其他原因很久才能收到响应，甚至收不到响应。为了避免服务器不能及时响应，应设置一个超时时间，超过该时间未响应就应该报错。可以使用timeout参数，这个时间的计算的是发出请求到服务器返回响应的时间。

[示例](../../codes/Module_2/lecture_7/lecture_7_22.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

r = requests.get("http://httpbin.org/get", timeout=1)
print(r.status_code)
```

可能响应，也可能不响应。

我们将超时时间设置为 1 秒，如果 1 秒内没有响应，那就抛出异常。

实际上，请求分为两个阶段，即连接 (connect) 和读取 (read)。 上面设置的 ```timeout``` 将用作连接和读取这二者的 ```timeout``` 总和，如果要分别指定，就可以传入一个元组。

```python
r = requests.get("http://httpbin.org/get", timeout=(5, 30))
```

如果想永久等待，可以直接将 ```timeout``` 设置为 ```None```，或者不设置直接留空，这样我们就会一直等待响应。

```python
r = requests.get("http://httpbin.org/get", timeout=None)
```

或者不加参数：

```python
r = requests.get("http://httpbin.org/get")
```

---

### 身份认证

在访问某些设置了身份认证的网站时，例如：[https://static3.scrape.cuiqingcai.com/](https://static3.scrape.cuiqingcai.com/) ，我们可能会遇到这样的认证窗口，如图所示：

![](../../images/Module_2/lecture_7_8.jpg)

这种情况是该网站启用了基本身份认证，英文叫作 ```HTTPBasicAccessAuthentication```，它是一种用来允许网页浏览器或其他客户端程序在请求时提供用户名和口令形式的身份凭证的一种登录验证方式。

遇到这种情况，我们可以使用 ```requests``` 自带的身份认证功能，通过 ```auth``` 参数即可设置。

[示例](../../codes/Module_2/lecture_7/lecture_7_23.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth

url = "https://static3.scrape.cuiqingcai.com/"
r = requests.get(url, auth=HTTPBasicAuth("admin", "admin"))
print(r.status_code)
```

结果为：

```text
200
```

这个示例网站的用户名和密码都是 admin，直接设置即可。

如果用户名和密码正确的话，请求时会自动认证成功，返回 200 状态码；如果认证失败，则返回 401 状态码。

不是有 ```HTTPBasicAuth```，直接传入一个元组也是可以的，它会默认使用 ```HTTPBasicAuth``` 这个类来认证。

简写 [如下](../../codes/Module_2/lecture_7/lecture_7_24.py) ：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://static3.scrape.cuiqingcai.com/"
r = requests.get(url, auth=("admin", "admin"))
print(r.status_code)
```

此外，```requests``` 还提供了其他认证方式，如 ```OAuth``` 认证，不过此时需要安装 ```oauth``` 包，安装命令如下：

```shell script
pip3 install requests_oauthlib
```

```requests_oauthlib``` 更多内容可参考其 [官方文档](https://requests-oauthlib.readthedocs.org/) 。

---

### 代理设置

如果我们使用单一 ip 频繁请求网站，网站可能会弹出验证码，或者跳转到登录认证页面，更甚者可能会直接封禁客户端的 IP，导致一定时间段内无法访问。

我们可以设置代理来避免这些问题，需要 ```proxies``` 参数。

[示例](../../codes/Module_2/lecture_7/lecture_7_25.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

url = "https://httpbin.org/get"
proxies = {
    "http": "http://10.10.10.10:1080",
    "https": "http://10.10.10.10:1080",
}
r = requests.get(url=url, proxies=proxies)
print(r)
```

报错了，这样八成不行，这要都可以的话，代理 ip 的厂家可以喝西北风去了。。。

我们可以直接搜索寻找有效的代理并替换试验一下。

若代理需要使用上文所述的身份认证，可以使用类似```http://user:password@host:port```这样的语法来设置代理，示例如下：

[示例](../../codes/Module_2/lecture_7/lecture_7_26.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

proxies = {
    "https": "http://user:password@10.10.10.10:1080/",
}
url = "https://httpbin.org/get"
requests.get(url, proxies=proxies)
```

除了基本的 HTTP 代理外，```requests``` 还支持 SOCKS 协议的代理。

首先，需要安装socks这个库：

```shell script
pip3 install "requests[socks]"
```

然后就可以使用 SOCKS 协议代理了。

[示例](../../codes/Module_2/lecture_7/lecture_7_26.py) 如下：

```python
# -*- coding: utf-8 -*-

import requests

proxies = {
    "http": "socks5://user:password@host:port",
    "https": "socks5://user:password@host:port",
}
url = "https://httpbin.org/get"
requests.get(url, proxies=proxies)
```

---

### Prepared Request

```requests``` 在发送请求时会构造一个 Request 对象，并给该对象赋予各种参数，包括 url，headers，data 等等。

下面我们尝试构造一个 Prepared Request 对象。

[示例](../../codes/Module_2/lecture_7/lecture_7_28.py) 如下：

```python
# -*- coding: utf-8 -*-

from requests import Request, Session

url = "http://httpbin.org/post"
data = {
    "name": "germey"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
s = Session()
req = Request("POST", url=url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)

print(r.text)
```

结果为：

```json5
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "name": "germey"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "11",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-5e732921-8aa94b987b7b42903544f248"
  },
  "json": null,
  "origin": "117.178.92.249",
  "url": "http://httpbin.org/post"
}
```

可以看出，我们得到了 POST 相同的请求效果，这样的方式显然更加灵活。

更多Request内容可参考官方文档：[http://docs.python-requests.org/](http://docs.python-requests.org/) 。
