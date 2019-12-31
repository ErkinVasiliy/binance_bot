from binance.client import Client

from .variables import API_KEY, SECRET_KEY
from .BalanceInfo import AccountBalance
from .Ticker import Tickers
from .CandlesInfo import Candles

from .binance_requests import get_candles

from time import sleep


def print_balance(client):
    ab = AccountBalance(client)
    while True:
        print(str(ab))
        sleep(10)


def get_klines():
    candles_list = get_candles('TNTBTC')
    candles = Candles.from_list(candles_list)
    c = candles[-5:]
    print(c.columns)





def run():
    get_klines()



