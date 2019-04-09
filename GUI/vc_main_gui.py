""""Provides the central GUI"""
import tkinter as tk


# https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
class ScrollFrame(tk.Frame):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff",
                                width=size)
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# ********************************
# Example usage of the above class
# ********************************

class scrollable_frame(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self, root.winfo_width())
        for row in range(100):
            a = row
            tk.Label(self.scrollFrame.viewPort, text="%s" % row,
                     width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t = "this is the second column for row %s" % row
            tk.Button(self.scrollFrame.viewPort, text=t,
                      command=lambda x=a:
                      self.printMsg("Hello " +
                                    str(x))).grid(row=row, column=1)

        self.scrollFrame.pack(side="top", fill="both", expand=tk.YES)

    def printMsg(self, msg):
        print(msg)


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
    window.menu_parent_frame = tk.Frame(window.main_frame, width=200,
                                        bg="#175ed1")
    window.central_frame = tk.Frame(window.main_frame, width=600,
                                    bg="#000000")
    window.menu_parent_frame.pack(expand=tk.NO,
                                  fill=tk.BOTH, side=tk.LEFT)
    window.central_frame.pack(expand=tk.YES,
                              fill=tk.BOTH, side=tk.LEFT)

    # Problem stuff
    window.update_idletasks()
    window.menu_frame = scrollable_frame(window.menu_parent_frame)
    window.menu_frame.pack(expand=tk.NO, fill=tk.BOTH, side=tk.LEFT)

# add menu buttons
