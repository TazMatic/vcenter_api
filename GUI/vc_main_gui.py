""""Provides the central GUI"""
import Tkinter as tk


def render_main_gui(window):
    # clear the screen of anything in it before
    for child in window.main_frame.winfo_children():
        child.destroy()

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
    window.menu_frame = tk.Frame(window.main_frame, width=200, bg="#ffffff")
    window.central_frame = tk.Frame(window.main_frame, width=600,
                                    bg="#000000")
    window.menu_frame.pack(expand=tk.NO,
                           fill=tk.BOTH, side=tk.LEFT)
    window.central_frame.pack(expand=tk.YES,
                              fill=tk.BOTH, side=tk.LEFT)
