from pyVmomi import vim


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


def get_parent_datacenter(obj):
        """ Walk the parent tree to find the objects datacenter """
        if isinstance(obj, vim.Datacenter):
            return obj
        datacenter = None
        while True:
            if not hasattr(obj, 'parent'):
                break
            obj = obj.parent
            if isinstance(obj, vim.Datacenter):
                datacenter = obj
                break
        return datacenter
