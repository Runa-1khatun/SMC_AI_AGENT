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