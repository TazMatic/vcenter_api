import tkinter as tk
from tkinter import messagebox
from pyVmomi import vim
import time
from GUI.scrollable_frame import scrollable_frame
# from core_functions.add_nic_to_vm import add_nic


def wait_for_task(task, window):
    """ wait for a vCenter task to finish """
    task_done = False
    start_time = time.time()
    while not task_done:
        if task.info.state == 'success':
            m, s = divmod(time.time()-start_time, 60)
            print('Done Cloning ({}.{} minutes)'.format(int(m), int(s)))
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            task_done = True

        if (time.time() - start_time) % 30 <= 1:
            print("cloning...")
            time.sleep(1)


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


def _clone_vm(
        content, template, vm_name, si,
        datacenter_name, vm_folder, datastore_name,
        cluster_name, resource_pool, power_on, datastorecluster_name, window):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """

    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
        datastore = get_obj(content, [vim.Datastore], datastore_name)
    else:
        datastore = get_obj(
            content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool

    vmconf = vim.vm.ConfigSpec()

    if datastorecluster_name:
        podsel = vim.storageDrs.PodSelectionSpec()
        pod = get_obj(content, [vim.StoragePod], datastorecluster_name)
        podsel.storagePod = pod

        storagespec = vim.storageDrs.StoragePlacementSpec()
        storagespec.podSelectionSpec = podsel
        storagespec.type = 'create'
        storagespec.folder = destfolder
        storagespec.resourcePool = resource_pool
        storagespec.configSpec = vmconf

        try:
            rec = content.storageResourceManager.RecommendDatastores(
                storageSpec=storagespec)
            rec_action = rec.recommendations[0].action[0]
            real_datastore_name = rec_action.destination.name
        except:
            real_datastore_name = template.datastore[0].info.name

        datastore = get_obj(content, [vim.Datastore], real_datastore_name)

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    print("cloning VM...")
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task, window)
    print("Clone successful")


def clone_vm(window):
    content = window.si.RetrieveContent()
    template = window.template_entry.get()

    template = get_obj(content, [vim.VirtualMachine], template)

    if template:
        _clone_vm(
            content, template, window.vm_name_entry.get(), window.si,
            window.datacenter_name_entry.get(), window.folder_entry.get(),
            # args.datastore_name,
            None,
            # args.cluster_name,
            None,
            # args.resource_pool,
            None,
            # args.power_on,
            False,
            # args.datastorecluster_name
            None,
            window
            )
        # if window.opaque_network_entry.get():
        #     vm = get_obj(content, [vim.VirtualMachine], args.vm_name)
        #     add_nic(window.si, vm, args.opaque_network)
    else:
        messagebox.showinfo("Error", "Please enter in a valid template")


def render_clone_vm(window):
    # if window.clone_frame, bring it to the front
    if(window.scroll_frame):
        if(window.last_rendered == window.scroll_frame):
            pass
        else:
            window.scroll_frame.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)
            window.last_rendered.pack_forget()
            window.last_rendered = window.scroll_frame
    else:
        # render scrollable frame
        window.update_idletasks()
        window.scroll_frame = scrollable_frame(window.central_frame, window)
        window.scroll_frame.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)
        if(window.last_rendered):
            window.last_rendered.pack_forget()
        window.last_rendered = window.scroll_frame
        # render template
        frame1 = tk.Frame(window.scroll_frame.scrollFrame.viewPort, width=565,
                          height=80, bg="#f442e8")
        frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        frame1_1 = tk.Frame(frame1, width=200,
                            height=80, bg="#ffffff")
        frame1_1.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)
        frame1_2 = tk.Frame(frame1, width=200,
                            height=80, bg="#000000")
        frame1_2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frame1_label = tk.Label(frame1_1, text="Enter template name:",
                                font=("Helvetica", 14), anchor="e", width=20)
        # add a resize event that increases font size
        frame1_label.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        window.template_entry = tk.Entry(frame1_2, font=("Helvetica", 14))
        window.template_entry.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # render new VM name
        frame2 = tk.Frame(window.scroll_frame.scrollFrame.viewPort, width=565,
                          height=80, bg="#f442e8")
        frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        frame2_1 = tk.Frame(frame2, width=200,
                            height=80, bg="#ffffff")
        frame2_1.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)
        frame2_2 = tk.Frame(frame2, width=200,
                            height=80, bg="#000000")
        frame2_2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frame2_label = tk.Label(frame2_1, text="Enter new VM name:",
                                font=("Helvetica", 14), anchor="e", width=20)
        # add a resize event that increases font size
        frame2_label.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        window.vm_name_entry = tk.Entry(frame2_2, font=("Helvetica", 14))
        window.vm_name_entry.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # add a optional divider
        tk.Label(window.scroll_frame.scrollFrame.viewPort,
                 text="optional parameters",
                 height=1, font=("Helvetica", 14),
                 anchor="center").pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        tk.Frame(window.scroll_frame.scrollFrame.viewPort, height=1,
                 bg="black").pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        # optional name of datacenter
        frame3 = tk.Frame(window.scroll_frame.scrollFrame.viewPort, width=565,
                          height=80, bg="#f442e8")
        frame3.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        frame3_1 = tk.Frame(frame3, width=200,
                            height=80, bg="#ffffff")
        frame3_1.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)
        frame3_2 = tk.Frame(frame3, width=200,
                            height=80, bg="#000000")
        frame3_2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        window.datacenter_name_entry = tk.Entry(frame3_2,
                                                font=("Helvetica", 14))
        frame3_label = tk.Label(frame3_1, text="Enter datacenter name:",
                                font=("Helvetica", 14), anchor="e", width=20)
        # add a resize event that increases font size
        frame3_label.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        window.datacenter_name_entry.pack(side=tk.LEFT,
                                          expand=tk.YES, fill=tk.BOTH)
        # optional vm folder
        frame4 = tk.Frame(window.scroll_frame.scrollFrame.viewPort, width=565,
                          height=80, bg="#f442e8")
        frame4.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        frame4_1 = tk.Frame(frame4, width=200,
                            height=80, bg="#ffffff")
        frame4_1.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)
        frame4_2 = tk.Frame(frame4, width=200,
                            height=80, bg="#000000")
        frame4_2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frame4_label = tk.Label(frame4_1, text="Enter VM folder:",
                                font=("Helvetica", 14), anchor="e", width=20)
        # add a resize event that increases font size
        frame4_label.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        window.folder_entry = tk.Entry(frame4_2, font=("Helvetica", 14))
        window.folder_entry.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # optional datastore
        # optional cluster name
        # optional resourcePool
        # power on tick box and send it button
        frame5 = tk.Frame(window.scroll_frame.scrollFrame.viewPort, width=565,
                          height=80, bg="#f442e8")
        frame5.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        frame5_1 = tk.Frame(frame5, width=200,
                            height=80, bg="#ffffff")
        frame5_1.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)
        frame5_2 = tk.Frame(frame5, width=200,
                            height=80, bg="#000000")
        frame5_2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # TODO add power on tick box
        # frame5_label = tk.Label(frame5_1, text="Enter VM folder:",
        #                         font=("Helvetica", 14), anchor="e", width=20)
        # frame5_label.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        tk.Button(frame5_2, font=("Helvetica", 14),
                  text="Clone VM",
                  command=lambda: clone_vm(window)).pack(
                  side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
