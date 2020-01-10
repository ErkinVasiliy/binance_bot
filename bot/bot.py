import os
import json

from binance.client import Client
from argparse import ArgumentParser
from time import sleep

from .BalanceInfo import AccountBalance
from .CandlesInfo import Candles
from .binance_requests import get_candles
from .plotter import plot


API_KEY = 'api_key'
SECRET_KEY = 'secret_key'
SAVE_PATH = 'save_path'


def read_settings(path):
    if not (os.path.exists(path) and os.path.isfile(path)):
        path = 'settings.json'

    with open(path, 'r') as file:
        data = json.load(file)

    return data


def print_balance(args):
    settings = read_settings(args.settings)
    client = Client(settings[API_KEY], settings[SECRET_KEY])
    ab = AccountBalance(client)
    while True:
        os.system('cls')
        print(str(ab))
        sleep(10)


def get_klines(args):
    settings = read_settings(args.settings)

    candles_list = get_candles('TNTBTC')
    candles = Candles.from_list(candles_list)
    candles.dump(settings[SAVE_PATH])
    plot(candles, 'TNTBTC')


def run():
    parser = ArgumentParser(prog='BinanceApp',
                            description='App for Binance trading')
    parser.add_argument('-s', '--setting_path', help='Path to setting file',
                        dest='settings', type=str)

    work_type = parser.add_subparsers(title='work_type',
                                      help='Type of work for bot',
                                      dest='work_type')

    show_b = work_type.add_parser('show_balance',
                                  help='Show balance of current user')
    show_b.add_argument('-t', '--ticker',
                        help='Show depth of coin',
                        default='all', dest='ticker')
    show_b.set_defaults(command=print_balance)

    build_g = work_type.add_parser('build_graphs',
                                   help='Build graph of candles and save')
    build_g.add_argument('--ctype', help='Choose type of graph', dest='ctype',
                         choices=['btc', 'usdt', 'all'], default='all')
    build_g.set_defaults(command=get_klines)

    args = parser.parse_args()
    print('Calling', args.work_type, 'command')
    args.command(args)
