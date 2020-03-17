# -*- coding: utf-8 -*-

import threading
import time


def target(second):
    thread_name = threading.current_thread().name
    print("Thread {0} is running".format(thread_name))
    print("Thread {0} sleep {1}s".format(thread_name, second))
    # 线程休眠时间
    time.sleep(second)
    print("Thread {0} is ended".format(thread_name))


if __name__ == "__main__":
    main_thread_name = threading.current_thread().name
    print("Thread {0} is running".format(main_thread_name))
    for i in [1, 5]:
        thread = threading.Thread(target=target, args=[i])
        thread.start()
        # thread.join()
    # threads = list()
    # for i in [1, 5]:
    #     thread = threading.Thread(target=target, args=[i])
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    print("Thread {0} is ended".format(main_thread_name))
