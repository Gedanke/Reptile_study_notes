# 多线程

如果你对操作系统有一定的了解，那么 [多线程](lecture_5.md) 和 [多进程](lecture_6.md) 的概念方面不会有大的问题，这两节的重点是其在 python 中的使用。

---
---

## 多线程的含义

进程 (Process) 是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位。而线程 (thread) 是操作系统能够进行运算调度的最小单位。

进程是线程的集合，即一个进程中至少运行一个线程，线程是操作系统进行运算调度的最小单位，是进程中的一个最小运行单元。

---

## 并发与并行

并发，同一时间间隔内多条指令执行，而并行是同一时刻内多条指令执行。在同一时刻内，并发只有一条指令执行，在一个时间间隔内会有不同线程或进程的指令依据一定的调度算法轮流执行；而并行是一个时刻内多条指令的同时执行。

并行必须在多个处理器或者多核 CPU 才能发生，而并发在一个核心上就可以发生。

---

## 多线程适用场景

对于 IO 密集型任务，多线程会大大提高程序运行效率，例如网络爬虫，在向服务器发起一个请求时，需要等待服务器的响应，那在这段时间内，如果是单线程，我们只能等待它完成，白白浪费时间，使用多线程，我们就可以在等待它时去干别的事情，提高效率。

但是，对于计算密集型任务，它需要处理器的全程参与，使用多线程，不仅仅不会提高效率，处理器反而因线程创建，切换白白浪费宝贵的计算时间，效率降低。

对于爬虫这种 IO 密集型任务，多线程无疑可以提高爬取效率。

---

## Python 多线程

在 Python 中，实现多线程是 Python 自带的库 ```threading```。

---

### Thread 直接创建子线程

```Thread``` 类传入运行方法名称，```args``` 列表指定待传参数。

[程序](../../codes/Module_1/lecture_5/lecture_5_1.py) 如下：

```python
# -*- coding: utf-8 -*-

import threading
import time


def target(second):
    thread_name = threading.current_thread().name
    print("Thread {0} is running".format(thread_name))
    print("Thread {0} sleep {1} s".format(thread_name, second))
    '''线程休眠时间'''
    time.sleep(second)
    print("Thread {0} is ended".format(thread_name))


if __name__ == "__main__":
    main_thread_name = threading.current_thread().name
    print("Thread {0} is running".format(main_thread_name))
    for i in [1, 5]:
        thread = threading.Thread(target=target, args=[i])
        thread.start()
        thread.join()
    # threads = list()
    # for i in [1, 5]:
    #     thread = threading.Thread(target=target, args=[i])
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    print("Thread {0} is ended".format(main_thread_name))
```

结果：

```text
Thread MainThread is running
Thread Thread-1 is running
Thread Thread-1 sleep 1 s
Thread Thread-2 is running
Thread Thread-2 sleep 5 s
Thread MainThread is ended
Thread Thread-1 is ended
Thread Thread-2 is ended
```

我们发现，Thread-2 由于休眠时间长，还没等其运行完，主线程就结果了，如果想 **让主线程等待子线程执行完退出**，可以如下操作。让每个子线程都调用 ```join()``` 方法。

```text
for i in [1, 5]:
    thread = threading.Thread(target=target, args=[i])
    thread.start()
    thread.join()
```

结果为：

```text
Thread MainThread is running
Thread Thread-1 is running
Thread Thread-1 sleep 1 s
Thread Thread-1 is ended
Thread Thread-2 is running
Thread Thread-2 sleep 5 s
Thread Thread-2 is ended
Thread MainThread is ended
```

或者

```text
threads = list()
for i in [1, 5]:
    thread = threading.Thread(target=target, args=[i])
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
```

结果为：

```text
Thread MainThread is running
Thread Thread-1 is running
Thread Thread-1 sleep 1 s
Thread Thread-2 is running
Thread Thread-2 sleep 5 s
Thread Thread-1 is ended
Thread Thread-2 is ended
Thread MainThread is ended
```

---

### 继承 Thread 类创建子线程

继承 ```Thread``` 类，重写 ```run``` 方法。

[程序](../../codes/Module_1/lecture_5/lecture_5_2.py) 如下：

```python
# -*- coding: utf-8 -*-

import threading
import time


class MyThread(threading.Thread):
    def __init__(self, second):
        threading.Thread.__init__(self)
        self.second = second

    def run(self):
        thread_name = threading.current_thread().name
        print("Thread {0} is running".format(thread_name))
        print("Thread {0} sleep {1} s".format(thread_name, self.second))
        '''线程休眠时间'''
        time.sleep(self.second)
        print("Thread {0} is ended".format(thread_name))


if __name__ == "__main__":
    main_thread_name = threading.current_thread().name
    print("Thread {0} is running".format(main_thread_name))
    threads = list()
    for i in [1, 5]:
        thread = MyThread(i)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Thread {0} is ended".format(main_thread_name))
```

