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
        print("Thread {0} sleep {1}s".format(thread_name, self.second))
        # 线程休眠时间
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
