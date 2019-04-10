import tkinter as tk
from idlelib.WidgetRedirector import WidgetRedirector


# https://stackoverflow.com/a/11612656
class ReadOnlyText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register("insert",
                                               lambda *args, **kw: "break")
        self.delete = self.redirector.register("delete",
                                               lambda *args, **kw: "break")


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


# TODO print to log rather than CLI
def list_vms(window):
    # clear the screen of anything in it before
    for child in window.central_frame.winfo_children():
        child.destroy()
    # create the log to print to
    log = ReadOnlyText(window.central_frame, bg="#3a3d42",
                       fg="#ffffff", font=("Helvetica", 12))
    log.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)

    content = window.si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                printvminfo(log, vm)
