from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from PyQt5.QtWidgets import QDialog
import json
import os
from pandas.tseries.offsets import BDay
from pandasmodel import PandasModel
from PyQt5.QtWidgets import QMessageBox
import csv
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class QDialogSignal(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 500, 500)
        self.setWindowTitle('Signal Criteria')
        self.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                       "background-color: rgb(211, 222, 127);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 75 11pt \"Freemono Bold\";")
        self.label_signal_name = QtWidgets.QLabel(self, text = 'Signal name:')
        self.label_signal_name.setGeometry(10, 10, 110, 20)
        self.signal_name = QtWidgets.QLineEdit(self)
        self.signal_name.setGeometry(QtCore.QRect(120, 10, 65, 20))
        self.signal_name.setObjectName("signal_name")
        self.gb_ma = QtWidgets.QGroupBox(self)
        self.gb_ma.setGeometry(QtCore.QRect(10, 40, 450, 230))
        self.gb_ma.setObjectName("gb1")
        self.gb_ma.setTitle('Select signal criteria based on MA')
        self.label_above_below = QtWidgets.QLabel(self.gb_ma, text = 'Above or below MA:')
        self.label_above_below.setGeometry(10, 40, 200, 20)
        self.above_below = QtWidgets.QComboBox(self.gb_ma)
        self.above_below.setGeometry(QtCore.QRect(10, 70, 79, 20))
        self.above_below.setObjectName("chart_stock")
        self.above_below.clear()
        self.above_below.addItems(['Above', 'Below'])
        self.label_days_ma = QtWidgets.QLabel(self.gb_ma, text='How many days in MA:')
        self.label_days_ma.setGeometry(10, 100, 200, 20)
        rx = QtCore.QRegExp("[0-9]{4}")
        val = QtGui.QRegExpValidator(rx)
        self.days_ma = QtWidgets.QLineEdit(self.gb_ma)
        self.days_ma.setGeometry(QtCore.QRect(10, 130, 65, 20))
        self.days_ma.setObjectName("pct_of_ma")
        self.days_ma.setValidator(val)
        self.label_pct_ma = QtWidgets.QLabel(self.gb_ma, text='Percentage of MA:')
        self.label_pct_ma.setGeometry(10, 160, 200, 20)
        self.pct_of_ma = QtWidgets.QLineEdit(self.gb_ma)
        self.pct_of_ma.setGeometry(QtCore.QRect(10, 190, 65, 20))
        self.pct_of_ma.setObjectName("pct_of_ma")
        self.pct_of_ma.setValidator(val)

        self.submit = QtWidgets.QPushButton(self)
        self.submit.setGeometry(QtCore.QRect(10, 300, 90, 30))
        self.submit.setObjectName("submit")
        self.submit.clicked.connect(self.close)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.submit.setText(_translate("MainWindow", "Submit"))


