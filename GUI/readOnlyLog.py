import tkinter as tk


# https://stackoverflow.com/a/11612656
class ReadOnlyText(tk.Text):
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)
		def txtEvent(event):
			if(event.state==12 and event.keysym=='c' ):
				return
			else:
				return "break"

		self.bind("<Key>", lambda e: txtEvent(e))
