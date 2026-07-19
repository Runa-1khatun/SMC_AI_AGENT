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