def detect_liquidity_sweep(candles, swing_highs, swing_lows, max_age=100):

    sweeps = []

    total_candles = len(candles)

    # =========================
    # Swing High Sweeps
    # =========================

    for index, level in swing_highs:

        # অনেক পুরোনো swing ignore
        start = index + 1
        end = min(total_candles, index + max_age + 1)

        for i in range(start, end):

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

    # =========================
    # Swing Low Sweeps
    # =========================

    for index, level in swing_lows:

        # অনেক পুরোনো swing ignore
        start = index + 1
        end = min(total_candles, index + max_age + 1)

        for i in range(start, end):

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