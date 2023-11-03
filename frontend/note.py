from functools import partial

from PySide6 import QtCore
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QCheckBox, QGridLayout, QPlainTextEdit

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

from draw_line import QHSeparationLine, QVSeparationLine
from frontend import draw_line


class NoteList(QFrame):
    def __init__(self, database_util, user):
        super(NoteList, self).__init__()
        self.database_util = database_util
        self.user = user
        self.setStyleSheet("QFrame{background:white;}")
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()

        add_new = QPushButton(" ADD NEW NOTE")
        add_new.clicked.connect(self.add_new_login)
        add_new.setIcon(QIcon("../images/add.png"))
        add_new.setStyleSheet("padding:8px;border-radius:3px;"
                              "background:white;font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                              )
        regresh_btn = QPushButton("Refresh")
        regresh_btn.clicked.connect(self.refresh_btn)
        regresh_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        # menu_layout.addWidget(session_label)
        # menu_layout.addWidget(QVSeparationLine())
        # menu_layout.addWidget(term_label)
        menu_layout.addWidget(add_new)
        menu_layout.addWidget(regresh_btn)
        menu_layout.addStretch()
        # menu_layout.addWidget()
        name_label = QLabel("NAME")
        created_on = QLabel("CREATED ON")

        password = QGridLayout()
        password.addWidget(name_label, 0, 0)
        password.addWidget(created_on, 0, 1)
        self.record = self.database_util.fetch_data("Notes", self.user[0])
        if self.record:
            def btn_click(data):
                print(data)

            for index, logins in enumerate(self.record):
                frame = QVBoxLayout()
                site_value = QLabel(logins[1])
                site_value.setStyleSheet("font-size:20px; font-weight:bold;")

                username_value = QLabel(logins[2])
                username_value.setStyleSheet("font-size:10px;")

                frame.addWidget(site_value)
                frame.addWidget(username_value)

                password.addLayout(frame, index + 2, 0)

                password.addWidget(QLabel("Two Days Ago"), index + 2, 1)
                self.action_button = QPushButton(f"view")
                self.action_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                                 "border-radius:4px")
                self.action_button.setFixedWidth(40)
                self.action_button.clicked.connect(partial(btn_click, logins[0]))
                password.addWidget(self.action_button, index + 2, 2)
                password.addWidget(draw_line.QHSeparationLine(), index + 3 + 1, 0, 1, 3, Qt.AlignLeft)
        else:
            password = QVBoxLayout()
            image = QPixmap("../images/empty.jpg")  # load image
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
        app = NewNote(self, self.database_util, self.user)
        app.open()
        self.update()

    def refresh_btn(self):
        self.update()

class NewNote(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_util, user):
        super(NewNote, self).__init__(parent)
        self.user = user
        self.database_util = database_util
        self.setFixedWidth(320)
        self.setWindowTitle("New Note")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.title = QLineEdit()
        self.title.setObjectName('entry')
        self.title.setPlaceholderText("Enter Title Of Note")
        self.note = QPlainTextEdit()
        self.note.setObjectName('entry')
        self.note.setPlaceholderText("Type your note here")
        submit_btn = QPushButton("Add Note")
        submit_btn.setObjectName("Add Login")
        submit_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                 "background:white;color:rgba(41, 128, 140,1);"
                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")
        submit_btn.clicked.connect(self.add_note)
        layout.addWidget(self.title)
        layout.addWidget(self.note)
        # layout.addWidget(self.sitename)

        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def add_note(self):
        note_title = self.title.text()
        note_content = self.note.toPlainText()
        print(note_title, note_content)
        if note_title and note_content:
            self.database_util.insert_note(note_title, note_content, owner=self.user[0])
            QMessageBox.information(self, 'Success', "Note Added successfully")

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


class NoteDetail(QDialog):
    """Dialog window for viewing details of note"""

    def __init__(self, parent, point_x, point_y):
        super(NoteDetail, self).__init__(parent)
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
