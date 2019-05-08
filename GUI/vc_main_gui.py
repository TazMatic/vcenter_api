""""Provides the central GUI"""
import tkinter as tk
from core_functions.list_vms import list_vms
from core_functions.clone_vm import render_clone_vm
from GUI.scrollable_frame import scrollable_frame


def render_main_gui(window):
    # clear the screen of anything in it before
    for child in window.main_frame.winfo_children():
        child.destroy()

    # Clear binds
    window.unbind('<Return>')

    # Centering the window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    screen_resolution = '800'+'x'+'600'+'+'+str(int(screen_width/2) - 400) + \
        '+' + str(int(screen_height/2) - 300)

    # resize window for login prompt
    window.geometry(screen_resolution)
    window.minsize(800, 600)
    window.maxsize(99999, 99999)
    window.main_frame.config(bg='#3a3d42')

# add two frames, one for the verticle menu and one for the selected options
    window.menu_parent_frame = tk.Frame(window.main_frame, width=200,
                                        bg="#175ed1")
    window.central_frame = tk.Frame(window.main_frame, width=600,
                                    bg="#000000")
    window.menu_parent_frame.pack(expand=tk.NO,
                                  fill=tk.BOTH, side=tk.LEFT)
    window.central_frame.pack(expand=tk.YES,
                              fill=tk.BOTH, side=tk.LEFT)

    window.update_idletasks()
    window.menu_frame = scrollable_frame(window.menu_parent_frame, window)
    window.menu_frame.pack(expand=tk.NO, fill=tk.BOTH, side=tk.LEFT)
    # make menu buttons, should be a dict of functions I beleive
    tk.Button(window.menu_frame.scrollFrame.viewPort,
              text="List VM's", width=21,
              command=lambda: list_vms(window)).pack(side="top")
    tk.Button(window.menu_frame.scrollFrame.viewPort,
              text="Clone VM", width=21,
              command=lambda: render_clone_vm(window)).pack(side="top")
