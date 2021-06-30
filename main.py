from app_login import LoginScreen
from PyQt5 import QtWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app2 = LoginScreen()
    app2.show()
    sys.exit(app.exec_())