class Signals(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.signal_frame = QtWidgets.QFrame(self)
        self.signal_frame.setGeometry(QtCore.QRect(0, 0, 1001, 541))
        self.signal_frame.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                        "background-color: rgb(0, 255, 127);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 75 11pt \"Freemono Bold\";")
        self.signal_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signal_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.signal_frame.setObjectName("signal_frame")
        self.signal_table = QtWidgets.QTableView(self.signal_frame)
        self.signal_table.setGeometry(QtCore.QRect(0, 61, 1001, 541))
        self.signal_table.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                        "background-color: rgb(1, 222, 127);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 75 11pt \"Freemono Bold\";")
        self.signal_table.setObjectName("signal_table")
        self.signal_table.horizontalHeader().hide()
        self.signal_table.verticalHeader().hide()
        self.signal_create = QtWidgets.QPushButton(self.signal_frame)
        self.signal_create.setGeometry(QtCore.QRect(30, 15, 90, 30))
        self.signal_create.setObjectName("signal_create")
        self.signal_list = QtWidgets.QComboBox(self.signal_frame)
        self.signal_list.setGeometry(QtCore.QRect(150, 15, 90, 30))
        self.signal_list.setObjectName("signal_list")
        self.signal_send = QtWidgets.QPushButton(self.signal_frame)
        self.signal_send.setGeometry(QtCore.QRect(260, 15, 90, 30))
        self.signal_send.setObjectName("signal_send")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.dummy_df = self.back.quandl_asset_df('WSE/ALIOR')
        
        # same here
        if os.path.exists('signals'):
            self.signal_no_ext = [".".join(f.split(".")[:-1]) for f in os.listdir('signals/')]
        else:
            os.makedirs('signals')
            self.signal_no_ext = []

        # Update signal list
        self.signal_list.clear()
        self.signal_list.addItems(self.signal_no_ext)
        self.signal_list.update()

        # Create signal
        self.signal_create.clicked.connect(self.create_signal)

        # Send signals
        self.signal_send.clicked.connect(self.send_signal)

    def create_signal(self):
        print('Create signal')
        dlg = QDialogSignal()
        QtCore.QTimer.singleShot(
            0,
            lambda: dlg.move(
                self.mapToGlobal(self.rect().center() - dlg.rect().center())
            ),
        )
        dlg.exec()

        ma_signal = {'Above/Below': dlg.above_below.currentText(), 'Days of MA': dlg.days_ma.text(), 'Percentage of MA': dlg.pct_of_ma.text()}

        with open(f'signals/{dlg.signal_name.text()}.json', 'w') as new_signal:
            json.dump(ma_signal, new_signal)

        self.signal_list.clear()
        self.update_signal_list()
        self.signal_list.addItems(self.signal_no_ext)
        self.signal_list.update()
        self.signal_list.setCurrentText(dlg.signal_name.text())

        self.signal_success_add(dlg.signal_name.text())

    def send_signal(self):
        signal_path = f'signals/{self.signal_list.currentText()}.json'
        signal_stocks = []
        with open (signal_path, 'r') as signal:
            signal_criteria = json.load(signal)
            start_date = pd.to_datetime(self.back.today - BDay(int(signal_criteria['Days of MA']))).date()
            pct_of_ma = int(signal_criteria['Percentage of MA']) / 100
            for quandl in self.back.wig20_stocks:
                df = self.back.quandl_asset_df(quandl, start_date) #['Close']
                if signal_criteria['Above/Below'] == 'Above':
                    if df['Close'].values[-1] > pct_of_ma * df['Close'].mean():
                        signal_stocks.append(f'  {self.back.ticker_from_quandl(quandl)} is {round((df["Close"].values[-1] / df["Close"].mean()) * 100, 2)} percent above {signal_criteria["Days of MA"]} MA.')
                else:
                    if df['Close'].values[-1] < pct_of_ma * df['Close'].mean():
                        signal_stocks.append(f'  {self.back.ticker_from_quandl(quandl)} is {round((df["Close"].values[-1] / df["Close"].mean()) * 100, 2)} percent below {signal_criteria["Days of MA"]} MA.')

        result_df = pd.DataFrame(signal_stocks)
        result_df.to_csv('signal_email.csv')

        model = PandasModel(result_df)
        self.signal_table.setModel(model)
        self.signal_table.setColumnWidth(0, 500)

        self.send_email('signal_email.csv')

    def signal_success_add(self, signal_name):
        msg = QMessageBox()
        msg.setWindowTitle('Success')
        msg.setText(f'You have successfully created {signal_name} signal.         ')
        msg.setIcon(QMessageBox.Information)

        x = msg.exec()

    def update_signal_list(self):
        self.signal_no_ext = [".".join(f.split(".")[:-1]) for f in os.listdir('signals/')]

    @staticmethod
    def send_email(file_path):
        me = 'jacek.dzarnecki@gmail.com'
        password = '****'
        server = 'smtp.gmail.com:587'
        you = '****'

        text = """
        Hello,

        Here is your data:

        {table}

        Regards,

        FinOlo"""

        html = """
        <html><body><p>Hello,</p>
        <p>Here is your data:</p>
        {table}
        <p>Regards,</p>
        <p>FinOlo</p>
        </body></html>
        """

        with open(file_path) as input_file:
            reader = csv.reader(input_file)
            data = list(reader)

        text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
        html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

        message = MIMEMultipart(
            "alternative", None, [MIMEText(text), MIMEText(html, 'html')])

        message['Subject'] = "Your data"
        message['From'] = me
        message['To'] = you
        server = smtplib.SMTP(server)
        server.ehlo()
        server.starttls()
        server.login(me, password)
        server.sendmail(me, you, message.as_string())
        server.quit()
        
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.signal_create.setText(_translate("MainWindow", "Create"))
        self.signal_send.setText(_translate("MainWindow", "Send"))
