# 代理的基本原理和用法

做爬虫的过程中经常会遇到这样的情况，最初爬虫正常运行，正常抓取数据，然而之后可能就会出现错误，比如 403 Forbidden，这时候打开网页一看，可能会看到 “您的 IP 访问频率太高”
这样的提示，或者跳出一个验证码让我们输入，输入之后才可能解封，但是输入之后过一会儿就又这样了。

出现这种现象的原因是网站采取了一些反爬虫措施，比如服务器会检测某个 IP 在单位时间内的请求次数，如果超过了这个阈值，那么会直接拒绝服务，返回一些错误信息，这种情况可以称之为封 IP，于是乎就成功把我们的爬虫禁掉了。

既然服务器检测的是某个 IP 单位时间的请求次数，那么我们借助某种方式来伪装我们的 IP，让服务器识别不出是由我们本机发起的请求，不就可以成功防止封 IP 了吗？所以这时候代理就派上用场了。

本课时我们先来看下代理的基本原理和使用代理处理反爬虫的方法。

---
---

## 基本原理

代理实际上指的就是代理服务器，英文叫作 ```proxy server```，它的功能是代理网络用户去获取网络信息。形象地说，它是网络信息的中转站。在我们正常请求一个网站时，是发送了请求给 Web 服务器，Web
服务器把响应传回给我们。如果设置了代理服务器，实际上就是在本机和服务器之间搭建了一个桥，此时本机不是直接向 Web 服务器发起请求，而是向代理服务器发出请求，请求会发送给代理服务器，然后由代理服务器再发送给 Web
服务器，接着由代理服务器再把 Web 服务器返回的响应转发给本机。这样我们同样可以正常访问网页，但这个过程中 Web 服务器识别出的真实 IP 就不再是我们本机的 IP 了，就成功实现了 IP 伪装，这就是代理的基本原理。

---

## 代理的作用

那么，代理有什么作用呢？我们可以简单列举如下。

* 突破自身 IP 访问限制，访问一些平时不能访问的站点
* 访问一些单位或团体内部资源，如使用教育网内地址段免费代理服务器，就可以用于对教育网开放的各类 FTP 下载上传，以及各类资料查询共享等服务
* 提高访问速度，通常代理服务器都设置一个较大的硬盘缓冲区，当有外界的信息通过时，也将其保存到缓冲区中，当其他用户再访问相同的信息时， 则直接由缓冲区中取出信息，传给用户，以提高访问速度
* 隐藏真实 IP，上网者也可以通过这种方法隐藏自己的 IP，免受攻击，对于爬虫来说，我们用代理就是为了隐藏自身 IP，防止自身的 IP 被封锁

---

## 爬虫代理

对于爬虫来说，由于爬虫爬取速度过快，在爬取过程中可能遇到同一个 IP 访问过于频繁的问题，此时网站就会让我们输入验证码登录或者直接封锁 IP，这样会给爬取带来极大的不便。

使用代理隐藏真实的 IP，让服务器误以为是代理服务器在请求自己。这样在爬取过程中通过不断更换代理，就不会被封锁，可以达到很好的爬取效果。

---

## 代理分类

代理分类时，既可以根据协议区分，也可以根据其匿名程度区分，下面分别总结如下：

---

### 根据协议区分

根据代理的协议，代理可以分为如下类别：

* FTP 代理服务器，主要用于访问 FTP 服务器，一般有上传、下载以及缓存功能，端口一般为 21、2121 等
* HTTP 代理服务器，主要用于访问网页，一般有内容过滤和缓存功能，端口一般为 80、8080、3128 等
* SSL/TLS 代理，主要用于访问加密网站，一般有 SSL 或 TLS 加密功能(最高支持 128 位加密强度)，端口一般为 443
* RTSP 代理，主要用于 Realplayer 访问 Real 流媒体服务器，一般有缓存功能，端口一般为 554
* Telnet 代理，主要用于 telnet 远程控制(黑客入侵计算机时常用于隐藏身份)，端口一般为 23
* POP3/SMTP 代理，主要用于 POP3/SMTP 方式收发邮件，一般有缓存功能，端口一般为 110/25
* SOCKS 代理，只是单纯传递数据包，不关心具体协议和用法，所以速度快很多，一般有缓存功能，端口一般为 1080。SOCKS 代理协议又分为 SOCKS4 和 SOCKS5，SOCKS4 协议只支持 TCP，而 SOCKS5 协议支持
  TCP 和 UDP，还支持各种身份验证机制、服务器端域名解析等。简单来说，SOCK4 能做到的 SOCKS5 都可以做到，但 SOCKS5 能做到的 SOCK4 不一定能做到

