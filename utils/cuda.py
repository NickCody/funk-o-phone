#!/usr/bin/env python
import torch

def is_cuda_capable(device_index=0):
    count = torch.cuda.device_count()
    assert count > 0, "No available cuda devices"
    print(count)
    assert device_index <= count, f"Device index out of range, max devices: {count}"
    major, minor = torch.cuda.get_device_capability(device_index)
    name = torch.cuda.get_device_name(device_index)
    min_arch = min(
        (int(arch.split("_")[1]) for arch in torch.cuda.get_arch_list()),
        default=35,
    )
    major_min, minor_min = (min_arch // 10, min_arch % 10,)
    return (major >= major_min and minor >= minor_min, name,)

if __name__ == "__main__":
    cuda, devicename = is_cuda_capable()
    print(f"Cuda is capable on this {devicename} device: {cuda}")