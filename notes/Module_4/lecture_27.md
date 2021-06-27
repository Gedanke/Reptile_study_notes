# JavaScript 混淆技术

在爬取网站的时候，经常会遇到各种各样类似加密的情形，比如：

* 某个网站的 ```URL``` 带有一些看不懂的长串加密参数，想要抓取就必须要懂得这些参数是怎么构造的
* 分析某个网站的 ```Ajax``` 接口的时候，可以看到接口的一些参数也是加密的，或者 ```Request Headers```
  里面也可能带有一些加密参数，如果不知道这些参数的具体构造逻辑就无法直接用程序来模拟这些 ```Ajax``` 请求
* 翻看网站的 JavaScript 源代码，可以发现很多压缩了或者看不太懂的字符，比如 JavaScript 文件名被编码，JavaScript 的文件内容被压缩成几行，JavaScript
  变量也被修改成单个字符或者一些十六进制的字符，导致我们不好轻易根据 JavaScript 找出某些接口的加密逻辑

这些情况，基本上都是网站为了保护其本身的一些数据不被轻易抓取而采取的一些措施，我们可以把它归为两大类：

* 接口加密技术
* JavaScript 压缩、混淆和加密技术

本课时我们就来了解下这两类技术的实现原理。

---
---

## 数据保护

当今大数据时代，数据已经变得越来越重要，网页和 App 现在是主流的数据载体，如果其数据的接口没有设置任何保护措施，在解决了一些基本的反爬如封 IP、验证码的问题之后，那么数据还是可以被轻松抓取到。

那么，有没有可能在接口或 JavaScript 层面也加上一层防护呢？答案是可以的。

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

对于网页来说，其逻辑是依赖于 JavaScript 来实现的，JavaScript 有如下特点：

* JavaScript 代码运行于客户端，也就是它必须要在用户浏览器端加载并运行
* JavaScript 代码是公开透明的，也就是说浏览器可以直接获取到正在运行的 JavaScript 的源码

由于这两个原因，导致 JavaScript 代码是不安全的，任何人都可以读、分析、复制、盗用，甚至篡改。

所以说，对于上述情形，客户端 JavaScript 对于某些加密的实现是很容易被找到或模拟的，了解了加密逻辑后，模拟参数的构造和请求也就是轻而易举了，所以如果 JavaScript
没有做任何层面的保护的话，接口加密技术基本上对数据起不到什么防护作用。

如果不想让自己的数据被轻易获取，不想他人了解 JavaScript 逻辑的实现，或者想降低被不怀好意的人甚至是黑客攻击。那么你就需要用到 JavaScript 压缩、混淆和加密技术了。

这里压缩、混淆、加密技术简述如下。

* 代码压缩：即去除 JavaScript 代码中的不必要的空格、换行等内容，使源码都压缩为几行内容，降低代码可读性，当然同时也能提高网站的加载速度
* 代码混淆：使用变量替换、字符串阵列化、控制流平坦化、多态变异、僵尸函数、调试保护等手段，使代码变得难以阅读和分析，达到最终保护的目的。但这不影响代码原有功能。是理想、实用的 JavaScript 保护方案
* 代码加密：可以通过某种手段将 JavaScript 代码进行加密，转成人无法阅读或者解析的代码，如将代码完全抽象化加密，如 ```eval``` 加密。另外还有更强大的加密技术，可以直接将 JavaScript
  代码用 ```C/C++``` 实现，JavaScript 调用其编译后形成的文件来执行相应的功能，如 ```Emscripten``` 还有 ```WebAssembly```

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

这里要实现接口参数加密就需要用到一些加密算法，客户端和服务器肯定也都有对应的 SDK 实现这些加密算法，如 JavaScript 的 ```crypto-js```，```Python```
的 ```hashlib、Crypto``` 等等。

但还是如上文所说，如果是网页的话，客户端实现加密逻辑如果是用 JavaScript 来实现，其源代码对用户是完全可见的，如果没有对 JavaScript 做任何保护的话，是很容易弄清楚客户端加密的流程的。

因此，我们需要对 JavaScript 利用压缩、混淆、加密的方式来对客户端的逻辑进行一定程度上的保护。

---

## JavaScript 压缩、混淆、加密

下面我们再来介绍下 JavaScript 的压缩、混淆和加密技术。

---

### JavaScript 压缩

这个非常简单，JavaScript 压缩即去除 JavaScript 代码中的不必要的空格、换行等内容或者把一些可能公用的代码进行处理实现共享，最后输出的结果都被压缩为几行内容，代码可读性变得很差，同时也能提高网站加载速度。

如果仅仅是去除空格换行这样的压缩方式，其实几乎是没有任何防护作用的，因为这种压缩方式仅仅是降低了代码的直接可读性。如果我们有一些格式化工具可以轻松将 JavaScript 代码变得易读，比如利用 IDE、在线工具或 ```Chrome```
浏览器都能还原格式化的代码。

目前主流的前端开发技术大多都会利用 ```Webpack``` 进行打包，```Webpack``` 会对源代码进行编译和压缩，输出几个打包好的 JavaScript 文件，其中我们可以看到输出的 JavaScript
文件名带有一些不规则字符串，同时文件内容可能只有几行内容，变量名都是一些简单字母表示。这其中就包含 JavaScript 压缩技术，比如一些公共的库输出成 ```bundle``` 文件，一些调用逻辑压缩和转义成几行代码，这些都属于
JavaScript 压缩。另外其中也包含了一些很基础的 JavaScript 混淆技术，比如把变量名、方法名替换成一些简单字符，降低代码可读性。

但整体来说，JavaScript 压缩技术只能在很小的程度上起到防护作用，要想真正提高防护效果还得依靠 JavaScript 混淆和加密技术。

---

### JavaScript 混淆

JavaScript 混淆完全是在 JavaScript 上面进行的处理，它的目的就是使得 JavaScript 变得难以阅读和分析，大大降低代码可读性，是一种很实用的 JavaScript 保护方案。

JavaScript 混淆技术主要有以下几种：

* 变量混淆: 将带有含意的变量名、方法名、常量名随机变为无意义的类乱码字符串，降低代码可读性，如转成单个字符或十六进制字符串
* 字符串混淆: 将字符串阵列化集中放置、并可进行 ```MD5``` 或 ```Base64``` 加密存储，使代码中不出现明文字符串，这样可以避免使用全局搜索字符串的方式定位到入口点
* 属性加密: 针对 JavaScript 对象的属性进行加密转化，隐藏代码之间的调用关系
* 控制流平坦化: 打乱函数原有代码执行流程及函数调用关系，使代码逻变得混乱无序
* 僵尸代码: 随机在代码中插入无用的僵尸代码、僵尸函数，进一步使代码混乱
* 调试保护: 基于调试器特性，对当前运行环境进行检验，加入一些强制调试 ```debugger``` 语句，使其在调试模式下难以顺利执行 JavaScript 代码
* 多态变异: 使 JavaScript 代码每次被调用时，将代码自身即立刻自动发生变异，变化为与之前完全不同的代码，即功能完全不变，只是代码形式变异，以此杜绝代码被动态分析调试
* 锁定域名: 使 JavaScript 代码只能在指定域名下执行
* 反格式化: 如果对 JavaScript 代码进行格式化，则无法执行，导致浏览器假死
* 特殊编码: 将 JavaScript 完全编码为人不可读的代码，如表情符号、特殊表示内容等等

总之，以上方案都是 JavaScript 混淆的实现方式，可以在不同程度上保护 JavaScript 代码。

在前端开发中，现在 JavaScript 混淆主流的实现是 ```javascript-obfuscator``` 这个库，利用它我们可以非常方便地实现页面的混淆，它与 ```Webpack```
结合起来，最终可以输出压缩和混淆后的 JavaScript 代码，使得可读性大大降低，难以逆向。

下面我们会介绍下 ```javascript-obfuscator``` 对代码混淆的实现，了解了实现，那么自然我们就对混淆的机理有了更加深刻的认识。

