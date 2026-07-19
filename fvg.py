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