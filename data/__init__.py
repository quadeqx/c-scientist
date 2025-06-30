import requests
from functools import wraps
import time

def log_request(func):
    """Log decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        #print(f"[LOG] Calling: {func.__name__} with args: {args[1:]}, kwargs: {kwargs}\n\n")
        result = func(*args, **kwargs)
        #print(f"[LOG] Result type: {type(result)}, length: {len(result) if hasattr(result, '__len__') else 'N/A'}\n\n")
        return result
    return wrapper

def retry(times=3, delay=1):
    """Retries decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Attempt {attempt} failed: {e}\n\n")
                    continue
                    last_exception = e
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def accepts(*types):
    """Input verification decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for a, t in zip(args[1:], types):  # skip self
                if not isinstance(a, t):
                    raise TypeError(f"Arg {a} does not match {t}\n\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def returns(expected_type, expected_type2):
    """Return type verification decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, expected_type):
                raise TypeError(f"Return value {result} is not {expected_type}\n\n")
            return result
        return wrapper
    return decorator





class BinanceClient:
    """Binance API calls to request market data."""

    done = False
    BASE_URL = "https://api.binance.com"

    def __init__(self):
        self.session = requests.Session()

    @log_request
    @retry(times=3, delay=2)
    #@returns(dict, list)
    @accepts(str, str, int)
    def get_uiklines(self, symbol, interval, limit=999):
        """


        Parameters.

        ----------

        symbol : coin ticker
            string
        interval : Candlestick interval
            integer
        limit : Number of candlestcks data, optional
            integer(1-1000). The default is 999.

        Returns
        -------
        processed : One ticker price
            dictionary.

        """
        UIKLINE_KEYS = [
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ]

        url = f"{self.BASE_URL}/api/v3/uiKlines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        raw_data = response.json()

        processed = dict(zip(UIKLINE_KEYS, raw_data[0]))

        plottable = processed = [dict(zip(UIKLINE_KEYS, kline)) for kline in raw_data]

        BinanceClient.done = True

        return processed, plottable





