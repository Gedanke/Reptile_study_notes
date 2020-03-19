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
            self.lock.acquire()
            print("Pid: {0} LoopCount: {1}".format(self.pid, num))
            self.lock.release()


if __name__ == "__main__":
    lock = Lock()
    for i in range(10, 15):
        p = MyProcess(i, lock)
        p.start()
