import logging
from data import BinanceClient


# Configure logging
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
logger.propagate = False
"""
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File handler with rotation (1MB per file, keep 3 backups)

from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('coin_data.log', maxBytes=1_000_000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
"""
class Data:
    """A dictionary of coin categories."""

    def __init__(self):
        self.watchlists = {
            "Payments": ["BTC", "XRP", "BCH", "ARK", "PEPE", "TRX", "DOGE"],
            "Artificial Int": ["LTC", "AI", "TAO", "NEAR", "WLD", "AIXBT", "FET", "RENDER"],
            "Meme": ["TRUMP", "SHIB", "BONK", "NOT", "BOME", "PEOPLE"],
            "Analytics": ["ARKM", "CGPT"],
            "Dexchange": ["BNB", "INJ", "FTT", "ARKM", "TKO"],
            "Liquid Staking": ["WBETH", "LDO", "ANKR", "RPL", "LISTA", "OGN", "QI", "HAEDAL", "FIS", "CHESS"],
            "Layer 0": ["ATOM", "DOT", "DATA", "ZRO", "AVAX"],
            "Layer 1": ["ADA", "FIL", "TON", "APT", "TAO", "TIA", "KAVA", "VANRY"],
            "Layer 2": ["OP", "CYBER", "ARB", "STX", "IMX", "DYDX", "SNX", "ZK", "ZRX", "STRK"],
            "Layer 3": ["XAI", "GHST"]
        }

    def get_watchlist_by_key(self, key):
        """Return a list of coins for the given key."""
        return [[item] for item in self.watchlists.get(key, [])]

class coinprice:
    """Get prices for watchlists."""

    def __init__(self):
        self.data = Data()
        self.binc = BinanceClient()

    def getprices(self, key):
        """Query the API for watchlist prices."""
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
                    prices, _ = self.binc.get_uiklines(trading_pair, '1h', limit=1)
                    watchlist[trading_pair] = prices[0]
                except Exception as e:
                    logger.error(f"Failed to fetch prices for {trading_pair}: {str(e)}")

            logger.info(f"Fetched prices for {key}: {watchlist}")
            print(watchlist)
            return watchlist
        except Exception as e:
            logger.error(f"Error fetching watchlist for {key}: {str(e)}")
            return watchlist

    def prepare_table_data(self, data, key):
        """Prepare data for tabular display."""
        if not data:
            print('No data')
            return []
        print(data)
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
        return table_data
