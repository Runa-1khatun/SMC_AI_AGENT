def score_trend(trend_h4, trend_h1):

    buy_score = 0
    sell_score = 0
    reasons = []

    # H4 Trend

    if trend_h4 == "BULLISH":
        buy_score += 20
        reasons.append("H4 Bullish Trend")

    elif trend_h4 == "BEARISH":
        sell_score += 20
        reasons.append("H4 Bearish Trend")

    # H1 Trend

    if trend_h1 == "BULLISH":
        buy_score += 10
        reasons.append("H1 Bullish Trend")

    elif trend_h1 == "BEARISH":
        sell_score += 10
        reasons.append("H1 Bearish Trend")

    # Alignment Bonus

    if trend_h4 == trend_h1:

        if trend_h4 == "BULLISH":
            buy_score += 10
            reasons.append("HTF Bullish Alignment")

        elif trend_h4 == "BEARISH":
            sell_score += 10
            reasons.append("HTF Bearish Alignment")

    return buy_score, sell_score, reasons