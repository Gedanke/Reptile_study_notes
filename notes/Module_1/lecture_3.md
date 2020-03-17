# 爬虫基本原理

如果互联网是一张蜘蛛网，那爬虫就是网上的蜘蛛，每一个节点相对于一个个网页，节点之间的连线可以看着网页间的链接关系。爬虫到了某一个节点，该网页的信息就被获取了，如果我们使用一些方式，能够使爬虫自行访问节点并进行处理，就可以自动得到我们预期的数据和信息了。

<br>

## 爬虫概述

网络爬虫(又称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者)，是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。
来源于[百度百科](https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB)。


## 获取网页

获取网页就是获取网页的源代码，进而从中提取有用信息。

之前我们讲了请求和响应，客户端构造并发送一个请求给服务器，服务器接收请求后发送响应给客户端浏览器，浏览器解析响应呈现网页。

那么这样一个过程我们不可能手动完成，python提供了urllib，requests等库来帮助我们完成这些过程。


## 提取信息

当我们得到网页源代码时，某种程度上我们就得到了信息，不过我们需要从中提取，常用的方法是正则表达式，但正则表达式复制且易出错。

根据网页自身的规则，可以根据网页节点属性，CSS选择器或者XPath来提取网页信息，常见的库有Beautiful Soup，pyquery，lxml等等，进而可以高效地提取网页地信息。

## 保存数据

我们可以讲提取地信息保存在TXT或者JSON文件中，也可以保存至数据库(关系型数据库或者非关系型数据库)，还可以保存到服务器中。

## 抓到怎样的数据

有些网站抓取返回的是HTML代码，而有的却是JSON字符串。图片，视频等抓取结果是二进制数据，提过转换可以保存到相应的文件中。

此外，源代码中还会有各种文件，如CSS，JavaSript文件等等。

上面内容是基于HTTP或者HTTPS协议的，都可以被抓取下来。

## 其他情况

很多时候，我们抓取的网页和浏览器中看到的不一致。

这是因为它们是使用Ajax，前端模块化工具构建的，网页内容是由JavaSript渲染得到的。

如：
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
</head>
<body>
  <script> src="content.js"</script>
</body>
</html>
```

这样的网页的主要内容就是由```content.js```渲染处理的，那爬取的网页内容自然和实践看到的不一致了。

对于这样的情况，我们可以使用其后台Ajax接口，也可使用Selenium，Splash这样的库来实现模拟JavaScript渲染。

这些内容在之后都会提到。



