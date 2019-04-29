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
