try:
    import pandas as pd  # type: ignore[import]
except ImportError:
    pd = None

def add_ema(candles):
    if pd is None:
        raise ImportError("pandas is required to use add_ema")

    df = pd.DataFrame(candles)

    df["EMA50"] = df["close"].ewm(span=50).mean()
    df["EMA200"] = df["close"].ewm(span=200).mean()

    return df