import requests
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict

from .CandlesInfo import Candles


def get_candles(ticker, interval='4h'):
    url = 'https://api.binance.com/api/v1/klines?symbol='+ticker+'&interval='+interval
    data = requests.get(url).json()
    return data


def task(ticker):
    kl = Candles.from_list(get_candles(ticker), ticker)

    return ticker, kl


def get_all_candles(tickers):
    e = ThreadPoolExecutor(100)

    return {t: k for t, k in e.map(task, tickers)}


def exec(tickers):

    def _price(k):
        return int(k.last_candles(1).to_dict()[0]['Close'] * 10e7)

    def _change(k):
        return round(k.last_candles(2).change, 2)

    kl = get_all_candles(tickers)

    d = {t: (_change(k), _price(k))
         for t, k in kl.items() if _price(k) > 100 and _change(k) > 0.5}

    return OrderedDict(sorted(d.items(), key=lambda kv: kv[1]))