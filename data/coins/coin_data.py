from data import BinanceClient


class Data:
    def __init__(self):
        self.watchlists = {
            "payments": ["BTC", "XRP", "BCH", "ARK", "PEPE", "TRX", "DOGE"],
            "ai": ["LTC", "AI", "TAO", "NEAR", "WLD", "AIXBT", "FET", "RENDER", "FET"],
            "meme": ["TRUMP", "SHIB", "BONK", "NOT", "BOME", "PEOPLE"],
            "analytics": ["ARKM", "CGPT"],
            "dexchange": ["BNB", "INJ", "FTT", "ARKM", "TKO"],
            "liquid_staking": ["WBETH", "LDO", "ANKR", "RPL", "LISTA", "OGN", "QI", "HAEDAL", "FIS", "CHESS"],
            "L_0": ["ATOM", "DOT", "DATA", "ZRO", "AVAX"],
            "L_1": ["ADA", "FIL", "TON", "APT", "TAO", "TIA", "KAVA", "VANRY"],
            "L_2": ["OP", "CYBER", "ARB", "STX", "IMX","DYDX", "SNX", "ZK", "ZRX","STRK"],
            "L_3": ["XAI", "GHST"]
        }

    def get_watchlist_by_key(self, key):
        return [[item] for item in self.watchlists.get(key, [])]


class coinprice:
    def __init__(self):
        self.data = Data()
        self.binc = BinanceClient()

    def getprices(self, key):
        self.pays = self.data.get_watchlist_by_key(key)
        self.watchlist = {}
        for _, self.pay in enumerate(self.pays):
            self.prices = self.binc.get_uiklines(self.pay[0]+'USDT', '1m', limit=1)
            self.watchlist[self.pay[0]+'USDT'] = self.prices
        return self.watchlist

    def prepare_table_data(self, data):
        columns = ['open', 'high', 'low', 'close', 'volume']
        table_data = []

        for coin, values in data.items():
            row = {'Coin': coin}

            for col in columns:
                row[col] = f"{float(values[col]):.8f}".rstrip('0').rstrip('.')
            table_data.append(row)

        return table_data