```javascript-obfuscator``` 的官网地址为：[https://obfuscator.io/](https://obfuscator.io/) ，其官方介绍内容如下：

```textmate
A free and efficient obfuscator for JavaScript (including ES2017). Make your code harder to copy and prevent people from
stealing your work.
```

它是支持 ES8 的免费、高效的 JavaScript 混淆库，它可以使得你的 JavaScript 代码经过混淆后难以被复制、盗用，混淆后的代码具有和原来的代码一模一样的功能。

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

---

#### 代码混淆

接下来我们就可以编写代码来实现混淆了，如新建一个[main.js](../../codes/Module_4/lecture_27/main.js)文件，内容如下：

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

整体看来，代码的可读性大大降低，也大大加大了 JavaScript 调试的难度。

接下来我们来跟着 ```javascript-obfuscator``` 走一遍，就能具体知道 JavaScript 混淆到底有多少方法了。

---

#### 代码压缩

这里 ```javascript-obfuscator``` 也提供了代码压缩的功能，使用其参数 ```compact``` 即可完成 JavaScript 代码的压缩，输出为一行内容。默认是 ```true```
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

#### 变量名混淆

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

可以看到混淆后的变量前缀加上了我们自定义的字符串 ```germey```。

另外 ```renameGlobals``` 这个参数还可以指定是否混淆全局变量和函数名称，默认为 ```false```。示例[如下](../../codes/Module_4/lecture_27/rename_globals.js)：

```javascript
const code = `
var $ = function(id) {
    return document.getElementById(id);
};
`

const options = {
    renameGlobals: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
var _0x4afe = ['getElementById', '97196bwlkSq', '291613OZJAOf', '43839ihNOaT', '263146HpfyAT', '286899IacSsh', '60425hGfkGt', '247550JKlywv', '1XXDKeR'];

function _0x484e(_0x48a618, _0x27bb91) {
    return _0x484e = function (_0x4afe47, _0x484eb9) {
        _0x4afe47 = _0x4afe47 - 0xc4;
        var _0x254350 = _0x4afe[_0x4afe47];
        return _0x254350;
    }, _0x484e(_0x48a618, _0x27bb91);
}

(function (_0x5e0452, _0x1f5b9c) {
    var _0x2f12e1 = _0x484e;
    while (!![]) {
        try {
            var _0x513cbf = -parseInt(_0x2f12e1(0xc9)) + parseInt(_0x2f12e1(0xc8)) + -parseInt(_0x2f12e1(0xca)) + -parseInt(_0x2f12e1(0xc5)) * -parseInt(_0x2f12e1(0xcb)) + -parseInt(_0x2f12e1(0xc7)) + parseInt(_0x2f12e1(0xc6)) + parseInt(_0x2f12e1(0xc4));
            if (_0x513cbf === _0x1f5b9c) break; else _0x5e0452['push'](_0x5e0452['shift']());
        } catch (_0x526e77) {
            _0x5e0452['push'](_0x5e0452['shift']());
        }
    }
}(_0x4afe, 0x243ca));
var _0x321bad = function (_0x546132) {
    var _0x1c97ac = _0x484e;
    return document[_0x1c97ac(0xcc)](_0x546132);
};
```

可以看到这里我们声明了一个全局变量 ```$```，在 ```renameGlobals``` 设置为 true 之后，$ 这个变量也被替换了。如果后文用到了这个 $ 对象，可能就会有找不到定义的错误，因此这个参数可能导致代码执行不通。

如果我们不设置 renameGlobals 或者设置为 false，[如下](../../codes/Module_4/lecture_27/rename_globals_false.js)：

```javascript
const code = `
var $ = function(id) {
    return document.getElementById(id);
};
`

const options = {
    renameGlobals: false
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

结果:

```javascript
var _0xf3b9 = ['1612103fWnCQI', '1538177NNubeB', '1194416fuIOsG', '1056566fSHOQm', 'getElementById', '1258063gGwiDs', '411005nnJRoV', '1OIgCBG', '1AUbJWo', '299033FUHiYN'];

function _0x6c3f(_0x373243, _0x2467a7) {
    return _0x6c3f = function (_0xf3b919, _0x6c3f56) {
        _0xf3b919 = _0xf3b919 - 0x165;
        var _0x179f77 = _0xf3b9[_0xf3b919];
        return _0x179f77;
    }, _0x6c3f(_0x373243, _0x2467a7);
}

(function (_0x15e66f, _0x23b524) {
    var _0x16abfb = _0x6c3f;
    while (!![]) {
        try {
            var _0xe2381e = parseInt(_0x16abfb(0x168)) + parseInt(_0x16abfb(0x167)) + -parseInt(_0x16abfb(0x16b)) + parseInt(_0x16abfb(0x165)) + parseInt(_0x16abfb(0x169)) * parseInt(_0x16abfb(0x16d)) + -parseInt(_0x16abfb(0x16c)) + -parseInt(_0x16abfb(0x166)) * parseInt(_0x16abfb(0x16e));
            if (_0xe2381e === _0x23b524) break; else _0x15e66f['push'](_0x15e66f['shift']());
        } catch (_0x47da4d) {
            _0x15e66f['push'](_0x15e66f['shift']());
        }
    }
}(_0xf3b9, 0xc506d));
var $ = function (_0x5dcfa9) {
    var _0x13c476 = _0x6c3f;
    return document[_0x13c476(0x16a)](_0x5dcfa9);
};
```

可以看到，最后还是有 ```$``` 的声明，其全局名称没有被改变。

---

#### 字符串混淆

字符串混淆，即将一个字符串声明放到一个数组里面，使之无法被直接搜索到。

* 通过控制 ```stringArray``` 参数来控制，默认为 ```true```
* 还可以通过 ```rotateStringArray``` 参数来控制数组化后结果的元素顺序，默认为 ```true```
* 还可以通过 ```stringArrayEncoding``` 参数来控制数组的编码形式，参数以 ```array```
  形式传入，```Each value in stringArrayEncoding must be one of the following values: none, base64, rc4 ; All stringArrayEncoding's elements must be unique; StringArrayEncoding must be an array```
  ，如['none'],['base64'],['rc4']
* 还可以通过 ```stringArrayThreshold``` 来控制启用编码的概率，范围 0 到 1，默认 0.8。

示例[如下](../../codes/Module_4/lecture_27/string_array.js)：

```javascript
const code = `
var a = 'hello world'   
`
const options = {
    stringArray: true,
    rotateStringArray: true,
    stringArrayEncoding: ['base64'], //  ['none'],['base64'],['rc4']
    stringArrayThreshold: 1,
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
var _0x4f3b = ['mtC1nde0nxjvEwz1EG', 'mti3odrIuMn3yKK', 'ode3oda0y2jUAfDs', 'AgvSBg8GD29YBgq', 'oxnjy2PSsq', 'oteXmdG2EgHTu1fy', 'mteYDg9hEvnK', 'mxflENPkqW', 'mtaXndK1wxvgBxju', 'mJy4mJfLwwfkExi', 'odC3nte4Axv2ENz0'];
var _0x655567 = _0x5e81;

function _0x5e81(_0x33c6a7, _0x2c2e32) {
    return _0x5e81 = function (_0x4f3b15, _0x5e810f) {
        _0x4f3b15 = _0x4f3b15 - 0x17e;
        var _0xb7a98d = _0x4f3b[_0x4f3b15];
        if (_0x5e81['kFMMcP'] === undefined) {
            var _0x572b7d = function (_0x2ae011) {
                var _0x5bd63e = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';
                var _0x193852 = '', _0x29bc4c = '';
                for (var _0x455441 = 0x0, _0x43db45, _0x323105, _0xc60dda = 0x0; _0x323105 = _0x2ae011['charAt'](_0xc60dda++); ~_0x323105 && (_0x43db45 = _0x455441 % 0x4 ? _0x43db45 * 0x40 + _0x323105 : _0x323105, _0x455441++ % 0x4) ? _0x193852 += String['fromCharCode'](0xff & _0x43db45 >> (-0x2 * _0x455441 & 0x6)) : 0x0) {
                    _0x323105 = _0x5bd63e['indexOf'](_0x323105);
                }
                for (var _0x540620 = 0x0, _0x5a21ec = _0x193852['length']; _0x540620 < _0x5a21ec; _0x540620++) {
                    _0x29bc4c += '%' + ('00' + _0x193852['charCodeAt'](_0x540620)['toString'](0x10))['slice'](-0x2);
                }
                return decodeURIComponent(_0x29bc4c);
            };
            _0x5e81['vvOSZH'] = _0x572b7d, _0x33c6a7 = arguments, _0x5e81['kFMMcP'] = !![];
        }
        var _0x238f8a = _0x4f3b[0x0], _0x15607f = _0x4f3b15 + _0x238f8a, _0x14e0d8 = _0x33c6a7[_0x15607f];
        return !_0x14e0d8 ? (_0xb7a98d = _0x5e81['vvOSZH'](_0xb7a98d), _0x33c6a7[_0x15607f] = _0xb7a98d) : _0xb7a98d = _0x14e0d8, _0xb7a98d;
    }, _0x5e81(_0x33c6a7, _0x2c2e32);
}

(function (_0x512e9e, _0x17a10c) {
    var _0x10dc08 = _0x5e81;
    while (!![]) {
        try {
            var _0x43469d = parseInt(_0x10dc08(0x187)) * -parseInt(_0x10dc08(0x17e)) + -parseInt(_0x10dc08(0x180)) * parseInt(_0x10dc08(0x186)) + parseInt(_0x10dc08(0x181)) + parseInt(_0x10dc08(0x184)) + parseInt(_0x10dc08(0x17f)) + -parseInt(_0x10dc08(0x183)) * parseInt(_0x10dc08(0x188)) + parseInt(_0x10dc08(0x182));
            if (_0x43469d === _0x17a10c) break; else _0x512e9e['push'](_0x512e9e['shift']());
        } catch (_0x303b01) {
            _0x512e9e['push'](_0x512e9e['shift']());
        }
    }
}(_0x4f3b, 0xec017));
var a = _0x655567(0x185);
```

可以看到这里就把字符串进行了 ```Base64``` 编码，我们再也无法通过查找的方式找到字符串的位置了。

如果将 ```stringArray``` 设置为 ```false``` 的话，输出就是这样：

```javascript
var a = 'hello\x20world';
```

字符串就仍然是明文显示的，没有被编码。

另外我们还可以使用 ```unicodeEscapeSequence``` 这个参数对字符串进行 ```Unicode```
转码，使之更加难以辨认，示例[如下](../../codes/Module_4/lecture_27/unicode_escape_sequence.js)：

```javascript
const code = `
var a = 'hello world'
`
const options = {
    compact: false,
    unicodeEscapeSequence: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
var _0x1d2b = [
    '\x34\x30\x38\x39\x32\x31\x69\x75\x58\x77\x68\x41',
    '\x34\x38\x32\x34\x32\x64\x70\x68\x73\x7a\x48',
    '\x31\x35\x32\x30\x35\x39\x32\x66\x7a\x44\x78\x67\x41',
    '\x32\x61\x41\x59\x52\x76\x4b',
    '\x34\x35\x35\x36\x36\x66\x59\x4c\x77\x53\x55',
    '\x34\x33\x30\x33\x62\x4d\x49\x48\x74\x4b',
    '\x31\x31\x33\x39\x32\x36\x34\x75\x42\x4d\x73\x4f\x59',
    '\x31\x30\x30\x38\x34\x32\x31\x77\x76\x45\x49\x69\x43',
    '\x33\x31\x37\x72\x7a\x71\x75\x4b\x6c',
    '\x33\x6e\x62\x46\x4d\x55\x70',
    '\x39\x33\x69\x76\x4f\x48\x6d\x77',
    '\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64',
    '\x31\x67\x77\x71\x52\x4d\x61'
];
var _0x235740 = _0x3d01;

function _0x3d01(_0x1c31c9, _0x145bbf) {
    return _0x3d01 = function (_0x1d2b29, _0x3d0170) {
        _0x1d2b29 = _0x1d2b29 - 0x83;
        var _0x4fef4a = _0x1d2b[_0x1d2b29];
        return _0x4fef4a;
    }, _0x3d01(_0x1c31c9, _0x145bbf);
}

(function (_0x43487f, _0x432cc4) {
    var _0x3a516a = _0x3d01;
    while (!![]) {
        try {
            var _0x21a875 = parseInt(_0x3a516a(0x86)) * -parseInt(_0x3a516a(0x87)) + parseInt(_0x3a516a(0x88)) * parseInt(_0x3a516a(0x8b)) + parseInt(_0x3a516a(0x83)) * -parseInt(_0x3a516a(0x8c)) + -parseInt(_0x3a516a(0x89)) + parseInt(_0x3a516a(0x8a)) * -parseInt(_0x3a516a(0x8f)) + -parseInt(_0x3a516a(0x85)) + -parseInt(_0x3a516a(0x84)) * -parseInt(_0x3a516a(0x8d));
            if (_0x21a875 === _0x432cc4)
                break;
            else
                _0x43487f['push'](_0x43487f['shift']());
        } catch (_0x1333dc) {
            _0x43487f['push'](_0x43487f['shift']());
        }
    }
}(_0x1d2b, 0xd3081));
var a = _0x235740(0x8e);
```

可以看到，这里字符串被数字化和 ```Unicode``` 化，非常难以辨认。

在很多 JavaScript 逆向的过程中，一些关键的字符串可能会作为切入点来查找加密入口。用了这种混淆之后，如果有人想通过全局搜索的方式搜索 ```hello``` 这样的字符串找加密入口，也没法搜到了。

---

#### 代码自我保护

我们可以通过设置 ```selfDefending``` 参数来开启代码自我保护功能。开启之后，混淆后的 JavaScript 会强制以一行形式显示，如果我们将混淆后的代码进行格式化(美化)或者重命名，该段代码将无法执行。

[例如](../../codes/Module_4/lecture_27/self_defending.js)：

```javascript
const code = `
var a = 'hello world'
`
const options = {
    compact: false,
    unicodeEscapeSequence: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```textmate
var _0x1a98=['349TMnZhh','hello\x20world','constructor','103439Itbspl','722060OIxYpI','9qVUQzg','198028OqliKv','2YuBsEz','24799WqJtMA','return\x20/\x22\x20+\x20this\x20+\x20\x22/','^([^\x20]+(\x20+[^\x20]+)+)+[^\x20]}','619259xYwvxo','1711wjYfIb','log','13bLjSSk','110669uxFvyo','52DXHlmZ'];var _0x344a17=_0x1a2f;(function(_0xeec45b,_0x4bceaa){var _0x2b8a52=_0x1a2f;while(!![]){try{var _0x5e5542=parseInt(_0x2b8a52(0xba))*parseInt(_0x2b8a52(0xb9))+parseInt(_0x2b8a52(0xb3))*-parseInt(_0x2b8a52(0xbb))+parseInt(_0x2b8a52(0xb6))*parseInt(_0x2b8a52(0xb2))+parseInt(_0x2b8a52(0xb0))*-parseInt(_0x2b8a52(0xae))+parseInt(_0x2b8a52(0xaf))+parseInt(_0x2b8a52(0xb7))*-parseInt(_0x2b8a52(0xbc))+parseInt(_0x2b8a52(0xb1));if(_0x5e5542===_0x4bceaa)break;else _0xeec45b['push'](_0xeec45b['shift']());}catch(_0x5a31ba){_0xeec45b['push'](_0xeec45b['shift']());}}}(_0x1a98,0xbe591));var _0xf89d82=function(){var _0x2d8207=!![];return function(_0x57a29d,_0x4f7e07){var _0x3d6803=_0x2d8207?function(){if(_0x4f7e07){var _0x29f046=_0x4f7e07['apply'](_0x57a29d,arguments);return _0x4f7e07=null,_0x29f046;}}:function(){};return _0x2d8207=![],_0x3d6803;};}(),_0x476e6f=_0xf89d82(this,function(){var _0x32c408=function(){var _0xe8c3de=_0x1a2f,_0x1f90c1=_0x32c408[_0xe8c3de(0xad)](_0xe8c3de(0xb4))()[_0xe8c3de(0xad)](_0xe8c3de(0xb5));return!_0x1f90c1['test'](_0x476e6f);};return _0x32c408();});function _0x1a2f(_0x5201c5,_0x5d62d4){return _0x1a2f=function(_0xf0cf9b,_0x476e6f){_0xf0cf9b=_0xf0cf9b-0xac;var _0xf89d82=_0x1a98[_0xf0cf9b];return _0xf89d82;},_0x1a2f(_0x5201c5,_0x5d62d4);}_0x476e6f(),console[_0x344a17(0xb8)](_0x344a17(0xac));
```

如果我们将上述代码放到控制台，它的执行结果和之前是一模一样的，没有任何问题。 如

果我们将其进行格式化，会变成如下内容：

```javascript
var _0x1a98 = ['349TMnZhh', 'hello\x20world', 'constructor', '103439Itbspl', '722060OIxYpI', '9qVUQzg', '198028OqliKv', '2YuBsEz', '24799WqJtMA', 'return\x20/\x22\x20+\x20this\x20+\x20\x22/', '^([^\x20]+(\x20+[^\x20]+)+)+[^\x20]}', '619259xYwvxo', '1711wjYfIb', 'log', '13bLjSSk', '110669uxFvyo', '52DXHlmZ'];
var _0x344a17 = _0x1a2f;
(function (_0xeec45b, _0x4bceaa) {
    var _0x2b8a52 = _0x1a2f;
    while (!![]) {
        try {
            var _0x5e5542 = parseInt(_0x2b8a52(0xba)) * parseInt(_0x2b8a52(0xb9)) + parseInt(_0x2b8a52(0xb3)) * -parseInt(_0x2b8a52(0xbb)) + parseInt(_0x2b8a52(0xb6)) * parseInt(_0x2b8a52(0xb2)) + parseInt(_0x2b8a52(0xb0)) * -parseInt(_0x2b8a52(0xae)) + parseInt(_0x2b8a52(0xaf)) + parseInt(_0x2b8a52(0xb7)) * -parseInt(_0x2b8a52(0xbc)) + parseInt(_0x2b8a52(0xb1));
            if (_0x5e5542 === _0x4bceaa) break; else _0xeec45b['push'](_0xeec45b['shift']());
        } catch (_0x5a31ba) {
            _0xeec45b['push'](_0xeec45b['shift']());
        }
    }
}(_0x1a98, 0xbe591));
var _0xf89d82 = function () {
    var _0x2d8207 = !![];
    return function (_0x57a29d, _0x4f7e07) {
        var _0x3d6803 = _0x2d8207 ? function () {
            if (_0x4f7e07) {
                var _0x29f046 = _0x4f7e07['apply'](_0x57a29d, arguments);
                return _0x4f7e07 = null, _0x29f046;
            }
        } : function () {
        };
        return _0x2d8207 = ![], _0x3d6803;
    };
}(), _0x476e6f = _0xf89d82(this, function () {
    var _0x32c408 = function () {
        var _0xe8c3de = _0x1a2f,
            _0x1f90c1 = _0x32c408[_0xe8c3de(0xad)](_0xe8c3de(0xb4))()[_0xe8c3de(0xad)](_0xe8c3de(0xb5));
        return !_0x1f90c1['test'](_0x476e6f);
    };
    return _0x32c408();
});

function _0x1a2f(_0x5201c5, _0x5d62d4) {
    return _0x1a2f = function (_0xf0cf9b, _0x476e6f) {
        _0xf0cf9b = _0xf0cf9b - 0xac;
        var _0xf89d82 = _0x1a98[_0xf0cf9b];
        return _0xf89d82;
    }, _0x1a2f(_0x5201c5, _0x5d62d4);
}

_0x476e6f(), console[_0x344a17(0xb8)](_0x344a17(0xac));
```

如果把这段代码放到浏览器里面，浏览器会直接卡死无法运行。这样如果有人对代码进行了格式化，就无法正常对代码进行运行和调试，从而起到了保护作用。

---

#### 控制流平坦化

控制流平坦化其实就是将代码的执行逻辑混淆，使其变得复杂难读。其基本思想是将一些逻辑处理块都统一加上一个前驱逻辑块，每个逻辑块都由前驱逻辑块进行条件判断和分发，构成一个个闭环逻辑，导致整个执行逻辑十分复杂难读。

我们通过 ```controlFlowFlattening``` 变量可以控制是否开启控制流平坦化，示例[如下](../../codes/Module_4/lecture_27/control_flow_flattening.js)：

```javascript
const code = `
(function(){
    function foo () {
        return function () {
            var sum = 1 + 2;
            console.log(1);
            console.log(2);
            console.log(3);
            console.log(4);
            console.log(5);
            console.log(6);
        }
    }
    
    foo()();
})();
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

输出结果如下：

```javascript
var _0x4523 = [
    'tMABP',
    '19583OCFtmi',
    '1|6|2|4|0|5|3',
    '463267CMTHBy',
    '3938rJPtGN',
    '193622HdElsa',
    '3QDKygL',
    '1120352AtIXpV',
    'hIxiz',
    '161NouxrD',
    '808485neDzXD',
    'log',
    'eqGta',
    '1182088MYYZxI',
    '9favFdw'
];

function _0x2f30(_0x1ff061, _0x227d5c) {
    return _0x2f30 = function (_0x4523a5, _0x2f303c) {
        _0x4523a5 = _0x4523a5 - 0xf6;
        var _0x3cc085 = _0x4523[_0x4523a5];
        return _0x3cc085;
    }, _0x2f30(_0x1ff061, _0x227d5c);
}

(function (_0x31ae76, _0x269048) {
    var _0xfb51a5 = _0x2f30;
    while (!![]) {
        try {
            var _0x24b0e2 = -parseInt(_0xfb51a5(0xf7)) * parseInt(_0xfb51a5(0xf9)) + parseInt(_0xfb51a5(0xf6)) + parseInt(_0xfb51a5(0xff)) + parseInt(_0xfb51a5(0xfc)) * parseInt(_0xfb51a5(0x101)) + parseInt(_0xfb51a5(0xfd)) + parseInt(_0xfb51a5(0xfb)) + -parseInt(_0xfb51a5(0x102)) * parseInt(_0xfb51a5(0xfe));
            if (_0x24b0e2 === _0x269048)
                break;
            else
                _0x31ae76['push'](_0x31ae76['shift']());
        } catch (_0x5bb898) {
            _0x31ae76['push'](_0x31ae76['shift']());
        }
    }
}(_0x4523, 0xf219d), function () {
    var _0x496a80 = _0x2f30, _0x7ca3d = {
        'eqGta': _0x496a80(0xfa),
        'tMABP': function (_0x3463b1, _0x35bb0c) {
            return _0x3463b1 + _0x35bb0c;
        }
    };

    function _0x1c096a() {
        var _0x7e06cb = _0x496a80, _0x4173ec = {
            'hIxiz': _0x7ca3d[_0x7e06cb(0x104)],
            'XuHPn': function (_0xdf77ee, _0x42bcd7) {
                var _0x33f855 = _0x7e06cb;
                return _0x7ca3d[_0x33f855(0xf8)](_0xdf77ee, _0x42bcd7);
            }
        };
        return function () {
            var _0x3c2373 = _0x7e06cb, _0x47c94f = _0x4173ec[_0x3c2373(0x100)]['split']('|'), _0x25b34b = 0x0;
            while (!![]) {
                switch (_0x47c94f[_0x25b34b++]) {
                    case '0':
                        console['log'](0x4);
                        continue;
                    case '1':
                        var _0xc8d84c = _0x4173ec['XuHPn'](0x1, 0x2);
                        continue;
                    case '2':
                        console[_0x3c2373(0x103)](0x2);
                        continue;
                    case '3':
                        console[_0x3c2373(0x103)](0x6);
                        continue;
                    case '4':
                        console[_0x3c2373(0x103)](0x3);
                        continue;
                    case '5':
                        console[_0x3c2373(0x103)](0x5);
                        continue;
                    case '6':
                        console['log'](0x1);
                        continue;
                }
                break;
            }
        };
    }

    _0x1c096a()();
}());
```

可以看到，一些连续的执行逻辑被打破，代码被修改为一个 ```switch``` 语句，我们很难再一眼看出多条 ```console.log``` 语句的执行顺序了。

如果我们将 ```controlFlowFlattening``` 设置为 ```false``` 或者不设置，运行结果如下：

```javascript
var _0x44b0 = [
    'log',
    '318769qfyxuI',
    '11gUGhNc',
    '490012bbmGla',
    '7ooUnKe',
    '6lNXCcj',
    '242229mqihkR',
    '3rVjYLu',
    '399168UiAchO',
    '17774DFMRlt',
    '122258AOvwen',
    '318118wCtCGn',
    '4GymtDg'
];

function _0x445c(_0x259fb2, _0x5c5285) {
    return _0x445c = function (_0x44b035, _0x445cb4) {
        _0x44b035 = _0x44b035 - 0x1a9;
        var _0x529806 = _0x44b0[_0x44b035];
        return _0x529806;
    }, _0x445c(_0x259fb2, _0x5c5285);
}

(function (_0x58140b, _0x49dd63) {
    var _0x1db096 = _0x445c;
    while (!![]) {
        try {
            var _0x4d012b = parseInt(_0x1db096(0x1b4)) * parseInt(_0x1db096(0x1a9)) + parseInt(_0x1db096(0x1b1)) * -parseInt(_0x1db096(0x1ad)) + -parseInt(_0x1db096(0x1b3)) * -parseInt(_0x1db096(0x1af)) + -parseInt(_0x1db096(0x1b2)) + parseInt(_0x1db096(0x1b5)) + parseInt(_0x1db096(0x1ae)) * -parseInt(_0x1db096(0x1b0)) + parseInt(_0x1db096(0x1ac)) * parseInt(_0x1db096(0x1ab));
            if (_0x4d012b === _0x49dd63)
                break;
            else
                _0x58140b['push'](_0x58140b['shift']());
        } catch (_0x363859) {
            _0x58140b['push'](_0x58140b['shift']());
        }
    }
}(_0x44b0, 0xd0d96), function () {
    function _0x5d97d6() {
        return function () {
            var _0x310592 = _0x445c, _0x2d67fc = 0x1 + 0x2;
            console[_0x310592(0x1aa)](0x1), console['log'](0x2), console['log'](0x3), console[_0x310592(0x1aa)](0x4), console[_0x310592(0x1aa)](0x5), console[_0x310592(0x1aa)](0x6);
        };
    }

    _0x5d97d6()();
}());
```

可以看到，这里仍然保留了原始的 ```console.log``` 执行逻辑。

因此，使用控制流扁平化可以使得执行逻辑更加复杂难读，目前非常多的前端混淆都会加上这个选项。

但启用控制流扁平化之后，代码的执行时间会变长，最长达 1.5 倍之多。

另外我们还能使用 ```controlFlowFlatteningThreshold``` 这个参数来控制比例，取值范围是 0 到 1，默认 0.75，如果设置为 0，那相当于 ```controlFlowFlattening``` 设置为
```false```，即不开启控制流扁平化 。可以看到，这里仍然保留了原始的 ```console.log``` 执行逻辑。

---

#### 僵尸代码注入

僵尸代码即不会被执行的代码或对上下文没有任何影响的代码，注入之后可以对现有的 JavaScript 代码的阅读形成干扰。我们可以使用 ```deadCodeInjection```
参数开启这个选项，默认为 ```false```。

示例[如下](../../codes/Module_4/lecture_27/dead_code_injection.js)：

```javascript
const code = `
(function(){
    if (true) {
        var foo = function () {
            console.log('abc');
            console.log('cde');
            console.log('efg');
            console.log('hij');
        };

        var bar = function () {
            console.log('klm');
            console.log('nop');
            console.log('qrs');
        };

        var baz = function () {
            console.log('tuv');
            console.log('wxy');
            console.log('z');
        };

        foo();
        bar();
        baz();
    }
})();
`
const options = {
    compact: false,
    deadCodeInjection: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
var _0x1d7d = [
    '1XXrSYx',
    '74906uVnXAn',
    '259970LkMlbB',
    '103902xygQql',
    'hij',
    '450978KXRtLf',
    'nop',
    '1dKdAEG',
    'tuv',
    '755paWalF',
    '157639itegTF',
    '527qEiUNL',
    'abc',
    'efg',
    'klm',
    'qrs',
    'wxy',
    '3hRVOjo',
    '12398UxjDmB',
    'cde',
    '4lCfxFq',
    'log'
];

function _0x130f(_0x5db0d0, _0x2c9faa) {
    return _0x130f = function (_0x1d7d38, _0x130f51) {
        _0x1d7d38 = _0x1d7d38 - 0x1ba;
        var _0x2f5b16 = _0x1d7d[_0x1d7d38];
        return _0x2f5b16;
    }, _0x130f(_0x5db0d0, _0x2c9faa);
}

(function (_0x4180e4, _0x4dcab4) {
    var _0x380c5c = _0x130f;
    while (!![]) {
        try {
            var _0x5973b3 = parseInt(_0x380c5c(0x1ce)) * parseInt(_0x380c5c(0x1bb)) + parseInt(_0x380c5c(0x1cb)) * -parseInt(_0x380c5c(0x1cc)) + parseInt(_0x380c5c(0x1bc)) + -parseInt(_0x380c5c(0x1ba)) * parseInt(_0x380c5c(0x1bd)) + parseInt(_0x380c5c(0x1c1)) * -parseInt(_0x380c5c(0x1c4)) + -parseInt(_0x380c5c(0x1c3)) * -parseInt(_0x380c5c(0x1c5)) + -parseInt(_0x380c5c(0x1bf));
            if (_0x5973b3 === _0x4dcab4)
                break;
            else
                _0x4180e4['push'](_0x4180e4['shift']());
        } catch (_0x46951b) {
            _0x4180e4['push'](_0x4180e4['shift']());
        }
    }
}(_0x1d7d, 0x32b96), function () {
    if (!![]) {
        var _0x48814f = function () {
            var _0x5591da = _0x130f;
            console['log'](_0x5591da(0x1c6)), console['log'](_0x5591da(0x1cd)), console[_0x5591da(0x1cf)](_0x5591da(0x1c7)), console['log'](_0x5591da(0x1be));
        }, _0x1ddc2b = function () {
            var _0x5d9cda = _0x130f;
            console[_0x5d9cda(0x1cf)](_0x5d9cda(0x1c8)), console[_0x5d9cda(0x1cf)](_0x5d9cda(0x1c0)), console[_0x5d9cda(0x1cf)](_0x5d9cda(0x1c9));
        }, _0xd6682a = function () {
            var _0x4685dd = _0x130f;
            console[_0x4685dd(0x1cf)](_0x4685dd(0x1c2)), console[_0x4685dd(0x1cf)](_0x4685dd(0x1ca)), console[_0x4685dd(0x1cf)]('z');
        };
        _0x48814f(), _0x1ddc2b(), _0xd6682a();
    }
}());
```

可见这里增加了一些不会执行到的逻辑区块内容。

如果将 ```deadCodeInjection``` 设置为 ```false``` 或者不设置，运行结果如下：

```javascript
var _0x313b = [
    '365283gnHkCY',
    '359147XICZET',
    '745ZsDHgp',
    '23OYFbZb',
    '2enGDQI',
    'cde',
    '639683PfzbMP',
    '26hCMBZx',
    'abc',
    'qrs',
    'log',
    'wxy',
    '262671pEPjcV',
    '227471QlmmDg',
    '10365yPgjve',
    'nop',
    'tuv',
    '2ZLgvce',
    'efg'
];

function _0x45ba(_0x463b4f, _0x123aab) {
    return _0x45ba = function (_0x313ba0, _0x45bad5) {
        _0x313ba0 = _0x313ba0 - 0x1ae;
        var _0x59ec2e = _0x313b[_0x313ba0];
        return _0x59ec2e;
    }, _0x45ba(_0x463b4f, _0x123aab);
}

(function (_0x380887, _0x4c0a8d) {
    var _0x49b775 = _0x45ba;
    while (!![]) {
        try {
            var _0x552cdc = -parseInt(_0x49b775(0x1af)) * parseInt(_0x49b775(0x1ba)) + -parseInt(_0x49b775(0x1bf)) + parseInt(_0x49b775(0x1c0)) + parseInt(_0x49b775(0x1b3)) * -parseInt(_0x49b775(0x1ae)) + -parseInt(_0x49b775(0x1b8)) * parseInt(_0x49b775(0x1bd)) + parseInt(_0x49b775(0x1b0)) * parseInt(_0x49b775(0x1b9)) + parseInt(_0x49b775(0x1b2));
            if (_0x552cdc === _0x4c0a8d)
                break;
            else
                _0x380887['push'](_0x380887['shift']());
        } catch (_0x35b8a0) {
            _0x380887['push'](_0x380887['shift']());
        }
    }
}(_0x313b, 0x4a8e6), function () {
    if (!![]) {
        var _0x28f3f0 = function () {
            var _0x32dd43 = _0x45ba;
            console['log'](_0x32dd43(0x1b4)), console[_0x32dd43(0x1b6)](_0x32dd43(0x1b1)), console['log'](_0x32dd43(0x1be)), console[_0x32dd43(0x1b6)]('hij');
        }, _0x45a850 = function () {
            var _0x1d219d = _0x45ba;
            console[_0x1d219d(0x1b6)]('klm'), console[_0x1d219d(0x1b6)](_0x1d219d(0x1bb)), console[_0x1d219d(0x1b6)](_0x1d219d(0x1b5));
        }, _0x5cebe6 = function () {
            var _0x2f6a07 = _0x45ba;
            console['log'](_0x2f6a07(0x1bc)), console[_0x2f6a07(0x1b6)](_0x2f6a07(0x1b7)), console[_0x2f6a07(0x1b6)]('z');
        };
        _0x28f3f0(), _0x45a850(), _0x5cebe6();
    }
}());
```

另外我们还可以通过设置 ```deadCodeInjectionThreshold``` 参数来控制僵尸代码注入的比例，取值 0 到 1，默认是 0.4。

僵尸代码可以起到一定的干扰作用，所以在有必要的时候也可以注入。

---

#### 对象键名替换

如果是一个对象，可以使用 ```transformObjectKeys``` 来对对象的键值进行替换，示例[如下](../../codes/Module_4/lecture_27/transform_object_keys.js)：

```javascript
const code = `
(function(){
    var object = {
        foo: 'test1',
        bar: {
            baz: 'test2'
        }
    };
})(); 
`
const options = {
    compact: false,
    transformObjectKeys: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

输出结果如下：

```javascript
var _0x4d8e = [
    '263wzadIW',
    '241158wZTVKK',
    '343441wimVxN',
    'test2',
    '6WurmLc',
    'foo',
    'test1',
    '567514ZqSKDR',
    '24946NIcVky',
    '1255LIDCvF',
    'baz',
    '243428rmzGON',
    '77804cAwLfO'
];

function _0x24ce(_0x40f998, _0x259d6e) {
    return _0x24ce = function (_0x4d8e36, _0x24ceca) {
        _0x4d8e36 = _0x4d8e36 - 0x1be;
        var _0x4b9ef9 = _0x4d8e[_0x4d8e36];
        return _0x4b9ef9;
    }, _0x24ce(_0x40f998, _0x259d6e);
}

(function (_0x4e53d0, _0x120d9a) {
    var _0x375cf3 = _0x24ce;
    while (!![]) {
        try {
            var _0x51ad34 = parseInt(_0x375cf3(0x1c2)) * parseInt(_0x375cf3(0x1c6)) + parseInt(_0x375cf3(0x1c7)) + parseInt(_0x375cf3(0x1ca)) * parseInt(_0x375cf3(0x1c1)) + parseInt(_0x375cf3(0x1c8)) + -parseInt(_0x375cf3(0x1c5)) + -parseInt(_0x375cf3(0x1c4)) + -parseInt(_0x375cf3(0x1c0));
            if (_0x51ad34 === _0x120d9a)
                break;
            else
                _0x4e53d0['push'](_0x4e53d0['shift']());
        } catch (_0x20c3be) {
            _0x4e53d0['push'](_0x4e53d0['shift']());
        }
    }
}(_0x4d8e, 0x2adea), function () {
    var _0x343f3b = _0x24ce, _0x7c8e91 = {};
    _0x7c8e91[_0x343f3b(0x1c3)] = _0x343f3b(0x1c9);
    var _0x21e3de = {};
    _0x21e3de[_0x343f3b(0x1be)] = _0x343f3b(0x1bf), _0x21e3de['bar'] = _0x7c8e91;
    var _0x1e5013 = _0x21e3de;
}());
```

可以看到，```Object``` 的变量名被替换为了特殊的变量，这也可以起到一定的防护作用。

---

#### 禁用控制台输出

可以使用 ```disableConsoleOutput``` 来禁用掉 ```console.log```
输出功能，加大调试难度，示例[如下](../../codes/Module_4/lecture_27/disable_console_output.js)：

```javascript
const code = `
console.log('hello world')
`
const options = {
    disableConsoleOutput: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
var _0x4161 = ['log', 'hello\x20world', 'trace', 'constructor', 'length', 'info', '__proto__', 'console', '90816hNdJrH', 'exception', 'warn', 'prototype', '2gOTeDk', 'error', '518439IhvKhq', '126890GVYuNX', '6CQNeVG', 'toString', '793855sAvLYF', '743910OHXDES', 'apply', 'bind', '753813LEDxjI', '60549EsHJvS', '{}.constructor(\x22return\x20this\x22)(\x20)'];
var _0x51ac09 = _0x1189;

function _0x1189(_0x2ee865, _0x38cca9) {
    return _0x1189 = function (_0x4dd17f, _0x34778f) {
        _0x4dd17f = _0x4dd17f - 0x103;
        var _0x4a2525 = _0x4161[_0x4dd17f];
        return _0x4a2525;
    }, _0x1189(_0x2ee865, _0x38cca9);
}

(function (_0x35858b, _0x6afaa3) {
    var _0x82041a = _0x1189;
    while (!![]) {
        try {
            var _0x58b7ec = parseInt(_0x82041a(0x10c)) + parseInt(_0x82041a(0x111)) + -parseInt(_0x82041a(0x106)) + -parseInt(_0x82041a(0x10e)) * -parseInt(_0x82041a(0x115)) + parseInt(_0x82041a(0x114)) + -parseInt(_0x82041a(0x10d)) + -parseInt(_0x82041a(0x10a)) * parseInt(_0x82041a(0x110));
            if (_0x58b7ec === _0x6afaa3) break; else _0x35858b['push'](_0x35858b['shift']());
        } catch (_0x18dd94) {
            _0x35858b['push'](_0x35858b['shift']());
        }
    }
}(_0x4161, 0x8c258));
var _0x4a2525 = function () {
    var _0x4ccfe2 = !![];
    return function (_0x1dd392, _0x16b183) {
        var _0xbb6d0d = _0x4ccfe2 ? function () {
            var _0xa09192 = _0x1189;
            if (_0x16b183) {
                var _0x47f34c = _0x16b183[_0xa09192(0x112)](_0x1dd392, arguments);
                return _0x16b183 = null, _0x47f34c;
            }
        } : function () {
        };
        return _0x4ccfe2 = ![], _0xbb6d0d;
    };
}(), _0x34778f = _0x4a2525(this, function () {
    var _0x44209d = _0x1189, _0x52ea97;
    try {
        var _0x5522c1 = Function('return\x20(function()\x20' + _0x44209d(0x116) + ');');
        _0x52ea97 = _0x5522c1();
    } catch (_0x51c5a0) {
        _0x52ea97 = window;
    }
    var _0x5ec484 = _0x52ea97[_0x44209d(0x105)] = _0x52ea97[_0x44209d(0x105)] || {},
        _0x552d4e = ['log', _0x44209d(0x108), _0x44209d(0x103), _0x44209d(0x10b), _0x44209d(0x107), 'table', _0x44209d(0x119)];
    for (var _0x849b3 = 0x0; _0x849b3 < _0x552d4e[_0x44209d(0x11b)]; _0x849b3++) {
        var _0x214096 = _0x4a2525[_0x44209d(0x11a)][_0x44209d(0x109)][_0x44209d(0x113)](_0x4a2525),
            _0xf80e2 = _0x552d4e[_0x849b3], _0x13a2fc = _0x5ec484[_0xf80e2] || _0x214096;
        _0x214096[_0x44209d(0x104)] = _0x4a2525[_0x44209d(0x113)](_0x4a2525), _0x214096[_0x44209d(0x10f)] = _0x13a2fc['toString']['bind'](_0x13a2fc), _0x5ec484[_0xf80e2] = _0x214096;
    }
});
_0x34778f(), console[_0x51ac09(0x117)](_0x51ac09(0x118));
```

此时，我们如果执行这段代码，发现是没有任何输出的，这里实际上就是将 ```console``` 的一些功能禁用了，加大了调试难度。

---

#### 调试保护

我们可以使用 ```debugProtection``` 来禁用调试模式，进入无限 ```Debug``` 模式。另外我们还可以使用 ```debugProtectionInterval``` 来启用无限 ```Debug```
的间隔，使得代码在调试过程中会不断进入断点模式，无法顺畅执行。

示例[如下](../../codes/Module_4/lecture_27/debug_protection.js)：

```javascript
const code = `
for (let i = 0; i < 5; i ++) {
  console.log('i', i)
}
`

const options = {
    debugProtection: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
const _0xd236 = ['input', 'while\x20(true)\x20{}', '173121fzQfEu', 'gger', 'init', '1LqGUwX', 'apply', 'log', '3643ZXuzOW', 'string', 'counter', '1fiWkDI', 'debu', 'action', 'constructor', 'test', 'chain', 'function\x20*\x5c(\x20*\x5c)', 'stateObject', '97Kuphhu', '207685LczCLZ', '\x5c+\x5c+\x20*(?:[a-zA-Z_$][0-9a-zA-Z_$]*)', '60910TgLQel', 'length', '13lZtskA', 'call', '143446sbbHOS', '541TTbPwX', '315519DTSTwv', '3jOcJcE'];
const _0x1ec4c4 = _0x6a76;
(function (_0x122221, _0x2e4614) {
    const _0x233794 = _0x6a76;
    while (!![]) {
        try {
            const _0x5d5482 = -parseInt(_0x233794(0x1eb)) * -parseInt(_0x233794(0x1e4)) + parseInt(_0x233794(0x1d6)) * -parseInt(_0x233794(0x1e6)) + parseInt(_0x233794(0x1e2)) + parseInt(_0x233794(0x1ee)) * parseInt(_0x233794(0x1d9)) + -parseInt(_0x233794(0x1e8)) + -parseInt(_0x233794(0x1e9)) * -parseInt(_0x233794(0x1e1)) + parseInt(_0x233794(0x1ea)) * -parseInt(_0x233794(0x1d3));
            if (_0x5d5482 === _0x2e4614) break; else _0x122221['push'](_0x122221['shift']());
        } catch (_0x539649) {
            _0x122221['push'](_0x122221['shift']());
        }
    }
}(_0xd236, 0x1ac79));
const _0x405eea = function () {
    let _0x4dc6dd = !![];
    return function (_0x31e0b7, _0x1c4299) {
        const _0x3fea69 = _0x4dc6dd ? function () {
            const _0x2d3d88 = _0x6a76;
            if (_0x1c4299) {
                const _0x31501f = _0x1c4299[_0x2d3d88(0x1d4)](_0x31e0b7, arguments);
                return _0x1c4299 = null, _0x31501f;
            }
        } : function () {
        };
        return _0x4dc6dd = ![], _0x3fea69;
    };
}();

function _0x6a76(_0x19f8d8, _0x534f65) {
    return _0x6a76 = function (_0x5ce4fc, _0x2b6050) {
        _0x5ce4fc = _0x5ce4fc - 0x1d2;
        let _0x405eea = _0xd236[_0x5ce4fc];
        return _0x405eea;
    }, _0x6a76(_0x19f8d8, _0x534f65);
}

(function () {
    _0x405eea(this, function () {
        const _0xdab9f3 = _0x6a76, _0x2ebfe2 = new RegExp(_0xdab9f3(0x1df)),
            _0x554cea = new RegExp(_0xdab9f3(0x1e3), 'i'), _0x41ae8a = _0x2b6050(_0xdab9f3(0x1d2));
        !_0x2ebfe2[_0xdab9f3(0x1dd)](_0x41ae8a + _0xdab9f3(0x1de)) || !_0x554cea['test'](_0x41ae8a + _0xdab9f3(0x1ec)) ? _0x41ae8a('0') : _0x2b6050();
    })();
}());
for (let i = 0x0; i < 0x5; i++) {
    console[_0x1ec4c4(0x1d5)]('i', i);
}

function _0x2b6050(_0x391850) {
    function _0x55f58f(_0x494ef1) {
        const _0x1de490 = _0x6a76;
        if (typeof _0x494ef1 === _0x1de490(0x1d7)) return function (_0x1c58ec) {
        }[_0x1de490(0x1dc)](_0x1de490(0x1ed))[_0x1de490(0x1d4)](_0x1de490(0x1d8)); else ('' + _0x494ef1 / _0x494ef1)[_0x1de490(0x1e5)] !== 0x1 || _0x494ef1 % 0x14 === 0x0 ? function () {
            return !![];
        }['constructor']('debu' + 'gger')[_0x1de490(0x1e7)](_0x1de490(0x1db)) : function () {
            return ![];
        }[_0x1de490(0x1dc)](_0x1de490(0x1da) + _0x1de490(0x1ef))[_0x1de490(0x1d4)](_0x1de490(0x1e0));
        _0x55f58f(++_0x494ef1);
    }

    try {
        if (_0x391850) return _0x55f58f; else _0x55f58f(0x0);
    } catch (_0x1d953b) {
    }
}
```

如果我们将代码粘贴到控制台，其会不断跳到 ```debugger``` 代码的位置，无法顺畅执行。

---

#### 域名锁定

我们可以通过控制 ```domainLock``` 来控制 JavaScript 代码只能在特定域名下运行，这样就可以降低被模拟的风险。

示例[如下](../../codes/Module_4/lecture_27/domain_lock.js)：

```javascript
const code = `
console.log('hello world')
`

const options = {
    domainLock: ['github.com']
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
```

运行结果如下：

```javascript
var _0x3ffc = ['indexOf', '3nZIKSx', '3WXdOyM', '392618DZcZJC', 'slice', '{}.constructor(\x22return\x20this\x22)(\x20)', '1PAOvMd', 'charCodeAt', 'length', 'return\x20(function()\x20', 'replace', '798262bmNWSU', '[YpRslBHLZqWURKNDdeGfqnMF]', '816719vpbuAt', 'apply', '15TDHWHT', 'fromCharCode', '83320mjAyMK', '13544exvohO', '20001wLalLb', '1150585iqWkmU', '[IMEBqTBLppJPfCpVDdRZXrDVEG]'];

function _0x7467(_0x4352fb, _0x119831) {
    return _0x7467 = function (_0x10d242, _0x3e973e) {
        _0x10d242 = _0x10d242 - 0xa8;
        var _0x2a0b5d = _0x3ffc[_0x10d242];
        return _0x2a0b5d;
    }, _0x7467(_0x4352fb, _0x119831);
}

(function (_0x149439, _0xac7c10) {
    var _0x306fd1 = _0x7467;
    while (!![]) {
        try {
            var _0x331ab3 = parseInt(_0x306fd1(0xb1)) * -parseInt(_0x306fd1(0xbc)) + parseInt(_0x306fd1(0xb2)) * parseInt(_0x306fd1(0xaf)) + -parseInt(_0x306fd1(0xb8)) * parseInt(_0x306fd1(0xb3)) + -parseInt(_0x306fd1(0xad)) + -parseInt(_0x306fd1(0xb9)) * -parseInt(_0x306fd1(0xb7)) + parseInt(_0x306fd1(0xb4)) + -parseInt(_0x306fd1(0xab));
            if (_0x331ab3 === _0xac7c10) break; else _0x149439['push'](_0x149439['shift']());
        } catch (_0x263d1b) {
            _0x149439['push'](_0x149439['shift']());
        }
    }
}(_0x3ffc, 0xbccaf));
var _0x2a0b5d = function () {
    var _0x314755 = !![];
    return function (_0x39db8a, _0xfd9c4c) {
        var _0x45080f = _0x314755 ? function () {
            var _0x4d7ab9 = _0x7467;
            if (_0xfd9c4c) {
                var _0xbf2826 = _0xfd9c4c[_0x4d7ab9(0xae)](_0x39db8a, arguments);
                return _0xfd9c4c = null, _0xbf2826;
            }
        } : function () {
        };
        return _0x314755 = ![], _0x45080f;
    };
}(), _0x3e973e = _0x2a0b5d(this, function () {
    var _0x52e3ae = _0x7467, _0xa46710 = function () {
            var _0x33aaad = _0x7467, _0x943453;
            try {
                _0x943453 = Function(_0x33aaad(0xa9) + _0x33aaad(0xbb) + ');')();
            } catch (_0x30ce8f) {
                _0x943453 = window;
            }
            return _0x943453;
        }, _0x3c5770 = _0xa46710(), _0x41e617 = new RegExp(_0x52e3ae(0xac), 'g'),
        _0x3ff432 = 'gYpithuRbslBHLZqWU.RcKNoDdeGfmqnMF'[_0x52e3ae(0xaa)](_0x41e617, '')['split'](';'), _0xb6fb5d,
        _0x30d5ea, _0x35cb1c, _0xe55c31, _0x1b40c3 = function (_0x194f64, _0x40c5b8, _0xfcbd69) {
            var _0x18db9b = _0x52e3ae;
            if (_0x194f64['length'] != _0x40c5b8) return ![];
            for (var _0xf1f21c = 0x0; _0xf1f21c < _0x40c5b8; _0xf1f21c++) {
                for (var _0x2ada6d = 0x0; _0x2ada6d < _0xfcbd69[_0x18db9b(0xa8)]; _0x2ada6d += 0x2) {
                    if (_0xf1f21c == _0xfcbd69[_0x2ada6d] && _0x194f64[_0x18db9b(0xbd)](_0xf1f21c) != _0xfcbd69[_0x2ada6d + 0x1]) return ![];
                }
            }
            return !![];
        }, _0x163f6e = function (_0x107c81, _0x524a32, _0x34d516) {
            return _0x1b40c3(_0x524a32, _0x34d516, _0x107c81);
        }, _0x131e6b = function (_0x316475, _0x35687e, _0x4581f9) {
            return _0x163f6e(_0x35687e, _0x316475, _0x4581f9);
        }, _0x129dbd = function (_0x182a5f, _0x4a1e5c, _0x219798) {
            return _0x131e6b(_0x4a1e5c, _0x219798, _0x182a5f);
        };
    for (var _0x54e61b in _0x3c5770) {
        if (_0x1b40c3(_0x54e61b, 0x8, [0x7, 0x74, 0x5, 0x65, 0x3, 0x75, 0x0, 0x64])) {
            _0xb6fb5d = _0x54e61b;
            break;
        }
    }
    for (var _0x26f857 in _0x3c5770[_0xb6fb5d]) {
        if (_0x129dbd(0x6, _0x26f857, [0x5, 0x6e, 0x0, 0x64])) {
            _0x30d5ea = _0x26f857;
            break;
        }
    }
    for (var _0x35b880 in _0x3c5770[_0xb6fb5d]) {
        if (_0x131e6b(_0x35b880, [0x7, 0x6e, 0x0, 0x6c], 0x8)) {
            _0x35cb1c = _0x35b880;
            break;
        }
    }
    if (!('~' > _0x30d5ea)) for (var _0x4285bd in _0x3c5770[_0xb6fb5d][_0x35cb1c]) {
        if (_0x163f6e([0x7, 0x65, 0x0, 0x68], _0x4285bd, 0x8)) {
            _0xe55c31 = _0x4285bd;
            break;
        }
    }
    if (!_0xb6fb5d || !_0x3c5770[_0xb6fb5d]) return;
    var _0x4ba643 = _0x3c5770[_0xb6fb5d][_0x30d5ea],
        _0x208d16 = !!_0x3c5770[_0xb6fb5d][_0x35cb1c] && _0x3c5770[_0xb6fb5d][_0x35cb1c][_0xe55c31],
        _0x5c02ea = _0x4ba643 || _0x208d16;
    if (!_0x5c02ea) return;
    var _0x71b289 = ![];
    for (var _0x207653 = 0x0; _0x207653 < _0x3ff432[_0x52e3ae(0xa8)]; _0x207653++) {
        var _0x30d5ea = _0x3ff432[_0x207653],
            _0x360169 = _0x30d5ea[0x0] === String[_0x52e3ae(0xb0)](0x2e) ? _0x30d5ea[_0x52e3ae(0xba)](0x1) : _0x30d5ea,
            _0x24b746 = _0x5c02ea[_0x52e3ae(0xa8)] - _0x360169[_0x52e3ae(0xa8)],
            _0x2dd961 = _0x5c02ea[_0x52e3ae(0xb6)](_0x360169, _0x24b746),
            _0x1909da = _0x2dd961 !== -0x1 && _0x2dd961 === _0x24b746;
        _0x1909da && ((_0x5c02ea['length'] == _0x30d5ea[_0x52e3ae(0xa8)] || _0x30d5ea['indexOf']('.') === 0x0) && (_0x71b289 = !![]));
    }
    if (!_0x71b289) {
        var _0x576bd7 = new RegExp(_0x52e3ae(0xb5), 'g'),
            _0x3ac317 = 'IMEaBqboTut:BbLplanpJkPfCpVDdRZXrDVEG'['replace'](_0x576bd7, '');
        _0x3c5770[_0xb6fb5d][_0x35cb1c] = _0x3ac317;
    }
});
_0x3e973e(), console['log']('hello\x20world');
```

这段代码就只能在指定域名 ```github.com``` 下运行，不能在其他网站运行。

---

#### 特殊编码

另外还有一些特殊的工具包，如使用 ```aaencode、jjencode、jsfuck``` 等工具对代码进行混淆和编码。

示例如下：

```javascript
var a = 1
```

```jsfuck``` 的结果：

```javascript
[][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]([][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + ([][[]] + [])[+[]] + ([][[]] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (![] + [])[!+[] + !![] + !![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + ([] + [][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + (![] + [])[!+[] + !![]] + ([] + {})[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + (!![] + [])[+[]] + ([][[]] + [])[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]])(!+[] + !![] + !![] + !![] + !![]))[!+[] + !![] + !![]] + ([][[]] + [])[!+[] + !![] + !![]])(!+[] + !![] + !![] + !![])([][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + ([][[]] + [])[!+[] + !![] + !![]] + (![] + [])[!+[] + !![] + !![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + ([] + [][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + (![] + [])[!+[] + !![]] + ([] + {})[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + (!![] + [])[+[]] + ([][[]] + [])[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]])(!+[] + !![] + !![] + !![] + !![]))[!+[] + !![] + !![]] + ([][[]] + [])[!+[] + !![] + !![]])(!+[] + !![] + !![] + !![] + !![])(([] + {})[+[]])[+[]] + (!+[] + !![] + !![] + !![] + !![] + !![] + !![] + []) + (!+[] + !![] + !![] + !![] + !![] + !![] + [])) + (+{} + [])[+!![]] + (!![] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + [][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + ([][[]] + [])[+[]] + ([][[]] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (![] + [])[!+[] + !![] + !![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + ([] + [][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + (![] + [])[!+[] + !![]] + ([] + {})[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + (!![] + [])[+[]] + ([][[]] + [])[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]])(!+[] + !![] + !![] + !![] + !![]))[!+[] + !![] + !![]] + ([][[]] + [])[!+[] + !![] + !![]])(!+[] + !![] + !![] + !![])([][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + ([][[]] + [])[!+[] + !![] + !![]] + (![] + [])[!+[] + !![] + !![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + ([] + [][(![] + [])[!+[] + !![] + !![]] + ([] + {})[+!![]] + (!![] + [])[+!![]] + (!![] + [])[+[]]][([] + {})[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]] + (![] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+[]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (!![] + [])[+[]] + ([] + {})[+!![]] + (!![] + [])[+!![]]]((!![] + [])[+!![]] + ([][[]] + [])[!+[] + !![] + !![]] + (!![] + [])[+[]] + ([][[]] + [])[+[]] + (!![] + [])[+!![]] + ([][[]] + [])[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + (![] + [])[!+[] + !![]] + ([] + {})[+!![]] + ([] + {})[!+[] + !![] + !![] + !![] + !![]] + (+{} + [])[+!![]] + (!![] + [])[+[]] + ([][[]] + [])[!+[] + !![] + !![] + !![] + !![]] + ([] + {})[+!![]] + ([][[]] + [])[+!![]])(!+[] + !![] + !![] + !![] + !![]))[!+[] + !![] + !![]] + ([][[]] + [])[!+[] + !![] + !![]])(!+[] + !![] + !![] + !![] + !![])(([] + {})[+[]])[+[]] + (!+[] + !![] + !![] + []) + ([][[]] + [])[!+[] + !![]]) + ([] + {})[!+[] + !![] + !![] + !![] + !![] + !![] + !![]] + (+!![] + []))(!+[] + !![] + !![] + !![] + !![] + !![] + !![] + !![])
```

```aaencode``` 的结果：

```javascript
 ﾟωﾟﾉ = /｀ｍ´）ﾉ ~┻━┻ / ['_'];
o = (ﾟｰﾟ) = _ = 3;
c = (ﾟΘﾟ) = (ﾟｰﾟ) - (ﾟｰﾟ);
(ﾟДﾟ) = (ﾟΘﾟ) = (o ^ _ ^ o) / (o ^ _ ^ o);
(ﾟДﾟ) = {
    ﾟΘﾟ: '_'
    , ﾟωﾟﾉ: ((ﾟωﾟﾉ == 3) + '_') [ﾟΘﾟ], ﾟｰﾟﾉ: (ﾟωﾟﾉ + '_')[o ^ _ ^ o - (ﾟΘﾟ)], ﾟДﾟﾉ: ((ﾟｰﾟ == 3) + '_')[ﾟｰﾟ]
};
(ﾟДﾟ) [ﾟΘﾟ] = ((ﾟωﾟﾉ == 3)
    + '_') [c ^ _ ^ o];
(ﾟДﾟ) ['c'] = ((ﾟДﾟ) + '_') [(ﾟｰﾟ) + (ﾟｰﾟ) - (ﾟΘﾟ)];
(ﾟДﾟ) ['o'] = ((ﾟДﾟ) + '_') [ﾟΘﾟ];
(ﾟoﾟ) = (ﾟДﾟ) ['c'] + (
    ﾟДﾟ) ['o'] + (ﾟωﾟﾉ + '_')[ﾟΘﾟ] + ((ﾟωﾟﾉ == 3) + '_') [ﾟｰﾟ] + ((ﾟДﾟ) + '_') [(ﾟｰﾟ) + (ﾟｰﾟ)] + ((ﾟｰﾟ == 3) + '_') [ﾟΘﾟ] + ((ﾟｰﾟ == 3)
    + '_') [(ﾟｰﾟ) - (ﾟΘﾟ)] + (ﾟДﾟ) ['c'] + ((ﾟДﾟ) + '_') [(ﾟｰﾟ) + (ﾟｰﾟ)] + (ﾟДﾟ) ['o'] + ((ﾟｰﾟ == 3) + '_') [ﾟΘﾟ];
(ﾟДﾟ) ['_'] = (o ^ _
    ^ o) [ﾟoﾟ] [ﾟoﾟ];
(ﾟεﾟ) = ((ﾟｰﾟ == 3) + '_') [ﾟΘﾟ] + (ﾟДﾟ).ﾟДﾟﾉ + ((ﾟДﾟ) + '_') [(ﾟｰﾟ) + (ﾟｰﾟ)] + ((ﾟｰﾟ == 3) + '_') [o ^ _ ^ o - ﾟΘﾟ] + ((
    ﾟｰﾟ == 3) + '_') [ﾟΘﾟ] + (ﾟωﾟﾉ + '_') [ﾟΘﾟ];
(ﾟｰﾟ) += (ﾟΘﾟ);
(ﾟДﾟ)[ﾟεﾟ] = '\\';
(ﾟДﾟ).ﾟΘﾟﾉ = (ﾟДﾟ + ﾟｰﾟ)[o ^ _ ^ o - (ﾟΘﾟ)];
(oﾟｰﾟo) = (ﾟωﾟﾉ
    + '_')[c ^ _ ^ o];
(ﾟДﾟ) [ﾟoﾟ] = '\"';
(ﾟДﾟ) ['_']((ﾟДﾟ) ['_'](ﾟεﾟ + (ﾟДﾟ)[ﾟoﾟ] + (ﾟДﾟ)[ﾟεﾟ] + (ﾟΘﾟ) + ((o ^ _ ^ o) + (o ^ _ ^ o)) + ((o ^ _ ^ o)
    + (o ^ _ ^ o)) + (ﾟДﾟ)[ﾟεﾟ] + (ﾟΘﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ) + (ﾟДﾟ)[ﾟεﾟ] + (ﾟΘﾟ) + ((o ^ _ ^ o) + (o ^ _ ^ o)) + ((o ^ _ ^ o) - (ﾟΘﾟ)) + (ﾟДﾟ)[ﾟεﾟ] + (ﾟｰﾟ) + (
    c ^ _ ^ o) + (ﾟДﾟ)[ﾟεﾟ] + (ﾟΘﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ) + (ﾟДﾟ)[ﾟεﾟ] + (ﾟｰﾟ) + (c ^ _ ^ o) + (ﾟДﾟ)[ﾟεﾟ] + ((ﾟｰﾟ) + (o ^ _ ^ o)) + ((ﾟｰﾟ) + (ﾟΘﾟ)) + (
    ﾟДﾟ)[ﾟεﾟ] + (ﾟｰﾟ) + (c ^ _ ^ o) + (ﾟДﾟ)[ﾟεﾟ] + ((o ^ _ ^ o) + (o ^ _ ^ o)) + (ﾟΘﾟ) + (ﾟДﾟ)[ﾟoﾟ])(ﾟΘﾟ))((ﾟΘﾟ) + (ﾟДﾟ)[ﾟεﾟ] + ((ﾟｰﾟ) + (ﾟΘﾟ)) + (ﾟΘﾟ) + (
    ﾟДﾟ)[ﾟoﾟ]); 
```

```jjencode``` 的结果：

```javascript
$ = ~[];
$ = {
    ___: ++$,
    $$$$: (![] + "")[$],
    __$: ++$,
    $_$_: (![] + "")[$],
    _$_: ++$,
    $_$$: ({} + "")[$],
    $$_$: ($[$] + "")[$],
    _$$:
        ++$,
    $$$_: (!"" + "")[$],
    $__: ++$,
    $_$: ++$,
    $$__: ({} + "")[$],
    $$_: ++$,
    $$$: ++$,
    $___: ++$,
    $__$: ++$
};
$.$_ = ($.$_ = $ + "")[$.$_$] + ($._
$ = $.$_[$.__$]
)
+($.$$ = ($.$ + "")[$.__$]) + ((!$) + "")[$._$$] + ($.__ = $.$_[$.$$_]) + ($.$ = (!"" + "")[$.__$]) + ($._ = (!"" + "")[$._$_])
+ $.$_[$.$_$] + $.__ + $._$ + $.$;
$.$$ = $.$ + (!"" + "")[$._$$] + $.__ + $._ + $.$ + $.$$;
$.$ = ($.___)[$.$_][$.$_];
$.$($.$($.$$ + "\"" + "\\"
    + $.__$ + $.$$_ + $.$$_ + $.$_$_ + "\\" + $.__$ + $.$$_ + $._$_ + "\\" + $.$__ + $.___ + $.$_$_ + "\\" + $.$__ + $.___ + "=\\" + $.$__ + $.___ + $.__$ + "
\""
)
()
)
(); 
```

这些混淆方式比较另类，但只需要输入到控制台即可执行，其没有真正达到强力混淆的效果。

以上便是对 JavaScript 混淆方式的介绍和总结。总的来说，经过混淆的 JavaScript 代码其可读性大大降低，同时防护效果也大大增强。

---

### JavaScript 加密

不同于 JavaScript 混淆技术，JavaScript 加密技术可以说是对 JavaScript 混淆技术防护的进一步升级，其基本思路是将一些核心逻辑使用诸如 ```C/C++```
语言来编写，并通过 JavaScript 调用执行，从而起到二进制级别的防护作用。

其加密的方式现在有 ```Emscripten``` 和 ```WebAssembly``` 等，其中后者越来越成为主流。

下面我们分别来介绍下。

---

#### Emscripten

现在，许多 3D 游戏都是用 ```C/C++``` 语言写的，如果能将 ```C/C++``` 语言编译成 JavaScript 代码，它们不就能在浏览器里运行了吗？众所周知，JavaScript 的基本语法与 ```C```
语言高度相似。于是，有人开始研究怎么才能实现这个目标，为此专门做了一个编译器项目 ```Emscripten```。这个编译器可以将 ```C/ C++``` 代码编译成 JavaScript 代码，但不是普通的
JavaScript，而是一种叫作 ```asm.js``` 的 JavaScript 变体。

因此说，某些 JavaScript 的核心功能可以使用 ```C/C++``` 语言实现，然后通过 ```Emscripten``` 编译成 ```asm.js```，再由 JavaScript 调用执行，这可以算是一种前端加密技术。

---

#### WebAssembly

如果你对 JavaScript 比较了解，可能知道还有一种叫作 ```WebAssembly``` 的技术，也能将 ```C/C++``` 转成 JavaScript 引擎可以运行的代码。那么它与 ```asm.js``` 有何区别呢？

其实两者的功能基本一致，就是转出来的代码不一样：```asm.js``` 是文本，```WebAssembly``` 是二进制字节码，因此运行速度更快、体积更小。从长远来看，```WebAssembly``` 的前景更光明。

```WebAssembly``` 是经过编译器编译之后的字节码，可以从 ```C/C++``` 编译而来，得到的字节码具有和 JavaScript 相同的功能，但它体积更小，而且在语法上完全脱离
JavaScript，同时具有沙盒化的执行环境。

利用 ```WebAssembly``` 技术，我们可以将一些核心的功能利用 ```C/C++``` 语言实现，形成浏览器字节码的形式。然后在 JavaScript 中通过类似如下的方式调用：

```javascript
WebAssembly.compile(new Uint8Array(`
  00 61 73 6d  01 00 00 00  01 0c 02 60  02 7f 7f 01
  7f 60 01 7f  01 7f 03 03  02 00 01 07  10 02 03 61
  64 64 00 00  06 73 71 75  61 72 65 00  01 0a 13 02
  08 00 20 00  20 01 6a 0f  0b 08 00 20  00 20 00 6c
  0f 0b`.trim().split(/[\s\r\n]+/g).map(str => parseInt(str, 16))
)).then(module => {
    const instance = new WebAssembly.Instance(module)
    const {add, square} = instance.exports
    console.log('2 + 4 =', add(2, 4))
    console.log('3^2 =', square(3))
    console.log('(2 + 5)^2 =', square(add(2 + 5)))
})
```

这种加密方式更加安全，因为作为二进制编码它能起到的防护效果无疑是更好的。如果想要逆向或破解那得需要逆向 ```WebAssembly```，难度也是很大的。

---

## 总结

以上，我们就介绍了接口加密技术和 JavaScript 的压缩、混淆和加密技术，了解了原理，我们才能更好地去实现 JavaScript 的逆向。

--- 
---


