from .Ticker import Tickers

'''
TODO:

add deco for update methods with datetime check
add normal support of usd coins

'''


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
