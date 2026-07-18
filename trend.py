def get_trend(ema50, ema200):

    if ema50 > ema200:
        return "BULLISH"

    elif ema50 < ema200:
        return "BEARISH"

    return "SIDEWAYS"