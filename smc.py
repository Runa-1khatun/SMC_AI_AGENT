def detect_fvg(candles):

    fvgs = []

    for i in range(2, len(candles)):

        # Bullish FVG
        if candles[i]["low"] > candles[i - 2]["high"]:

            fvgs.append({
                "type": "Bullish",
                "high": candles[i]["low"],
                "low": candles[i - 2]["high"],
                "index": i
            })

        # Bearish FVG
        elif candles[i]["high"] < candles[i - 2]["low"]:

            fvgs.append({
                "type": "Bearish",
                "high": candles[i - 2]["low"],
                "low": candles[i]["high"],
                "index": i
            })

    return fvgs

    return fvgs
def detect_order_blocks(candles):

    order_blocks = []

    for i in range(2, len(candles) - 2):

        candle = candles[i]

        body = abs(candle["close"] - candle["open"])
        rng = candle["high"] - candle["low"]

        # ছোট Body হলে Skip
        if rng == 0 or body / rng < 0.4:
            continue

        # ==========================
        # Bullish Order Block
        # ==========================
        if candle["close"] < candle["open"]:

            next1 = candles[i + 1]
            next2 = candles[i + 2]

            if (
                next1["close"] > next1["open"]
                and next2["close"] > next2["open"]
                and next2["close"] > candle["high"]
            ):

                order_blocks.append({
                    "type": "Bullish",
                    "high": candle["high"],
                    "low": candle["low"],
                    "index": i
                })

        # ==========================
        # Bearish Order Block
        # ==========================
        elif candle["close"] > candle["open"]:

            next1 = candles[i + 1]
            next2 = candles[i + 2]

            if (
                next1["close"] < next1["open"]
                and next2["close"] < next2["open"]
                and next2["close"] < candle["low"]
            ):

                order_blocks.append({
                    "type": "Bearish",
                    "high": candle["high"],
                    "low": candle["low"],
                    "index": i
                })

    return order_blocks
def detect_liquidity_sweep(candles, swing_highs, swing_lows):

    sweeps = []

    # Swing High Sweeps
    for index, level in swing_highs:

        for i in range(index + 1, len(candles)):

            if (
                candles[i]["high"] > level
                and candles[i]["close"] < level
            ):
                sweeps.append({
                    "type": "Bearish Sweep",
                    "level": level,
                    "index": i
                })
                break

    # Swing Low Sweeps
    for index, level in swing_lows:

        for i in range(index + 1, len(candles)):

            if (
                candles[i]["low"] < level
                and candles[i]["close"] > level
            ):
                sweeps.append({
                    "type": "Bullish Sweep",
                    "level": level,
                    "index": i
                })
                break

    return sweeps
def order_block_retest(candles, order_blocks):

    if not order_blocks:
        return False

    latest = order_blocks[-1]

    last_candle = candles[-1]

    high = latest["high"]
    low = latest["low"]

    if low <= last_candle["close"] <= high:
        return True

    return False
def premium_discount(candles):

    highest = max(c["high"] for c in candles)
    lowest = min(c["low"] for c in candles)

    equilibrium = (highest + lowest) / 2

    current = candles[-1]["close"]

    if current > equilibrium:
        return "PREMIUM"

    elif current < equilibrium:
        return "DISCOUNT"

    return "EQUILIBRIUM"
def get_valid_order_block(order_blocks, trend):

    if not order_blocks:
        return None

    # সর্বশেষ থেকে খুঁজবে
    for ob in reversed(order_blocks):

        if trend == "BULLISH" and ob["type"] == "Bullish":
            return ob

        if trend == "BEARISH" and ob["type"] == "Bearish":
            return ob

    return None
def get_valid_fvg(fvgs, trend):

    if not fvgs:
        return None

    for fvg in reversed(fvgs):

        if trend == "BULLISH" and fvg["type"] == "Bullish":
            return fvg

        if trend == "BEARISH" and fvg["type"] == "Bearish":
            return fvg

    return None
def fvg_retest(candles, valid_fvg):

    if valid_fvg is None:
        return False

    last_close = candles[-1]["close"]

    if valid_fvg["low"] <= last_close <= valid_fvg["high"]:
        return True

    return False