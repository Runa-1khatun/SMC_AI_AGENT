def confirm_entry(candles):

    if len(candles) < 3:
        return "NO ENTRY"

    prev = candles[-2]
    last = candles[-1]
    prev_range = prev["high"] - prev["low"]
    last_range = last["high"] - last["low"]

    # -------------------------
    # Bullish Engulfing
    # -------------------------
    if (
        prev["close"] < prev["open"] and
        last["close"] > last["open"] and
        last["close"] > prev["open"] and
        last["open"] < prev["close"]
        and last_range > prev_range
    ):
        return "BUY"

    # -------------------------
    # Bearish Engulfing
    # -------------------------
    if (
        prev["close"] > prev["open"] and
        last["close"] < last["open"] and
        last["open"] > prev["close"] and
        last["close"] < prev["open"]
        and last_range > prev_range
    ):
        return "SELL"

    return "NO ENTRY"