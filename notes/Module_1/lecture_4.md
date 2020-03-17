# Session与Cookies 

当我们浏览网页时需要登陆，当我们登陆进去后，可以连续访问该网站。有时候我们一会儿不访问它了，再次浏览发现处于未登录状态，而有时候我们关闭网页或者浏览器，再次访问依然处于登陆状态，这是为什么呢？

这其中涉及到Session与Cookies了，本节我们将介绍它们。

<br>

## 静态网页与动态网页

浏览器从服务器得到的超文本标记文档的后缀通常有两大类：
```text
静态页面：htm，html，shtml，xml
动态页面：asp，jsp，php，perl，cgi
```

静态网页是指存放在服务器文件系统中实实在在的HTML文件。当用户在浏览器中输入页面的URL，然后回车，浏览器就会将对应的html文件下载，渲染并呈现在窗口中。早期的网站通常都是由静态页面制作的。
如[https://www.runoob.com/css/css-tutorial.html](https://www.runoob.com/css/css-tutorial.html)是一个静态网页。

动态网页是相对于静态网页而言的。当浏览器请求服务器的某个页面时，服务器根据当前时间，环境参数，数据库操作等动态的生成HTML页面，然后在发送给浏览器(后面的处理就跟静态网页一样了)。而[https://www.w3school.com.cn/htmldom/dom_nodes.asp](https://www.w3school.com.cn/htmldom/dom_nodes.asp)是一个动态网页。

动态网页中的“动态”是指服务器端页面的动态生成，相反，“静态”则指页面是实实在在的，独立的文件。静态网页简单安全，加载快但可维护性，交互性差。动态网页可维护性号，内容丰富但成本高，对安全性和保密性要求高。

更多内容可参考[https://www.jianshu.com/p/649d2a0ebde5](https://www.jianshu.com/p/649d2a0ebde5)。

## 无状态HTTP

HTTP的无状态是指HTTP协议对事务处理是没有记忆能力的，也就是说服务器不知道客户端是什么状态。

我们向服务器发送请求，服务器解析请求返回相应，这个过程是独立的，也就是在此之前之后的事情服务器并不知道，它也不会取记录。

更多HTTP的无状态，可参考[https://www.cnblogs.com/bellkosmos/p/5237146.html](https://www.cnblogs.com/bellkosmos/p/5237146.html)。

那问题就来了，我们在连续访问网页时，每次请求和响应对于服务器而言都是独立的，如果当前处理需要之前的信息，就需要传递很多前面的重复请求，这会浪费时间和资源，显然对客户端和服务端都是不利的。

为了保存HTTP连接状态，Session和Cookies应运而生。
Session位于服务端，用来保存用户的Session信息；Cookies位于客户端，有了Cookies，浏览器在下次访问网页时会带上它并发送给服务器，服务器通过识别Cookies并鉴定出用户，然后判断用户的状态，进而返回对应的响应。

Cookies相当于一种凭证，下次请求时带上它，一些重复的请求就不需要携带了。

在爬虫中，我们一般将登陆成功后获取的Cookies放在请求头中，这样就不需要重新登陆了。

## Session

Session：在计算机中，尤其是在网络应用中，称为“会话控制”，指有始有终的一系列动作或者消息。

Session对象存储特定用户会话所需的属性及配置信息。这样，当用户在应用程序的Web页之间跳转时，存储在Session对象中的变量将不会丢失，而是在整个用户会话中一直存在下去。当用户请求来自应用程序的Web页时，如果该用户还没有会话，则Web服务器将自动创建一个Session对象。当会话过期或被放弃后，服务器将终止该会话。
来源于[百度百科](https://baike.baidu.com/item/Session/479100)。

## Cookies

Cookie，有时也用其复数形式Cookies。类型为“小型文本文件”，是某些网站为了辨别用户身份，进行Session跟踪而储存在用户本地终端上的数据(通常经过加密)，由用户客户端计算机暂时或永久保存的信息。
来源于[百度百科](https://baike.baidu.com/item/cookie/1119)。

## Session维持 

当客户端第一次请求服务器时，服务器会返回一个带有Set-Cookie字段的响应给客户端，用来标记是哪一个用户，客户端浏览器会把Cookies保存起来。当浏览器下一次再请求该网站时，浏览器会把此Cookies放到请求头一起提交给服务器，Cookies携带了Session ID信息，服务器检查该Cookies即可找到对应的Session是什么，然后再判断Session来以此来辨认用户状态。

成功登陆某个网站后，服务器会告诉客户端设置哪些Cookies消息，之后访问页面时客户端把Cookies发送给服务器，服务器找到相应的Session解析判断，若用户处于登陆状态，则返回登陆之后才可以查看的内容。

反之，若Cookies无效的，或者Session过期了，对于登陆后才能查看的内容我们将无法访问。

客户端的Cookies和服务端的Session需要配合协作，实现登录Session的控制。

更多内容可查看，[https://www.jianshu.com/p/25802021be63](https://www.jianshu.com/p/25802021be63)。

## 结构属性

以github为例，再Chrome中按下F12，选择Application，选中左侧Storage的Cookies，点开。

![](../../images/Module_1/lecture_4_1.jpg)

有很多的列，都是Cookie的属性，简介如下：
```text
Name: Cookie的名称
Value: Cookie的值，如果值为Unicode字符，需要为字符编码。如果值为二进制数据，则需要使用BASE64编码。
Max Age: Cookie失效时间
Path: Cookie的路径
Domain: 可以访问该Cookie的域名
Size: Cookie大小
Http: Cookie的httponly属性，为True，只有在HTTP Headers中会带有此Cookie的信息
Secure: 即该 Cookie 是否仅被使用安全协议传输默认为false
```
有关BASE内容可参考，[https://blog.csdn.net/wo541075754/article/details/81734770](https://blog.csdn.net/wo541075754/article/details/81734770)。

## 会话Cookie和持久Cookie

字面理解，会话Cookie是把Cookie放到浏览器内存里，浏览器关闭后就失效了，而持久Cookie保存到硬盘在，之后可以继续使用。

其实准确来说没有所谓的会话和持久之分，这是Cookie的Max Age或Expires字段设置的时间不同导致。

很多网站使用的是会话Cookie，退出浏览器后就被删除了，不在保存登陆状态，如果将其保存到硬盘上或者改写请求头，将其发送给服务器，我们依然可以处于登陆状态

对于Session来说，它也有一个失效时间，超过这个时间，服务器就会删除它以节省空间。



