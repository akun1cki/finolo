from PyQt5 import QtCore, QtGui, QtWidgets
import re


class RegisterAccount(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.parent = parent
        self.setObjectName("a")
        self.resize(313, 490)
        self.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                           "color: rgb(255, 255, 255);\n"
                           "font: 75 11pt \"FreeMono Bold\";")
        self.register_gb = QtWidgets.QGroupBox(self)
        self.register_gb.setGeometry(QtCore.QRect(10, 10, 300, 500))
        font = QtGui.QFont()
        font.setFamily("FreeMono Bold")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.register_gb.setFont(font)
        self.register_gb.setObjectName("groupBox")
        self.register_pass_1 = QtWidgets.QLineEdit(self.register_gb)
        self.register_pass_1.setGeometry(QtCore.QRect(10, 140, 271, 31))
        self.register_pass_1.setInputMask("")
        self.register_pass_1.setFrame(True)
        self.register_pass_1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.register_pass_1.setObjectName("register_pass_1")
        self.register_pass_1.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                                           "alternate-background-color: rgb(9, 21, 32); \n"
                                           "color: rgb(255, 255, 255); \n"
                                           "font: 50  10pt \"FreeMono Bold\";")
        self.register_username = QtWidgets.QLineEdit(self.register_gb)
        self.register_username.setGeometry(QtCore.QRect(10, 70, 271, 31))
        self.register_username.setInputMask("")
        self.register_username.setFrame(True)
        self.register_username.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.register_username.setObjectName("lineEdit_36")
        self.register_username.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                                             "alternate-background-color: rgb(9, 21, 32); \n"
                                             "color: rgb(255, 255, 255); \n"
                                             "font: 50  10pt \"FreeMono Bold\";")
        self.label = QtWidgets.QLabel(self.register_gb)
        self.label.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.register_gb)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 111, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.register_gb)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 141, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.register_gb)
        self.label_4.setGeometry(QtCore.QRect(10, 250, 141, 21))
        self.label_4.setObjectName("label_4")
        self.register_pass_2 = QtWidgets.QLineEdit(self.register_gb)
        self.register_pass_2.setGeometry(QtCore.QRect(10, 210, 271, 31))
        self.register_pass_2.setInputMask("")
        self.register_pass_2.setFrame(True)
        self.register_pass_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.register_pass_2.setObjectName("lineEdit_37")
        self.register_pass_2.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                                           "alternate-background-color: rgb(9, 21, 32); \n"
                                           "color: rgb(255, 255, 255); \n"
                                           "font: 50  10pt \"FreeMono Bold\";")
        self.register_email = QtWidgets.QLineEdit(self.register_gb)
        self.register_email.setGeometry(QtCore.QRect(10, 280, 271, 31))
        self.register_email.setObjectName("register_email")
        self.register_email.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                                          "alternate-background-color: rgb(9, 21, 32); \n"
                                          "color: rgb(255, 255, 255); \n"
                                          "font: 50  10pt \"FreeMono Bold\";")
        self.register_register = QtWidgets.QPushButton(self.register_gb)
        self.register_register.setGeometry(QtCore.QRect(150, 370, 131, 41))
        self.register_register.setObjectName("register_register")
        self.register_terms = QtWidgets.QPushButton(self.register_gb)
        self.register_terms.setGeometry(QtCore.QRect(10, 370, 131, 41))
        self.register_terms.setObjectName("register_terms")
        self.register_back = QtWidgets.QPushButton(self.register_gb)
        self.register_back.setGeometry(QtCore.QRect(150, 430, 131, 41))
        self.register_back.setObjectName("pushButton_35")
        self.register_terms_cb = QtWidgets.QCheckBox(self.register_gb)
        self.register_terms_cb.setGeometry(QtCore.QRect(10, 330, 201, 23))
        self.register_terms_cb.setObjectName("checkBox")

        self.retranslateUi()

        self.register_back.clicked.connect(self.go_back)
        self.register_register.clicked.connect(self.create_account)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def go_back(self):
        self.parent.resize(308, 318)
        self.close()

    def valid_email(self, email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if re.search(regex, email):
            return True
        else:
            return False

    def create_account(self):
        username = self.register_username.text().lower()
        pass1 = self.register_pass_1.text()
        pass2 = self.register_pass_2.text()
        email = self.register_email.text()

        query = f"SELECT user FROM users WHERE user='{username}'"
        usercheck = self.back.db.execute_read_query(query)

        print(usercheck)

        if usercheck:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Such user already exists.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return

        elif not username:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Please input username.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()

        elif not pass1:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Please input password.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()

        elif pass1 != pass2:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Passwords do not match.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return

        elif not self.register_terms_cb.checkState():
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Please accept terms of use.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return

        elif email and not self.valid_email(email):
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Enter valid e-mail.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return

        elif (pass1 == pass2) and self.register_terms_cb.checkState():
            self.back.add_hash(username, pass1)
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Registration successful.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            self.parent.resize(308, 318)
            self.close()

        else:
            return

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Create account"))
        self.register_gb.setTitle(_translate("Form", "   new account"))
        self.label.setText(_translate("Form", "login"))
        self.label_2.setText(_translate("Form", "password"))
        self.label_3.setText(_translate("Form", "confirm password"))
        self.label_4.setText(_translate("Form", "e-mail (optional)"))
        self.register_register.setText(_translate("Form", "register"))
        self.register_terms.setText(_translate("Form", "terms of use"))
        self.register_back.setText(_translate("Form", "back"))
        self.register_terms_cb.setText(_translate("Form", "I accept terms of use."))
