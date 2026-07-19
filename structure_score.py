def score_structure(
    bos,
    choch,
    trend_h4,
):

    buy_score = 0
    sell_score = 0
    reasons = []

    # =========================
# BOS
# =========================
    if bos == "Bullish BOS":

        if trend_h4 == "BULLISH":
            buy_score += 25
        else:
            buy_score += 5

        reasons.append("Bullish BOS")


    elif bos == "Bearish BOS":

        if trend_h4 == "BEARISH":
            sell_score += 25
        else:
            sell_score += 5

        reasons.append("Bearish BOS")
    # =========================
    # CHoCH
    # =========================

    if choch == "Bullish CHoCH":

        if trend_h4 == "BULLISH":
            buy_score += 20
        else:
            buy_score += 5

        reasons.append("Bullish CHoCH")


    elif choch == "Bearish CHoCH":

        if trend_h4 == "BEARISH":
            sell_score += 20
        else:
            sell_score += 5

        reasons.append("Bearish CHoCH")

    return buy_score, sell_score, reasons