import tkinter as tk
import GUI.readOnlyLog


def printvminfo(log, vm, depth=1):
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
            printvminfo(log, child, depth+1)
        return

    summary = vm.summary
    # print(summary.config.name)
    log.insert(tk.END, summary.config.name)
    log.insert(tk.END, "\n")


def _list_vms(window):
    content = window.si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                printvminfo(window.log, vm)


def list_vms(window):
    # clear the screen of anything in it before
    if(window.log):
        if(window.last_rendered == window.log):
            window.log.delete(1.0, tk.END)
            _list_vms(window)
        else:
            window.log.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)
            window.last_rendered.pack_forget()
            window.last_rendered = window.log
            window.log.delete(1.0, tk.END)
            _list_vms(window)
    else:
        # create the log to print to
        if(window.last_rendered):
            window.last_rendered.pack_forget()
        window.log = GUI.ReadOnlyLog.ReadOnlyText(window.central_frame,
                                                  bg="#3a3d42", fg="#ffffff",
                                                  font=("Helvetica", 12))
        window.log.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)
        window.last_rendered = window.log
        _list_vms(window)
