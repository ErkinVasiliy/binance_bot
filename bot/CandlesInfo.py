import pandas as pd
from os.path import join
from .Utils import ut2dt

klines_keys = [
    'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'BTC Volume',
    'Number of trades', 'Buy volume', 'BTC buy volume',
    'Can be ignored'
]


class KlinesInfo:
    def __init__(self, klines):
        self._klines = klines


    @staticmethod
    def __prepare_data(klines_list):



        df = pd.DataFrame(klines_list, columns=klines_keys)
        df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'BTC Volume']]
        df['datetime'] = df['Open time'].apply(ut2dt)
        #df['Time'] = df['datetime'].apply(mdates.date2num)

        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Close'] = df['Close'].astype(float)

        return df[['datetime', 'Open', 'High', 'Low', 'Close', 'BTC Volume']]

    @classmethod
    def from_list(cls, klines_list):
        return KlinesInfo(cls.__prepare_data(klines_list))

    @property
    def size(self):
        return self._klines.index.size

    @property
    def columns(self):
        return [v for k, v in self._klines.items()]

    def last_candles(self, num=1):
        return KlinesInfo(self._klines[-num:])

    @property
    def change(self):
        return (self._klines.iloc[-1]['Close'] / self._klines.iloc[0]['Open'] - 1.0) * 100.0


    def to_dict(self):
        return self._klines.to_dict('records')

    def dump(self, path=''):
        self._klines.to_csv(join(path, 'candles.csv'), index=False)


def get_klines(client, interval='1h', symbol='TNTBTC'):
    klines_list = client.get_klines(symbol=symbol, interval=interval, limit=125)
    return KlinesInfo(klines_list)


