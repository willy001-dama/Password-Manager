import sys
from PySide6 import QtWidgets as widget
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from backend import database
from frontend.dashboard import MainMenu


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Warehouse")
        self.setWindowIcon(QtGui.QIcon("images/icon.png"))
        self.setFixedSize(700, 550)
        self.setStyleSheet("background:white;margin:0px;")
        self.init_ui()
        self.show()

    def init_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = LoginPage()
        self.main_screen = MainMenu()

        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.main_screen)

        self.central_widget.setCurrentWidget(self.login_screen)


class LoginPage(widget.QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = widget.QVBoxLayout(self)  # main layout

        image = QtGui.QPixmap("../images/lock.jfif") # load image
        image_label = widget.QLabel()
        image_label.setPixmap(image)  # display image using label
        image_label.setAlignment(QtCore.Qt.AlignCenter)

        login_center = widget.QVBoxLayout() # create layout for form
        # ---------------------------------------------------------------
        label1 = widget.QLabel("Username Field")
        label1.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.entry1 = widget.QLineEdit()
        self.entry1.setFixedWidth(400)
        self.entry1.setPlaceholderText("Enter Username")
        self.entry1.setStyleSheet(
            """
            padding:5px;font-size:20px;
            color:brown;margin-top:10px;
            border-radius:5px;border:1px solid grey;""")

        label2 = widget.QLabel("Password Field")
        label2.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.entry2 = widget.QLineEdit()
        self.entry2.setPlaceholderText("Enter Your Password")
        self.entry2.setEchoMode(widget.QLineEdit.Password)
        self.entry2.setStyleSheet(
            """
            padding:5px;font-size:20px;
            color:gray;margin-top:10px;
            border-radius:5px;border:1px solid grey;""")
        self.entry2.setFixedWidth(400)
        login_btn = widget.QPushButton("Login")
        login_btn.clicked.connect(self.validate_login)
        login_btn.setStyleSheet(
            """
            padding:5px;font-size:15px;
            margin-top:10px;
            border-radius:5px;border:1px solid grey;""")

        sub_layout = widget.QHBoxLayout()  # sub layout for buttons
        forgot_pass = widget.QPushButton("Recover Password")
        forgot_pass.setStyle
        register = widget.QPushButton("Register Here")
        sub_layout.addWidget(forgot_pass)
        sub_layout.addWidget(register)
        #  Position widgets
        login_center.addWidget(self.entry1)
        login_center.addWidget(self.entry2)
        login_center.addWidget(login_btn)
        login_center.addLayout(sub_layout)
        login_center.setAlignment(QtCore.Qt.AlignCenter)

        # right part of the login body
        # ------------------------------------------------------------------
        # add head and body layout to the main layout

        main_layout.addWidget(image_label)
        main_layout.addStretch(1)
        main_layout.addLayout(login_center)
        main_layout.addStretch(2)
        self.setStyleSheet("background:white")
        self.setLayout(main_layout)  # set main layout

    def validate_login(self):
        username = self.entry1.text()
        password = self.entry2.text()
        if not username or not password:
            widget.QMessageBox.warning(self, "Error", "Fields can't be empty")
        else:
            login = database.DatabaseOps().login(username, password)
            if login and login == 1:
                widget.QMessageBox.information(self, "Success", "Login Successful")
            else:
                widget.QMessageBox.warning(self, "Error", "Incorrect Login Details. Try Again!")
            print(login)


win = widget.QApplication(sys.argv)
my_app = MainApp()
my_app.resize(600, 200)
my_app.show()
win.exec()
