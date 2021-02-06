# PyQuery 使用

上节我们了解了正则表达式的基本用法，它是一种强大的工具，但是也有一些不足之处，例如一旦写法出了问题，就无法获得信息了。

实际上，每个网页，都有一定的特殊结构和层级关系，而且很多节点都有 id 或 class 作为区分，我们可以利用它们的结构和属性来提取信息。

这便是 ```pyquery```，一个强大的 HTML 解析库。利用它，我们可以直接解析 DOM 节点的结构，并通过 DOM 节点的一些属性快速进行内容提取。

---
---

## 安装

使用 pip3 安装即可：

```textmate
pip3 install pyquery
```

---

## 初始化

在解析 HTML 文本时，首先需要将其初始化为一个 ```pyquery``` 对象。初始化方式有多种，比如直接传入字符串，传入 URL，传入文件名等等。

下面我们将逐一介绍。

---

## 字符串初始化

可以直接将 HTML 的内容当参数来初始化 ```pyquery``` 对象。

[示例](../../codes/Module_2/lecture_9/lecture_9_1.py) 如下：
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

这里先引入 ```pyquery``` 对象，然后声明了一个 HTML 字符串，并将其当作参数传递给 ```pyquery``` 类，完成了初始化。

接下来，将初始化的对象传入 CSS 选择器。在这个实例中，我们传入 li 节点，这样就可以选择所有的 li 节点。

---

## URL 初始化

将 URL 作为参数初始化 ```pyquery``` 对象。

[示例](../../codes/Module_2/lecture_9/lecture_9_2.py) 如下：

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

```pyquery``` 对象首先请求这个URL，然后用得到的 HTML 内容完成初始化。相当于将网页的源代码以字符串的形式传递给 ```pyquery``` 类来初始化。

和 [以下](../../codes/Module_2/lecture_9/lecture_9_3.py) 等价：

```python
# -*- coding: utf-8 -*-

from pyquery import PyQuery
import requests

url = "https://dogedoge.com"
doc = PyQuery(requests.get(url=url).text)
print(doc("title"))
```

结果同上。

---

## 文件初始化

我们可以传入一个文件 [demo.html](../../codes/Module_2/lecture_9/demo.html) 作为参数进行初始化。

[示例](../../codes/Module_2/lecture_9/lecture_9_4.py) 如下：

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

这里 ```pyquery``` 先读取文件，并将文件内容以字符串形式传递给 ```pyquery``` 类进行初始化。

常用的是以字符串形式初始化。

---

## 基本 CSS 选择器

用一个 [实例](../../codes/Module_2/lecture_9/lecture_9_5.py ) 感受下 ```pyquery``` 的 CSS 选择器用法：

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

初始化 ```pyquery``` 对象之后，传入 CSS 选择器 #container.list li 。它会先选取 id 为 container 的节点，然后再选取其内部 class 为 list 的所有 li 节点，最后打印输出。

得到节点的类型依然是 ```pyquery``` ，下面我们直接遍历这些节点，使用 ```text``` 方法获取节点内容。

[示例](../../codes/Module_2/lecture_9/lecture_9_6.py) 如下：

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

通过选择器和 ```text``` 方法就得到了我们需要的文本。

下面我们详细了解一下如何使用 ```pyquery``` 来查找节点，遍历节点，获取各种信息等操作。

---

## 查找节点

下面我们介绍一些常用的查询方法。

---

### 子节点

还是之前的 HTML 文本，查找子节点需要用到 ```find``` 方法，传入的参数是 CSS 选择器。

[示例](../../codes/Module_2/lecture_9/lecture_9_7.py) 如下：

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

首先，我们通过 .list 参数选取 class 为 list 的节点，然后调用 ```find``` 方法，传入 CSS 选择器，选取其内部的 li 节点，最后打印输出。如结果所示，```find``` 方法会将选择符合条件的所有节点选择，其结果是 ```pyquery``` 类型。

```find``` 的查找范围是节点的所有子孙节点，如果我们只想查找子节点，可以用 ```children```方法：

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

如果要筛选所有子节点中符合条件的节点，比如想筛选出子节点中 class 为 active 的节点，可以向 ```children``` 方法传入CSS选择器 .active ，代码如下：

```textmate
lis = items.children(".active")
print(lis)
```

结果为：

```html
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
```

输出结果进行了筛选，留下了 class 为 active 的节点。

---

### 父节点

我们可以用 ```parent``` 方法来获取某个节点的父节点。

来看个 [实例](../../codes/Module_2/lecture_9/lecture_9_8.py) ：

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

我们首先用 .list 选取 class 为 list 的节点，然后调用 ```parent``` 方法得到其父节点，其类型依然是 ```pyquery``` 类型。

