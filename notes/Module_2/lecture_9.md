# PyQuery使用

上节我们了解了正则表达式的基本用法，它是一种强大的工具，但是也有一些不足之处，例如一旦写法出了问题，就无法获得信息了。

实际上，每个网页，都有一定的特殊结构和层级关系，而且很多节点都有id或class作为区分，我们可以利用它们的结构和属性来提取信息。

这便是pyquery，一个强大的HTML解析库。利用它，我们可以直接解析DOM节点的结构，并通过DOM节点的一些属性快速进行内容提取。

## 安装

使用pip3安装即可：
```textmate
pip3 install pyquery
```

## 初始化

在解析HTML文本时，首先需要将其初始化为一个pyquery对象。初始化方式有多种，比如直接传入字符串，传入 URL，传入文件名等等。

下面我们将逐一介绍。

## 字符串初始化

可以直接将HTML的内容当参数来初始化pyquery对象。

[示例](../../codes/Module_2/lecture_9/lecture_9_1.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div>
    <ul>
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
'''
doc = PyQuery(html)
print(doc('li'))
```
结果为：
```html
<li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
```
这里先引入pyquery对象，然后声明了一个HTML字符串，并将其当作参数传递给pyquery类，完成了初始化。

接下来，将初始化的对象传入CSS选择器。在这个实例中，我们传入li节点，这样就可以选择所有的li节点。

## URL初始化

将URL作为参数初始化pyquery对象。

[示例](../../codes/Module_2/lecture_9/lecture_9_2.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

url = "https://dogedoge.com"
doc = PyQuery(url=url)
print(doc("title"))
```
结果为：
```textmate
<title>DogeDoge 多吉搜索 — 不追踪，不误导</title>
```
pyquery对象首先请求这个URL，然后用得到的HTML内容完成初始化。相当于将网页的源代码以字符串的形式传递给pyquery类来初始化。

和[以下](../../codes/Module_2/lecture_9/lecture_9_3.py)等价：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery
import requests

url = "https://dogedoge.com"
doc = PyQuery(requests.get(url=url).text)
print(doc("title"))
```
结果同上。

## 文件初始化

我们可以传入一个文件[demo.html](../../codes/Module_2/lecture_9/demo.html)作为参数进行初始化。

[示例](../../codes/Module_2/lecture_9/lecture_9_4.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

filename = "demo.html"
doc = PyQuery(filename=filename)
print(doc("title"))
```
结果为：
```textmate
<title>Document</title>
```
这里pyquery先读取文件，并将文件内容以字符串形式传递给pyquery类进行初始化。

常用的是以字符串形式初始化。

## 基本CSS选择器

用一个[实例](../../codes/Module_2/lecture_9/lecture_9_5.py)感受下pyquery的CSS选择器用法：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div id="container">
    <ul class="list">
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
'''
doc = PyQuery(html)

print(doc('#container .list li'))
print(type(doc('#container .list li')))
```
结果为：
```html
<li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    
<class 'pyquery.pyquery.PyQuery'>
```
初始化pyquery对象之后，传入CSS选择器#container.listli。它会先选取id为container的节点，然后再选取其内部class为list的所有li节点，最后打印输出。

得到节点的类型依然是pyquery，下面我们直接遍历这些节点，使用text方法获取节点内容。

[示例](../../codes/Module_2/lecture_9/lecture_9_6.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div id="container">
    <ul class="list">
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
'''
doc = PyQuery(html)

for item in doc("#container .list li").items():
    print(item.text())
```
结果为：
```textmate
first item
second item
third item
fourth item
fifth item
```
通过选择器和text方法就得到了我们需要的文本。

下面我们详细了解一下如何使用pyquery来查找节点，遍历节点，获取各种信息等操作。

## 查找节点

下面我们介绍一些常用的查询方法。

### 子节点

还是之前的HTML文本，查找子节点需要用到find方法，传入的参数是CSS选择器。

[示例](../../codes/Module_2/lecture_9/lecture_9_7.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div id="container">
    <ul class="list">
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
'''
doc = PyQuery(html)
items = doc(".list")
print(type(items))
print(items)

lis = items.find("li")
print(type(lis))
print(lis)
```
结果为：
```html
<class 'pyquery.pyquery.PyQuery'>
<ul class="list">
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
```
首先，我们通过.list参数选取class为list的节点，然后调用find方法，传入CSS选择器，选取其内部的li节点，最后打印输出。如结果所示，find方法会将选择符合条件的所有节点选择，其结果是pyquery类型。

find的查找范围是节点的所有子孙节点，如果我们只想查找子节点，可以用children方法：
```textmate
lis = items.children()
print(type(lis))
print(lis)
```
结果为
```html
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
```
如果要筛选所有子节点中符合条件的节点，比如想筛选出子节点中class为active的节点，可以向children方法传入CSS选择器.active，代码如下：
```textmate
lis = items.children(".active")
print(lis)
```
结果为：
```html
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
```
输出结果进行了筛选，留下了class为active的节点。

### 父节点

我们可以用parent方法来获取某个节点的父节点。

来看个[实例](../../codes/Module_2/lecture_9/lecture_9_8.py)：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
items = doc('.list')
container = items.parent()

print(type(container))
print(container)
```
结果为：
```html
<class 'pyquery.pyquery.PyQuery'>
<div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
```
我们首先用.list选取class为list的节点，然后调用parent方法得到其父节点，其类型依然是pyquery类型。

这里的父节点是该节点的直接父节点，也就是说，它不会再去查找父节点的父节点，即祖先节点。

如果想获取某个祖先节点，可以使用parents方法：

[示例](../../codes/Module_2/lecture_9/lecture_9_9.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
items = doc('.list')
parents = items.parents()

print(type(parents))
print(parents)
```
结果为：
```html
<class 'pyquery.pyquery.PyQuery'>
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
<div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
```
输出结果有两个：一个是class为wrap的节点，一个是id为container的节点。也就是说，使用parents方法会返回所有的祖先节点。

如果你想要筛选某个祖先节点的话，可以向parents方法传入CSS选择器，这样就会返回祖先节点中符合CSS选择器的节点：
```textmate
parent = items.parents(".wrap")
print(parent)
```
结果为：
```html
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
```
可以看到，输出结果少了一个节点，只保留了class为wrap的节点。

### 兄弟节点

还是以上面的HTML代码为例，如果要获取兄弟节点，可以使用siblings方法。

[示例](../../codes/Module_2/lecture_9/lecture_9_10.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
li = doc(".list .item-0.active")
print(li.siblings())
```
结果为：
```html
<li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0">first item</li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
```
在这个例子中我们首先选择class为list的节点，内部class为item-0和active的节点，也就是第3个li节点。很明显，它的兄弟节点有4个，那就是第1，2，4，5个li节点。

如果要筛选某个兄弟节点，我们依然可以用siblings方法传入CSS选择器，这样就会从所有兄弟节点中挑选出符合条件的节点了：
```textmate
doc = PyQuery(html)
li = doc(".list .item-0.active")
print(li.siblings(".active"))
```
结果为：
```html
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
```

### 遍历

以上，我们发现pyquery的选择结果既可能是多个节点，也可能是单个节点，类型都是pyquery类型，并没有返回列表。

对于单个节点来说，可以直接打印输出，也可以直接转成字符串。

[示例](../../codes/Module_2/lecture_9/lecture_9_11.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
li = doc(".item-0.active")

print(li)
print(str(li))
```
结果为：
```html
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
```
对于有多个节点的结果，我们就需要用遍历来获取了。例如，如果要遍历每一个li节点，可以调用items方法：
```textmate
doc = PyQuery(html)
lis = doc("li").items()
print(type(lis))
for li in lis:
    print(li, type(li))
```
结果为：
```html
<class 'generator'>
<li class="item-0">first item</li>
             <class 'pyquery.pyquery.PyQuery'>
<li class="item-1"><a href="link2.html">second item</a></li>
             <class 'pyquery.pyquery.PyQuery'>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <class 'pyquery.pyquery.PyQuery'>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <class 'pyquery.pyquery.PyQuery'>
<li class="item-0"><a href="link5.html">fifth item</a></li>
         <class 'pyquery.pyquery.PyQuery'>
```
可以发现，调用items方法后，会得到一个生成器，遍历一下，就可以逐个得到li节点对象了，它的类型也是pyquery类型。每个li节点还可以调用前面所说的方法进行选择，比如继续查询子节点，寻找某个祖先节点等，非常灵活。

### 获取信息

提取到节点之后，我们的最终目的当然是提取节点所包含的信息了。比较重要的信息有两类，一是获取属性，二是获取文本，下面分别进行说明。

### 获取属性

提取到某个pyquery类型的节点后，就可以调用attr方法来获取属性。

[示例](../../codes/Module_2/lecture_9/lecture_9_12.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
a = doc(".item-0.active a")

print(a, type(a))
print(a.attr("href"))
```
结果为：
```html
<a href="link3.html"><span class="bold">third item</span></a> <class 'pyquery.pyquery.PyQuery'>
link3.html
```
在这个例子中我们首先选中class为item-0和active的li节点内的a节点，它的类型是pyquery类型。然后调用attr方法。在这个方法中传入属性的名称，就可以得到属性值了。

此外，也可以通过调用attr属性来获取属性值，用法如下：
```textmate
print(a.attr.href)
```
结果为：
```textmate
link3.html
```
如果选中的是多个元素，然后调用attr方法，会出现怎样的结果呢？我们用实例来测试一下：
```textmate
a = doc("a")
print(a, type(a))
print(a.attr("href"))
print(a.attr.href)
```
结果为：
```html
<a href="link2.html">second item</a><a href="link3.html"><span class="bold">third item</span></a><a href="link4.html">fourth item</a><a href="link5.html">fifth item</a> <class 'pyquery.pyquery.PyQuery'>
link2.html
link2.html
```
照理来说，我们选中的a节点应该有4个，打印结果也应该是4个，但是当我们调用attr方法时，返回结果却只有第1个。这是因为，当返回结果包含多个节点时，调用attr方法，只会得到第1个节点的属性。

那么，遇到这种情况时，如果想获取所有的a节点的属性，就要用到前面所说的遍历了：
```textmate
doc = PyQuery(html)
a = doc("a")
for item in a.items():
    print(item.attr("href"))
```
```html
link2.html
link3.html
link4.html
link5.html
```
因此，在进行属性获取时，先要观察返回节点是一个还是多个，如果是多个，则需要遍历才能依次获取每个节点的属性。

### 获取文本

获取节点之后的另一个主要操作就是获取其内部文本了，此时可以调用text方法来实现。

[示例](../../codes/Module_2/lecture_9/lecture_9_13.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
a = doc(".item-0.active a")

print(a)
print(a.text())
```
结果为：
```html
<a href="link3.html"><span class="bold">third item</span></a>
third item
```
这里我们首先选中一个a节点，然后调用text方法，就可以获取其内部的文本信息了。text会忽略节点内部包含的所有HTML，只返回纯文字内容。

但如果你想要获取这个节点内部的HTML文本，就要用html方法了：
```textmate
doc = PyQuery(html)
li = doc(".item-0.active")
print(li)
print(li.html())
```
结果为：
```html
<a href="link3.html"><span class="bold">third item</span></a>
```
如果我们选中的结果是多个节点，text或html方法会返回什么内容？

用一个[实例](../../codes/Module_2/lecture_9/lecture_9_14.py)来看一下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
li = doc("li")

print(li.html())
print(li.text())
print(type(li.text()))
```
结果为：
```html
<a href="link2.html">second item</a>
second item third item fourth item fifth item
<class 'str'>
```
结果比较出乎意料，html方法返回的是第1个li节点的内部HTML文本，而text则返回了所有的li节点内部的纯文本，中间用一个空格分割开，即返回结果是一个字符串。

这个地方值得注意，如果你想要得到的结果是多个节点，并且需要获取每个节点的内部HTML文本，则需要遍历每个节点。而text方法不需要遍历就可以获取，它将所有节点取文本之后合并成一个字符串。

### 节点操作

pyquery提供了一系列方法来对节点进行动态修改，比如为某个节点添加一个class，移除某个节点等，这些操作有时会为提取信息带来极大的便利。

下面举几个典型的例子来说明它的用法。

### addClass和removeClass

来看个[示例](../../codes/Module_2/lecture_9/lecture_9_15.py)：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
li = doc(".item-0.active")
print(li)
li.remove_class("active")
print(li)
li.add_class("active")
print(li)
```
结果为：
```html
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            
<li class="item-0"><a href="link3.html"><span class="bold">third item</span></a></li>
            
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
```
首先选中第3个li节点，然后调用remove_class方法，将li节点的active这个class移除，第2步调用add_class方法，将class添加回来。每执行一次操作，就打印输出当前li节点的内容。

可以看到，一共输出了3次。第2次输出时，li节点的active这个class被移除了，第3次class又添加回来了。

所以说，add_class和remove_class方法可以动态改变节点的class属性。

### attr，text，html

当然，除了操作class这个属性外，也可以用attr方法对属性进行操作。此外，我们还可以用text和html方法来改变节点内部的内容。

[示例](../../codes/Module_2/lecture_9/lecture_9_16.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<ul class="list">
    <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
</ul>
'''
doc = PyQuery(html)
li = doc(".item-0.active")
print(li)
li.attr("name", "link")
print(li)
li.text("changed item")
print(li)
li.html("<span>changed item</span>")
print(li)
```
结果为：
```html
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0 active" name="link"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0 active" name="link">changed item</li>
<li class="item-0 active" name="link"><span>changed item</span></li>
```
这里我们首先选中li节点，然后调用attr方法来修改属性。该方法的第1个参数为属性名，第2个参数为属性值。最后调用text和html方法来改变节点内部的内容。3次操作后，分别打印输出当前的li节点。

我们发现，调用attr方法后，li节点多了一个原本不存在的属性name，其值为link。接着调用text方法传入文本，li节点内部的文本全被改为传入的字符串文本。最后，调用html方法传入HTML文本，li节点内部又变为传入的HTML文本了。

所以说，使用attr方法时如果只传入第1个参数的属性名，则是获取这个属性值；如果传入第2个参数，可以用来修改属性值。使用text和html方法时如果不传参数，则是获取节点内纯文本和HTML文本，如果传入参数，则进行赋值。

### remove

remove方法就是移除，它有时会为信息的提取带来非常大的便利。

以该文本为例：
```html
<div class="wrap">
    Hello,world
    <p>This is a paragraph.</p>
</div>
```

我们想提取“Hello, World”这个字符串，该怎样操作呢？

这里先直接尝试提取class为wrap的节点的内容，看看是不是我们想要的。

[示例](../../codes/Module_2/lecture_9/lecture_9_17.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    Hello,world
    <p>This is a paragraph.</p>
</div>
'''
doc = PyQuery(html)
wrap = doc(".wrap")
print(wrap.text())
```
结果为：
```html
Hello,world
This is a paragraph.
```
这个结果还包含了内部的p节点的内容，也就是说text把所有的纯文本全提取出来了。

如果我们想去掉p节点内部的文本，可以选择再把p节点内的文本提取一遍，然后从整个结果中移除这个子串，但这个做法明显比较烦琐。

我们可以使用remove方法：
```textmate
wrap.find("p").remove()
print(wrap.text())
```
结果为：
```html
Hello,world
```
先选中p节点，然后调用remove方法将其移除，这时wrap内部就只剩下“Hello, World”这句话了，最后利用text方法提取即可。

更多pyquery内容可以参考官方文档：[https://pyquery.readthedocs.io/en/latest/api.html](https://pyquery.readthedocs.io/en/latest/api.html)。

### 伪类选择器

CSS选择器之所以强大，还有一个很重要的原因，那就是它支持多种多样的伪类选择器，例如选择第一个节点，最后一个节点，奇偶数节点，包含某一文本的节点等。

[示例](../../codes/Module_2/lecture_9/lecture_9_18.py)如下：
```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</div>
'''
doc = PyQuery(html)
li = doc("li:first-child")
print(li)
li = doc("li:last-child")
print(li)
li = doc("li:nth-child(2)")
print(li)
li = doc("li:gt(2)")
print(li)
li = doc("li:nth-child(2n)")
print(li)
li = doc("li:contains(second)")
print(li)
```
结果为：
```html
<li class="item-0">first item</li>
            
<li class="item-0"><a href="link5.html">fifth item</a></li>
        
<li class="item-1"><a href="link2.html">second item</a></li>
            
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        
<li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            
<li class="item-1"><a href="link2.html">second item</a></li>
```
在这个例子中我们使用了CSS3的伪类选择器，依次选择了第1个li节点，最后一个li节点，第2个li节点，第3个li之后的li节点，偶数位置的li节点，包含second文本的li节点。

<br>

更多有关CSS选择器的内容可参考，[https://www.w3school.com.cn/css/index.asp](https://www.w3school.com.cn/css/index.asp)。

更多有关pyquery内容的可参考官方文档，[https://pyquery.readthedocs.io/en/latest/](https://pyquery.readthedocs.io/en/latest/)。
