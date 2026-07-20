import structure
import orderblock
import fvg as fvg_module
import liquidity
import pd_zone

def analyze_market(
    candles,
    trend_h4,
    trend_h1,
    entry_signal,
):
    highs, lows = structure.find_swings(candles, lookback=3)

    bos = structure.detect_bos(candles, highs, lows)
    choch = structure.detect_choch(candles, highs, lows)
    bias = structure.structure_bias(
        trend_h4,
        bos,
        choch,
    )

    pd_zone_result = pd_zone.premium_discount(candles)

    fvgs = fvg_module.detect_fvg(candles)
    order_blocks = orderblock.detect_order_blocks(candles)
    valid_order_block = orderblock.get_valid_order_block(order_blocks, trend_h4)
    sweeps = liquidity.detect_liquidity_sweep(candles, highs, lows)
    ob_retest = orderblock.order_block_retest(candles, order_blocks)
    valid_ob = orderblock.get_valid_order_block(
        order_blocks,
        trend_h4,
    )
    valid_fvg = fvg_module.get_valid_fvg(
        fvgs,
        trend_h4,
    )

    fvg_retest = fvg_module.fvg_retest(
        candles,
        valid_fvg,
    )
    return (
        highs,
        lows,
        bos,
        choch,
        bias,
        pd_zone_result,
        fvgs,
        order_blocks,
        valid_order_block,
        sweeps,
        ob_retest,
        valid_ob,
        valid_fvg,
        fvg_retest
    )