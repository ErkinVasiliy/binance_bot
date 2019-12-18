deprecated_t = ['DENTBTC', 'BCHSVBTC', 'BCCBTC', 'TRIGBTC', 'SALTBTC', 'CLOAKBTC', 'RPXBTC', 'ICNBTC']


class Tickers:
    def __init__(self, client):
        self._client = client
        self._prices = None
        self.update()

    def update(self):
        self._prices = {t['symbol']: float(t['price'])
                        for t in self._client.get_all_tickers()
                        if t['symbol'] not in deprecated_t}

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