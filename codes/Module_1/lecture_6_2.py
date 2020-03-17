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
