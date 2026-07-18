def find_swings(candles, lookback=3):

    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(candles) - lookback):

        high = candles[i]["high"]
        low = candles[i]["low"]

        is_high = True
        is_low = True

        for j in range(1, lookback + 1):

            if high <= candles[i-j]["high"] or high <= candles[i+j]["high"]:
                is_high = False

            if low >= candles[i-j]["low"] or low >= candles[i+j]["low"]:
                is_low = False

        # Minimum swing distance filter
        if is_high:
            if len(swing_highs) > 0:
                last_high = swing_highs[-1][1]

                if abs(high - last_high) < 3:
                    is_high = False

        if is_low:
            if len(swing_lows) > 0:
                last_low = swing_lows[-1][1]

                if abs(low - last_low) < 3:
                    is_low = False

        if is_high:
            swing_highs.append((i, high))

        if is_low:
            swing_lows.append((i, low))

    return swing_highs, swing_lows


def detect_bos(candles, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "No BOS"

    last_close = candles[-1]["close"]

    prev_high = swing_highs[-2][1]
    last_high = swing_highs[-1][1]

    prev_low = swing_lows[-2][1]
    last_low = swing_lows[-1][1]

    # Strong Bullish BOS
    if last_high > prev_high and last_close > last_high:
        return "Bullish BOS"

    # Strong Bearish BOS
    elif last_low < prev_low and last_close < last_low:
        return "Bearish BOS"

    return "No BOS"
    
def detect_choch(candles, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "No CHoCH"

    last_high = swing_highs[-1][1]
    prev_high = swing_highs[-2][1]

    last_low = swing_lows[-1][1]
    prev_low = swing_lows[-2][1]

    if last_high > prev_high and last_low > prev_low:
        return "Bullish CHoCH"

    elif last_high < prev_high and last_low < prev_low:
        return "Bearish CHoCH"

    else:
        return "No CHoCH"


def detect_fvg(candles):
    fvgs = []

    for i in range(2, len(candles)):
        first = candles[i - 2]
        third = candles[i]

        # Bullish FVG
        if third["low"] > first["high"]:
            fvgs.append({
                "type": "Bullish",
                "top": third["low"],
                "bottom": first["high"],
                "index": i
            })

        # Bearish FVG
        elif third["high"] < first["low"]:
            fvgs.append({
                "type": "Bearish",
                "top": first["low"],
                "bottom": third["high"],
                "index": i
            })

    return fvgs
def detect_order_blocks(candles):

    order_blocks = []

    for i in range(1, len(candles) - 2):

        prev = candles[i - 1]
        current = candles[i]
        next_candle = candles[i + 1]

        # Bullish Order Block
        if (
            prev["close"] < prev["open"]
            and current["close"] > current["open"]
            and current["close"] > prev["high"]
            and (current["close"] - current["open"]) > 2
            and next_candle["close"] > next_candle["open"]
        ):
            order_blocks.append({
                "type": "Bullish",
                "high": prev["high"],
                "low": prev["low"],
                "index": i - 1
            })

        # Bearish Order Block
        elif (
            prev["close"] > prev["open"]
            and current["close"] < current["open"]
            and current["close"] < prev["low"]
            and (current["open"] - current["close"]) > 2
            and next_candle["close"] < next_candle["open"]
        ):
            order_blocks.append({
                "type": "Bearish",
                "high": prev["high"],
                "low": prev["low"],
                "index": i - 1
            })

    return order_blocks
def detect_liquidity_sweep(candles, swing_highs, swing_lows):

    sweeps = []

    if not swing_highs or not swing_lows:
        return sweeps

    # শুধু সর্বশেষ Swing High এবং Swing Low ব্যবহার
    last_swing_high = swing_highs[-1][1]
    last_swing_low = swing_lows[-1][1]

    # শুধু শেষ ১০টি ক্যান্ডেল পরীক্ষা
    for i in range(max(1, len(candles) - 10), len(candles)):

        high = candles[i]["high"]
        low = candles[i]["low"]
        close = candles[i]["close"]

        # Bearish Sweep
        if high > last_swing_high and close < last_swing_high:
            sweeps.append({
                "type": "Bearish Sweep",
                "level": last_swing_high,
                "index": i
            })

        # Bullish Sweep
        elif low < last_swing_low and close > last_swing_low:
            sweeps.append({
                "type": "Bullish Sweep",
                "level": last_swing_low,
                "index": i
            })

    return sweeps