from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QCheckBox, QGridLayout

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from draw_line import QHSeparationLine, QVSeparationLine
from frontend import draw_line


class PasswordList(QFrame):
    def __init__(self, database_handle):
        super(PasswordList, self).__init__()
        self.database_handle = database_handle
        self.setStyleSheet("QFrame{background:white;}")
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()

        add_new = QPushButton("+ Add New")
        add_new.clicked.connect(self.add_new_login)
        add_new.setStyleSheet("padding:8px;border-radius:0px;"
                              "background:rgba(41, 128, 140,1);color:white;font-weight:bold;")
        change_pass = QPushButton("Change Password")
        change_pass.clicked.connect(self.update_password)
        change_pass.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        # menu_layout.addWidget(session_label)
        # menu_layout.addWidget(QVSeparationLine())
        # menu_layout.addWidget(term_label)
        menu_layout.addWidget(add_new)
        menu_layout.addWidget(change_pass)
        menu_layout.addStretch()
        # menu_layout.addWidget()
        name_label = QLabel("NAME")
        created_on = QLabel("CREATED ON")

        password = QGridLayout()
        password.addWidget(name_label, 0, 0)
        password.addWidget(created_on, 0, 1)

        def btn_click():
            print("hello")

        record = self.database_handle.retrieve_all_records(1)

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
            action_button = QPushButton("....")
            action_button.setStyleSheet("border:none;font-size:20px;cursor:hand;")
            action_button.setFixedWidth(40)
            action_button.clicked.connect(btn_click)
            password.addWidget(action_button, index + 2, 2)
            password.addWidget(draw_line.QHSeparationLine(), index + 3 + 1, 0, 1, 3, Qt.AlignLeft)

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addLayout(password)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def add_new_login(self):
        app = NewPassword(self, self.database_handle)
        app.open()
        self.update()

    def update_password(self):
        win = UpdatePassword(self, self.database_handle)
        win.open()

    def update_student_callback(self):
        pass


class NewPassword(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_handle):
        super(NewPassword, self).__init__(parent)
        self.database_handle = database_handle
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
        label = QLabel("Encrypt Password?")
        label.setStyleSheet("font-size:16px;padding-top:5px;")
        self.encrypt_data = QCheckBox()
        stat_frame.addWidget(label)
        stat_frame.addWidget(self.encrypt_data)
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
        encrypt = self.encrypt_data.isChecked()
        if site_name and username and password:
            self.database_handle.save_record(site_name, username, password, encrypt, owner=1)
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

        self.database_handle.update_password(site_name, password, 1)
        QMessageBox.information(self, 'Success', "Password Updated Successfully")
        self.hide()
