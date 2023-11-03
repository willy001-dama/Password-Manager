from PySide6 import QtCore, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QCheckBox, QGridLayout

from PySide6.QtCore import Qt

from draw_line import QHSeparationLine, QVSeparationLine
from frontend import draw_line


class PasswordList(QFrame):
    def __init__(self, database_util, user):
        super(PasswordList, self).__init__()
        self.database_util = database_util
        self.user = user
        self.setStyleSheet("QFrame{background:white;}")
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()

        add_new = QPushButton("+ Add New")
        add_new.clicked.connect(self.add_new_login)
        add_new.setStyleSheet("padding:8px;border-radius:0px;"
                              "background:rgba(41, 128, 140,1);color:white;font-weight:bold;")
        change_pass = QPushButton("Change Password")
        change_pass.clicked.connect(self.update_password)
        change_pass.setIcon(QIcon('../images/password.png'))
        change_pass.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_btn)
        refresh_btn.setIcon(QIcon('../images/refresh.png'))
        refresh_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")


        menu_layout.addWidget(add_new)
        menu_layout.addWidget(change_pass)
        menu_layout.addWidget(refresh_btn)
        menu_layout.addStretch()
        # menu_layout.addWidget()
        name_label = QLabel("NAME")
        created_on = QLabel("CREATED ON")



        def btn_click(event=None, hello=None):
            print(event, hello)
            x = event.pos().x()
            y = event.pos().y()
            print(dir(event))
            print(x,y, event.globalX(), event.globalY(), event.globalPosition())
            ActionButton(self, event.globalX(), event.globalY())

        record = self.database_util.fetch_data("Login", user[0])
        if record:
            password = QGridLayout()
            password.addWidget(name_label, 0, 0)
            password.addWidget(created_on, 0, 1)

            for index, logins in enumerate(record):
                frame = QVBoxLayout()
                site_value = QLabel(logins[1])
                site_value.setStyleSheet("font-size:20px; font-weight:bold;")

                username_value = QLabel(logins[2])
                username_value.setStyleSheet("font-size:10px;")

                frame.addWidget(site_value)
                frame.addWidget(username_value)

                password.addLayout(frame, index + 2, 0)

                password.addWidget(QLabel("Two Days Ago"), index + 2, 1)
                self.action_button = QPushButton("....")
                self.action_button.setStyleSheet("border:none;font-size:20px;cursor:hand;")
                self.action_button.setFixedWidth(40)
                # self.action_button.clicked.connect(lambda text=logins[0]: btn_click(text))
                self.action_button.mousePressEvent = lambda:btn_click(logins[0])
                password.addWidget(self.action_button, index + 2, 2)
                password.addWidget(draw_line.QHSeparationLine(), index + 3 + 1, 0, 1, 3, Qt.AlignLeft)
        else:
            password = QVBoxLayout()
            image = QtGui.QPixmap("../images/empty.jpg")  # load image
            image_label = QLabel()
            image_label.setPixmap(image)  # display image using label
            image_label.setAlignment(QtCore.Qt.AlignCenter)
            password.addStretch()
            password.addWidget(image_label)
            password.addStretch()

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addLayout(password)
        # main_layout.addStretch()

        self.setLayout(main_layout)

    def add_new_login(self):
        app = NewPassword(self, self.database_util, self.user)
        app.open()

    def update_password(self):
        win = UpdatePassword(self, self.database_util)
        win.open()

    def refresh_btn(self):
        pass


