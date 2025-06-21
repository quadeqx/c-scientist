import logging
from data import BinanceClient  # Assumes decorators in data/__init__.py
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File handler with rotation (1MB per file, keep 3 backups)
file_handler = RotatingFileHandler('coin_data.log', maxBytes=1_000_000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Data:
    def __init__(self):
        self.watchlists = {
            "payments": ["BTC", "XRP", "BCH", "ARK", "PEPE", "TRX", "DOGE"],
            "ai": ["LTC", "AI", "TAO", "NEAR", "WLD", "AIXBT", "FET", "RENDER"],
            "meme": ["TRUMP", "SHIB", "BONK", "NOT", "BOME", "PEOPLE"],
            "analytics": ["ARKM", "CGPT"],
            "dexchange": ["BNB", "INJ", "FTT", "ARKM", "TKO"],
            "liquid_staking": ["WBETH", "LDO", "ANKR", "RPL", "LISTA", "OGN", "QI", "HAEDAL", "FIS", "CHESS"],
            "L_0": ["ATOM", "DOT", "DATA", "ZRO", "AVAX"],
            "L_1": ["ADA", "FIL", "TON", "APT", "TAO", "TIA", "KAVA", "VANRY"],
            "L_2": ["OP", "CYBER", "ARB", "STX", "IMX", "DYDX", "SNX", "ZK", "ZRX", "STRK"],
            "L_3": ["XAI", "GHST"]
        }

    def get_watchlist_by_key(self, key):
        return [[item] for item in self.watchlists.get(key, [])]

class coinprice:
    def __init__(self):
        self.data = Data()
        self.binc = BinanceClient()

    def getprices(self, key):
        watchlist = {}
        try:
            pays = self.data.get_watchlist_by_key(key)
            if not pays:
                logger.warning(f"No coins found in watchlist for key: {key}")
                return watchlist

            for pay in pays:
                symbol = pay[0]
                trading_pair = f"{symbol}USDT"
                try:
                    if not isinstance(symbol, str) or not symbol.isalnum():
                        logger.error(f"Invalid symbol: {symbol}")
                        continue
                    prices = self.binc.get_uiklines(trading_pair, '1h', limit=1)
                    watchlist[trading_pair] = prices
                except Exception as e:
                    logger.error(f"Failed to fetch prices for {trading_pair}: {str(e)}")

            logger.info(f"Fetched prices for {key}: {watchlist}")
            #print('\n\n\n Watchlist data: ', watchlist, '\n\n\n')
            return watchlist
        except Exception as e:
            logger.error(f"Error fetching watchlist for {key}: {str(e)}")
            return watchlist

    def prepare_table_data(self, data, key):
        if not data:
            return []

        columns = ['open', 'high', 'low', 'close', 'volume', 'number_of_trades']
        table_data = []
        for symbol, values in data.items():
            row = [symbol[:-4]]
            for col in columns:
                try:
                    row.append(f"{float(values[col]):.8f}".rstrip('0').rstrip('.'))
                except (KeyError, ValueError) as e:
                    logger.error(f"Error formatting {col} for {symbol}: {str(e)}")
                    row.append("N/A")
            table_data.append(row)
        #print('\n\n\nprocessed data: ', table_data, '\n\n\n')
        return table_data
