def score_zones(
    order_blocks,
    fvgs,
    sweeps,
    ob_retest,
    fvg_retest,
):

    buy_score = 0
    sell_score = 0
    reasons = []

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

        if fvg_retest:
            buy_score += 15
            sell_score += 15
            reasons.append("FVG Retest")

    # =========================
    # Liquidity Sweep
    # =========================

    if sweeps:

        latest = sweeps[-1]

        if latest["type"] == "Bullish Sweep":
            buy_score += 10
        else:
            sell_score += 10

        reasons.append("Liquidity Sweep")

    return buy_score, sell_score, reasons