import trend_score
import structure_score
import zone_score
import session_filter
import killzone
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
    session = session_filter.get_session()
    kill_zone = killzone.get_killzone()
    buy_score = 0
    sell_score = 0
    reasons = []

    # =========================
    # Trend Scores
    # =========================

    buy_trend_score, sell_trend_score, trend_reasons = trend_score.score_trend(trend_h4, trend_h1)
    buy_score += buy_trend_score
    sell_score += sell_trend_score
    reasons.extend(trend_reasons)

    # =========================
    # Structure Scores
    # =========================

    buy_structure_score, sell_structure_score, structure_reasons = structure_score.score_structure(bos, choch, trend_h4)
    buy_score += buy_structure_score
    sell_score += sell_structure_score
    reasons.extend(structure_reasons)

    # =========================
    # Zone Scores
    # =========================

    buy_zone_score, sell_zone_score, zone_reasons = zone_score.score_zones(order_blocks, fvgs, sweeps, ob_retest, fvg_retest)
    buy_score += buy_zone_score
    sell_score += sell_zone_score
    reasons.extend(zone_reasons)

    # =========================
    # Entry
    # =========================

    if entry_signal == "BUY":
        buy_score += 15
    elif entry_signal == "SELL":
        sell_score += 15

    # =========================
    # Session Score
    # =========================

    if session == "ASIAN":
        buy_score -= 10
        sell_score -= 10
        reasons.append("Asian Session")

    elif session == "CLOSED":
        buy_score -= 100
        sell_score -= 100
        reasons.append("Market Closed")

    # =========================
    # Kill Zone Score
    # =========================

    if kill_zone == "LONDON":
       buy_score += 10
       sell_score += 10
       reasons.append("London Kill Zone")

    elif kill_zone == "NEWYORK":
         buy_score += 10
         sell_score += 10
         reasons.append("New York Kill Zone")

    elif kill_zone == "OVERLAP":
        buy_score += 20
        sell_score += 20
        reasons.append("London/New York Overlap")

    else:
        buy_score -= 10
        sell_score -= 10
        reasons.append("Outside Kill Zone")

    # =========================
    # Trend Filter
    # =========================

    if trend_h4 == "BEARISH":
        if bos == "Bullish BOS":
            reasons.append("Counter Trend BOS")

        if choch == "Bullish CHoCH":
            reasons.append("Counter Trend CHoCH")

    elif trend_h4 == "BULLISH":
        if bos == "Bearish BOS":
            reasons.append("Counter Trend BOS")

        if choch == "Bearish CHoCH":
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