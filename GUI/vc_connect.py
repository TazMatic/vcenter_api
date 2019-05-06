""""Provides the main_window"""
import tkinter as tk
from tkinter import messagebox
import socket
from pyvim.connect import SmartConnectNoSSL, Disconnect
import atexit
import GUI.vc_main_gui as vc_main_gui
from pyVmomi import vim
from functools import partial
lastRendered = None


# https://stackoverflow.com/a/4552646
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst = [
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        global lastRendered
        if lastRendered:
            lastRendered.unpost()

        rmenu = tk.Menu(None, tearoff=0, takefocus=0)
        lastRendered = rmenu

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.post(e.x_root+40, e.y_root+10)

    except tk.TclError:
        print(' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in ['Text', 'Entry', 'Listbox', 'Label']:
            r.bind_class(b, sequence='<Button-3> ',
                         func=rClicker, add='')
    except tk.TclError:
        print(' - rClickbinder, something wrong')
        pass


def vc_connect(window):
    window.si = None
    try:
        window.si = SmartConnectNoSSL(host=window.host_text.get(),
                                      user=window.username_text.get(),
                                      pwd=window.password_text.get())
        atexit.register(Disconnect, window.si)
    except vim.fault.InvalidLogin:
        messagebox.showinfo("title", "Unable to connect to host"
                                     " with supplied credentials.")
        return
        # raise SystemExit("Unable to connect to host "
        #                 "with supplied credentials.")
    except socket.error:
        messagebox.showinfo("title", "Unable to connect to host")
        return
        # raise SystemExit("Unable to connect to host.")
    except Exception as e:
        messagebox.showinfo("title", e)
        return

    # render clone_vm window
    vc_main_gui.render_main_gui(window)


def render_login(window):
    # clear the screen of anything in it before
    for child in window.main_frame.winfo_children():
        child.destroy()

    # Centering the window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    screen_resolution = '600'+'x'+'400'+'+'+str(int(screen_width/2) - 300) + \
        '+' + str(int(screen_height/2) - 200)

    # resize window for login prompt
    window.geometry(screen_resolution)
    window.minsize(600, 400)
    window.maxsize(600, 400)
    window.main_frame.config(bg='#3a3d42')
    rClickbinder(window)

    # create label and entry for host name/ip
    tk.Label(window.main_frame, text="VCenter IP",
             height=1,  width=15, font=("Helvetica", 14), bg='#3a3d42',
             foreground="#ffffff").place(x=60, y=50)

    window.host_text = tk.Entry(window.main_frame, font=("Helvetica", 14),
                                width=30)
    window.host_text.place(x=200, y=50)

    # create label and entry for username
    tk.Label(window.main_frame,
             text="Username", height=1,  width=15, bg='#3a3d42',
             foreground="#ffffff", font=("Helvetica", 14)).place(x=60, y=100)

    window.username_text = tk.Entry(window.main_frame, font=("Helvetica", 14),
                                    width=30)
    window.username_text.place(x=200, y=100)

    # create label and entry for username
    tk.Label(window.main_frame,
             text="Password", height=1,  width=15, bg='#3a3d42',
             foreground="#ffffff", font=("Helvetica", 14)).place(x=60, y=150)

    window.password_text = tk.Entry(window.main_frame, show="*", font=("Helvetica", 14),
                                    width=30)
    window.password_text.place(x=200, y=150)

    # create login and cancel button
    tk.Button(window.main_frame, text="Login", width=15,
              command=partial(vc_connect, window),
              font=("Helvetica", 14)).place(x=150, y=200)
    tk.Button(window.main_frame, text="Cancel", width=15,
              command=window.destroy,
              font=("Helvetica", 14)).place(x=300, y=200)
