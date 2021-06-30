import finplot as fplt
from PyQt5 import QtCore, QtWidgets
from datetime import timedelta
import pandas as pd
import numpy as np


class ChartWidget(QtWidgets.QWidget):
    def __init__(self, parent, back):
        super().__init__(parent)
        self.back = back
        self.setGeometry(QtCore.QRect(0, 0, 1000, 471))
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1222, 471))
        self.frame.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                 "background-color: rgb(0, 255, 127);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"Freemono Bold\";")
        self.chart_tabs = QtWidgets.QTabWidget(self.frame) # try changing colors here
        self.chart_tabs.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                      "background-color: rgb(0, 255, 127);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.chart_tabs.setGeometry(QtCore.QRect(0, 0, 1000, 471))
        self.chart_tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.chart_tabs.setMovable(True)

    def ohlc_chart(self, df):
        tab = OHLCChart(df, self)
        self.chart_tabs.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                      "background-color: rgb(255, 255, 255);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.chart_tabs.addTab(tab, df.name)
        self.chart_tabs.setCurrentIndex(self.chart_tabs.currentIndex()+1)

    def add_indicator(self, df):
        ind = OHLCChart(df, self)
        ind.indicator()
        self.chart_tabs.addTab(ind, df.name)
        self.chart_tabs.setCurrentIndex(self.chart_tabs.currentIndex() + 1)

    def add_bollinger(self, df):
        bol = OHLCChart(df, self)
        bol.bollinger()
        self.chart_tabs.addTab(bol, df.name)
        self.chart_tabs.setCurrentIndex(self.chart_tabs.currentIndex() + 1)

    def line_chart(self, df):
        lc = LineChart(df, self)
        self.chart_tabs.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                      "background-color: rgb(255, 255, 255);\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "font: 75 11pt \"Freemono Bold\";")
        self.chart_tabs.setGeometry(QtCore.QRect(0, 0, 850, 470))
        self.chart_tabs.addTab(lc, df.name)
        self.chart_tabs.setCurrentIndex(self.chart_tabs.currentIndex() + 1)

    def add_ichomoku(self, df):
        ichimoku = OHLCChart(df, self)
        ichimoku.ichimoku()
        self.chart_tabs.addTab(ichimoku, df.name)
        self.chart_tabs.setCurrentIndex(self.chart_tabs.currentIndex() + 1)


class OHLCChart(QtWidgets.QWidget):
    def __init__(self, df, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(-50, -50, 903, 460))
        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(903, 460)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graph)
        self.setStyleSheet("background-color: rgb(5, 16, 36);\n"
                           "color: rgb(255, 255, 255);\n"
                           "border-color: rgb(0, 0, 0);\n")

        self.df = df.copy()
        self.df['Date'] = pd.to_datetime(self.df['Date']).astype('int64')  # use finplot's internal representation, which is ns

        # self.set_colors()

        self.ax = fplt.create_plot(init_zoom_periods = 100, maximize = True, rows = 1)

        # Price on right side
        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        fplt.candle_bull_color = fplt.candle_bear_color = '#000'
        fplt.volume_bull_color = fplt.volume_bear_color = '#333'
        fplt.candle_bull_body_color = fplt.volume_bull_body_color = '#fff'

        # OHLC chart
        fplt.candlestick_ochl(self.df[['Date', 'Open', 'Close', 'High', 'Low']], ax = self.ax)

        self.hover_label = fplt.add_legend('', ax = self.ax)
        self.ax.showGrid(x = True, y = True, alpha = 0.7)
        fplt.side_margin = 0
        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]

        # Volume
        self.axo = self.ax.overlay()
        self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)

        fplt.volume_ocv(self.df[['Date', 'Open', 'Close', 'Volume']], ax = self.axo)
        fplt.plot(self.df.Volume.ewm(span = 24).mean(), ax = self.axo, color = 1)

        # Crosshair
        fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')
        fplt.add_crosshair_info(self.update_crosshair_info, ax=self.ax)

        fplt.show(qt_exec=False)

    def update_crosshair_info(self, x, y, xtext, ytext):
        ytext = '%s (Close%+.2f)' % (ytext, (y - self.df.iloc[x].Close))
        return xtext, ytext

    def update_legend(self, x, y):
        row = self.df.loc[self.df['Date'] == x]
        # row = self.df.loc[x/1000000]
        fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open < row.Close).all() else 'a00')
        text = 'O %s H %s L %s C %s Vol %s' % (fmt, fmt, fmt, fmt, fmt)
        self.hover_label.setText(text % (row.Open, row.High, row.Low, row.Close, row.Volume))

    def set_colors(self):
        fplt.background = '#000e19'
        fplt.foreground = '#EFFBF8'
        fplt.cross_hair_color = '#EFFBF8'
        fplt.candle_bear_color = '#bd0000'
        fplt.candle_bull_body_color = '#000f14'
        fplt.candle_bear_body_color = '#ffffff'

    def indicator(self):
        ax2 = fplt.create_plot(init_zoom_periods = 10, maximize = False)
        self.graph.axs.append(ax2)
        # self.layout.addWidget(ax2.vb.win, 0, 0, 3, 2)

        macd = self.df.Close.ewm(span = 12).mean() - self.df.Close.ewm(span = 26).mean()
        signal = macd.ewm(span = 9).mean()
        self.df['macd_diff'] = macd - signal
        fplt.volume_ocv(self.df[['Date', 'Open', 'Close', 'macd_diff']], ax = ax2,
                        colorfunc=fplt.strength_colorfilter)
        fplt.plot(macd, ax = ax2, legend ='MACD')
        fplt.plot(signal, ax = ax2, legend ='Signal')

        fplt.show(qt_exec=False)

    def bollinger(self):
        mean_30 = self.df['Close'].rolling(window=30).mean()
        upper = mean_30 + 2 * self.df['Close'].rolling(window=30).std()
        lower = mean_30 - 2 * self.df['Close'].rolling(window=30).std()
        fplt.plot(upper, ax = self.ax, color = '#C52310', width = 4)
        fplt.plot(lower, ax = self.ax, color = '#18D023', width = 4)

        fplt.show(qt_exec=False)

    def ichimoku(self):
        high_9 = self.df['High'].rolling(window=9).max()
        low_9 = self.df['Low'].rolling(window=9).min()
        self.df['tenkan_sen'] = (high_9 + low_9) / 2

        high_26 = self.df['High'].rolling(window=26).max()
        low_26 = self.df['Low'].rolling(window=26).min()
        self.df['kijun_sen'] = (high_26 + low_26) / 2

        # this is to extend the 'df' in future for 26 days
        # the 'df' here is numerical indexed df
        last_index = self.df.iloc[-1:].index[0]
        last_date = self.df['Date'].iloc[-1].date()
        for i in range(26):
            self.df.loc[last_index + 1 + i, 'Date'] = last_date + timedelta(days=i)

        self.df['senkou_span_a'] = ((self.df['tenkan_sen'] + self.df['kijun_sen']) / 2).shift(26)

        high_52 = self.df['High'].rolling(window=52).max()
        low_52 = self.df['Low'].rolling(window=52).min()
        self.df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(26)

        # most charting softwares dont plot this line
        self.df['chikou_span'] = self.df['Close'].shift(-22)  # sometimes -26

        #
        # self.df.index = self.df.index.date()
        self.df['Date'] = self.df['Date'].apply(lambda x: np.datetime64(x))              #(Timestamp(x)).to_pydatetime().date())
        self.df.index = self.df['Date']

        self.df.fillna(0, inplace = True)
        print(self.df)
        print(self.df.tail(35))
        self.df.drop(self.df.tail(35).index, inplace = True, axis = 0)
        print(self.df)
        print(self.df.index.dtype)

        tmp = self.df[['senkou_span_a', 'senkou_span_b', 'kijun_sen', 'tenkan_sen']].tail(300) # 'Close',
        # print(tmp)
        fplt.plot(tmp, ax = self.ax)
        fplt.fill_between(tmp.index, tmp.senkou_span_a, tmp.senkou_span_b)
        fplt.show()
        # a1 = tmp.plot(figsize=(15, 10))
        # a1.fill_between(tmp.index, tmp.senkou_span_a, tmp.senkou_span_b)