这里的父节点是该节点的直接父节点，也就是说，它不会再去查找父节点的父节点，即祖先节点。

如果想获取某个祖先节点，可以使用 ```parents``` 方法：

[示例](../../codes/Module_2/lecture_9/lecture_9_9.py) 如下：

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

输出结果有两个：一个是 class 为 wrap 的节点，一个是 id 为 container 的节点。也就是说，使用 ```parents``` 方法会返回所有的祖先节点。

如果你想要筛选某个祖先节点的话，可以向 ```parents``` 方法传入 CSS 选择器，这样就会返回祖先节点中符合 CSS 选择器的节点：

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

可以看到，输出结果少了一个节点，只保留了 class 为 wrap 的节点。

---

### 兄弟节点

还是以上面的 HTML 代码为例，如果要获取兄弟节点，可以使用 ```siblings``` 方法。

[示例](../../codes/Module_2/lecture_9/lecture_9_10.py) 如下：
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

在这个例子中我们首先选择 class 为 list 的节点，内部 class 为 item-0 和 active 的节点，也就是第 3 个 li 节点。很明显，它的兄弟节点有 4 个，那就是第 1，2，4，5 个 li 节点。

如果要筛选某个兄弟节点，我们依然可以用 siblings 方法传入 CSS 选择器，这样就会从所有兄弟节点中挑选出符合条件的节点了：

```textmate
doc = PyQuery(html)
li = doc(".list .item-0.active")
print(li.siblings(".active"))
```

结果为：

```html
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
```

---

### 遍历

以上，我们发现 ```pyquery``` 的选择结果既可能是多个节点，也可能是单个节点，类型都是 ```pyquery``` 类型，并没有返回列表。

对于单个节点来说，可以直接打印输出，也可以直接转成字符串。

[示例](../../codes/Module_2/lecture_9/lecture_9_11.py) 如下：

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

对于有多个节点的结果，我们就需要用遍历来获取了。例如，如果要遍历每一个 li 节点，可以调用 ```items``` 方法：

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

可以发现，调用 ```items``` 方法后，会得到一个生成器，遍历一下，就可以逐个得到 li 节点对象了，它的类型也是 ```pyquery``` 类型。每个li节点还可以调用前面所说的方法进行选择，比如继续查询子节点，寻找某个祖先节点等，非常灵活。

---

### 获取信息

提取到节点之后，我们最终目的当然是提取节点所包含的信息了。比较重要的信息有两类，一是获取属性，二是获取文本，下面分别进行说明。

---

### 获取属性

提取到某个 ```pyquery``` 类型的节点后，就可以调用 ```attr``` 方法来获取属性。

[示例](../../codes/Module_2/lecture_9/lecture_9_12.py) 如下：

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

在这个例子中我们首先选中 class 为 item-0 和 active 的 li 节点内的 a 节点，它的类型是 ```pyquery``` 类型。然后调用 ```attr``` 方法。在这个方法中传入属性的名称，就可以得到属性值了。

此外，也可以通过调用 ```attr``` 属性来获取属性值，用法如下：

```textmate
print(a.attr.href)
```

结果为：

```textmate
link3.html
```

如果选中的是多个元素，然后调用 ```attr``` 方法，会出现怎样的结果呢？我们用实例来测试一下：

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

照理来说，我们选中的 a 节点应该有 4 个，打印结果也应该是 4 个，但是当我们调用 ```attr``` 方法时，返回结果却只有第 1 个。这是因为，当返回结果包含多个节点时，调用 ```attr``` 方法，只会得到第 1 个节点的属性。

那么，遇到这种情况时，如果想获取所有的 a 节点的属性，就要用到前面所说的遍历了：

```textmate
doc = PyQuery(html)
a = doc("a")
for item in a.items():
    print(item.attr("href"))
```

result:

```html
link2.html
link3.html
link4.html
link5.html
```

因此，在进行属性获取时，先要观察返回节点是一个还是多个，如果是多个，则需要遍历才能依次获取每个节点的属性。

---

### 获取文本

获取节点之后的另一个主要操作就是获取其内部文本了，此时可以调用 ```text``` 方法来实现。

[示例](../../codes/Module_2/lecture_9/lecture_9_13.py) 如下：

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

这里我们首先选中一个 a 节点，然后调用 ```text``` 方法，就可以获取其内部的文本信息了。```text``` 会忽略节点内部包含的所有 HTML，只返回纯文字内容。

但如果你想要获取这个节点内部的 HTML 文本，就要用 ```html``` 方法了：

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

如果我们选中的结果是多个节点，```text``` 或 ```html``` 方法会返回什么内容？

用一个 [实例](../../codes/Module_2/lecture_9/lecture_9_14.py) 来看一下：

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

