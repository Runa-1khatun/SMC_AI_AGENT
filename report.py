def show_smc_report(
    highs,
    lows,
    bos,
    choch,
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