class LineChart(QtWidgets.QWidget):
    def __init__(self, df, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 10, 200, 481))

        self.df = df.copy()

        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(900, 500)
        self.layout = QtWidgets.QGridLayout(self)
        # self.layout.addWidget(self.graph)

        self.ax = fplt.create_plot(init_zoom_periods = 100, maximize = True, rows = 1)

        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x = True, y = True, alpha = 0.3)

        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]

        fplt.side_margin = 0
        fplt.y_label_width = 0

        fplt.plot(self.df, ax = self.ax)
        fplt.show()

        # self.hover_label = fplt.add_legend('', ax = self.ax)

        # self.axo = self.ax.overlay()

        # fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')
        # fplt.add_crosshair_info(self.update_crosshair_info, ax=self.ax)

        # self.graph.axs = [self.ax]
        # self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)


class LineChart_mpl(QtWidgets.QWidget):
    def __init__(self, df, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 10, 200, 481))

        self.df = df.copy()

        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(765, 500)
        self.layout = QtWidgets.QGridLayout(self)

        self.ax = fplt.create_plot(init_zoom_periods = 100, maximize = True, rows = 1)

        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x = True, y = True, alpha = 0.3)

        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]

        fplt.side_margin = 0
        fplt.y_label_width = 0

        fplt.plot(self.df, ax = self.ax)
        fplt.show()


class MultiLineChart(QtWidgets.QWidget):
    def __init__(self, df, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 10, 450, 200))

        self.lines = dict()
        self.log_scale = True
        self.df = df.copy()
        self.log_df = None

        #self.df.set_index('Date', inplace=True)
        self.df.index = pd.to_datetime(self.df.index).astype('int64')

        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(450, 200)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graph)
        # self.set_colors()

        self.ax = fplt.create_plot(init_zoom_periods=100, maximize=True, rows=1)
        #fplt.plot(self.df, ax=self.ax)

        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x=True, y=True, alpha=0.3)
        self.hover_label = fplt.add_legend('', ax=self.ax)
        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]

        fplt.side_margin = 0
        fplt.y_label_width = 60

        fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')
        #fplt.add_crosshair_info(self.update_crosshair_info, ax=self.ax)

        for col in self.df.columns:
            fplt.plot(self.df[col], ax=self.ax)

        self.graph.axs = [self.ax]
        self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)
        fplt.show(qt_exec=False)

    def update_legend(self, x, y):
        row = self.df.loc[x]

        col0 = self.df.columns[0]
        col1 = self.df.columns[1]

        fmt1 = '<span style="color:#%s">%%s</span>' % '0052ff'
        fmt2 = '<span style="color:#%s">%%.2f</span>' % '0052ff'
        fmt3 = '<span style="color:#%s">%%s</span>' % 'c48800'
        fmt4 = '<span style="color:#%s">%%.2f</span>' % 'c48800'

        text = '%s: %s %s: %s' % (fmt1, fmt2, fmt3, fmt4)

        self.hover_label.setText(text % (col0, row[col0].round(2), col1, row[col1].round(2)))
