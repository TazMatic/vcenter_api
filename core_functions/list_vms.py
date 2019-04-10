def printvminfo(vm, depth=1):
    """
    Print information for a particular virtual machine or recurse into a folder
    with depth protection
    """

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > 10:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            printvminfo(child, depth+1)
        return

    summary = vm.summary
    print(summary.config.name)


# TODO print to log rather than CLI
def list_vms(window):
    content = window.si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                printvminfo(vm)
