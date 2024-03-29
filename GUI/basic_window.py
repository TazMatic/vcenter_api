""""Provides the main_window"""
import tkinter
import GUI.vc_connect


class main_window(tkinter.Tk):
    """Provides a root window"""
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.geometry("400x200+300+0")
        self.minsize(400, 200)
        self.title("VCenter ACDC GUI")

        self.main_frame = tkinter.Frame(self, width=200, bg="#ffffff")
        self.main_frame.pack(expand=tkinter.YES,
                             fill=tkinter.BOTH, side=tkinter.LEFT)

        self.host_text = None

        GUI.vc_connect.render_login(self)