class NewPassword(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_handle, user):
        super(NewPassword, self).__init__(parent)
        self.database_handle = database_handle
        self.user = user
        self.setFixedWidth(320)
        self.setWindowTitle("New Password")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.sitename = QLineEdit()
        self.sitename.setObjectName('entry')
        self.sitename.setPlaceholderText("Enter Site Name")
        self.username = QLineEdit()
        self.username.setObjectName('entry')
        self.username.setPlaceholderText("Enter Username")
        self.password = QLineEdit()
        self.password.setObjectName('entry')
        self.password.setPlaceholderText("Enter Password")
        submit_btn = QPushButton("Add Login")
        submit_btn.setObjectName("Add Login")
        submit_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                 "background:white;color:rgba(41, 128, 140,1);"
                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")
        submit_btn.clicked.connect(self.add_password)
        stat_frame = QHBoxLayout()
        layout.addWidget(self.sitename)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        # layout.addWidget(self.sitename)

        layout.addLayout(stat_frame)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def add_password(self):
        site_name = self.sitename.text()
        username = self.username.text()
        password = self.password.text()
        if site_name and username and password:
            self.database_handle.save_password(site_name, username, password, owner=self.user[0])
            QMessageBox.information(self, 'Success', "Logins Added successfully")

        else:
            QMessageBox.warning(self, 'Error Occurred', "All fields most be filled!")
        self.hide()


class UpdatePassword(QDialog):
    """Dialog window for Updating current term"""

    def __init__(self, parent, database_handle):
        super(UpdatePassword, self).__init__(parent)
        self.database_handle = database_handle
        self.setFixedWidth(320)
        self.setWindowTitle("Update Password")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.login_selection = QComboBox()
        record = self.database_handle.retrieve_all_records(1)
        for logins in record:
            self.login_selection.addItem(logins[1])
        self.login_selection.setStyleSheet("padding:3px;font-size:15px;color:rgba(41, 128, 140,1);"
                                           "margin-top:10px;"
                                           "border-radius:1px;border:1px solid grey;")
        self.login_selection.setPlaceholderText("Select Site To Update")
        self.password = QLineEdit()
        self.password.setObjectName('entry')
        self.password.setPlaceholderText("Enter Password")
        self.password.setStyleSheet("padding:4px;border-radius:2px;color:rgba(41, 128, 140,1);")
        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("submit")
        submit_btn.clicked.connect(self.updated_term)
        layout.addWidget(self.login_selection)
        layout.addWidget(self.password)
        layout.addWidget(submit_btn)
        style = """QPushButton#submit{padding:8px;border-radius:2px;
                            background:white;color:rgba(41, 128, 140,1);
                            font-weight:bold;border:1px solid rgba(41, 128, 140,1);}"""
        self.setStyleSheet(style)
        self.setLayout(layout)

    def updated_term(self):
        site_name = self.login_selection.currentText()
        password = self.password.text()
        if not password:
            QMessageBox.warning(self, 'Warning', "Password field cannot be empty")
            return

        self.database_handle.refresh_btn(site_name, password, 1)
        QMessageBox.information(self, 'Success', "Password Updated Successfully")
        self.hide()


class ActionButton(QDialog):
    """Dialog window for Updating current term"""

    def __init__(self, parent, point_x, point_y):
        super(ActionButton, self).__init__(parent)
        # self.database_handle = database_handle
        self.setFixedWidth(120)
        self.setWindowTitle("Update Password")

        # create widget and layout
        layout = QVBoxLayout()
        view_btn = QPushButton("View Login")
        update_btn = QPushButton("Update Login")
        update_btn.clicked.connect(self.update_login)
        delete_btn = QPushButton("Delete Login")
        delete_btn.clicked.connect(self.delete_login)
        layout.addWidget(view_btn)
        layout.addWidget(update_btn)
        layout.addWidget(delete_btn)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_QuitOnClose)
        self.setWindowFlags(Qt.Popup)
        # self.setWindowFlags(Qt.)
        self.move(point_x - 100, point_y)
        self.setStyleSheet("QDialog{background:white;border-radius:20px};"
                           "QPushButton{background:red;border:none;color:rgba(41, 128, 140,1);}")
        self.show()

    def delete_login(self):
        print("have been clicked")

    def update_login(self):
        print("hello here")
