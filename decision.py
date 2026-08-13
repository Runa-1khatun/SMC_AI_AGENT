import confluence
import checklist
import risk


def make_decision(
    candles,
    highs,
    lows,
    equal_highs,
    equal_lows,
    current_price,
    ote_zone,
    trend_h4,
    trend_h1,
    bos,
    choch,
    mss_signal,
    displacement_signal,
    liquidity_grab_signal,
    entry_confirmation_signal,
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
        mss_signal,
        ote_zone,
        displacement_signal,
        liquidity_grab_signal,
        equal_highs,
        equal_lows,
        entry_confirmation_signal,
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