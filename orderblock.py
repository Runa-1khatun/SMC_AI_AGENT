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