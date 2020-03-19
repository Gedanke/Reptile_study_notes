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
