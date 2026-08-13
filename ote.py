def detect_ote(candles, trend):

    if len(candles) < 20:
        return None

    highs = [c["high"] for c in candles[-20:]]
    lows = [c["low"] for c in candles[-20:]]

    swing_high = max(highs)
    swing_low = min(lows)

    if trend == "BULLISH":
        fib_62 = swing_high - (swing_high - swing_low) * 0.62
        fib_79 = swing_high - (swing_high - swing_low) * 0.79

        return {
            "type": "BUY",
            "high": round(fib_62, 3),
            "low": round(fib_79, 3),
        }

    elif trend == "BEARISH":
        fib_62 = swing_low + (swing_high - swing_low) * 0.62
        fib_79 = swing_low + (swing_high - swing_low) * 0.79

        return {
            "type": "SELL",
            "low": round(fib_62, 3),
            "high": round(fib_79, 3),
        }

    return None