# JavaScript 混淆技术

在爬取网站的时候，经常会遇到各种各样类似加密的情形，比如：

* 某个网站的 ```URL``` 带有一些看不懂的长串加密参数，想要抓取就必须要懂得这些参数是怎么构造的，否则我们连完整的 URL 都构造不出来，更不用说爬取了
* 分析某个网站的 ```Ajax``` 接口的时候，可以看到接口的一些参数也是加密的，或者 ```Request Headers```
  里面也可能带有一些加密参数，如果不知道这些参数的具体构造逻辑就无法直接用程序来模拟这些 ```Ajax``` 请求
* 翻看网站的 ```JavaScript``` 源代码，可以发现很多压缩了或者看不太懂的字符，比如 ```JavaScript``` 文件名被编码，```JavaScript``` 的文件内容被压缩成几行，```JavaScript```
  变量也被修改成单个字符或者一些十六进制的字符，导致我们不好轻易根据 ```JavaScript``` 找出某些接口的加密逻辑

这些情况，基本上都是网站为了保护其本身的一些数据不被轻易抓取而采取的一些措施，我们可以把它归为两大类：

* 接口加密技术
* ```JavaScript``` 压缩、混淆和加密技术

本课时我们就来了解下这两类技术的实现原理。

---
---

## 数据保护

当今大数据时代，数据已经变得越来越重要，网页和 App 现在是主流的数据载体，如果其数据的接口没有设置任何保护措施，在爬虫工程师解决了一些基本的反爬如封 IP、验证码的问题之后，那么数据还是可以被轻松抓取到。

那么，有没有可能在接口或 ```JavaScript``` 层面也加上一层防护呢？答案是可以的。

---

## 接口加密技术

网站运营商首先想到防护措施可能是对某些数据接口进行加密，比如说对某些 URL 的一些参数加上校验码或者把一些 ID 信息进行编码，使其变得难以阅读或构造；或者对某些接口请求加上一些 ```token、sign```
等签名，这样这些请求发送到服务器时，服务器会通过客户端发来的一些请求信息以及双方约定好的秘钥等来对当前的请求进行校验，如果校验通过，才返回对应数据结果。

比如说客户端和服务端约定一种接口校验逻辑，客户端在每次请求服务端接口的时候都会附带一个 ```sign``` 参数，这个 ```sign``` 参数可能是由当前时间信息、请求的 ```URL```、请求的数据、设备的
ID、双方约定好的秘钥经过一些加密算法构造而成的，客户端会实现这个加密算法构造 ```sign```，然后每次请求服务器的时候附带上这个参数。服务端会根据约定好的算法和请求的数据对 ```sign```
进行校验，如果校验通过，才返回对应的数据，否则拒绝响应。

---

## JavaScript 压缩、混淆和加密技术

接口加密技术看起来的确是一个不错的解决方案，但单纯依靠它并不能很好地解决问题。为什么呢？

对于网页来说，其逻辑是依赖于 ```JavaScript``` 来实现的，```JavaScript``` 有如下特点：

* ```JavaScript``` 代码运行于客户端，也就是它必须要在用户浏览器端加载并运行
* ```JavaScript``` 代码是公开透明的，也就是说浏览器可以直接获取到正在运行的 ```JavaScript``` 的源码

由于这两个原因，导致 ```JavaScript``` 代码是不安全的，任何人都可以读、分析、复制、盗用，甚至篡改。

所以说，对于上述情形，客户端 ```JavaScript``` 对于某些加密的实现是很容易被找到或模拟的，了解了加密逻辑后，模拟参数的构造和请求也就是轻而易举了，所以如果 JavaScript
没有做任何层面的保护的话，接口加密技术基本上对数据起不到什么防护作用。

如果你不想让自己的数据被轻易获取，不想他人了解 ```JavaScript``` 逻辑的实现，或者想降低被不怀好意的人甚至是黑客攻击。那么你就需要用到 ```JavaScript``` 压缩、混淆和加密技术了。

这里压缩、混淆、加密技术简述如下。

