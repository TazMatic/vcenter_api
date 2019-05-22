""""Provides the main_window"""
from PyQt5 import QtWidgets

import GUI.vc_connect

class main_window(QtWidgets.QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()
        self.setGeometry(400, 200, 300, 0)
        self.setWindowTitle("VCenter ACDC GUI")
        self.show()
        
		# Create main frame
        self.main_frame = QtWidgets.QFrame()
        self.main_frame.setStyleSheet("background-color: #3a3d42;")
        self.setCentralWidget(self.main_frame)
		
		# Variable creation
        self.host_text = None
        self.log = None
        self.scroll_frame = None
        self.last_rendered = None
        self.vms = list()
        self.app = QtWidgets.QApplication.instance() 
        GUI.vc_connect.render_login(self)

