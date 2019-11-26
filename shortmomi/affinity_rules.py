from .views import (get_all_clusters, get_vm_by_name)
from pyVmomi import vim
from pyVim.task import WaitForTask


def get_cluster_affinity_groups(cluster):
    """
    Get the VM/Host groups of a given cluster
    https://github.com/vmware/pyvmomi/issues/663#issuecomment-374397624
    """
    return cluster.configurationEx.group


def get_cluster_affinity_rules(cluster):
    """
    Get the VM/Host rules of a given cluster
    """
    # return cluster.configurationEx.rule
    return cluster.configuration.rule


def get_affinity_rules(cluster, search_criteria):
    """
    Get an affinity rule by its name
    """
    rules = []
    for rule in cluster.configuration.rule:
        # Keys are unique
        if rule.key == search_criteria:
            return rule
        # Names are not
        if rule.name == search_criteria:
            rules.append(rule)
    return rules if rules else None


def get_affinity_rules_affecting(content, vm):
    """
    Get a list of rules affecting a VM
    :param content: VMware API content
    :type content: pyVmomi.VmomiSupport.vim.ServiceInstanceContent
    :param vm: Name of the VM (or the API object)
    :type vm: str or pyVmomi.VmomiSupport.vim.VirtualMachine
    :return: A list of dicts holding the cluster and the rules affecting the VM
    :rtype: list
    """
    if isinstance(vm, str):
        vm = get_vm_by_name(content, vm)
    rules = []
    for cl in get_all_clusters(content):
        for rule in cl.configuration.rule:
            if vm in rule.vm:
                rules.append({"cluster": cl, "rule": rule})
    return rules if rules else None


def create_affinity_rule(cluster, vms, name=None, together=True):
    """
    Create a new affinity rule for VMs
    https://github.com/vmware/pyvmomi-community-samples/issues/247
    """
    if not name:
        name = 'affinity_shortmomi'
    if together:
        aff_rule_spec = vim.cluster.AffinityRuleSpec
    else:
        aff_rule_spec = vim.cluster.AntiAffinityRuleSpec
    rule = aff_rule_spec(vm=vms, enabled=True, mandatory=True, name=name)
    rule_spec = vim.cluster.RuleSpec(info=rule, operation='add')
    config_spec = vim.cluster.ConfigSpecEx(rulesSpec=[rule_spec])
    return WaitForTask(cluster.ReconfigureEx(config_spec, modify=True))


def delete_affinity_rule(cluster, rule):
    """
    Delete an affinity rule
    """
    rules = get_affinity_rules(cluster, rule)
    if not rules:
        # Nothing to do
        return

    spec = vim.cluster.ConfigSpecEx()
    spec.rulesSpec = []
    for rule in rules:
        rule_spec = vim.cluster.RuleSpec(operation="remove", removeKey=rule.key)
        spec.rulesSpec.append(rule_spec)
    return WaitForTask(cluster.ReconfigureEx(spec, modify=True))
