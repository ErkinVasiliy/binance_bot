from binance.client import Client

from .variables import API_KEY, SECRET_KEY
from .BalanceInfo import AccountBalance

from time import sleep


def print_balance(client):
    ab = AccountBalance(client)
    while True:
        print(str(ab))
        sleep(10)


def run():
    client = Client(API_KEY, SECRET_KEY)
    print_balance(client)


