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