* 代码压缩：即去除 ```JavaScript``` 代码中的不必要的空格、换行等内容，使源码都压缩为几行内容，降低代码可读性，当然同时也能提高网站的加载速度
* 代码混淆：使用变量替换、字符串阵列化、控制流平坦化、多态变异、僵尸函数、调试保护等手段，使代码变得难以阅读和分析，达到最终保护的目的。但这不影响代码原有功能。是理想、实用的 ```JavaScript``` 保护方案
* 代码加密：可以通过某种手段将 ```JavaScript``` 代码进行加密，转成人无法阅读或者解析的代码，如将代码完全抽象化加密，如 ```eval``` 加密。另外还有更强大的加密技术，可以直接将 ```JavaScript```
  代码用 ```C/C++``` 实现，```JavaScript``` 调用其编译后形成的文件来执行相应的功能，如 ```Emscripten``` 还有 ```WebAssembly```

下面我们对上面的技术分别予以介绍。

---

## 接口加密技术

数据一般都是通过服务器提供的接口来获取的，网站或 App 可以请求某个数据接口获取到对应的数据，然后再把获取的数据展示出来。

但有些数据是比较宝贵或私密的，这些数据肯定是需要一定层面上的保护。所以不同接口的实现也就对应着不同的安全防护级别，我们这里来总结下。

---

### 完全开放的接口

有些接口是没有设置任何防护的，谁都可以调用和访问，而且没有任何时空限制和频率限制。任何人只要知道了接口的调用方式就能无限制地调用。

这种接口的安全性是非常非常低的，如果接口的调用方式一旦泄露或被抓包获取到，任何人都可以无限制地对数据进行操作或访问。此时如果接口里面包含一些重要的数据或隐私数据，就能轻易被篡改或窃取了。

---

### 接口参数加密

为了提升接口的安全性，客户端会和服务端约定一种接口校验方式，一般来说会使用到各种加密和编码算法，如 ```Base64、Hex``` 编码，```MD5、AES、DES、RSA``` 等加密。

比如客户端和服务器双方约定一个 ```sign``` 用作接口的签名校验，其生成逻辑是客户端将 ```URL Path``` 进行 ```MD5``` 加密然后拼接上 ```URL``` 的某个参数再进行 ```Base64```
编码，最后得到一个字符串 ```sign```，这个 ```sign``` 会通过 ```Request URL``` 的某个参数或 ```Request Headers```
发送给服务器。服务器接收到请求后，对 ```URL Path``` 同样进行 ```MD5``` 加密，然后拼接上 ```URL``` 的某个参数，也进行 ```Base64``` 编码得到了一个 ```sign```
，然后比对生成的 ```sign``` 和客户端发来的 ```sign```
是否是一致的，如果是一致的，那就返回正确的结果，否则拒绝响应。这就是一个比较简单的接口参数加密的实现。如果有人想要调用这个接口的话，必须要定义好 ```sign```
的生成逻辑，否则是无法正常调用接口的。

以上就是一个基本的接口参数加密逻辑的实现。

当然上面的这个实现思路比较简单，这里还可以增加一些时间戳信息增加时效性判断，或增加一些非对称加密进一步提高加密的复杂程度。但不管怎样，只要客户端和服务器约定好了加密和校验逻辑，任何形式加密算法都是可以的。

这里要实现接口参数加密就需要用到一些加密算法，客户端和服务器肯定也都有对应的 SDK 实现这些加密算法，如 ```JavaScript``` 的 ```crypto-js```，```Python```
的 ```hashlib、Crypto``` 等等。

但还是如上文所说，如果是网页的话，客户端实现加密逻辑如果是用 ```JavaScript``` 来实现，其源代码对用户是完全可见的，如果没有对 ```JavaScript``` 做任何保护的话，是很容易弄清楚客户端加密的流程的。

因此，我们需要对 ```JavaScript``` 利用压缩、混淆、加密的方式来对客户端的逻辑进行一定程度上的保护。

---

## JavaScript 压缩、混淆、加密

下面我们再来介绍下 ```JavaScript``` 的压缩、混淆和加密技术。

---

### JavaScript 压缩

这个非常简单，```JavaScript``` 压缩即去除 ```JavaScript```
代码中的不必要的空格、换行等内容或者把一些可能公用的代码进行处理实现共享，最后输出的结果都被压缩为几行内容，代码可读性变得很差，同时也能提高网站加载速度。

如果仅仅是去除空格换行这样的压缩方式，其实几乎是没有任何防护作用的，因为这种压缩方式仅仅是降低了代码的直接可读性。如果我们有一些格式化工具可以轻松将 ```JavaScript``` 代码变得易读，比如利用
IDE、在线工具或 ```Chrome``` 浏览器都能还原格式化的代码。

