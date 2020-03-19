# 多进程

上节提到，单一进程同一时刻内只有一个线程运行，无法发挥多核优势，如果想发挥多核优势，就得使用多进程。

<br>

## 多进程的实现

在Python中也有内置的库来实现多进程，它就是multiprocessing。
 
multiprocessing提供了一系列的组件，如Process(进程)，Queue(队列)，Semaphore(信号量)，Pipe(管道)，Lock(锁)，Pool(进程池)等，接下来让我们来了解下它们的使用方法。

需要注意的是，进程是操作系统进行资源分配和调度的基本单位，因此多个进程是无法共享全局变量的，这需要有单独的机制来实现进程间的通信，如管道。

<br>

### 使用Process类直接创建

在multiprocessing中，使用Process类创建进程：
```text
Process([group [, target [, name [, args [, kwargs]]]]])
```
其中
```text
target: 传入方法的名字
args: 被调用对象的位置参数元组
kwargs: 调用对象的字典
name: 进程别名
group: 分组
```

先看个[例子](../../codes/Module_1/lecture_6/lecture_6_1.py)：
```python
# -*- coding: utf-8 -*-

import multiprocessing


def process(index):
    print("process : {0}".format(index))


# 一定要有 if __name__ == "__main__":
if __name__ == "__main__":
    for i in range(5):
        # 传参为元组
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()
```
结果如下，创建顺序不唯一：
```text
process : 0
process : 3
process : 4
process : 2
process : 1
```
multiprocessing的其他方法，如cpu_count的方法来获取当前机器CPU的核心数量，通过active_children方法获取当前还在运行的所有进程。

来看个[例子](../../codes/Module_1/lecture_6/lecture_6_2.py)：
```python
# -*- coding: utf-8 -*-

import multiprocessing
import time


def process(index):
    time.sleep(index)
    print("process : {0}".format(index))


if __name__ == "__main__":
    for i in range(5):
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()
    print("CPU number: {0}".format(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("Child process name: {0} id: {1}".format(p.name, p.pid))
    print("Process Ended")
```
结果为，结果可能不唯一：
```text
CPU number: 4
Child process name: Process-4 id: 17356
Child process name: Process-2 id: 19772
Child process name: Process-3 id: 19780
Child process name: Process-5 id: 9332
Child process name: Process-1 id: 19340
Process Ended
process : 0
process : 1
process : 2
process : 3
process : 4
```

进程号直接使用pid属性即可获取，进程名称直接通过name属性即可获取。

### 继承Process类

和线程类似，我们可以继承Process类，重写run方法来实现我们的操作。

