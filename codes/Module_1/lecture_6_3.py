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