目前主流的前端开发技术大多都会利用 ```Webpack``` 进行打包，```Webpack``` 会对源代码进行编译和压缩，输出几个打包好的 ```JavaScript```
文件，其中我们可以看到输出的 ```JavaScript``` 文件名带有一些不规则字符串，同时文件内容可能只有几行内容，变量名都是一些简单字母表示。这其中就包含 ```JavaScript```
压缩技术，比如一些公共的库输出成 ```bundle``` 文件，一些调用逻辑压缩和转义成几行代码，这些都属于 ```JavaScript``` 压缩。另外其中也包含了一些很基础的 ```JavaScript```
混淆技术，比如把变量名、方法名替换成一些简单字符，降低代码可读性。

但整体来说，```JavaScript``` 压缩技术只能在很小的程度上起到防护作用，要想真正提高防护效果还得依靠 ```JavaScript``` 混淆和加密技术。

---

### JavaScript 混淆

```JavaScript``` 混淆完全是在 ```JavaScript``` 上面进行的处理，它的目的就是使得 ```JavaScript``` 变得难以阅读和分析，大大降低代码可读性，是一种很实用的 ```JavaScript```
保护方案。

```JavaScript``` 混淆技术主要有以下几种：

* 变量混淆: 将带有含意的变量名、方法名、常量名随机变为无意义的类乱码字符串，降低代码可读性，如转成单个字符或十六进制字符串
* 字符串混淆: 将字符串阵列化集中放置、并可进行 ```MD5``` 或 ```Base64``` 加密存储，使代码中不出现明文字符串，这样可以避免使用全局搜索字符串的方式定位到入口点
* 属性加密: 针对 ```JavaScript``` 对象的属性进行加密转化，隐藏代码之间的调用关系
* 控制流平坦化: 打乱函数原有代码执行流程及函数调用关系，使代码逻变得混乱无序
* 僵尸代码: 随机在代码中插入无用的僵尸代码、僵尸函数，进一步使代码混乱
* 调试保护: 基于调试器特性，对当前运行环境进行检验，加入一些强制调试 ```debugger``` 语句，使其在调试模式下难以顺利执行 ```JavaScript``` 代码
* 多态变异: 使 ```JavaScript``` 代码每次被调用时，将代码自身即立刻自动发生变异，变化为与之前完全不同的代码，即功能完全不变，只是代码形式变异，以此杜绝代码被动态分析调试
* 锁定域名: 使 ```JavaScript``` 代码只能在指定域名下执行
* 反格式化: 如果对 ```JavaScript``` 代码进行格式化，则无法执行，导致浏览器假死
* 特殊编码: 将 ```JavaScript``` 完全编码为人不可读的代码，如表情符号、特殊表示内容等等

总之，以上方案都是 ```JavaScript``` 混淆的实现方式，可以在不同程度上保护 ```JavaScript``` 代码。

在前端开发中，现在 ```JavaScript``` 混淆主流的实现是 ```javascript-obfuscator``` 这个库，利用它我们可以非常方便地实现页面的混淆，它与 ```Webpack```
结合起来，最终可以输出压缩和混淆后的 ```JavaScript``` 代码，使得可读性大大降低，难以逆向。

下面我们会介绍下 ```javascript-obfuscator``` 对代码混淆的实现，了解了实现，那么自然我们就对混淆的机理有了更加深刻的认识。

