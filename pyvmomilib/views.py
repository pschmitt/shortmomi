# pylint: disable=invalid-name

'''
General helper functions for pyVmomi
Author: Philipp Schmitt <philipp.schmitt@post.lu>
'''

from __future__ import print_function
from pyVmomi import vim


def get_all(content, container, object_type):
    '''
    Get all items of a certain type
    Example: get_all(content, vim.Datastore) return all datastore objects
    '''
    obj_list = list()
    view_manager = content.viewManager
    object_view = view_manager.CreateContainerView(
        container, [object_type], True
    )
    for obj in object_view.view:
        if isinstance(obj, object_type):
            obj_list.append(obj)
    object_view.Destroy()
    return obj_list


def get_all_vms(content):
    '''
    Get all VMs managed by a vCenter
    '''
    return get_all(content, content.rootFolder, vim.VirtualMachine)


def get_all_datastores(content):
    '''
    Get all datastore on a vCenter
    '''
    return get_all(content, content.rootFolder, vim.Datastore)


def get_all_clusters(content):
    '''
    Get all hosts on a vCenter
    '''
    return get_all(content, content.rootFolder, vim.ClusterComputeResource)


def get_all_hosts(content):
    '''
    Get all clusters on a vCenter
    '''
    return get_all(content, content.rootFolder, vim.HostSystem)


def get_hosts_in_datacenter(content, datacenter):
    '''
    Get all hosts belonging to a given datacenter
    '''
    return get_all(content, datacenter, vim.HostSystem)


def get_vms_in_datacenter(content, datacenter):
    '''
    Get all vms belonging to a given datacenter
    '''
    return get_all(content, datacenter, vim.VirtualMachine)


def get_datacenter(content, obj):
    '''
    Get the datacenter to whom an object belongs
    '''
    datacenters = content.rootFolder.childEntity
    for d in datacenters:
        dch = get_all(content, d, type(obj))
        if dch is not None and obj in dch:
            return d

def print_vm_info(vm):
    '''
    Print information for a particular virtual machine
    '''
    summary = vm.summary
    print('Name  : ', summary.config.name)
    print('Path  : ', summary.config.vmPathName)
    print('Guest : ', summary.config.guestFullName)
    annotation = summary.config.annotation
    if annotation is not None and annotation != '':
        print('Annotation : ', annotation)
    print('State : ', summary.runtime.powerState)
    if summary.guest is not None:
        ip = summary.guest.ipAddress
        if ip is not None and ip != '':
            print('IP    : ', ip)
    if summary.runtime.question is not None:
        print('Question : ', summary.runtime.question.text)
    print('')
