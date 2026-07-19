def structure_bias(trend, bos, choch):

    # Perfect Alignment
    if (
        trend == "BULLISH"
        and bos == "Bullish BOS"
        and choch == "Bullish CHoCH"
    ):
        return "STRONG BUY"

    if (
        trend == "BEARISH"
        and bos == "Bearish BOS"
        and choch == "Bearish CHoCH"
    ):
        return "STRONG SELL"

    # Pullback
    if trend == "BULLISH":
        return "BULLISH PULLBACK"

    if trend == "BEARISH":
        return "BEARISH PULLBACK"

    return "RANGE"
def find_swings(candles, lookback=3):

    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(candles) - lookback):

        high = candles[i]["high"]
        low = candles[i]["low"]

        # Swing High
        if all(
            high > candles[j]["high"]
            for j in range(i - lookback, i + lookback + 1)
            if j != i
        ):
            swing_highs.append((i, high))

        # Swing Low
        if all(
            low < candles[j]["low"]
            for j in range(i - lookback, i + lookback + 1)
            if j != i
        ):
            swing_lows.append((i, low))

    return swing_highs, swing_lows


def detect_bos(candles, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "No BOS"

    # -------------------------
    # Bullish BOS
    # -------------------------
    for index, level in reversed(swing_highs):

        for i in range(index + 1, len(candles)):

            if candles[i]["close"] > level:
                return "Bullish BOS"

    # -------------------------
    # Bearish BOS
    # -------------------------
    for index, level in reversed(swing_lows):

        for i in range(index + 1, len(candles)):

            if candles[i]["close"] < level:
                return "Bearish BOS"

    return "No BOS"
    
def detect_choch(candles, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "No CHoCH"

    # শেষ দুইটি Swing High
    prev_high_idx, prev_high = swing_highs[-2]
    last_high_idx, last_high = swing_highs[-1]

    # শেষ দুইটি Swing Low
    prev_low_idx, prev_low = swing_lows[-2]
    last_low_idx, last_low = swing_lows[-1]

    # Bullish CHoCH
    if last_high > prev_high and last_low > prev_low:
        return "Bullish CHoCH"

    # Bearish CHoCH
    if last_high < prev_high and last_low < prev_low:
        return "Bearish CHoCH"

    return "No CHoCH"