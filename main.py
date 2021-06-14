from PyQt5 import QtCore, QtGui, QtWidgets
from front_v4 import Ui_MainWindow
from app_login import LoginScreen

if __name__ == "__main__":
    import sys
    # Launch up without loging in
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
