from collections import defaultdict
import time


def to_dict(lst):
    return {l['symbol']: float(l['price']) for l in lst
            if l['symbol'].find('BTC', 1) != -1 or l['symbol'] == 'BTCUSDT'}


'''
TODO:

add deco for update methods with datetime check
add normal support of usd coins

'''


class CoinsPrice:
    def __init__(self, client):
        self._client = client
        self._prices = None

    def update(self):
        self._prices = to_dict(self._client.get_all_tickers())
        self._prices['USDTBTC'] = 1.0 / self._prices['BTCUSDT']

    def coin_price(self, coin_name):
        #here is a problem with usdc, tusd, and some other coins
        #need to fix it

        if coin_name.find('USD') != -1:
            return self._prices['USDTBTC']

        if coin_name in ['BTC', 'BGBP']:
            return 1.0
        return self._prices[coin_name + 'BTC']

    @property
    def all_tickers(self):
        return [key for key in self._prices.keys() if key.find('USD') == -1]


class AccountBalance(CoinsPrice):
    def __init__(self, client):
        super().__init__(client)
        self.coins = defaultdict(dict)
        self.update()

    def update(self):
        super().update()
        balance = self._client.get_account()['balances']

        for coin in balance:
            if coin['asset'] == 'NGN':
                continue

            btc_price = self.coin_price(coin['asset'])
            info = {'name': coin['asset'],
                    'volume': (float(coin['free']) + float(coin['locked'])) * btc_price,
                    'btc_price': btc_price,
                    'usdt_price': btc_price * self._prices['BTCUSDT']}

            self.coins[coin['asset']] = info

    def positive_coins(self):
        return [coin for coin in self.coins.values() if coin['volume'] > 0.0]

    def coin_info(self, coin_name):
        return self.coins[coin_name]

    @property
    def btc_balance(self):
        return sum(v['volume'] for v in self.positive_coins())

    @property
    def usdt_balance(self):
        return self.btc_balance * self._prices['BTCUSDT']

    def __str__(self):
        balance_str = 'Balance: BTC-{}, USDT-{}'
        coin_template = '{name}, volume: {volume:.5f}, ' \
                        'BTC price: {btc_price}, USDT price: {usdt_price}'

        strs = [coin_template.format(**coin) for coin in self.positive_coins()]
        strs.append(balance_str.format(self.btc_balance, self.usdt_balance))

        return '\n'.join(strs)


def print_balance(client):
    ab = AccountBalance(client)
    while True:
        ab.update()
        print(str(ab))
        time.sleep(30)
        print()