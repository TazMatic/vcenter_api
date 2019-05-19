""""Provides the main_window"""
from PyQt5 import QtWidgets
import sys
# import GUI.vc_connect

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(400, 200, 300, 0)
        self.setWindowTitle("VCenter ACDC GUI")
        self.show()
		
app = QtWidgets.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
# class main_window(tkinter.Tk):
    # """Provides a root window"""
	
    # def __init__(self):
        # tkinter.Tk.__init__(self)
        # self.geometry("400x200+300+0")
        # self.minsize(400, 200)
        # self.title("VCenter ACDC GUI")

        # self.main_frame = tkinter.Frame(self, width=200, bg="#ffffff")
        # self.main_frame.pack(expand=tkinter.YES,
                             # fill=tkinter.BOTH, side=tkinter.LEFT)

        # self.host_text = None
        # self.log = None
        # self.scroll_frame = None
        # self.last_rendered = None
        # self.vms = list()

        # GUI.vc_connect.render_login(self)
        # # from GUI.vc_main_gui import render_main_gui
        # # render_main_gui(self)
