import MetaTrader5 as mt5
import mt5_data
import risk
import chart
import indicators
import trend
import entry
import confluence
import structure
import orderblock
import fvg as fvg_module
import liquidity
import pd_zone
import checklist
import market
import report

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

data = market.load_market()

candles = data["candles"]
candles_m15 = data.get("candles_m15", candles)
trend_h4 = data["trend_h4"]
trend_h1 = data["trend_h1"]
entry_signal = data["entry_signal"]

df = indicators.add_ema(candles)

ema50 = df["EMA50"].iloc[-1]
ema200 = df["EMA200"].iloc[-1]

print()
print("========== TREND ==========")

trend_result = trend_h1

print("Trend :", trend_result)

highs, lows = structure.find_swings(candles, lookback=3)

bos = structure.detect_bos(candles, highs, lows)
choch = structure.detect_choch(candles, highs, lows)
bias = structure.structure_bias(
    trend_result,
    bos,
    choch,
)

print("Structure Bias :", bias)
pd_zone = pd_zone.premium_discount(candles)

print("Premium/Discount :", pd_zone)
fvgs = fvg_module.detect_fvg(candles_m15)
order_blocks = orderblock.detect_order_blocks(candles_m15)
valid_order_block = orderblock.get_valid_order_block(order_blocks, trend_result)
sweeps = liquidity.detect_liquidity_sweep(candles_m15, highs, lows)
ob_retest = orderblock.order_block_retest(candles, order_blocks)
valid_ob = orderblock.get_valid_order_block(
    order_blocks,
    trend_result,
)
valid_fvg = fvg_module.get_valid_fvg(
    fvgs,
    trend_result,
)

fvg_retest = fvg_module.fvg_retest(
    candles,
    valid_fvg,
)
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
trade = risk.calculate_trade(decision, candles, highs, lows)

report.show_smc_report(
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
)
report.show_trade_checklist(checks)
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