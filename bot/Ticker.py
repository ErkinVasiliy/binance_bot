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

