from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from PyQt5.QtWidgets import QLineEdit, QCompleter
import quandl
from charts import ChartWidget, LineChart
import os
import datetime
from PyQt5.QtWidgets import QMessageBox
from pandas._libs.tslibs.timestamps import Timestamp


class Portfolio(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.portf_frame = QtWidgets.QFrame(self)
        self.portf_frame.setGeometry(QtCore.QRect(0, 0, 1001, 541))
        self.portf_frame.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                       "background-color: rgb(0, 255, 127);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 75 11pt \"Freemono Bold\";")
        self.portf_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.portf_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.portf_frame.setObjectName("portf_frame")
        self.portf_left = QtWidgets.QFrame(self.portf_frame)
        self.portf_left.setGeometry(QtCore.QRect(0, 61, 160, 541))
        self.portf_left.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                      "background-color: rgb(123, 123, 127);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.portf_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.portf_left.setFrameShadow(QtWidgets.QFrame.Raised)

        self.portf_left.setObjectName("portf_left")
        self.portf_left_curr = QtWidgets.QComboBox(self.portf_left)
        self.portf_left_curr.setGeometry(QtCore.QRect(30, 10, 90, 25))
        self.portf_left_curr.setObjectName("portf_left_curr")

        self.portf_left_load = QtWidgets.QPushButton(self.portf_left)
        self.portf_left_load.setGeometry(QtCore.QRect(30, 50, 90, 25))
        self.portf_left_load.setObjectName("portf_left_load")

        self.portf_left_close = QtWidgets.QPushButton(self.portf_left)
        self.portf_left_close.setGeometry(QtCore.QRect(30, 90, 90, 25))
        self.portf_left_close.setObjectName("portf_left_close")

        self.portf_left_name = QtWidgets.QLineEdit(self.portf_left)
        self.portf_left_name.setGeometry(QtCore.QRect(30, 130, 90, 25))
        self.portf_left_name.setObjectName("portf_left_name")

        self.portf_left_create = QtWidgets.QPushButton(self.portf_left)
        self.portf_left_create.setGeometry(QtCore.QRect(30, 170, 90, 25))
        self.portf_left_create.setObjectName("portf_left_create")

        self.portf_chart = QtWidgets.QFrame(self.portf_frame)
        self.portf_chart.setGeometry(QtCore.QRect(160, 61, 840, 541))
        self.portf_chart.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                       "background-color: rgb(211, 12, 127);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 75 11pt \"Freemono Bold\";")
        self.portf_chart.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.portf_chart.setFrameShadow(QtWidgets.QFrame.Raised)
        self.portf_chart.setObjectName("portf_chart")
        self.portf_gb = QtWidgets.QGroupBox(self.portf_frame)
        self.portf_gb.setGeometry(QtCore.QRect(20, 0, 861, 61))
        self.portf_gb.setObjectName("portf_gb")
        self.portf_remove = QtWidgets.QPushButton(self.portf_gb)
        self.portf_remove.setGeometry(QtCore.QRect(570, 30, 91, 21))
        self.portf_remove.setObjectName("portf_remove")
        self.portf_add = QtWidgets.QPushButton(self.portf_gb)
        self.portf_add.setGeometry(QtCore.QRect(330, 30, 91, 21))
        self.portf_add.setObjectName("portf_add")
        self.portf_asset = QtWidgets.QLineEdit(self.portf_gb)
        self.portf_asset.setGeometry(QtCore.QRect(10, 31, 65, 20))
        self.portf_asset.setObjectName("portf_asset")
        self.portf_start = QtWidgets.QDateEdit(self.portf_gb)
        self.portf_start.setGeometry(QtCore.QRect(200, 30, 115, 22))
        self.portf_start.setObjectName("portf_start")
        self.portf_start.setDateTime(self.back.today)
        self.portf_end = QtWidgets.QDateEdit(self.portf_gb)
        self.portf_end.setGeometry(QtCore.QRect(440, 30, 115, 22))
        self.portf_end.setObjectName("portf_end")
        self.portf_end.setDateTime(self.back.today)
        self.portf_quantity = QtWidgets.QLineEdit(self.portf_gb)
        self.portf_quantity.setGeometry(QtCore.QRect(95, 30, 80, 20))
        self.portf_quantity.setObjectName("portf_quantity")
        rx = QtCore.QRegExp("[0-9]{7}")
        val = QtGui.QRegExpValidator(rx)
        self.portf_quantity.setValidator(val)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.test_df = pd.DataFrame(quandl.get('WSE/ALIOR', start_date = '2021-02-05', end_date = '2021-02-20', authtoken = self.back.api_key))
        self.dummy_df = self.back.quandl_asset_df('WSE/ALIOR')
        self.completer = QCompleter(self.back.wig20_tickers, self.portf_asset)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.portf_asset.setCompleter(self.completer)

        self.portf_add.clicked.connect(self.add_asset)
        self.portf_remove.clicked.connect(self.remove_asset)

                # zmieniłem żeby stworzyło folder jak nie ma
        if os.path.exists('portfolios'):
            self.portf_no_ext = [".".join(f.split(".")[:-1]) for f in
                                 os.listdir('portfolios/')]  # if os.path.isfile(f)]
        else:
            os.makedirs('portfolios')
            self.portf_no_ext = []

        self.portf_left_load.clicked.connect(self.load_portf)

        self.portf_left_create.clicked.connect(self.create_portf)

        self.portf_left_curr.clear()
        self.portf_left_curr.addItems(self.portf_no_ext)
        self.portf_left_curr.update()

        self.chartwidget = ChartWidget(self.portf_chart, self.back)

    def create_portf(self):
        if self.portf_left_name.text():
            new_portf = pd.DataFrame(index = self.dummy_df.index)
            new_portf.index = pd.to_datetime(new_portf.index)
            new_portf.index.name = 'Date'
            new_portf.to_csv(f'portfolios/{self.portf_left_name.text()}.csv')
            self.portf_left_curr.clear()
            self.update_portf_list()
            self.portf_left_curr.addItems(self.portf_no_ext)
            self.portf_left_curr.update()
            self.portf_left_curr.setCurrentText(self.portf_left_name.text())

    def add_asset(self):
        if not self.portf_quantity.text():
            self.portf_qty_popup()
        else:
            qty = int(self.portf_quantity.text())
            ticker = self.portf_asset.text()
            portf = self.portf_left_curr.currentText()
            asset = self.back.quandl_asset_df(self.back.quandl_from_ticker(ticker), self.portf_start.text())
            asset_close = pd.DataFrame(asset['Close'])
            asset_close.columns = [ticker]
            portf_data = pd.read_csv(f'portfolios/{portf}.csv', index_col = 'Date')
            portf_data.index = pd.to_datetime(portf_data.index)
            portf_data = pd.concat([portf_data, asset_close], axis=1)
            portf_data[f'{ticker}_qty'] = qty
            portf_data[f'{ticker}_total'] = asset_close * qty
            portf_data.fillna(0, inplace = True)
            portf_data = portf_data.sort_index()
            portf_data.to_csv(f'portfolios/{portf}.csv')
            self.portf_success_add(ticker, qty, portf)

    def remove_asset(self):
        if not self.portf_quantity.text():
            self.portf_qty_popup()
        else:
            portf = self.portf_left_curr.currentText()
            df = pd.read_csv(f'portfolios/{portf}.csv', index_col='Date')
            df.index = pd.to_datetime(df.index)
            ticker = self.portf_asset.text()
            qty = int(self.portf_quantity.text())
            date = pd.to_datetime(self.portf_end.text())
            if ticker not in df.columns:
                print('Asset not in Portfolio')
            else:
                df.loc[date:, f'{ticker}_qty'] = df.loc[date:, f'{ticker}_qty'] - qty
                df.loc[date:, f'{ticker}_total'] = df.loc[date:, f'{ticker}'] * df.loc[date:, f'{ticker}_qty']
                df.to_csv(f'portfolios/{portf}.csv')
            self.portf_success_remove(ticker, qty, portf)

    def update_portf_list(self):
        self.portf_no_ext = [".".join(f.split(".")[:-1]) for f in os.listdir('portfolios/')]

    def load_portf(self):
        df = pd.read_csv(f'portfolios/{self.portf_left_curr.currentText()}.csv', index_col='Date').copy()
        df.index = pd.to_datetime(df.index)
        self.update_portf(df)
        df_total = df[[col for col in df.columns if col.endswith('_total')]].sum(axis=1)
        df_total.name = self.portf_left_curr.currentText()
        self.chartwidget.line_chart(df_total)
        # self.chartwidget.line_chart(df[[col for col in df.columns if col.endswith('_total')]].sum(axis=1))

    def update_portf(self, df):
        up_portf = pd.DataFrame(df.iloc[-1])
        up_portf = up_portf.T
        date = Timestamp(up_portf.index.values[0]) #datetime.datetime.strptime(up_portf.index.values[0], "%Y-%m-%d") #+ datetime.timedelta(days=1)
        date = date.to_pydatetime()
        date = date + datetime.timedelta(days=1)
        weekend = set([5, 6])
        if not up_portf.index == [self.back.prev_bus_day]:
            while date <= self.back.prev_bus_day:
                if date.weekday() not in weekend:
                    up_portf.index = [date]
                    for ticker in up_portf.columns.values:
                        try:
                            if ticker in self.back.wig20_tickers:
                                up_portf[ticker] = self.back.quandl_asset_df(self.back.quandl_from_ticker(ticker), start=date, end=date)['Close'].values[0]
                                up_portf[f'{ticker}_total'] = up_portf[ticker] * up_portf[f'{ticker}_qty']
                        except IndexError:
                            pass
                df = df.append(up_portf)
                date += datetime.timedelta(days=1)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        df.index.name = 'Date'
        df.to_csv(f'portfolios/{self.portf_left_curr.currentText()}.csv')

    def portf_qty_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle('Error: Invalid quantity')
        msg.setText('Please fill in quantity         ')
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec()

    def portf_success_add(self, ticker, qty, portf):
        msg = QMessageBox()
        msg.setWindowTitle('Success')
        msg.setText(f'{qty} shares of {ticker} were added to {portf}.         ')
        msg.setIcon(QMessageBox.Information)

        x = msg.exec()

    def portf_success_remove(self, ticker, qty, portf):
        msg = QMessageBox()
        msg.setWindowTitle('Success')
        msg.setText(f'{qty} shares of {ticker} were removed from {portf}.         ')
        msg.setIcon(QMessageBox.Information)

        x = msg.exec()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.portf_gb.setTitle(_translate("MainWindow", "  Asset     Quantity        Start date                           End date"))
        self.portf_remove.setText(_translate("MainWindow", "Remove"))
        self.portf_add.setText(_translate("MainWindow", "Add"))
        self.portf_left_load.setText(_translate("MainWindow", "Load"))
        self.portf_left_close.setText(_translate("MainWindow", "Close"))
        self.portf_left_create.setText(_translate("MainWindow", "Create"))
