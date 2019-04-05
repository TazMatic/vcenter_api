""""Provides the main_window"""
import Tkinter
import GUI.vc_connect


class main_window(Tkinter.Tk):
    """Provides a root window"""
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.geometry("400x200+300+0")
        self.minsize(400, 200)
        self.title("VCenter ACDC GUI")

        self.main_frame = Tkinter.Frame(self, width=200, bg="#ffffff")
        self.main_frame.pack(expand=Tkinter.YES,
                             fill=Tkinter.BOTH, side=Tkinter.LEFT)

        self.host_text = None

        GUI.vc_connect.render_login(self)
