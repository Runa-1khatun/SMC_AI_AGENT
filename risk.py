def calculate_trade(decision, candles, highs, lows):

    close = candles[-1]["close"]

    if decision == "BUY":

        if not lows:
            return None

        valid_lows = [low for _, low in lows if low < close]

        if not valid_lows:
            return None

        last_low = max(valid_lows)

        entry = close
        sl = last_low - 0.50
        risk = entry - sl
        tp = entry + (risk * 3)

    elif decision == "SELL":

        if not highs:
            return None

        valid_highs = [high for _, high in highs if high > close]

        if not valid_highs:
            return None

        last_high = min(valid_highs)

        entry = close
        sl = last_high + 0.50
        risk = sl - entry
        tp = entry - (risk * 3)

    else:
        return None

    return {
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp": round(tp, 2),
        "rr": "1 : 3"
    }