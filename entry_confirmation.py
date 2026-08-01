def confirm_entry(
    trend_h4,
    trend_h1,
    bos,
    choch,
    mss_signal,
    ob_retest,
    fvg_retest,
    killzone,
):

    # BUY Confirmation
    if (
        trend_h4 == "BULLISH"
        and trend_h1 == "BULLISH"
        and bos == "Bullish BOS"
        and (
            choch == "Bullish CHoCH"
            or mss_signal == "Bullish MSS"
        )
        and ob_retest
        and fvg_retest
        and killzone in ("LONDON", "NEW_YORK")
    ):
        return "BUY"

    # SELL Confirmation
    if (
        trend_h4 == "BEARISH"
        and trend_h1 == "BEARISH"
        and bos == "Bearish BOS"
        and (
            choch == "Bearish CHoCH"
            or mss_signal == "Bearish MSS"
        )
        and ob_retest
        and fvg_retest
        and killzone in ("LONDON", "NEW_YORK")
    ):
        return "SELL"

    return "WAIT"