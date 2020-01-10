import pandas as pd
from os.path import join
from .Utils import ut2dt

klines_keys = [
    'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'BTC Volume',
    'Number of trades', 'Buy volume', 'BTC buy volume',
    'Can be ignored'
]


class Candles:
    def __init__(self, klines, ticker=None):
        self._klines = klines
        self._ticker = ticker

    @classmethod
    def from_list(cls, klines_list, ticker=None):
        df = pd.DataFrame(klines_list, columns=klines_keys)

        df['datetime'] = df['Open time'].apply(ut2dt)
        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Close'] = df['Close'].astype(float)
        df['BTC Volume'] = df['BTC Volume'].astype(float)

        return cls(df[['datetime', 'Open', 'High', 'Low', 'Close', 'BTC Volume']], ticker)

    def __getitem__(self, val):
        return Candles(self._klines.iloc[val], self._ticker)

    def __len__(self):
        return self._klines.index.size

    @property
    def columns(self):
        return [v for k, v in self._klines.items()]

    def dump(self, path=''):
        self._klines.to_csv(join(path, '{}.csv'.format(self._ticker)), index=False)

