import sys
from PySide6 import QtWidgets as widget
from PySide6 import QtGui, QtCore

# user import
import draw_line
import password
import payment
import note

from backend.database import DatabaseOps


class MainMenu(widget.QWidget):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.setWindowTitle("Main Menu")
        self.setWindowIcon(QtGui.QIcon("../images/icon.png"))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(700, 550)
        # self.showMaximized()
        # create DB instance and pass to different pages
        self.database_handle = DatabaseOps()
        # create instance of other window and arrange in stack
        self.right_window_holder = widget.QStackedWidget()
        self.right_window_holder.addWidget(password.PasswordList(self.database_handle))
        self.right_window_holder.addWidget(payment.PaymentInfo(self.database_handle))
        self.right_window_holder.addWidget(note.NoteList(self.database_handle))
        # self.right_window_holder.addWidget(result_menu.Result(self.database_handle))
        self.right_window_holder.setCurrentIndex(0)
        self.current = 0
        self.style_active = """
        QPushButton#menu_button{background:rgba(41, 128, 140,1);color:white;}
        QPushButton#menu_button:hover{
        background:rgba(41, 128, 140, 0.7);
        color:white;
        }
        """
        self.style_non_active = """
            QPushButton#menu_button{
                background:rgb(31, 214, 199, 0);
                padding:10px;
                border:none;
                font-style:bolder;
                font-size:20px;
                text-align:left;
                color:rgb(41, 128, 140);
                font-family:Consolas Bold;
            }
            QPushButton#menu_button:hover{
                color:rgb(74, 228, 215)
            }
        
        """
        with open("style.qss") as file:
            style = file.read()
        self.setStyleSheet(style)
        # build the UI
        self.buildUi()

    def buildUi(self):
        body_layout = widget.QHBoxLayout(self)
        body_layout.setContentsMargins(0, 0, 0, 0)
        # --------------------------------------------
        # left  menu goes here
        left_frame = widget.QFrame()
        left_frame.setObjectName("left_frame")
        left_side = widget.QVBoxLayout()
        # -------------------- left side button and text here

        label = widget.QLabel("Welcome! Dama")
        # label.setPixmap(QtGui.QPixmap("images/retouch.pngg").scaled(100, 100))
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.logins = widget.QPushButton(text="Logins")
        self.logins.clicked.connect(lambda: self.switch_page1(0))
        self.logins.setObjectName("menu_button")
        self.logins.setFixedWidth(220)
        #
        # add_student = widget.QPushButton(text="-> View ")
        # add_student.setObjectName("menu_button")
        # add_student.setFixedWidth(300)

        self.payment = widget.QPushButton(text="Payments")
        self.payment.setObjectName("menu_button")
        self.payment.clicked.connect(lambda: self.switch_page1(1))
        self.payment.setFixedWidth(220)

        self.note = widget.QPushButton(text="Secure Note")
        self.note.clicked.connect(lambda: self.switch_page1(2))
        self.note.setObjectName("menu_button")

        self.personal = widget.QPushButton(text="Personal Info")
        self.personal.clicked.connect(lambda: self.switch_page1(3))
        self.personal.setObjectName("menu_button")

        self.generate_pass = widget.QPushButton(text="Generate Password")
        self.generate_pass.clicked.connect(lambda: self.switch_page1(4))
        self.generate_pass.setObjectName("menu_button")

        self.test_pass = widget.QPushButton(text="Test Password Strength")
        self.test_pass.clicked.connect(lambda: self.switch_page1(4))
        self.test_pass.setObjectName("menu_button")


        add_record = widget.QPushButton(text="-> General Settings")
        add_record.setObjectName("menu_button")
        view_record = widget.QPushButton(text="Add new student")

        # add widget to layout
        left_side.addWidget(label)
        left_side.addWidget(draw_line.QHSeparationLine())
        left_side.addWidget(self.logins)
        left_side.addWidget(self.payment)
        left_side.addWidget(self.personal)
        left_side.addWidget(self.note)
        left_side.addWidget(draw_line.QHSeparationLine())
        left_side.addWidget(self.generate_pass)
        left_side.addStretch()
        left_side.addWidget(self.test_pass)
        # left_side.addWidget(view_record)
        # left_side.addStretch()

        # self.right_window_holder.addWidget(student_info.StudentInfo())
        # self.right_window_holder.setCurrentIndex(1)
        right_side = self.right_window_holder
        # right_side.addStretch()

        left_frame.setLayout(left_side)
        body_layout.addWidget(left_frame)
        body_layout.addWidget(right_side)
        # body_layout.addStretch()
        self.update_selection(0)
        self.setLayout(body_layout)

    def switch_page1(self, value):
        if not value == self.right_window_holder.currentIndex():
            self.right_window_holder.setCurrentIndex(value)
            self.update_selection(value=value)

    def update_selection(self, value):
        if value == 0:
            self.logins.setStyleSheet(self.style_active)
            self.payment.setStyleSheet(self.style_non_active)
            self.personal.setStyleSheet(self.style_non_active)
            self.note.setStyleSheet(self.style_non_active)
            self.generate_pass.setStyleSheet(self.style_non_active)
        elif value == 1:
            self.payment.setStyleSheet(self.style_active)
            self.logins.setStyleSheet(self.style_non_active)
            self.personal.setStyleSheet(self.style_non_active)
            self.generate_pass.setStyleSheet(self.style_non_active)
            self.note.setStyleSheet(self.style_non_active)

        elif value == 2:
            self.personal.setStyleSheet(self.style_non_active)
            self.generate_pass.setStyleSheet(self.style_non_active)
            self.logins.setStyleSheet(self.style_non_active)
            self.payment.setStyleSheet(self.style_non_active)
            self.note.setStyleSheet(self.style_active)
        elif value == 3:
            self.personal.setStyleSheet(self.style_active)
            self.payment.setStyleSheet(self.style_non_active)
            self.logins.setStyleSheet(self.style_non_active)
            self.note.setStyleSheet(self.style_non_active)
            self.generate_pass.setStyleSheet(self.style_non_active)
        elif value == 4:
            self.logins.setStyleSheet(self.style_active)
            self.note.setStyleSheet(self.style_non_active)
            self.payment.setStyleSheet(self.style_non_active)
            self.personal.setStyleSheet(self.style_non_active)
            self.generate_pass.setStyleSheet(self.style_non_active)


# with open("style.qss") as file:
#     style = file.read()
# #
# win = widget.QApplication(sys.argv)
# my_app = MainMenu()
# my_app.show()
# win.setStyleSheet(style)
# win.exec()
