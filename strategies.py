from charts import MultiLineChart
from itertools import product
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd


class Strategies(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.strat_frame = QtWidgets.QFrame(self)
        self.strat_frame.setGeometry(QtCore.QRect(0, 0, 1001, 541))
        self.strat_frame.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                       "background-color: rgb(0, 170, 127);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 75 11pt \"Freemono Bold\";")
        self.strat_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.strat_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.strat_frame.setObjectName("strat_frame")

        self.strat_details = QtWidgets.QFrame(self.strat_frame)
        self.strat_details.setGeometry(QtCore.QRect(0, 61, 1001, 541))
        self.strat_details.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                         "background-color: rgb(0, 255, 127);\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "font: 75 11pt \"Freemono Bold\";")
        self.strat_details.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.strat_details.setFrameShadow(QtWidgets.QFrame.Raised)
        self.strat_details.setObjectName("strat_details")
        self.strat_gb = QtWidgets.QGroupBox(self.strat_frame)
        self.strat_gb.setGeometry(QtCore.QRect(20, 0, 300, 61))
        self.strat_gb.setObjectName("strat_gb")
        self.strat_select = QtWidgets.QPushButton(self.strat_gb)
        self.strat_select.setGeometry(QtCore.QRect(200, 30, 91, 21))
        self.strat_select.setObjectName("strat_select")
        self.strat_strategies = QtWidgets.QComboBox(self.strat_gb)
        self.strat_strategies.setGeometry(QtCore.QRect(20, 30, 160, 21))
        self.strat_strategies.setObjectName("strat_strategies")
        self.strat_strategies.addItem("")
        self.strat_strategies.addItem("")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Select strategy
        self.strat_test = Bollinger(self.strat_details, self.back)
        self.strat_select.clicked.connect(self.customize_strategy)

    def customize_strategy(self):
        if self.strat_strategies.currentText() == 'Bollinger Bands':
            self.strat_test.close()
            self.strat_test = Bollinger(self.strat_details, self.back)
            self.strat_test.show()
        elif self.strat_strategies.currentText() == 'Neural Network':
            self.strat_test.close()
            self.strat_test = DNN(self.strat_details, self.back)
            self.strat_test.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.strat_gb.setTitle(_translate("MainWindow", "  Select strategy"))
        self.strat_select.setText(_translate("MainWindow", "Select"))
        self.strat_strategies.setItemText(0, _translate("MainWindow", "Bollinger Bands"))
        self.strat_strategies.setItemText(1, _translate("MainWindow", "Neural Network"))


