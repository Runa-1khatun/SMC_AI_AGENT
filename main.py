import MetaTrader5 as mt5
import mt5_data
import smc
import strategy
import risk
import chart
import indicators
import trend
import entry
import confluence
import structure
import orderblock
import fvg
import liquidity

# initialize defaults to avoid NameError when not connected
candles = []
highs, lows = [], []
bos = None
choch = None
fvg = []
order_blocks = []
sweeps = []
decision = None
confidence = None
reasons = []
trade = None

if mt5_data.connect():

    candles_h1 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_H1)
    candles_m15 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_M15)
    candles_m5 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_M5)

    print("H1 Candles :", len(candles_h1))
    print("M15 Candles:", len(candles_m15))
    print("M5 Candles :", len(candles_m5))

    df_h1 = indicators.add_ema(candles_h1)

    ema50_h1 = df_h1["EMA50"].iloc[-1]
    ema200_h1 = df_h1["EMA200"].iloc[-1]

    trend_h1 = trend.get_trend(ema50_h1, ema200_h1)

    print("H1 Trend :", trend_h1)
    entry_signal = entry.confirm_entry(candles_m5)
    print("Entry Signal :", entry_signal)

    candles = candles_m15

df = indicators.add_ema(candles)

ema50 = df["EMA50"].iloc[-1]
ema200 = df["EMA200"].iloc[-1]

print()
print("========== TREND ==========")

trend_result = trend_h1

print("Trend :", trend_result)

highs, lows = structure.find_swings(candles, lookback=3)

bos = structure.detect_bos(candles_m15, highs, lows)
choch = structure.detect_choch(candles_m15, highs, lows)
bias = structure.structure_bias(
    trend_result,
    bos,
    choch,
)

print("Structure Bias :", bias)
pd_zone = smc.premium_discount(candles)

print("Premium/Discount :", pd_zone)
fvg = fvg.detect_fvg(candles_m15)
order_blocks = orderblock.detect_order_blocks(candles_m15)
valid_order_block = orderblock.get_valid_order_block(order_blocks, trend_result)
sweeps = liquidity.detect_liquidity_sweep(candles_m15, highs, lows)
ob_retest = orderblock.order_block_retest(candles, order_blocks)
valid_ob = orderblock.get_valid_order_block(
    order_blocks,
    trend_result,
)
valid_fvg = fvg.get_valid_fvg(
    fvg,
    trend_result,
)

fvg_retest = fvg.fvg_retest(
    candles,
    valid_fvg,
)
decision, confidence, reasons, buy_score, sell_score = confluence.analyze(
    trend_result,
    bos,
    choch,
    order_blocks,
    fvg,
    sweeps,
    entry_signal,
    ob_retest,
    fvg_retest,
)

confidence = max(buy_score, sell_score)
trade = risk.calculate_trade(decision, candles, highs, lows)

print("========== SMC REPORT ==========")
print("Swing Highs:", len(highs))
print("Swing Lows :", len(lows))
print("BOS :", bos)
print("CHoCH :", choch)
print("FVG :", len(fvg))
if valid_fvg:
    print("Valid FVG :", valid_fvg)
    print("FVG Retest :", fvg_retest)
print("Order Blocks :", len(order_blocks))
print("Liquidity Sweeps :", len(sweeps))
print("Order Block Retest :", ob_retest)
chart.plot_chart(candles, highs, lows, bos)

mt5_data.disconnect()

if valid_ob:
    print("Valid Order Block :", valid_ob)

if sweeps:
    print("Latest Sweep :", sweeps[-1])

print()
print("========== AI DECISION ==========")
print("Buy Score :", buy_score)
print("Sell Score:", sell_score)
print("Decision :", decision)
print("Confidence :", confidence, "%")


print("Reasons :")
for r in reasons:
    print("-", r)

if trade:
    print()
    print("========== TRADE ==========")
    print("Entry :", trade["entry"])
    print("SL    :", trade["sl"])
    print("TP    :", trade["tp"])
    print("RR    :", trade["rr"])