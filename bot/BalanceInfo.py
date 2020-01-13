'''
TODO:

add deco for update methods with datetime check
add normal support of usd coins

'''
deprecated_tickers = ['DENTBTC', 'BCHSVBTC', 'BCCBTC', 'TRIGBTC', 'SALTBTC',
                      'CLOAKBTC', 'RPXBTC', 'ICNBTC', 'BTTBTC', 'WINBTC']

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

    #coin_name -> (price_to_btc, price_to_usdt)
    def prices(self, coin):
        btc_price = self._prices['BTCUSDT']

        if coin == 'BTC':
            price_to_btc = 1.0
            price_to_usdt = btc_price
        elif coin == 'USDT':
            price_to_btc = 1 / btc_price
            price_to_usdt = 1.0
        else:
            try:
                price_to_btc = self._prices[coin + 'BTC']
                price_to_usdt = price_to_btc * btc_price
            except:
                price_to_usdt = self._prices[coin + 'USDT']
                price_to_btc = price_to_usdt / btc_price

        return price_to_btc, price_to_usdt


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


        for coin in balance:
            coin_volume = float(coin['free']) + float(coin['locked'])

            if coin_volume == 0.0:
                continue

            name = coin['asset']
            btc_price, usdt_price = self.tickers.prices(name)

            info = {'name': name,
                    'BTC_volume': coin_volume * btc_price,
                    'USDT_volume': coin_volume * usdt_price,
                    'BTC_price': btc_price,
                    'USDT_price': usdt_price}

            self.coins[name] = info

    @property
    def btc_balance(self):
        return sum(c['BTC_volume'] for c in self.coins.values())

    @property
    def usdt_balance(self):
        return self.btc_balance * self.tickers['BTCUSDT']

    def __str__(self):
        self.update()
        balance_str = 'Balance: BTC-{:.5f}, USDT-{:.1f} '
        coin_template = '{name}, BTC volume: {BTC_volume:.5f}, ' \
                        'BTC price: {BTC_price:.8f}, ' \
                        'USDT volume: {USDT_volume:.2f}, ' \
                        'USDT price: {USDT_price:.7f}'

        strs = [coin_template.format(**coin) for coin in self.coins.values()]
        strs.append(balance_str.format(self.btc_balance, self.usdt_balance))

        return '\n'.join(strs)

    def get_tickers(self, type):
        return self.tickers.get_tickers(type)