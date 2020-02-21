# coding: utf-8

import time


def shutdown_vm(vm, blocking=True):
    if vm.runtime.powerState == "poweredOn":
        vm.ShutdownGuest()
        if blocking:
            while vm.runtime.powerState == "poweredOn":
                time.sleep(1)
