def trade_decision(trend, bos, choch, fvgs, order_blocks, sweeps, entry_signal):

    reasons = []
    confidence = 0

    # Trend
    if trend == "BULLISH":
        reasons.append("Bullish Trend")
    elif trend == "BEARISH":
        reasons.append("Bearish Trend")

    # BOS
    if bos == "Bullish BOS":
        reasons.append("Bullish BOS")
    elif bos == "Bearish BOS":
        reasons.append("Bearish BOS")

    # CHoCH
    if choch == "Bullish CHoCH":
        reasons.append("Bullish CHoCH")
    elif choch == "Bearish CHoCH":
        reasons.append("Bearish CHoCH")

    # Extra confirmations
    if fvgs:
        reasons.append("FVG Found")

    if order_blocks:
        reasons.append("Order Block Found")

    if sweeps:
        reasons.append("Liquidity Sweep")

    # Smart Decision
    if (
        trend == "BEARISH"
        and bos == "Bearish BOS"
        and choch == "Bearish CHoCH"
        and entry_signal == "SELL"
    ):
        decision = "SELL"

    elif (
        trend == "BULLISH"
        and bos == "Bullish BOS"
        and choch == "Bullish CHoCH"
        and entry_signal == "BUY"
    ):
        decision = "BUY"

    else:
        decision = "NO TRADE"

    confidence = 40

    return decision, confidence, reasons