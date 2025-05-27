import requests
from datetime import datetime
from functools import wraps
import time

# Helper decorators (simplified versions for demonstration)
def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling: {func.__name__} with args: {args[1:]}, kwargs: {kwargs}\n\n")
        result = func(*args, **kwargs)
        print(f"[LOG] Result type: {type(result)}, length: {len(result) if hasattr(result, '__len__') else 'N/A'}\n\n")
        return result
    return wrapper

def retry(times=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Attempt {attempt} failed: {e}\n\n")
                    last_exception = e
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def accepts(*types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for a, t in zip(args[1:], types):  # skip self
                if not isinstance(a, t):
                    raise TypeError(f"Arg {a} does not match {t}\n\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def returns(expected_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, expected_type):
                raise TypeError(f"Return value {result} is not {expected_type}\n\n")
            return result
        return wrapper
    return decorator

# Timestamp conversion helper
def ts_to_datetime(ts):
    return datetime.utcfromtimestamp(ts / 1000).isoformat()

# Binance client class
class BinanceClient:
    done = False
    BASE_URL = "https://api.binance.com"
    UIKLINE_KEYS = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ]

    def __init__(self):
        self.session = requests.Session()

    @log_request
    @retry(times=3, delay=2)
    @returns(list)
    @accepts(str, str, int)
    def get_uiklines(self, symbol, interval, limit=1000):
        url = f"{self.BASE_URL}/api/v3/uiKlines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        raw_data = response.json()

        # Convert list of lists to list of dicts
        structured = [dict(zip(self.UIKLINE_KEYS, row)) for row in raw_data]

        # Convert timestamps to ISO format
        converted = [
            {
                **candle,
                "open_time": ts_to_datetime(candle["open_time"]),
                "close_time": ts_to_datetime(candle["close_time"])
            }
            for candle in structured
        ]
        BinanceClient.done = True
        return converted

