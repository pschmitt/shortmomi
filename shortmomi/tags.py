# coding: utf-8

import requests



def get_tag_by_name(stub, tag_name):
    """
    Get a TagModel bbyy its name
    """
    import com.vmware.cis.tagging_client as tagclient

    tag_svc = tagclient.Tag(stub)
    all_tag_ids = tag_svc.list()
    for tag_id in all_tag_ids:
        tag_obj = tag_svc.get(tag_id)
        if tag_obj.name == tag_name:
            return tag_obj


def tag_vm(stub, vm, tag):
    """
    Tag a VM
    """
    import com.vmware.cis.tagging_client as tagclient
    from com.vmware.vapi.std_client import DynamicID

    if isinstance(tag, tagclient.TagModel):
        tag_id = tag.id
    else:
        tag_obj = get_tag_by_name(stub, tag)
        tag_id = tag_obj.id
    if isinstance(vm, DynamicID):
        obj_did = vm
    else:
        obj_did = DynamicID(type="VirtualMachine", id=vm._moId)
    tag_ass = tagclient.TagAssociation(stub)
    result = tag_ass.attach(tag_id=tag_id, object_id=obj_did)
    return result