class Bollinger(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.boll_frame = QtWidgets.QFrame(self)
        self.boll_frame.setGeometry(QtCore.QRect(0, 0, 450, 541))
        self.boll_frame.setStyleSheet("alternate-background-color: rgb(0, 255, 127);\n"
                                      "background-color: rgb(0, 255, 127);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.boll_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.boll_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.boll_frame.setObjectName("boll_frame")
        self.boll_ticker_label = QtWidgets.QLabel(self, text='Choose ticker from the list:')
        self.boll_ticker_label.setGeometry(20, 10, 250, 20)
        self.boll_ticker_cb = QtWidgets.QComboBox(self.boll_frame)
        self.boll_ticker_cb.setGeometry(QtCore.QRect(20, 40, 80, 20))
        self.boll_ticker_cb.setObjectName("boll_ticker_cb")
        self.boll_ticker_cb.clear()
        self.boll_ticker_cb.addItems(self.back.W20['Ticker'])
        self.boll_sma_days_label = QtWidgets.QLabel(self, text='Enter number of days for Simple Moving Average:')
        self.boll_sma_days_label.setGeometry(20, 70, 500, 20)
        self.boll_sma_days = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_sma_days.setGeometry(QtCore.QRect(20, 100, 60, 20))
        self.boll_sma_days.setObjectName("boll_sma_days")
        rx_4_digits = QtCore.QRegExp("[0-9]{4}")
        val_4_digits = QtGui.QRegExpValidator(rx_4_digits)
        self.boll_sma_days.setValidator(val_4_digits)
        self.boll_std_qty_label = QtWidgets.QLabel(self, text='Enter distance of bands in standard deviation units:')
        self.boll_std_qty_label.setGeometry(20, 130, 500, 20)
        self.boll_std_qty = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_std_qty.setGeometry(QtCore.QRect(20, 160, 40, 20))
        self.boll_std_qty.setObjectName("boll_std_qty")
        rx_2_digits = QtCore.QRegExp("[0-9]{2}")
        val_2_digits = QtGui.QRegExpValidator(rx_2_digits)
        self.boll_std_qty.setValidator(val_2_digits)
        self.boll_start_label = QtWidgets.QLabel(self, text='Enter start date:')
        self.boll_start_label.setGeometry(20, 190, 200, 20)
        self.boll_start = QtWidgets.QDateEdit(self.boll_frame)
        self.boll_start.setGeometry(QtCore.QRect(20, 220, 115, 22))
        self.boll_start.setObjectName("boll_start")
        self.boll_start.setDateTime(self.back.prev_bus_day)
        self.boll_end_label = QtWidgets.QLabel(self, text='Enter end date:')
        self.boll_end_label.setGeometry(230, 190, 200, 20)
        self.boll_end = QtWidgets.QDateEdit(self.boll_frame)
        self.boll_end.setGeometry(QtCore.QRect(230, 220, 115, 22))
        self.boll_end.setObjectName("boll_end")
        self.boll_end.setDateTime(self.back.prev_bus_day)
        self.boll_cost_label = QtWidgets.QLabel(self, text='Enter percentage cost per trade:')
        self.boll_cost_label.setGeometry(20, 250, 500, 20)
        self.boll_cost = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_cost.setGeometry(QtCore.QRect(20, 280, 70, 20))
        self.boll_cost.setObjectName("boll_cost")
        self.boll_backtest = QtWidgets.QPushButton(self.boll_frame)
        self.boll_backtest.setGeometry(QtCore.QRect(20, 310, 91, 21))
        self.boll_backtest.setObjectName("boll_backtest")
        self.boll_backtest.setText("Backtest")

        self.boll_optimize_label = QtWidgets.QLabel(self, text='To optimize, enter following parameters:')
        self.boll_optimize_label.setGeometry(20, 340, 500, 20)

        self.boll_min_sma_label = QtWidgets.QLabel(self, text='Min SMA:')
        self.boll_min_sma_label.setGeometry(20, 370, 80, 20)

        self.boll_min_sma = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_min_sma.setGeometry(QtCore.QRect(110, 370, 40, 20))
        self.boll_min_sma.setObjectName("boll_min_sma")
        rx_3_digits = QtCore.QRegExp("[0-9]{3}")
        val_3_digits = QtGui.QRegExpValidator(rx_3_digits)
        self.boll_min_sma.setValidator(val_3_digits)

        self.boll_max_sma_label = QtWidgets.QLabel(self, text='Max SMA:')
        self.boll_max_sma_label.setGeometry(200, 370, 80, 20)

        self.boll_max_sma = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_max_sma.setGeometry(QtCore.QRect(290, 370, 40, 20))
        self.boll_max_sma.setObjectName("boll_max_sma")
        self.boll_max_sma.setValidator(val_3_digits)

        self.boll_min_std_label = QtWidgets.QLabel(self, text='Min std:')
        self.boll_min_std_label.setGeometry(20, 400, 80, 20)

        self.boll_min_std = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_min_std.setGeometry(QtCore.QRect(110, 400, 40, 20))
        self.boll_min_std.setObjectName("boll_min_std")
        self.boll_min_std.setValidator(val_2_digits)

        self.boll_max_std_label = QtWidgets.QLabel(self, text='Max std:')
        self.boll_max_std_label.setGeometry(200, 400, 80, 20)

        self.boll_max_std = QtWidgets.QLineEdit(self.boll_frame)
        self.boll_max_std.setGeometry(QtCore.QRect(290, 400, 40, 20))
        self.boll_max_std.setObjectName("boll_max_std")
        self.boll_max_std.setValidator(val_2_digits)

        self.boll_optimize = QtWidgets.QPushButton(self.boll_frame)
        self.boll_optimize.setGeometry(QtCore.QRect(20, 430, 91, 21))
        self.boll_optimize.setObjectName("boll_optimize")
        self.boll_optimize.setText("Optimize")

        self.ticker = None
        self.data = None
        self.SMA = None
        self.std_qty = None
        self.results = None
        self.cost = None
        self.results_overview = None
        self.boll_chart = QtWidgets.QWidget(self)
        self.boll_chart.setGeometry(QtCore.QRect(449, 0, 550, 460))
        self.boll_chart.setStyleSheet("alternate-background-color: rgb(0, 255, 127);\n"
                                      "background-color: rgb(0, 255, 127);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.boll_chart.setObjectName("boll_chart")

        self.boll_backtest.clicked.connect(self.all)
        self.boll_optimize.clicked.connect(self.optimize_parameters)

    def all(self):
        self.get_data()
        self.set_parameters2(int(self.boll_sma_days.text()), int(self.boll_std_qty.text()))
        self.test_strategy()
        self.plot_results()

    def get_data(self):
        """Imports the data from Quandl"""
        self.ticker = self.boll_ticker_cb.currentText()
        df = self.back.quandl_asset_df(self.back.quandl_from_ticker(self.ticker),
                                       start=self.boll_start.text(),
                                       end=self.boll_end.text())
        pd.set_option('display.max_columns', None)
        df = df['Close'].to_frame()
        df['returns'] = np.log(df / df.shift(1))
        self.data = df

    def set_parameters(self):
        """Updates parameters (SMA, dev) and the prepared dataset"""
        self.SMA = int(self.boll_sma_days.text())
        self.std_qty = int(self.boll_std_qty.text())
        self.data['SMA'] = self.data['Close'].rolling(self.SMA).mean()
        self.data['Lower'] = self.data['SMA'] - self.data['Close'].rolling(self.SMA).std() * self.std_qty
        self.data['Upper'] = self.data['SMA'] + self.data['Close'].rolling(self.SMA).std() * self.std_qty

    def set_parameters2(self, SMA, std_qty):
        """Updates parameters (SMA, dev) and the prepared dataset"""
        self.data['SMA'] = self.data['Close'].rolling(SMA).mean()
        self.data['Lower'] = self.data['SMA'] - self.data['Close'].rolling(SMA).std() * std_qty
        self.data['Upper'] = self.data['SMA'] + self.data['Close'].rolling(SMA).std() * std_qty

    def test_strategy(self):
        """Backtests the Bollinger Bands-based trading strategy"""
        self.cost = float(self.boll_cost.text())
        data = self.data.copy().dropna()
        data['distance'] = data['Close'] - data.SMA
        data['position'] = np.where(data['Close'] < data.Lower, 1, np.nan)
        data['position'] = np.where(data['Close'] > data.Upper, -1, data['position'])
        data['position'] = np.where(data.distance * data.distance.shift(1) < 0, 0, data['position'])
        data['position'] = data.position.ffill().fillna(0)
        data['strategy'] = data.position.shift(1) * data['returns']
        data.dropna(inplace=True)

        # determine the number of trades in each bar
        data['trades'] = data.position.diff().fillna(0).abs()

        # subtract transaction/trading costs from pre-cost return
        data.strategy = data.strategy - data.trades * self.cost

        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data

        perf = data['cstrategy'].iloc[-1]  # absolute performance of the strategy
        outperf = perf - data['creturns'].iloc[-1]  # out-/underperformance of strategy

        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        """ Plots the performance of the trading strategy and compares to 'buy and hold'"""
        chart = MultiLineChart(self.results[['creturns', 'cstrategy']], self.boll_chart)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(chart)
        self.boll_chart.setStyleSheet("alternate-background-color: rgb(0, 255, 127);\n"
                                      "background-color: rgb(255, 255, 255);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.boll_chart.setLayout(layout)

    def optimize_parameters(self):
        ''' Finds the optimal strategy (global maximum) given the Bollinger Bands parameter ranges.

        Parameters
        ----------
        SMA_range, dev_range: tuple
            tuples of the form (start, end, step size)
        '''
        SMA_range = range(int(self.boll_min_sma.text()), int(self.boll_max_sma.text()))
        std_range = range(int(self.boll_min_std.text()), int(self.boll_max_std.text()))

        combinations = list(product(SMA_range, std_range))

        # test all combinations
        results = []
        for comb in combinations:
            self.set_parameters2(comb[0], comb[1])
            results.append(self.test_strategy()[0])

        best_perf = np.max(results)  # best performance
        opt = combinations[np.argmax(results)]  # optimal parameters

        # run/set the optimal strategy
        self.set_parameters2(opt[0], opt[1])
        self.test_strategy()
        self.optimal_params(opt[0], opt[1])

        # create a df with many results
        many_results = pd.DataFrame(data=combinations, columns=["SMA", "dev"])
        many_results["performance"] = results
        self.results_overview = many_results

        return opt, best_perf

    @staticmethod
    def optimal_params(opt_sma, opt_std):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Optimal parameters')
        msg.setText(f'Optimal SMA: {opt_sma}, optimal std: {opt_std}.         ')
        msg.setIcon(QtWidgets.QMessageBox.Information)

        x = msg.exec()

    @staticmethod
    def regex_n_digits(n):
        reg = QtCore.QRegExp(f"[0-9]{int(n)}")
        return QtGui.QRegExpValidator(reg)


class DNN(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.dnn_frame = QtWidgets.QFrame(self)
        self.dnn_frame.setGeometry(QtCore.QRect(0, 0, 1001, 541))
        self.dnn_frame.setStyleSheet("alternate-background-color: rgb(0, 255, 127);\n"
                                     "background-color: rgb(0, 255, 127);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 75 11pt \"Freemono Bold\";")
        self.dnn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dnn_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.dnn_frame.setObjectName("dnn_frame")
        self.dnn_button = QtWidgets.QPushButton(self.dnn_frame)
        self.dnn_button.setGeometry(QtCore.QRect(200, 30, 200, 21))
        self.dnn_button.setObjectName("dnn_button")