---

### 根据匿名程度区分

根据代理的匿名程度，代理可以分为如下类别。

* 高度匿名代理，高度匿名代理会将数据包原封不动的转发，在服务端看来就好像真的是一个普通客户端在访问，而记录的 IP 是代理服务器的 IP
* 普通匿名代理，普通匿名代理会在数据包上做一些改动，服务端上有可能发现这是个代理服务器，也有一定几率追查到客户端的真实 IP。代理服务器通常会加入的 HTTP 头有 ```HTTP_VIA```
  和 ```HTTP_X_FORWARDED_FOR```
* 透明代理，透明代理不但改动了数据包，还会告诉服务器客户端的真实 IP。这种代理除了能用缓存技术提高浏览速度，能用内容过滤提高安全性之外，并无其他显著作用，最常见的例子是内网中的硬件防火墙
* 间谍代理，间谍代理指组织或个人创建的，用于记录用户传输的数据，然后进行研究、监控等目的的代理服务器

---

### 常见代理类型

* 使用网上的免费代理，最好使用高匿代理，使用前抓取下来筛选一下可用代理，也可以进一步维护一个代理池
* 使用付费代理服务，互联网上存在许多代理商，可以付费使用，质量比免费代理好很多
* ADSL 拨号，拨一次号换一次 IP，稳定性高，也是一种比较有效的解决方案
* 蜂窝代理，即用 4G 或 5G 网卡等制作的代理，由于蜂窝网络用作代理的情形较少，因此整体被封锁的几率会较低，但搭建蜂窝代理的成本较高

---

## 代理设置

在前面我们介绍了多种请求库，如 ```Requests、Selenium、Pyppeteer``` 等。我们接下来首先贴近实战，了解一下代理怎么使用，为后面了解代理池打下基础。

下面我们来梳理一下这些库的代理的设置方法。

