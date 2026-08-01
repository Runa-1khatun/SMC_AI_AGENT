def detect_mss(candles, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "No MSS"

    last_close = candles[-1]["close"]

    prev_high = swing_highs[-2][1]
    prev_low = swing_lows[-2][1]

    # Bullish MSS
    if last_close > prev_high:
        return "Bullish MSS"

    # Bearish MSS
    if last_close < prev_low:
        return "Bearish MSS"

    return "No MSS"