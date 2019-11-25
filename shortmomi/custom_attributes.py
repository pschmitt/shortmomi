from pyVmomi import vim
from pyVmomi import vmodl

from .views import get_all_vms


def get_field_by_key(content, field_key):
    """
    Get a custom field by its key
    :param content: Service Content
    :type content: vim.ServiceContent
    :param field_id: Key of the field
    :type field_id: str or unicode
    :return: The requested field, or None if the field does not exist
    :rtype: vim.CustomFieldDef or NoneType
    """
    fields_manager = content.customFieldsManager
    for field in fields_manager.field:
        if hasattr(field, "key") and field.key == field_key:
            return field


def get_field_by_name(content, fieldname):
    """
    Get a custom field by its name
    :param content: Service Content
    :type content: vim.ServiceContent
    :param fieldname: Name of the field
    :type fieldname: str or unicode
    :return: The requested field, or None if the field does not exist
    :rtype: vim.CustomFieldDef or NoneType
    """
    fields_manager = content.customFieldsManager
    for field in fields_manager.field:
        if hasattr(field, "name") and field.name == fieldname:
            return field


def get_or_create_custom_field(
    content, fieldname, fieldtype=vim.VirtualMachine
):
    """
    Create a new custom field
    :param content: Service Content
    :type content: vim.ServiceContent
    :param fieldname: Name of the new field
    :type fieldname: str or unicode
    :param fieldtype: Type of the new Field (vim.VirtualMachine,
    vim.HostSystem etc.)
    :type fieldtype: object
    :return: The newly created field
    :rtype: vim.CustomFieldDef
    """
    fields_manager = content.customFieldsManager
    # Check if the field already exists
    field = get_field_by_name(content, fieldname)
    # Return the field if it exists
    if field:
        return field
    return fields_manager.AddCustomFieldDef(
        name=fieldname,
        moType=fieldtype
        # fieldDefPolicy=None,
        # fieldPolicy=None
    )


def set_field(content, vm, name, value):
    """
    Set a custom field for a given VM
    :param content: Service Content
    :type content: vim.ServiceContent
    :param vm: Virtual Machine whose field is to be set
    :type vm: vim.VirtualMachine
    :param name: Name of the custom field
    :type name: str or unicode
    :param value: Value of the custom field
    :type value: str or unicode
    """
    # FIXME There should be a way to get the field name from vm.customValue
    #       -> Get rid of the content parameter
    # Check if the field is already set to the desired value
    for cfield in vm.customValue:
        field = get_field_by_key(content, cfield.key)
        if field.name == name:
            # Only set the value if it differs
            if cfield.value == value:
                return
            break
    # Field was not found or value differs, set its value
    # FIXME Passing the name instead of the key is weird but works
    vm.setCustomValue(key=name, value=value)


def clear_field(content, vm, field):
    """
    Clear a field by setting its value to empty string
    :param content: Service Content
    :type content: vim.ServiceContent
    :param vm: Virtual Machine whose field is to be set
    :type vm: vim.VirtualMachine
    :param name: Name of the custom field
    :type name: str or unicode
    :param value: Value of the custom field
    :type value: str or unicode
    """
    return set_field(content, vm, field, "")


def find_vms_by_custom_field(content, name, value):
    """
    Find virtual machines who match a certain criteria
    :param content: Service Content
    :type content: vim.ServiceContent
    :param name: Name of the annotation/custom field (not the integer key)
    :type name: str or unicode
    :param value: Value of the annotation/custom field
    :type value: str or unicode
    :return: A list of VMs that match
    :rtype: list
    """
    matching = []
    vm_list = get_all_vms(content)
    for vm in vm_list:
        for cfield in vm.customValue:
            field = get_field_by_key(content, cfield.key)
            if field.name == name and cfield.value == value:
                matching.append(vm)
    return matching


def get_obj_field_value(content, obj, name):
    """
    Get the value of the named field for a given object
    :param content: Service Content
    :type content: vim.ServiceContent
    :param name: Name of the annotation/custom field (not the integer key)
    :type name: str or unicode
    :return: The value of the field
    :rtype: str or NoneType
    """
    field = get_field_by_name(content, name)
    if not field:
        # Named field does not exist
        return
    fld_key = field.key
    for fld in obj.customValue:
        if fld_key == fld.key:
            return fld.value
