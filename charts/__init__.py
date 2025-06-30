def preprocess_binance_data(binance_data):
    """Preprocesses the long data received."""
    for candle in binance_data:
        processed = {
            "Open": float(candle["open"]),
            "High": float(candle["high"]),
            "Low": float(candle["low"]),
            "Close": float(candle["close"])
        }
    return processed
