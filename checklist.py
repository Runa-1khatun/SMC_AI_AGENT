def trade_checklist(
    trend_h4,
    trend_h1,
    entry_signal,
    ob_retest,
    fvg_retest,
):

    checks = {}

    checks["HTF Alignment"] = (trend_h4 == trend_h1)
    checks["Entry Signal"] = (entry_signal != "NO ENTRY")
    checks["Order Block Retest"] = ob_retest
    checks["FVG Retest"] = fvg_retest

    return checks