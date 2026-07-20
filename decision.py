import confluence
import checklist
import risk


def make_decision(
    candles,
    highs,
    lows,
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

    decision, confidence, reasons, buy_score, sell_score = confluence.analyze(
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
    )

    checks = checklist.trade_checklist(
        trend_h4,
        trend_h1,
        entry_signal,
        ob_retest,
        fvg_retest,
    )

    confidence = max(buy_score, sell_score)

    trade = risk.calculate_trade(
        decision,
        candles,
        highs,
        lows,
    )

    return {
        "decision": decision,
        "confidence": confidence,
        "reasons": reasons,
        "buy_score": buy_score,
        "sell_score": sell_score,
        "checks": checks,
        "trade": trade,
    }