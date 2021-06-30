import quandl
import numpy as np
import pandas as pd
import datetime
from datetime import date
from pandas.tseries.offsets import BDay
from db import Database
from hashlib import sha3_512


class Backend(object):
    def __init__(self):
        self.front = None
        self.db = Database()
        self.today = datetime.datetime.today()
        self.today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.prev_bus_day = pd.to_datetime(self.today - BDay(1)) #.strftime('%Y-%m-%d')
        self.prev_bus_day2 = pd.to_datetime(self.today - BDay(2))

        self.api_key = 'BJVHzuYs1s6oVDuyEukv'

        self.wig20 = 'WSE/WIG20'
        self.wig20_stocks = 'WSE/ALIOR WSE/ALLEGRO WSE/ASSECOPOL WSE/CCC WSE/CDPROJEKT WSE/CYFRPLSAT WSE/DINOPL WSE/JSW WSE/KGHM WSE/LOTOS WSE/LPP WSE/ORANGEPL ' \
                            'WSE/PEKAO WSE/PGE WSE/PGNIG WSE/PKNORLEN WSE/PKOBP WSE/PZU WSE/SANPL WSE/TAURONPE'.split()
        self.wig20_names = 'ALIOR ALLEGRO ASSECO CCC CDPROJEKT CYFRPOLSAT DINO JSW KGHM LOTOS LPP ORANGE PEKAO PGE PGNIG ORLEN PKOBP PZU SANPL TAURON'.split()
        self.wig20_tickers = 'ALR ALE ACP CCC CDR CPS DNP JSW KGH LTS LPP OPL PEO PGE PGN PKN PKO PZU SPL TPE'.split()

        try:
            self.df = pd.read_csv('last_day_info.csv', index_col = 0)
        except:
            self.df = pd.DataFrame(columns = ['Close', 'Percent change'], index = self.wig20_tickers)

        wig20_np = np.zeros((20, 2))
        self.W20 = pd.DataFrame(wig20_np)
        self.W20.index.name = 'Name'
        self.W20.columns = ['Ticker', 'Quandl']
        self.W20['Quandl'] = self.wig20_stocks
        self.W20.index = self.wig20_names
        self.W20['Ticker'] = self.wig20_tickers

        self.prev_day_data = []
        self.last_data_load_date = (self.today - BDay(30)).date()
        # self.fill_prev_data()

    def quandl_from_ticker(self, ticker):
        return self.W20['Quandl'][self.W20['Ticker'] == ticker].values[0]

    def ticker_from_quandl(self, quandl):
        return self.W20['Ticker'][self.W20['Quandl'] == quandl].values[0]

    def quandl_asset_df(self, quandl_code, start = None, end = None, api_key = 'BJVHzuYs1s6oVDuyEukv'):
        if start is None:
            start = self.prev_bus_day
        if end is None:
            end = self.prev_bus_day
        return pd.DataFrame(quandl.get(quandl_code, start_date = start, end_date = end, authtoken = api_key))

    def prev_close_price(self, ticker):
        df = self.quandl_asset_df(self.quandl_from_ticker(ticker))
        return df['Close'].values[0]

    def fill_prev_data(self):
        last_run = open('last_run.txt', 'r+')
        last_run_date = last_run.read()
        if datetime.datetime.strptime(last_run_date, '%Y-%m-%d').date() != date.today():
            for ticker in self.wig20_tickers:
                df = self.quandl_asset_df(self.quandl_from_ticker(ticker), self.prev_bus_day2)
                df['Percent change'] = df['Close'].pct_change() * 100
                df['Percent change'] = df['Percent change'].round(2)
                df['Percent change'] = list(map(lambda x: str(x) + '%', df['Percent change'])) #df['Percent change'].apply(lambda x: f'{x}%')

                self.df.loc[ticker] = [df['Close'].values[0], df['Percent change'].values[1]]
        self.df.to_csv('last_day_info.csv')
        last_run.truncate(0)
        last_run.close()
        with open('last_run.txt', 'a') as myfile:
            myfile.write(f'{date.today()}')
            myfile.close()

    @staticmethod
    def str_to_date(str_date):
        return pd.to_datetime(str_date).date()

    @staticmethod
    def str_to_date2(str_date):
        return datetime.datetime.strptime(str_date, "%Y-%m-%d").date()

    @staticmethod
    def get_hash(text):
        salt = '37b949c239f2cef84bae24db756'
        for i in range(100000):
            text = sha3_512((text + salt).encode()).hexdigest()
        return text

    def add_hash(self, user, password):
        hsh = self.get_hash(password)
        self.db.add_hash(user, hsh)

    def check_hash(self, user, password):
        h1 = self.get_hash(password)
        h2 = self.db.get_hash(user)

        return h1 == h2[0][0]

    @staticmethod
    def login():
        print('login successful')
