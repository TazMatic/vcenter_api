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


class scrollable_frame(tk.Frame):
    def __init__(self, root, window):
        tk.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self, root.winfo_width())
        self.scrollFrame.pack(side="top", fill="both", expand=tk.YES)