结果为：

```text
Thread MainThread is running
Thread Thread-1 is running
Thread Thread-1 sleep 1 s
Thread Thread-2 is running
Thread Thread-2 sleep 5 s
Thread Thread-1 is ended
Thread Thread-2 is ended
Thread MainThread is ended
```

殊途同归。

---

## 守护线程

如果一个线程是守护线程，当主线程结束后，它将强行被终止，可以使用 ```setDaemon``` 方法。
[程序](../../codes/Module_1/lecture_5/lecture_5_3.py) 如下：

```python
# -*- coding: utf-8 -*-

import threading
import time


def target(second):
    thread_name = threading.current_thread().name
    print("Thread {0} is running".format(thread_name))
    print("Thread {0} sleep {1} s".format(thread_name, second))
    '''线程休眠时间'''
    time.sleep(second)
    print("Thread {0} is ended".format(thread_name))


if __name__ == "__main__":
    main_thread_name = threading.current_thread().name
    print("Thread {0} is running".format(main_thread_name))
    t1 = threading.Thread(target=target, args=[2])
    '''first'''
    # t1.daemon = True
    '''second'''
    t1.start()
    # t1.join()
    t2 = threading.Thread(target=target, args=[5])
    t2.setDaemon(True)
    t2.start()
    # t2.join()
    print("Thread {0} is ended".format(main_thread_name))
```

结果，打印的次序可能稍有不同：

```text
Thread MainThread is running
Thread Thread-1 is running
Thread Thread-1 sleep 2 s
Thread Thread-2 is running
Thread Thread-2 sleep 5 s
Thread MainThread is ended
Thread Thread-1 is ended
```

Thread-2 还没执行完就随主线程的退出而退出了。

**如果我们让 t1 和 t2 都调用 ```join``` 方法，主线程就会仍然等待各个子线程执行完毕再退出，不论其是否是守护线程。**

---

## 互斥锁

一个进程的多个线程是共享进程内的资源，在多线程中，如果不对线程访问资源继续约束，得到的结果往往事与愿违，先看一个例子。

[程序](../../codes/Module_1/lecture_5/lecture_5_4.py) 如下：

```python
# -*- coding: utf-8 -*-

import threading
import time

count = 0


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global count
        '''count 加一'''
        temp = count + 1
        time.sleep(0.001)
        count = temp


if __name__ == "__main__":
    threads = list()
    for _ in range(1000):
        thread = MyThread()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print("count : {0}".format(count))
```

结果为：

```text
count : 103
```

结果不是 1000，而且每次运行的结果都不同。

这是因为 count 是被所有线程共享的，每个线程都可以对 count 加一，但是在这些线程中，有的是串行执行，有的是并发执行，不同的线程操作的 count 可能是同一个，这样它们的加一操作没有生效，结果与预期不同。

为了解决这个问题，我们可以使用互斥锁 ```threading.Lock```，当一个线程访问该数据时，会对其加锁，其他线程无法访问，只能等待解锁，当到该线程执行完操作后，解锁，其他线程才可以访问。

这样就保证了一个时刻仅有一个线程访问该数据，保证了并发结果的正确性。

对源程序稍作修改，[如下](../../codes/Module_1/lecture_5/lecture_5_5.py) ：

```python
# -*- coding: utf-8 -*-

import threading
import time

count = 0
lock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global count, lock
        '''gain lock'''
        lock.acquire()
        temp = count + 1
        time.sleep(0.001)
        count = temp
        '''release lock'''
        lock.release()


if __name__ == "__main__":
    threads = list()
    for _ in range(1000):
        thread = MyThread()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print("count : {0}".format(count))
```

结果为：

```text
count : 1000
```

得到预期结果。

更多 Python
多线程可参考 [https://www.runoob.com/python/python-multithreading.html](https://www.runoob.com/python/python-multithreading.html)
。

----

## Python 多线程的限制

在 Python 中，由于 GIL(Global Interpreter Lock) 全局解释器锁的存在，每个线程的执行方式是：

* 获取 GIL
* 执行对应线程的代码
* 释放 GIL

这就意味着，在一个 Python 进程中，只有一个 GIL，某个线程只有得到 GIL 才能执行，这样在一个进程内同一时刻就有一个线程在允许，发挥不了多核的优势。

虽然对于爬虫这种 IO 密集型任务来说，问题不大，但对于计算密集型任务，单进程使用多线程的效率要比单线程低。

解决方法很简单，使用多线程，每个进程有自己的 GIL，在多核处理器上就可以发挥多核的优势了。

这就是我们 [下节](lecture_6.md) 要介绍的内容了。

---
---