做测试之前，我们需要先获取一个可用代理。搜索引擎搜索 “代理”
关键字，就可以看到许多代理服务网站，网站上会有很多免费或付费代理，比如免费代理“快代理”：[https://www.kuaidaili.com/free/](https://www.kuaidaili.com/free/)。但是这些免费代理大多数情况下都是不好用的，所以比较靠谱的方法是购买付费代理。付费代理各大代理商家都有套餐，数量不用多，稳定可用即可，我们可以自行选购。

如果本机有相关代理软件的话，软件一般会在本机创建 HTTP 或 SOCKS 代理服务，本机直接使用此代理也可以。

在这里，我的本机安装了一部代理软件，它会在本地的 8889 端口上创建 HTTP 代理服务，即代理为 ```127.0.0.1:8889```，另外还会在 8889 端口创建 SOCKS
代理服务，即代理为 ```127.0.0.1:8889```。

我只要设置了这个代理，就可以成功将本机 IP 切换到代理软件连接的服务器的 IP
了。下面的示例里，我将使用上述代理来演示其设置方法，你也可以自行替换成自己的可用代理。设置代理后测试的网址是：http://httpbin.org/get，我们访问该网址可以得到请求的相关信息，其中 ```origin```
字段就是客户端的 IP，我们可以根据它来判断代理是否设置成功，即是否成功伪装了 IP。

---

### requests 设置代理

对于 ```requests``` 来说，代理设置非常简单，我们只需要传入 ```proxies``` 参数即可。

我在这里以我本机的代理为例，来看下 ```requests``` 的 HTTP 代理的设置，[代码](../../codes/Module_4/lecture_20/lecture_20_1.py)如下：

```python
# -*- coding: utf-8 -*-

import requests

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
proxy = '127.0.0.1:8889'

'''https://github.com/urllib3/urllib3/issues/2075'''
proxies = {
    'https': 'http://' + proxy
}
try:
    response = requests.get('https://httpbin.org/get', headers=headers, proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
```

```json5
{
  "args": {},
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Host": "httpbin.org",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-60c30cff-183667a471a3727242a11441"
  },
  "origin": "18.166.63.222",
  "url": "https://httpbin.org/get"
}
```

可以发现，我们通过一个字典的形式就设置好了 HTTP 代理，它分为两个类别，有 HTTP 和 HTTPS，如果我们访问的链接是 HTTP 协议，那就用 http 字典名指定的代理，如果是 HTTPS 协议，那就用 https
字典名指定的代理。

其运行结果的 ```origin``` 如是代理服务器的 IP，则证明代理已经设置成功。

如果代理需要认证，同样在代理的前面加上用户名密码即可，代理的写法就变成如下所示：

```python
proxy = 'username:password@127.0.0.1:7890'
```

这里只需要将 ```username``` 和 ```password``` 替换即可。

如果需要使用 SOCKS 代理，则可以使用如下方式来设置，[代码](../../codes/Module_4/lecture_20/lecture_20_2.py)如下：

```python
# -*- coding: utf-8 -*-

import requests

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
proxy = '127.0.0.1:1089'
proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy
}
try:
    response = requests.get('https://httpbin.org/get', headers=headers, proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
```

在这里，我们需要额外安装一个包，这个包叫作 ```requests[socks]```，安装命令如下所示：

```shell
pip3 install "requests[socks]"
```

运行结果是完全相同的：

```json5
{
  "args": {},
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Host": "httpbin.org",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-60c30eab-1dcad83d407517756658e8cb"
  },
  "origin": "18.166.63.222",
  "url": "https://httpbin.org/get"
}
```

另外，还有一种设置方式即使用 ```socks``` 模块，也需要像上文一样安装 ```socks``` 库。这种设置方法[如下](../../codes/Module_4/lecture_20/lecture_20_3.py)所示：

```python
# -*- coding: utf-8 -*-

import requests
import socks
import socket

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1089)
socket.socket = socks.socksocket
try:
    response = requests.get('https://httpbin.org/get', headers=headers)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
```

使用这种方法也可以设置 SOCKS 代理，运行结果完全相同。相比第一种方法，此方法是全局设置。我们可以在不同情况下选用不同的方法。

---

### Selenium 设置代理

Selenium 同样可以设置代理，在这里以 Chrome 为例来介绍下其设置方法。

对于无认证的代理，设置方法[如下](../../codes/Module_4/lecture_20/lecture_20_4.py)：

```python
# -*- coding: utf-8 -*-

from selenium import webdriver

proxy = '127.0.0.1:8889'
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--proxy-server=http://" + proxy)
browser = webdriver.Chrome(options=options)
browser.get('https://httpbin.org/get')
print(browser.page_source)
browser.close()
```

运行结果如下：

```html

<html>
<head></head>
<body>
<pre style="word-wrap: break-word; white-space: pre-wrap;">{
  "args": {}, 
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-US", 
    "Host": "httpbin.org", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-60c31075-286ac03b6f5a535a6e743314"
  }, 
  "origin": "18.166.63.222", 
  "url": "https://httpbin.org/get"
}
</pre>
</body>
</html>
```

代理设置成功，```origin``` 同样为代理 IP 的地址。

如果代理是认证代理，则设置方法相对比较麻烦，设置方法[如下](../../codes/Module_4/lecture_20/lecture_20_5.py)所示：

```python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

ip = '127.0.0.1'
port = 8889
username = 'foo'
password = 'bar'

manifest_json = """{"version":"1.0.0","manifest_version": 2,"name":"Chrome Proxy","
permissions": ["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],"background":
{"scripts": ["background.js"]
} }
"""
background_js = """
var config = { mode: "fixed_servers", rules: { singleProxy: { scheme: "http", host: "%(ip) s", port: %(port) s } } }

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) { return { authCredentials: {username: "%(username) s", password: "%(password) s"
} } }

chrome.webRequest.onAuthRequired.addListener(
callbackFn, {urls: ["<all_urls>"]},
['blocking']
)
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}

plugin_file = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
zp.writestr("background.js", background_js)
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_extension(plugin_file)
browser = webdriver.Chrome(options=options)
browser.get('https://httpbin.org/get')
print(browser.page_source)
browser.close()
```

这里需要在本地创建一个 ```manifest.json``` 配置文件和 ```background.js``` 脚本来设置认证代理。运行代码之后本地会生成一个 ```proxy_auth_plugin.zip``` 文件来保存当前配置。

运行结果和上例一致，```origin``` 同样为代理 IP。

SOCKS 代理的设置也比较简单，把对应的协议修改为 ```socks5``` 即可，如无密码认证的代理设置[方法](../../codes/Module_4/lecture_20/lecture_20_6.py)为：

```python
# -*- coding: utf-8 -*-

from selenium import webdriver

proxy = '127.0.0.1:1089'
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--proxy-server=socks5://" + proxy)
browser = webdriver.Chrome(options=options)
browser.get('https://httpbin.org/get')
print(browser.page_source)
browser.close()
```

运行结果是一样的。

---

### aiohttp 设置代理

对于 ```aiohttp``` 来说，我们可以通过 ```proxy``` 参数直接设置即可，HTTP 代理设置[如下](../../codes/Module_4/lecture_20/lecture_20_7.py)：

```python
# -*- coding: utf-8 -*-


import asyncio
import aiohttp

proxy = 'http://127.0.0.1:8889'

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}


async def main():
    """

    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get', headers=headers, proxy=proxy) as response:
            print(await response.text())


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
```

如果代理有用户名密码，像 ```requests``` 一样，把 ```proxy``` 修改为如下内容：

```shell
proxy = 'http://username:password@127.0.0.1:7890'
```

这里只需要将 ```username``` 和 ```password``` 替换即可。

对于 SOCKS 代理，我们需要安装一个支持库，叫作 ```aiohttp-socks```，安装命令如下：

```shell
pip3 install aiohttp-socks
```

可以借助于这个库的 ```ProxyConnector``` 来设置 SOCKS 代理，[代码](../../codes/Module_4/lecture_20/lecture_20_8.py)如下：

```python
# -*- coding: utf-8 -*-


import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

connector = ProxyConnector.from_url('socks5://127.0.0.1:1089')


async def main():
    """

    :return:
    """
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get('https://httpbin.org/get', headers=headers) as response:
            print(await response.text())


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
```

运行结果是一样的。

另外这个库还支持设置 SOCKS4、HTTP 代理以及对应的代理认证，可以参考其官方介绍。

---

### Pyppeteer 设置代理

对于 Pyppeteer 来说，由于其默认使用的是类似 Chrome 的 Chromium 浏览器，因此设置方法和 Selenium 的 Chrome 是一样的，如 HTTP 无认证代理设置方法都是通过 ```args```
来设置，[实现](../../codes/Module_4/lecture_20/lecture_20_9.py)如下：

```python
# -*- coding: utf-8 -*-


import asyncio
from pyppeteer import launch

proxy = '127.0.0.1:8889'


async def main():
    """
    
    :return: 
    """
    browser = await  launch(
        {'args': ['--proxy-server=http://' + proxy], 'headless': True}
    )
    page = await  browser.newPage()
    await  page.goto('https://httpbin.org/get')
    print(await  page.content())
    await  browser.close()


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
```

运行结果：

```html

<html>
<head></head>
<body>
<pre style="word-wrap: break-word; white-space: pre-wrap;">{
  "args": {}, 
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-US,en;q=0.9", 
    "Host": "httpbin.org", 
    "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\"", 
    "Sec-Ch-Ua-Mobile": "?0", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4403.0 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-60c31db4-69c8860e35378d2a4f606793"
  }, 
  "origin": "18.166.63.222", 
  "url": "https://httpbin.org/get"
}
</pre>
</body>
</html>
```

同样可以看到设置成功。

对于 SOCKS 代理，也是一样的，只需要将协议修改为 ```socks5``` 即可，[代码](../../codes/Module_4/lecture_20/lecture_20_10.py)实现如下：

```python
# -*- coding: utf-8 -*-


import asyncio
from pyppeteer import launch

proxy = '127.0.0.1:1089'


async def main():
    """

    :return:
    """
    browser = await launch(
        {'args': ['--proxy-server=socks5://' + proxy], 'headless': True}
    )
    page = await browser.newPage()
    await page.goto('https://httpbin.org/get')
    print(await page.content())
    await browser.close()


if __name__ == '__main__':
    """"""
    asyncio.get_event_loop().run_until_complete(main())
```

运行结果也是一样的。

---

## 总结

以上总结了各个库的代理使用方式，以后如果遇到封 IP 的问题，我们就可以轻松通过加代理的方式来解决

---
---

