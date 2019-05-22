""""Provides the main_window"""
from PyQt5 import QtWidgets, QtGui, QtCore
import socket
from pyvim.connect import SmartConnectNoSSL, Disconnect
import atexit
import GUI.vc_main_gui as vc_main_gui
from pyVmomi import vim
from functools import partial
lastRendered = None


# https://stackoverflow.com/a/4552646
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst = [
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        global lastRendered
        if lastRendered:
            lastRendered.unpost()

        rmenu = tk.Menu(None, tearoff=0, takefocus=0)
        lastRendered = rmenu

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.post(e.x_root+40, e.y_root+10)

    except tk.TclError:
        print(' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in ['Text', 'Entry', 'Listbox', 'Label']:
            r.bind_class(b, sequence='<Button-3> ',
                         func=rClicker, add='')
    except tk.TclError:
        print(' - rClickbinder, something wrong')
        pass


def vc_connect(window):
    window.si = None
    try:
        window.si = SmartConnectNoSSL(host=window.host_text.text().strip(),
                                      user=window.username_text.text().strip(),
                                      pwd=window.password_text.text())
        atexit.register(Disconnect, window.si)
    except vim.fault.InvalidLogin:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Unable to connect to host"
                    " with supplied credentials.")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        return
    except socket.error:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Unable to connect to host")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        return
    except Exception as e:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText(e)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        return

    # render clone_vm window
    vc_main_gui.render_main_gui(window)


def render_login(window):
    # Getting screen dimensions
    screen = window.app.primaryScreen()
    size = screen.size()
    width = size.width()
    height = size.height()
    
    # Resize window for login prompt
    window.setGeometry(width/2 - 300, height/2 - 200, 600, 400)
    window.setMinimumSize(600, 400)
    window.setMaximumSize(600, 400)
    
    # rClickbinder(window)

    # Create label and entry for host name/ip
    hostname_label = QtWidgets.QLabel('VCenter IP', window.main_frame)
    hostname_label.setFont(QtGui.QFont('Helvetica', 14))
    hostname_label.setStyleSheet("background-color: #3a3d42; color: #ffffff")
    hostname_label.move(80, 50)
    window.host_text = QtWidgets.QLineEdit(window.main_frame)
    window.host_text.setFont(QtGui.QFont('Helvetica', 14))
    window.host_text.setStyleSheet("color: #3a3d42; background-color: #ffffff")
    window.host_text.resize(300,30)
    window.host_text.move(200, 50)


    # Create label and entry for username
    username_label = QtWidgets.QLabel('Username', window.main_frame)
    username_label.setFont(QtGui.QFont('Helvetica', 14))
    username_label.setStyleSheet("background-color: #3a3d42; color: #ffffff")
    username_label.move(80, 100)
    window.username_text = QtWidgets.QLineEdit(window.main_frame)
    window.username_text.setFont(QtGui.QFont('Helvetica', 14))
    window.username_text.setStyleSheet("color: #3a3d42; background-color: #ffffff")
    window.username_text.resize(300,30)
    window.username_text.move(200, 100)


    # Create label and entry for password
    password_label = QtWidgets.QLabel('Password', window.main_frame)
    password_label.setFont(QtGui.QFont('Helvetica', 14))
    password_label.setStyleSheet("background-color: #3a3d42; color: #ffffff")
    password_label.move(80, 150)
    window.password_text = QtWidgets.QLineEdit(window.main_frame)
    window.password_text.setEchoMode(QtWidgets.QLineEdit.Password)
    window.password_text.setFont(QtGui.QFont('Helvetica', 14))
    window.password_text.setStyleSheet("color: #3a3d42; background-color: #ffffff")
    window.password_text.resize(300,30)
    window.password_text.move(200, 150)
   
    # Bind enter to login
    def return_press():
        vc_connect(window)

    window.enter = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), window.main_frame)
    window.enter.activated.connect(return_press)
    
    # Create login and cancel button
    login_button = QtWidgets.QPushButton('Login', window.main_frame)
    login_button.setFont(QtGui.QFont('Helvetica', 14))
    login_button.setStyleSheet("color: #3a3d42; background-color: #ffffff")
    login_button.resize(180,35)
    login_button.move(130, 200)
    login_button.clicked.connect(partial(vc_connect, window))

    cancel_button = QtWidgets.QPushButton('Cancel', window.main_frame)
    cancel_button.setFont(QtGui.QFont('Helvetica', 14))
    cancel_button.setStyleSheet("color: #3a3d42; background-color: #ffffff")
    cancel_button.resize(180,35)
    cancel_button.move(320, 200)
    cancel_button.clicked.connect(window.app.quit)

