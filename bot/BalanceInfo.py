'''
TODO:

add deco for update methods with datetime check
add normal support of usd coins

'''
deprecated_tickers = ['DENTBTC', 'BCHSVBTC', 'BCCBTC', 'TRIGBTC', 'SALTBTC',
                      'CLOAKBTC', 'RPXBTC', 'ICNBTC']

COINS_TYPES = ['USDT', 'BTC']


class Tickers:
    def __init__(self, client):
        self._client = client
        self._prices = None

    def update(self):
        self._prices = {t['symbol']: float(t['price'])
                        for t in self._client.get_all_tickers() if t['symbol']
                        not in deprecated_tickers}

    def get_tickers(self, type='BTC'):
        self.update()
        type = type if type in COINS_TYPES else 'BTC'
        return [ticker for ticker, price in self._prices.items()
                if ticker.endswith(type)]

    def __getitem__(self, item):
        return self._prices[item]


class AccountBalance:
    def __init__(self, client):
        self.coins = {}
        self._client = client
        self.tickers = Tickers(client)

    def update(self):
        balance = self._client.get_account()['balances']
        self.tickers.update()

        btc_price = self.tickers['BTCUSDT']

        for coin in balance:
            coin_volume = float(coin['free']) + float(coin['locked'])

            if coin_volume == 0.0:
                continue

            name = coin['asset']
            info = {'name': name,
                    'volume': coin_volume / btc_price,
                    'price': self.__btc_price(name)}

            self.coins[name] = info

    @property
    def btc_balance(self):
        return sum(c['volume'] for c in self.coins.values())

    @property
    def usdt_balance(self):
        return self.btc_balance * self.tickers['BTCUSDT']

    def __str__(self):
        self.update()
        balance_str = 'Balance: BTC-{}, USDT-{}'
        coin_template = '{name}, volume: {volume:.5f}, BTC price: {price}'

        strs = [coin_template.format(**coin) for coin in self.coins.values()]
        strs.append(balance_str.format(self.btc_balance, self.usdt_balance))

        return '\n'.join(strs)


    def __btc_price(self, coin):
        if coin == 'BTC':
            return 1.0
        if coin == 'USDT':
            return 1 / self.tickers['BTCUSDT']

        return self.tickers[coin + 'BTC']

    def get_tickers(self, type):
        return self.tickers.get_tickers(type)