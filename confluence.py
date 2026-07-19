def analyze(
    trend_h4,
    trend_h1,
    bos,
    choch,
    order_blocks,
    fvgs,
    sweeps,
    entry_signal,
    ob_retest,
    fvg_retest,
):
    buy_score = 0
    sell_score = 0
    reasons = []

    # =========================
    # H4 Trend
    # =========================
    if trend_h4 == "BULLISH":
        buy_score += 20
        reasons.append("H4 Bullish Trend")

    elif trend_h4 == "BEARISH":
        sell_score += 20
        reasons.append("H4 Bearish Trend")

    # =========================
    # H1 Trend
    # =========================

    if trend_h1 == "BULLISH":
        buy_score += 10
        reasons.append("H1 Bullish Trend")

    elif trend_h1 == "BEARISH":
        sell_score += 10
        reasons.append("H1 Bearish Trend")

    # =========================
    # Trend Alignment Bonus
    # =========================

    if trend_h4 == trend_h1:

        if trend_h4 == "BULLISH":
            buy_score += 10
            reasons.append("HTF Bullish Alignment")

        elif trend_h4 == "BEARISH":
            sell_score += 10
            reasons.append("HTF Bearish Alignment")

    # =========================
    # BOS
    # =========================

    if bos == "Bullish BOS":
        buy_score += 25
        reasons.append("Bullish BOS")

    elif bos == "Bearish BOS":
        sell_score += 25
        reasons.append("Bearish BOS")

    # =========================
    # CHoCH
    # =========================

    if choch == "Bullish CHoCH":
        buy_score += 20
        reasons.append("Bullish CHoCH")

    elif choch == "Bearish CHoCH":
        sell_score += 20
        reasons.append("Bearish CHoCH")

    # =========================
    # Order Block
    # =========================

    if order_blocks:
        latest = order_blocks[-1]

        if latest["type"] == "Bullish":
            buy_score += 10
        else:
            sell_score += 10

        reasons.append("Order Block")

        # =========================
        # Order Block Retest
        # =========================

        if ob_retest:
            buy_score += 20
            sell_score += 20
            reasons.append("Order Block Retest")

    # =========================
    # FVG
    # =========================

    if fvgs:
        buy_score += 5
        sell_score += 5
        reasons.append("FVG")

        # =========================
        # FVG Retest
        # =========================

        if fvg_retest:
            buy_score += 15
            sell_score += 15
            reasons.append("FVG Retest")

    # =========================
    # Sweep
    # =========================

    if sweeps:
        latest = sweeps[-1]
        if latest["type"] == "Bullish Sweep":
            buy_score += 10
        else:
            sell_score += 10
        reasons.append("Liquidity Sweep")

    # =========================
    # Entry
    # =========================

    if entry_signal == "BUY":
        buy_score += 15
    elif entry_signal == "SELL":
        sell_score += 15

    # =========================
    # Trend Filter
    # =========================

    if trend_h4 == "BEARISH":
        if bos == "Bullish BOS":
            buy_score -= 20
            reasons.append("Counter Trend BOS")

        if choch == "Bullish CHoCH":
            buy_score -= 15
            reasons.append("Counter Trend CHoCH")

    elif trend_h4 == "BULLISH":
        if bos == "Bearish BOS":
            sell_score -= 20
            reasons.append("Counter Trend BOS")

        if choch == "Bearish CHoCH":
            sell_score -= 15
            reasons.append("Counter Trend CHoCH")

    # Negative Score येन ना हय
    buy_score = max(0, buy_score)
    sell_score = max(0, sell_score)

    confidence = max(buy_score, sell_score)

    # =========================
    # Final Decision
    # =========================

    if buy_score > sell_score and confidence >= 70:
        decision = "BUY"

    elif sell_score > buy_score and confidence >= 70:
        decision = "SELL"

    else:
        decision = "NO TRADE"

    return decision, confidence, reasons, buy_score, sell_score