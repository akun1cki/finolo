from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from portf import Portfolio
from strategies import Strategies
from charts import OHLCChart, ChartWidget
from pandasmodel import PandasModel
from signals import Signals


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, back):
        super().__init__()
        self.back = back
        self.setObjectName("MainWindow")
        self.resize(1136, 701)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(150, 0, 991, 571))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.main = QtWidgets.QTabWidget(self.frame_2)
        self.main.setGeometry(QtCore.QRect(-10, 0, 1011, 571))
        self.main.setStyleSheet("background-color: rgb(0, 170, 127);\n"
                                "font: 12pt \"MV Boli\";")
        self.main.setObjectName("main")
        # CHARTS
        self.chart = QtWidgets.QWidget()
        self.chart.setObjectName("chart")
        self.chart_gb1 = QtWidgets.QGroupBox(self.chart)
        self.chart_gb1.setGeometry(QtCore.QRect(10, 0, 411, 61))
        self.chart_gb1.setObjectName("chart_gb1")
        self.chart_stock = QtWidgets.QComboBox(self.chart_gb1)
        self.chart_stock.setGeometry(QtCore.QRect(10, 33, 79, 25))
        self.chart_stock.setObjectName("chart_stock")
        self.chart_interval = QtWidgets.QComboBox(self.chart_gb1)
        self.chart_interval.setGeometry(QtCore.QRect(110, 33, 73, 25))
        self.chart_interval.setObjectName("chart_interval")
        self.chart_show = QtWidgets.QPushButton(self.chart_gb1)
        self.chart_show.setGeometry(QtCore.QRect(200, 33, 81, 25))
        self.chart_show.setObjectName("chart_show")
        self.chart_close = QtWidgets.QPushButton(self.chart_gb1)
        self.chart_close.setGeometry(QtCore.QRect(300, 33, 81, 25))
        self.chart_close.setObjectName("chart_close")
        self.chart_gb2 = QtWidgets.QGroupBox(self.chart)
        self.chart_gb2.setGeometry(QtCore.QRect(790, 0, 201, 61))
        self.chart_gb2.setObjectName("chart_gb2")
        self.chart_indicators = QtWidgets.QComboBox(self.chart_gb2)
        self.chart_indicators.setGeometry(QtCore.QRect(20, 33, 171, 25))
        self.chart_indicators.setObjectName("chart_indicators")
        self.chart_indicators.addItem("")
        self.chart_indicators.addItem("")
        self.chart_indicators.addItem("")
        self.chart_indicators.addItem("")
        self.chart_indicators.addItem("")
        self.chart_indicators.addItem("")
        self.chart_chart2 = QtWidgets.QFrame(self.chart)
        self.chart_chart2.setGeometry(QtCore.QRect(0, 70, 991, 461))
        self.chart_chart2.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.chart_chart2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chart_chart2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chart_chart2.setObjectName("chart_chart2")
        self.main.addTab(self.chart, "")
        self.portf_tab = QtWidgets.QWidget()
        self.portf_tab.setObjectName("portf_tab")
        self.main.addTab(self.portf_tab, "")
        self.strat_tab = QtWidgets.QWidget()
        self.strat_tab.setObjectName("strat_tab")
        self.main.addTab(self.strat_tab, "")
        self.signal_tab = QtWidgets.QWidget()
        self.signal_tab.setObjectName("signal_tab")
        self.main.addTab(self.signal_tab, "")
        self.ml_tab = QtWidgets.QWidget()
        self.ml_tab.setStyleSheet("")
        self.ml_tab.setObjectName("ml_tab")
        self.main.addTab(self.ml_tab, "")
        self.news = QtWidgets.QFrame(self.centralwidget)
        self.news.setGeometry(QtCore.QRect(150, 560, 991, 121))
        self.news.setStyleSheet("background-color: rgb(255, 181, 78);")
        self.news.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.news.setFrameShadow(QtWidgets.QFrame.Raised)
        self.news.setObjectName("news")
        # LEFT PANEL
        self.left_panel = QtWidgets.QFrame(self.centralwidget)
        self.left_panel.setGeometry(QtCore.QRect(0, 0, 150, 681))
        self.left_panel.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.left_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_panel.setObjectName("frame")
        self.comboBox = QtWidgets.QComboBox(self.left_panel)
        self.comboBox.setGeometry(QtCore.QRect(0, 0, 150, 31))
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.left_panel_load = QtWidgets.QPushButton(self.left_panel)
        self.left_panel_load.setGeometry(QtCore.QRect(0, 31, 150, 35))
        self.left_panel_load.setObjectName("left_panel_load")
        self.price_table = QtWidgets.QTableView(self.left_panel)
        self.price_table.setGeometry(QtCore.QRect(0, 66, 150, 590))
        self.price_table.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.price_table.setObjectName("price_table")
        self.price_table.verticalHeader().setDefaultSectionSize(29)
        self.price_table.horizontalHeader().hide()
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuMore = QtWidgets.QMenu(self.menubar)
        self.menuMore.setObjectName("menuMore")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMore.menuAction())

        self.retranslateUi(self)
        self.main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        # CHARTS
        # add items to stocks list in charts section
        self.chart_stock.clear()
        self.chart_stock.addItems(self.back.W20['Ticker'])

        # instantiate chart object
        self.chartwidget = ChartWidget(self.chart_chart2, self.back)

        # show and close chart when button clicked
        self.chart_show.clicked.connect(self.ohlc_chart)
        self.chart_close.clicked.connect(self.close_chart_tab)

        # PORTFOLIO
        self.portfolio = Portfolio(self.portf_tab, self.back)

        # SIGNALS
        self.signals = Signals(self.signal_tab, self.back)

        # LEFT PANEL
        self.left_panel_load.clicked.connect(self.load_left_prices)

        # STRATEGIES
        self.strategies = Strategies(self.strat_tab, self.back)

    def ohlc_chart(self):
        asset_quandl = self.back.quandl_from_ticker(self.chart_stock.currentText())
        df = self.back.quandl_asset_df(asset_quandl, '2020-02-01', self.back.today)
        df = df.reset_index()
        df.name = self.chart_stock.currentText()
        if not self.chart_indicators.currentText():
            self.chartwidget.ohlc_chart(df)
        elif self.chart_indicators.currentText() == 'MACD':
            self.chartwidget.line_chart(df)
            # self.chartwidget.add_indicator(data)
        elif self.chart_indicators.currentText() == 'Bollinger Bands':
            self.chartwidget.add_bollinger(df)
        elif self.chart_indicators.currentText() == 'Ichimoku':
            self.chartwidget.add_ichomoku(df)

    def close_chart_tab(self):
        self.chartwidget.chart_tabs.removeTab(self.chartwidget.chart_tabs.currentIndex())

    def load_left_prices_old(self):
        for row in range(0, 20):
            values = self.back.prev_day_data[row].values()
            values_list = list(values)
            self.price_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{values_list[0]} | {values_list[1]} | {values_list[2]}%'))
            if values_list[2] >= 0:
                self.price_table.item(row, 0).setBackground(Qt.green)
            else:
                self.price_table.item(row, 0).setBackground(Qt.red)

    def load_left_prices(self):
        model = PandasModel(self.back.df)
        self.price_table.setModel(model)
        self.set_col_width()
        self.price_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def set_col_width(self):
        self.price_table.setColumnWidth(0, 60)
        self.price_table.setColumnWidth(1, 70)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chart_gb1.setTitle(_translate("MainWindow", "Stock     Interval"))
        self.chart_show.setText(_translate("MainWindow", "Show"))
        self.chart_close.setText(_translate("MainWindow", "Close"))
        self.chart_gb2.setTitle(_translate("MainWindow", "Indicators"))
        self.chart_indicators.setItemText(0, _translate("MainWindow", ""))
        self.chart_indicators.setItemText(1, _translate("MainWindow", "Bollinger Bands"))
        self.chart_indicators.setItemText(2, _translate("MainWindow", "MACD"))
        self.chart_indicators.setItemText(3, _translate("MainWindow", "Stochastic"))
        self.chart_indicators.setItemText(4, _translate("MainWindow", "RSI"))
        self.chart_indicators.setItemText(5, _translate("MainWindow", "Ichimoku"))
        self.main.setTabText(self.main.indexOf(self.chart), _translate("MainWindow", "Charts"))
        self.main.setTabText(self.main.indexOf(self.portf_tab), _translate("MainWindow", "Portfolio"))
        self.main.setTabText(self.main.indexOf(self.strat_tab), _translate("MainWindow", "Strategies"))
        self.main.setTabText(self.main.indexOf(self.signal_tab), _translate("MainWindow", "Signals"))
        self.main.setTabText(self.main.indexOf(self.ml_tab), _translate("MainWindow", "Machine learning"))
        self.comboBox.setItemText(0, _translate("MainWindow", "WIG20"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Mains"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Watch list"))
        self.left_panel_load.setText(_translate("MainWindow", "Load"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuMore.setTitle(_translate("MainWindow", "More"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
