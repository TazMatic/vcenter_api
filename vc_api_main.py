from GUI import basic_window
from PyQt5 import QtWidgets
import sys

# Create a reference to the main elements
app = QtWidgets.QApplication(sys.argv)
GUI = basic_window.main_window()
sys.exit(app.exec_())

