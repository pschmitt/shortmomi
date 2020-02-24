# coding: utf-8

import time

from pyVmomi import vim


def shutdown_vm(vm, blocking=True):
    if vm.runtime.powerState == "poweredOn":
        vm.ShutdownGuest()
        if blocking:
            while vm.runtime.powerState == "poweredOn":
                time.sleep(1)


# https://github.com/Akasurde/ansible-reproducers/blob/master/790/get_all_vms.py
def get_folder_path(obj):
    paths = []
    if isinstance(obj, vim.Folder):
        paths.append(obj.name)

    thisobj = obj
    while hasattr(thisobj, 'parent'):
        thisobj = thisobj.parent
        try:
            moid = thisobj._moId
        except AttributeError:
            moid = None
        if moid in ['group-d1', 'ha-folder-root']:
            break
        if isinstance(thisobj, vim.Folder):
            paths.append(thisobj.name)

    paths.reverse()
    return '/'.join(paths)
