from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
from backend import Backend
from register import RegisterAccount


class LoginScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.back = Backend()
        self.resize(308, 318)
        self.setStyleSheet("background-color: rgb(12, 111, 48);\n"
                           "color: rgb(255, 255, 255);\n"
                           "font: 75 11pt \"FreeMono Bold\";")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 291, 301))
        font = QtGui.QFont()
        font.setFamily("FreeMono Bold")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.login_line = QtWidgets.QLineEdit(self.groupBox)
        self.login_line.setGeometry(QtCore.QRect(10, 70, 271, 31))
        self.login_line.setInputMask("")
        self.login_line.setFrame(True)
        self.login_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.login_line.setObjectName("lineEdit_35")
        self.login_line.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                                      "alternate-background-color: rgb(9, 21, 32); \n"
                                      "color: rgb(255, 255, 255); \n"
                                      "font: 50  10pt \"FreeMono Bold\";")
        self.password_line = QtWidgets.QLineEdit(self.groupBox)
        self.password_line.setGeometry(QtCore.QRect(10, 140, 271, 31))
        self.password_line.setInputMask("")
        self.password_line.setFrame(True)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setObjectName("lineEdit_36")
        self.password_line.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                                         "alternate-background-color: rgb(9, 21, 32); \n"
                                         "color: rgb(255, 255, 255); \n"
                                         "font: 50  10pt \"FreeMono Bold\";")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 111, 17))
        self.label_2.setObjectName("label_2")
        self.login_button = QtWidgets.QPushButton(self.groupBox)
        self.login_button.setGeometry(QtCore.QRect(160, 190, 121, 41))
        self.login_button.setObjectName("login_button")
        self.register_button = QtWidgets.QPushButton(self.groupBox)
        self.register_button.setGeometry(QtCore.QRect(10, 190, 121, 41))
        self.register_button.setObjectName("register_button")
        self.exit_button = QtWidgets.QPushButton(self.groupBox)
        self.exit_button.setGeometry(QtCore.QRect(160, 250, 121, 41))
        self.exit_button.setObjectName("exit_button")

        self.ui = QtWidgets.QMainWindow()

        self.retranslateUi()

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        self.exit_button.clicked.connect(self.close)

    def login(self):
        user = self.login_line.text().lower()
        password = self.password_line.text()

        try:
            if self.back.check_hash(user, password):
                self.back.login()
                self.ui = Ui_MainWindow(self.back)
                self.ui.show()
                self.close()
            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.showMessage('Wrong password. Try again.')
        except:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Username not found.')

    def register(self):
        self.resize(313, 500)
        reg = RegisterAccount(self, self.back)
        reg.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Login"))
        self.groupBox.setTitle(_translate("Form", " finolo"))
        self.label.setText(_translate("Form", "login"))
        self.label_2.setText(_translate("Form", "password"))
        self.login_button.setText(_translate("Form", "log in"))
        self.register_button.setText(_translate("Form", "register"))
        self.exit_button.setText(_translate("Form", "exit"))
