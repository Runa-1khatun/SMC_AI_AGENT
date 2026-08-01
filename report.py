def show_smc_report(
    highs,
    lows,
    bos,
    choch,
    mss_signal,
    fvgs,
    valid_fvg,
    fvg_retest,
    order_blocks,
    valid_ob,
    ob_retest,
    sweeps,
):

    print("========== SMC REPORT ==========")
    print("Swing Highs:", len(highs))
    print("Swing Lows :", len(lows))
    print("BOS :", bos)
    print("CHoCH :", choch)
    print("MSS :", mss_signal)
    print("FVG :", len(fvgs))

    if valid_fvg:
        print("Valid FVG :", valid_fvg)
        print("FVG Retest :", fvg_retest)

    print("Order Blocks :", len(order_blocks))
    print("Liquidity Sweeps :", len(sweeps))
    print("Order Block Retest :", ob_retest)

    if valid_ob:
        print("Valid Order Block :", valid_ob)

    if sweeps:
        print("Latest Sweep :", sweeps[-1])


def show_trade_checklist(checks):
    print("\n========== TRADE CHECKLIST ==========")

    for name, status in checks.items():
        print(f"{name:<22}: {'YES' if status else 'NO'}")


def show_ai_decision(
    buy_score,
    sell_score,
    decision,
    confidence,
    reasons,
):
    """Print AI decision summary.

    reasons should be an iterable of strings.
    """
    print()
    print("========== AI DECISION ==========")
    print("Buy Score :", buy_score)
    print("Sell Score:", sell_score)
    print("Decision :", decision)
    print("Confidence :", confidence, "%")

    print("Reasons :")
    if reasons:
        for reason in reasons:
            print("-", reason)
    else:
        print("- None")


def show_trade(trade):
    if not trade:
        return

    print()
    print("========== TRADE ==========")
    print("Entry :", trade["entry"])
    print("SL    :", trade["sl"])
    print("TP    :", trade["tp"])
    print("RR    :", trade["rr"])