def detect_displacement(
    candles,
    bos,
    lookback=5,
    multiplier=2.0,
):

    if len(candles) < lookback + 2:
        return "No Displacement"

    recent = candles[-lookback - 1:-1]

    avg_body = sum(
        abs(c["close"] - c["open"])
        for c in recent
    ) / lookback

    last = candles[-1]

    body = abs(last["close"] - last["open"])

    high = last["high"]
    low = last["low"]

    upper_wick = high - max(last["open"], last["close"])
    lower_wick = min(last["open"], last["close"]) - low

    # বড় Body হতে হবে
    if body < avg_body * multiplier:
        return "No Displacement"

    # Strong Bullish Close
    if (
        bos == "Bullish BOS"
        and last["close"] > last["open"]
        and upper_wick < body * 0.30
    ):
        return "Bullish Displacement"

    # Strong Bearish Close
    if (
        bos == "Bearish BOS"
        and last["close"] < last["open"]
        and lower_wick < body * 0.30
    ):
        return "Bearish Displacement"

    return "No Displacement"