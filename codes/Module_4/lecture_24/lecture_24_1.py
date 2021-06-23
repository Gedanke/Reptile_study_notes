# -*- coding: utf-8 -*-


import torch

flag = torch.cuda.is_available()
if flag:
    print("CUDA 可使用")
else:
    print("CUDA 不可用")

ngpu = 1
# Decide which device we want to run on
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
print("驱动为：", device)
print("GPU型号： ", torch.cuda.get_device_name(0))
