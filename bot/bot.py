from binance.client import Client

from .variables import API_KEY, SECRET_KEY
from .Utils import timeit
from .Ticker import Tickers


@timeit
def run():
    client = Client(API_KEY, SECRET_KEY)

    coins = Tickers(client)
    coins.update()

    #animate_plot(kl, t, window=50)





