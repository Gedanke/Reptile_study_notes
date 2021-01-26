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