结果比较出乎意料，```html``` 方法返回的是第 1 个 li 节点的内部 HTML 文本，而 ```text``` 则返回了所有的 li 节点内部的纯文本，中间用一个空格分割开，即返回结果是一个字符串。

这个地方值得注意，如果你想要得到的结果是多个节点，并且需要获取每个节点的内部 ```HTML``` 文本，则需要遍历每个节点。而 ```text``` 方法不需要遍历就可以获取，它将所有节点取文本之后合并成一个字符串。

---

### 节点操作

```pyquery``` 提供了一系列方法来对节点进行动态修改，比如为某个节点添加一个 class ，移除某个节点等，这些操作有时会为提取信息带来极大的便利。

下面举几个典型的例子来说明它的用法。

---

### addClass 和 removeClass

来看个 [示例](../../codes/Module_2/lecture_9/lecture_9_15.py) ：

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

首先选中第 3 个 li 节点，然后调用 remove_class 方法，将 li 节点的 active 这个 class 移除，第 2 步调用 ```add_class``` 方法，将 class 添加回来。每执行一次操作，就打印输出当前 li 节点的内容。

可以看到，一共输出了 3 次。第 2 次输出时，li节点的 active 这个 class 被移除了，第3次 class 又添加回来了。

所以说，```add_class``` 和 ```remove_class``` 方法可以动态改变节点的 class 属性。

----

### attr，text，html

当然，除了操作 class 这个属性外，也可以用 ```attr``` 方法对属性进行操作。此外，我们还可以用 ```text``` 和 ```html``` 方法来改变节点内部的内容。

[示例](../../codes/Module_2/lecture_9/lecture_9_16.py) 如下：

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

这里我们首先选中 li 节点，然后调用 ```attr``` 方法来修改属性。该方法的第 1 个参数为属性名，第 2 个参数为属性值。最后调用 ```text``` 和 ```html``` 方法来改变节点内部的内容。3 次操作后，分别打印输出当前的 li 节点。

我们发现，调用 ```attr``` 方法后，li节点多了一个原本不存在的属性 ```name``` ，其值为 link。接着调用 ```text``` 方法传入文本，li 节点内部的文本全被改为传入的字符串文本。最后，调用 ```html``` 方法传入 HTML 文本，li 节点内部又变为传入的 HTML 文本了。

所以说，使用 ```attr``` 方法时如果只传入第 1 个参数的属性名，则是获取这个属性值；如果传入第 2 个参数，可以用来修改属性值。使用 ```text``` 和 ```html``` 方法时如果不传参数，则是获取节点内纯文本和 HTML 文本，如果传入参数，则进行赋值。

---

### remove

```remove``` 方法就是移除，它有时会为信息的提取带来非常大的便利。

以该文本为例：

```html
<div class="wrap">
    Hello,world
    <p>This is a paragraph.</p>
</div>
```

我们想提取 "Hello, World" 这个字符串，该怎样操作呢？

这里先直接尝试提取 class 为 wrap 的节点的内容，看看是不是我们想要的。

[示例](../../codes/Module_2/lecture_9/lecture_9_17.py) 如下：

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

这个结果还包含了内部的 p 节点的内容，也就是说 ```text``` 把所有的纯文本全提取出来了。

如果我们想去掉 p 节点内部的文本，可以选择再把 p 节点内的文本提取一遍，然后从整个结果中移除这个子串，但这个做法明显比较烦琐。

我们可以使用 ```remove``` 方法：

```textmate
wrap.find("p").remove()
print(wrap.text())
```

结果为：

```html
Hello,world
```

先选中 p 节点，然后调用 ```remove``` 方法将其移除，这时 wrap 内部就只剩下 "Hello, World" 这句话了，最后利用 ```text``` 方法提取即可。

更多 ```pyquery``` 内容可以参考官方文档：[https://pyquery.readthedocs.io/en/latest/api.html](https://pyquery.readthedocs.io/en/latest/api.html) 。

---

### 伪类选择器

CSS 选择器之所以强大，还有一个很重要的原因，那就是它支持多种多样的伪类选择器，例如选择第一个节点，最后一个节点，奇偶数节点，包含某一文本的节点等。

[示例](../../codes/Module_2/lecture_9/lecture_9_18.py) 如下：

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

在这个例子中我们使用了 CSS3 的伪类选择器，依次选择了第 1 个 li 节点，最后一个 li 节点，第 2 个 li 节点，第 3 个 li 之后的 li 节点，偶数位置的 li 节点，包含 second 文本的 li 节点。

更多有关 CSS 选择器的内容可参考，[https://www.w3school.com.cn/css/index.asp](https://www.w3school.com.cn/css/index.asp) 。

更多有关 ```pyquery``` 内容的可参考官方文档，[https://pyquery.readthedocs.io/en/latest/](https://pyquery.readthedocs.io/en/latest/) 。

---
---