```javascript-obfuscator``` 的官网地址为：[https://obfuscator.io/](https://obfuscator.io/) ，其官方介绍内容如下：

```textmate
A free and efficient obfuscator for JavaScript (including ES2017). Make your code harder to copy and prevent people from
stealing your work.
```

它是支持 ES8 的免费、高效的 ```JavaScript``` 混淆库，它可以使得你的 ```JavaScript``` 代码经过混淆后难以被复制、盗用，混淆后的代码具有和原来的代码一模一样的功能。

怎么使用呢？首先，我们需要安装好 ```Node.js```，可以使用 ```npm``` 命令。

然后新建一个文件夹，随后进入该文件夹，初始化工作空间：

```shell
npm init
```

这里会提示我们输入一些信息，创建一个 ```package.json``` 文件，这就完成了项目初始化了。

接下来我们来安装 ```javascript-obfuscator``` 这个库：

```shell
npm install --save-dev javascript-obfuscator
```

接下来我们就可以编写代码来实现混淆了，如新建一个 [main.js](../../codes/Module_4/lecture_27/main.js) 文件，内容如下：

```javascript
const code = `
let x = '1' + 1
console.log('x', x)
`

const options = {
    compact: false,
    controlFlowFlattening: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

在这里我们定义了两个变量，一个是 ```code```，即需要被混淆的代码，另一个是混淆选项，是一个 ```Object```。接下来我们引入了 ```javascript-obfuscator```
库，然后定义了一个方法，传入 ```code``` 和 ```options```，来获取混淆后的代码，最后控制台输出混淆后的代码。

代码逻辑比较简单，我们来执行一下代码：

```shell
node main.js
```

输出结果如下：

```javascript
const _0x5296 = [
    '108359TABkAY',
    '5048TihISs',
    '983953JsgBGM',
    '3eYuTGB',
    '476417ZSBGZL',
    '1373091ItxbTq',
    '193xbAlFP',
    '7knsFeO',
    '1696576njihxT',
    '11YFQuVD',
    '1zlPjfP',
    '4PXoEzj',
    '239535pDEwMB',
    'log'
];

function _0x3721(_0x4b4715, _0x3fcbf5) {
    return _0x3721 = function (_0x52964e, _0x372193) {
        _0x52964e = _0x52964e - 0xf6;
        let _0x3c896a = _0x5296[_0x52964e];
        return _0x3c896a;
    }, _0x3721(_0x4b4715, _0x3fcbf5);
}

const _0x595fcd = _0x3721;
(function (_0x31229b, _0x38b226) {
    const _0x18e311 = _0x3721;
    while (!![]) {
        try {
            const _0x311153 = -parseInt(_0x18e311(0x103)) * parseInt(_0x18e311(0xfc)) + -parseInt(_0x18e311(0xf9)) * -parseInt(_0x18e311(0xfe)) + -parseInt(_0x18e311(0xfd)) * parseInt(_0x18e311(0x102)) + -parseInt(_0x18e311(0x101)) * parseInt(_0x18e311(0xf8)) + -parseInt(_0x18e311(0x100)) + parseInt(_0x18e311(0xf6)) * -parseInt(_0x18e311(0xfb)) + -parseInt(_0x18e311(0xff)) * -parseInt(_0x18e311(0xfa));
            if (_0x311153 === _0x38b226)
                break;
            else
                _0x31229b['push'](_0x31229b['shift']());
        } catch (_0x4090b2) {
            _0x31229b['push'](_0x31229b['shift']());
        }
    }
}(_0x5296, 0xee4ae));
let x = '1' + 0x1;
console[_0x595fcd(0xf7)]('x', x);
```

这么简单的两行代码，被混淆成了这个样子，其实这里我们就是设定了一个“控制流扁平化”的选项。

整体看来，代码的可读性大大降低，也大大加大了 ```JavaScript``` 调试的难度。

接下来我们来跟着 ```javascript-obfuscator``` 走一遍，就能具体知道 ```JavaScript``` 混淆到底有多少方法了。

---

### 代码压缩

这里 ```javascript-obfuscator``` 也提供了代码压缩的功能，使用其参数 ```compact``` 即可完成 ```JavaScript``` 代码的压缩，输出为一行内容。默认是 ```true```
，如果定义为 ```false```，则混淆后的代码会分行显示。

[示例](../../codes/Module_4/lecture_27/compact.js)如下：

```javascript
const code = `
let x = '1' + 1
console.log('x', x)
`

const options = {
    compact: false,
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

这里我们先把代码压缩 ```compact``` 选项设置为 ```false```，运行结果如下：

```javascript
const _0x4bd4 = [
    'log',
    '1786099mHwobi',
    '94Txguhe',
    '439642MLDiGe',
    '2VJrNhY',
    '1803542aIevgA',
    '223282wSkRaB',
    '958180XSUrPc',
    '3008eiTCyq',
    '4764161zPHSLN'
];
const _0xc041d4 = _0x1dfc;

function _0x1dfc(_0x29463e, _0x5555a4) {
    return _0x1dfc = function (_0x4bd40c, _0x1dfcc7) {
        _0x4bd40c = _0x4bd40c - 0x158;
        let _0x4346f1 = _0x4bd4[_0x4bd40c];
        return _0x4346f1;
    }, _0x1dfc(_0x29463e, _0x5555a4);
}

(function (_0x256a08, _0x45e1f6) {
    const _0x5c8407 = _0x1dfc;
    while (!![]) {
        try {
            const _0x1e3f83 = parseInt(_0x5c8407(0x15d)) + parseInt(_0x5c8407(0x15c)) * parseInt(_0x5c8407(0x15e)) + parseInt(_0x5c8407(0x15b)) + parseInt(_0x5c8407(0x15a)) * parseInt(_0x5c8407(0x160)) + parseInt(_0x5c8407(0x15f)) + parseInt(_0x5c8407(0x159)) + -parseInt(_0x5c8407(0x161));
            if (_0x1e3f83 === _0x45e1f6)
                break;
            else
                _0x256a08['push'](_0x256a08['shift']());
        } catch (_0x3fca66) {
            _0x256a08['push'](_0x256a08['shift']());
        }
    }
}(_0x4bd4, 0xe892a));
let x = '1' + 0x1;
console[_0xc041d4(0x158)]('x', x);
```

如果不设置 ```compact``` 或把 ```compact``` 设置为 ```true```，结果如下：

```shell
const _0x4a96=['487160xdeYJd','454845Wuyxqw','log','156094qDISoy','419605GfHuEv','986715KCZjfd','1LkFkTX','1171121mvEbuv','620923UjhHpa','5eQdPzh'];function _0x3488(_0x564194,_0xd33a6a){return _0x3488=function(_0x4a96e2,_0x3488fe){_0x4a96e2=_0x4a96e2-0x126;let _0x3eff03=_0x4a96[_0x4a96e2];return _0x3eff03;},_0x3488(_0x564194,_0xd33a6a);}const _0x2f8e99=_0x3488;(function(_0x1bac39,_0x1b6ccf){const _0x317957=_0x3488;while(!![]){try{const _0x3d1fb0=-parseInt(_0x317957(0x12c))+parseInt(_0x317957(0x129))+-parseInt(_0x317957(0x126))+parseInt(_0x317957(0x12b))*-parseInt(_0x317957(0x12f))+-parseInt(_0x317957(0x12d))+parseInt(_0x317957(0x12a))+-parseInt(_0x317957(0x127))*-parseInt(_0x317957(0x128));if(_0x3d1fb0===_0x1b6ccf)break;else _0x1bac39['push'](_0x1bac39['shift']());}catch(_0x2b6c7b){_0x1bac39['push'](_0x1bac39['shift']());}}}(_0x4a96,0x9b707));let x='1'+0x1;console[_0x2f8e99(0x12e)]('x',x);
```

可以看到单行显示的时候，对变量名进行了进一步的混淆和控制流扁平化操作。

---

### 变量名混淆

变量名混淆可以通过配置 ```identifierNamesGenerator``` 参数实现，我们通过这个参数可以控制变量名混淆的方式，如 ```hexadecimal``` 则会替换为 16 进制形式的字符串，在这里我们可以设定如下值：

* ```hexadecimal```：将变量名替换为 16 进制形式的字符串，如 ```0xabc123```
* ```mangled```：将变量名替换为普通的简写字符，如 ```a、b、c``` 等

该参数默认为 ```hexadecimal```

我们将该参数修改为 ```mangled``` 来试一下，[示例](../../codes/Module_4/lecture_27/identifier_names_generator.js)如下：

```javascript
const code = `
let hello = '1' + 1
console.log('hello', hello)
`

const options = {
    compact: true,
    identifierNamesGenerator: 'mangled'
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
const a = ['1FLgMuz', '453741VOwATV', 'log', '2DrxegM', '683231sLOXGo', '899223faGfwC', '1wKRgOy', '212663FkplpM', '1FhNbhr', '653501BaKqPj', '1469183bYdSdm', '503712fLjiLm', '29SChvPw', 'hello'];
const h = b;
(function (c, d) {
    const g = b;
    while (!![]) {
        try {
            const e = -parseInt(g(0x128)) * parseInt(g(0x12e)) + -parseInt(g(0x12a)) + parseInt(g(0x134)) * -parseInt(g(0x12d)) + parseInt(g(0x12f)) * -parseInt(g(0x12b)) + -parseInt(g(0x130)) + -parseInt(g(0x129)) * parseInt(g(0x133)) + -parseInt(g(0x131)) * -parseInt(g(0x12c));
            if (e === d) break; else c['push'](c['shift']());
        } catch (f) {
            c['push'](c['shift']());
        }
    }
}(a, 0xcfcbf));
let hello = '1' + 0x1;

function b(c, d) {
    return b = function (e, f) {
        e = e - 0x127;
        let g = a[e];
        return g;
    }, b(c, d);
}

console[h(0x127)](h(0x132), hello);
```

可以看到这里的变量命名都变成了 ```a、b``` 等形式。

如果我们将 ```identifierNamesGenerator``` 修改为 ```hexadecimal```
或者不设置，[示例](../../codes/Module_4/lecture_27/identifier_names_generator_hexadecimal.js)如下：

```javascript
const code = `
let hello = '1' + 1
console.log('hello', hello)
`

const options = {
    compact: true,
    identifierNamesGenerator: 'hexadecimal'
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
const _0x6e46 = ['112378QLdlzj', '438157rbycqq', '1366869kTYiVH', '63tpnIDn', '43qksUkA', '1PhzqZX', '1oZFJhJ', '19009ASXsmj', 'hello', 'log', '21998bLmIEu', '39pDtJZA', '513012kOKNiT'];
const _0x39c44f = _0x1c06;
(function (_0x1148e9, _0x5b4bb8) {
    const _0x56a93b = _0x1c06;
    while (!![]) {
        try {
            const _0x51bbe0 = parseInt(_0x56a93b(0x94)) * -parseInt(_0x56a93b(0x91)) + -parseInt(_0x56a93b(0x9a)) + -parseInt(_0x56a93b(0x9b)) * parseInt(_0x56a93b(0x93)) + parseInt(_0x56a93b(0x99)) + parseInt(_0x56a93b(0x92)) * parseInt(_0x56a93b(0x97)) + parseInt(_0x56a93b(0x98)) * parseInt(_0x56a93b(0x90)) + parseInt(_0x56a93b(0x8f));
            if (_0x51bbe0 === _0x5b4bb8) break; else _0x1148e9['push'](_0x1148e9['shift']());
        } catch (_0x4a765a) {
            _0x1148e9['push'](_0x1148e9['shift']());
        }
    }
}(_0x6e46, 0x82f5e));
let hello = '1' + 0x1;

function _0x1c06(_0xa98a3e, _0x16e643) {
    return _0x1c06 = function (_0x6e4617, _0x1c0644) {
        _0x6e4617 = _0x6e4617 - 0x8f;
        let _0x897342 = _0x6e46[_0x6e4617];
        return _0x897342;
    }, _0x1c06(_0xa98a3e, _0x16e643);
}

console[_0x39c44f(0x96)](_0x39c44f(0x95), hello);
```

可以看到选用了 ```mangled```，其代码体积会更小，但 ```hexadecimal``` 其可读性会更低。

另外我们还可以通过设置 ```identifiersPrefix``` 参数来控制混淆后的变量前缀，[示例](../../codes/Module_4/lecture_27/identifiers_prefix.js)如下：

```javascript
const code = `
let hello = '1' + 1
console.log('hello', hello)
`

const options = {
    identifiersPrefix: 'germey'
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果：

```javascript
const germey_0x44e5 = ['441015scSqYO', '1251129wVQCmv', '3287FWTPhb', '13TcOgZA', '713131BjpUte', '57241skvbmO', '1864cGSVbd', '1mXVVfq', '439XmCGGK', '163XOZGlh', '1411VixNdA', 'hello'];
const germey_0x941b7e = germey_0xb510;

function germey_0xb510(_0x223209, _0x58dbbb) {
    return germey_0xb510 = function (_0x44e585, _0xb5105b) {
        _0x44e585 = _0x44e585 - 0x151;
        let _0x1cf1ff = germey_0x44e5[_0x44e585];
        return _0x1cf1ff;
    }, germey_0xb510(_0x223209, _0x58dbbb);
}

(function (_0x3a63ed, _0x2410e1) {
    const _0x39b26c = germey_0xb510;
    while (!![]) {
        try {
            const _0x225927 = parseInt(_0x39b26c(0x15b)) * parseInt(_0x39b26c(0x159)) + -parseInt(_0x39b26c(0x156)) * parseInt(_0x39b26c(0x15c)) + parseInt(_0x39b26c(0x158)) + parseInt(_0x39b26c(0x154)) + -parseInt(_0x39b26c(0x157)) * parseInt(_0x39b26c(0x15a)) + parseInt(_0x39b26c(0x155)) + parseInt(_0x39b26c(0x151)) * -parseInt(_0x39b26c(0x152));
            if (_0x225927 === _0x2410e1) break; else _0x3a63ed['push'](_0x3a63ed['shift']());
        } catch (_0xb95150) {
            _0x3a63ed['push'](_0x3a63ed['shift']());
        }
    }
}(germey_0x44e5, 0xbad72));
let hello = '1' + 0x1;
console['log'](germey_0x941b7e(0x153), hello);
```

---
---