来看一个[示例](../../codes/Module_1/lecture_6/lecture_6_3.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print("Pid: {0} LoopCount: {1}".format(self.pid, count))


if __name__ == "__main__":
    for i in range(2, 5):
        p = MyProcess(i)
        p.start()
```
结果为，结果可能不唯一：
```text
Pid: 3212 LoopCount: 0
Pid: 18112 LoopCount: 0
Pid: 21292 LoopCount: 0
Pid: 3212 LoopCount: 1
Pid: 18112 LoopCount: 1
Pid: 21292 LoopCount: 1
Pid: 3212 LoopCount: 2
Pid: 21292 LoopCount: 2
Pid: 21292 LoopCount: 3
```
进程的执行逻辑需要在run方法中实现，启动进程需要调用start方法，调用之后run方法便会执行。

### 守护进程

和多线程类似，多进程中同样存在守护进程的概念，属性是daemon。

在上个例子的基础上，稍微修改，[如下](../../codes/Module_1/lecture_6/lecture_6_4.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print("Pid: {0} LoopCount: {1}".format(self.pid, count))


if __name__ == "__main__":
    for i in range(2, 5):
        p = MyProcess(i)
        p.daemon = True
        p.start()
    print("Main Process ended")
```
结果为：
```text
Main Process ended
```

因为主进程未做任何事情，它早早结束了，其他进程都被终止。

显然，这样做有很大的好处，当一个程序中主进程结束了，其所有子进程应该都得结束，否则将会发生未知的错误。

### 进程等待

上面的例子当然有它的好处，但是子进程还没来得及运行就结束了，也不太合适，引入join方法，主进程可以等待所有子进程结束再结束。

[示例](../../codes/Module_1/lecture_6/lecture_6_5.py)如下：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print("Pid: {0} LoopCount: {1}".format(self.pid, count))


if __name__ == "__main__":
    processes = list()
    for i in range(2, 5):
        p = MyProcess(i)
        processes.append(p)
        p.daemon = True
        p.start()
    for p in processes:
        p.join()
    print("Main Process ended")
```
结果如下，进程pid不唯一：
```text
Pid: 17848 LoopCount: 0
Pid: 17972 LoopCount: 0
Pid: 20108 LoopCount: 0
Pid: 17848 LoopCount: 1
Pid: 17972 LoopCount: 1
Pid: 20108 LoopCount: 1
Pid: 17848 LoopCount: 2
Pid: 17972 LoopCount: 2
Pid: 17972 LoopCount: 3
Main Process ended
```

结果如我们所料，父进程等待所有子进程运行完后结束。

但是呢，join会等到所有子进程结束后，主进程结束，否则将一直等待，如果子进程陷入死循环，主进程会一直等待，这时，join方法可以传入一个超时参数，即最长等待时间，超过该时间，子进程将强制终止，主进程不会等待子进程。

我们传入2，表示最长等待2秒，[程序](../../codes/Module_1/lecture_6/lecture_6_6.py)如下：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print("Pid: {0} LoopCount: {1}".format(self.pid, count))


if __name__ == "__main__":
    processes = list()
    for i in range(3, 5):
        p = MyProcess(i)
        processes.append(p)
        p.daemon = True
        p.start()
    for p in processes:
        p.join(2)
    print("Main Process ended")
```
结果为，进程pid不唯一：
```text
Pid: 16796 LoopCount: 0
Pid: 19172 LoopCount: 0
Pid: 16796 LoopCount: 1
Pid: 19172 LoopCount: 1
Main Process ended
```

### 终止进程

我们也可以通过terminate方法来终止某个子进程，也可以通过is_alive方法判断进程是否还在运行。

来看一个[例子](../../codes/Module_1/lecture_6/lecture_6_7.py)：
```python
# -*- coding: utf-8 -*-

import multiprocessing
import time


def process():
    print("Starting")
    time.sleep(5)
    print("Finished")


if __name__ == "__main__":
    p = multiprocessing.Process(target=process)
    print("Before: ", p, p.is_alive())

    p.start()
    print("During: ", p, p.is_alive())

    p.terminate()
    print("Terminate: ", p, p.is_alive())

    p.join()
    print("Joined: ", p, p.is_alive())
```
结果为：
```text
Before:  <Process(Process-1, initial)> False
During:  <Process(Process-1, started)> True
Terminate:  <Process(Process-1, started)> True
Joined:  <Process(Process-1, stopped[SIGTERM])> False
```
在调用terminate方法之后，用is_alive方法获取进程的状态发现依然还是运行状态。在调用join方法之后，is_alive方法获取进程的运行状态才变为终止状态。

所以，在调用terminate方法之后，还得调用一下join方法，这里调用join方法可以为进程提供时间来更新对象状态，用来反映出最终的进程终止效果。

### 进程互斥锁

在上节多线程中，多个线程读取同一个全局变量时，若不加上互斥锁，得到的结果和串行结果不一致。

而在多进程中，我们可能会遇到，多个进程的输出显示在同一行中，这是因为多个进程虽不能读取同一个全局变量，但是在程序进行IO操作时，例如输出结果时，由于多个进程并行执行，进程同时输出，结果显示在同一行中。

如果我们能保证多个进程运行期间，只有一个进程输出，这样就不会出现多个进程并行输出显示在同一行了。

这种解决方案实际上就是实现了进程互斥，避免了多个进程同时抢占临界区(输出)资源。我们可以通过multiprocessing中的Lock来实现。Lock，即锁，在一个进程输出时，加锁，其他进程等待。等此进程执行结束后，释放锁，其他进程可以进行输出。

先看一个不加锁的[例子](../../codes/Module_1/lecture_6/lecture_6_8.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Lock
import time


class MyProcess(Process):
    def __init__(self, loop, lock):
        Process.__init__(self)
        self.loop = loop
        self.lock = lock

    def run(self):
        for num in range(self.loop):
            time.sleep(0.1)
            # self.lock.acquire()
            print("Pid: {0} LoopCount: {1}".format(self.pid, num))
            # self.lock.release()


if __name__ == "__main__":
    lock = Lock()
    for i in range(10, 15):
        p = MyProcess(i, lock)
        p.start()
```
部分结果：
```text
Pid: 14880 LoopCount: 0Pid: 20540 LoopCount: 0

Pid: 12384 LoopCount: 0
Pid: 7812 LoopCount: 0
Pid: 11196 LoopCount: 0
Pid: 14880 LoopCount: 1Pid: 20540 LoopCount: 1

Pid: 12384 LoopCount: 1
...
```
对其加锁，取消run方法的两行注释，部分结果如下：
```text
Pid: 19324 LoopCount: 0
Pid: 7368 LoopCount: 0
Pid: 16696 LoopCount: 0
Pid: 20008 LoopCount: 0
Pid: 11920 LoopCount: 0
Pid: 19324 LoopCount: 1
Pid: 7368 LoopCount: 1
Pid: 16696 LoopCount: 1
Pid: 20008 LoopCount: 1
Pid: 11920 LoopCount: 1
Pid: 19324 LoopCount: 2
Pid: 7368 LoopCount: 2
...
```

### 信号量

信号量(Semaphore)，有时被称为信号灯，是在多线程环境下使用的一种设施，是可以用来保证两个或多个关键代码段不被并发调用。在进入一个关键代码段之前，线程必须获取一个信号量；一旦该关键代码段完成了，那么该线程必须释放信号量。其它想进入该关键代码段的线程必须等待直到第一个线程释放信号量。为了完成这个过程，需要创建一个信号量VI，然后将Acquire Semaphore VI以及Release Semaphore VI分别放置在每个关键代码段的首末端。确认这些信号量VI引用的是初始创建的信号量。
来源于[百度百科](https://baike.baidu.com/item/%E4%BF%A1%E5%8F%B7%E9%87%8F)。

信号量是操作系统中的重要概念，在Python中，我们可以用multiprocessing库中的Semaphore来实现信号量机制。

来看一个[例子](../../codes/Module_1/lecture_6/lecture_6_9.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Semaphore, Lock, Queue
import time

buffer = Queue(10)
empty = Semaphore(2)
full = Semaphore(0)
lock = Lock()


class Consumer(Process):
    def run(self):
        global buffer, empty, full, lock
        while True:
            full.acquire()
            lock.acquire()
            buffer.get()
            print("Consumer pop an element")
            time.sleep(1)
            lock.release()
            empty.release()


class Producer(Process):
    def run(self):
        global buffer, empty, full, lock
        while True:
            empty.acquire()
            lock.acquire()
            buffer.put(1)
            print("Producer append an element")
            time.sleep(1)
            lock.release()
            full.release()


if __name__ == "__main__":
    p = Producer()
    c = Consumer()
    p.daemon = True
    c.daemon = True
    p.start()
    c.start()
    p.join()
    c.join()
    print("Main Process Ended")
```
结果为，注：Linux端运行结果如下，win10消费者进程发生阻塞：
```text
Producer append an element
Producer append an element
Consumer pop an element
Consumer pop an element
Producer append an element
...
```

### 队列

多进程间进行数据共享使用的是特定的数据结构Queue队列，这里的队列是multiprocessing中的Queue。

来看一个[例子](../../codes/Module_1/lecture_6/lecture_6_10.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Semaphore, Lock, Queue
import time
from random import random

buffer = Queue(10)
empty = Semaphore(2)
full = Semaphore(0)
lock = Lock()


class Consumer(Process):
    def run(self):
        global buffer, empty, full, lock
        while True:
            full.acquire()
            lock.acquire()
            print("Consumer get {0}".format(buffer.get()))
            time.sleep(1)
            lock.release()
            empty.release()


class Producer(Process):
    def run(self):
        global buffer, empty, full, lock
        while True:
            empty.acquire()
            lock.acquire()
            num = random()
            print("Producer put {0}".format(num))
            buffer.put(num)
            time.sleep(1)
            lock.release()
            full.release()


if __name__ == "__main__":
    p = Producer()
    c = Consumer()
    p.daemon = c.daemon = True
    p.start()
    c.start()
    p.join()
    c.join()
    print("Main Process Ended")
```

结果为，注：Linux端运行结果如下，win10消费者进程发生阻塞：
```text
Producer put 0.7168468518418151
Producer put 0.0717678851372644
Consumer get 0.7168468518418151
Consumer get 0.0717678851372644
Producer put 0.18752387120600655
...
```

在这个例子中，生产者进程使用Queue的put方法放数据，消费者使用get方法取出数据，通过Queue实现了进程间的数据共享。

### 管道

管道是两个进程之间直接通信的通道，它既可以是单向的half-duplex，一个进程发信息，另一个接收，也可以是双向的duplex，双方互相收发信息。

默认声明Pipe对象是双向管道，如果要创建单向管道，可以在初始化的时候传入deplex参数为False。

来看一个[例子](../../codes/Module_1/lecture_6/lecture_6_11.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Pipe


class Consumer(Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe

    def run(self):
        self.pipe.send("Consumer Words")
        print("Consumer Received: {0}".format(self.pipe.recv()))


class Producer(Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe

    def run(self):
        print("Producer Received: {0}".format(self.pipe.recv()))
        self.pipe.send("Producer Words")


if __name__ == "__main__":
    pipe = Pipe()
    p = Producer(pipe[0])
    c = Consumer(pipe[1])
    p.daemon = c.daemon = True
    p.start()
    c.start()
    p.join()
    c.join()
    print("Main Process Ended")
```
结果为：
```text
Producer Received: Consumer Words
Consumer Received: Producer Words
Main Process Ended
```

这里我们申明了一个双向管道，将管道的两端传送给两个进程用以它们的互相通信，在两个进程间起一个桥梁作用。

### 进程池

之前我们使用Semaphore来控制进程的并发执行数量，但是如果进程数量多，使用信号量机制会比较繁琐，而且并发数量高了，若不实时控制并发数量，CPU处理压力会很大。

此时multiprocessing中的Pool进程池就派上用场了，Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，如果池还没有满，就会创建一个新的进程用来执行该请求；但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来执行它。

来看一个[例子](../../codes/Module_1/lecture_6/lecture_6_12.py):
```python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import time


def function(index):
    print("Start process: {0}".format(index))
    time.sleep(3)
    print("End process {0}".format(index))


if __name__ == "__main__":
    pool = Pool(processes=3)
    for i in range(4):
        pool.apply_async(function, args=(i,))

    print("Main Process started")
    pool.close()
    pool.join()
    print("Main Process ended ")
```
结果为：
```text
Main Process started
Start process: 0
Start process: 1
Start process: 2
End process 0
Start process: 3
End process 1
End process 2
End process 3
Main Process ended 
```

我们创建了一个大小为3的线程池，可以有三个进程同时执行，当有进程执行完后，第四个进程就可以运行。

最后，我们要记得调用close方法来关闭进程池，使其不再接受新的任务，然后调用join方法让主进程等待子进程的退出，等子进程运行完毕之后，主进程接着运行并结束。

这里我们介绍map方法，map方法第一个参数就是要启动的进程对应的执行方法，第二个参数是一个可迭代对象，其中的每个元素会被传递给这个执行方法。

来看一个[例子](../../codes/Module_1/lecture_6/lecture_6_13.py)：
```python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import urllib.request
import urllib.error


def scrape(url):
    try:
        urllib.request.urlopen(url)
        print("URL {0} Scraped".format(url))
    except (urllib.error.HTTPError, urllib.error.URLError):
        print("URL {0} not Scraped".format(url))


if __name__ == "__main__":
    pool = Pool(processes=3)
    urls = [
        'https://www.dogedoge.com/',
        'https://www.csdn.net/',
        'https://bj.meituan.com/',
        'http://xxxyxxx.net'
    ]
    pool.map(scrape, urls)
    pool.close()
```
结果为：
```text
URL https://www.dogedoge.com/ Scraped
URL https://bj.meituan.com/ Scraped
URL https://www.csdn.net/ Scraped
URL http://xxxyxxx.net not Scraped
```
这个例子中我们先定义了一个scrape方法，它接收一个参数url，这里就是请求了一下这个链接，然后输出爬取成功的信息，如果发生错误，则会输出爬取失败的信息。 

首先我们要初始化一个Pool，指定进程数为3。然后我们声明一个urls列表，接着我们调用了map方法，第1个参数就是进程对应的执行方法，第2个参数就是urls列表，map方法会依次将urls的每个元素作为scrape的参数传递并启动一个新的进程，加到进程池中执行。

这样，我们就可以通过map方法实现多进程并行运行。不同的进程相互独立地输出了对应的爬取结果。

<br>

至此，爬虫基本原理介绍完毕，下一个模块将介绍爬虫基本库的使用。
