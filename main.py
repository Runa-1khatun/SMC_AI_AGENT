import MetaTrader5 as mt5
import mt5_data
import smc
import strategy
import risk
import chart
import indicators
import trend
import entry

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

highs, lows = smc.find_swings(candles, lookback=3)

bos = smc.detect_bos(candles_m15, highs, lows)
choch = smc.detect_choch(candles_m15, highs, lows)
fvg = smc.detect_fvg(candles_m15)
order_blocks = smc.detect_order_blocks(candles_m15)
sweeps = smc.detect_liquidity_sweep(candles_m15, highs, lows)
decision, confidence, reasons = strategy.trade_decision(
    trend_result,
    bos,
    choch,
    fvg,
    order_blocks,
    sweeps,
    entry_signal,
)
trade = risk.calculate_trade(decision, candles, highs, lows)

print("========== SMC REPORT ==========")
print("Swing Highs:", len(highs))
print("Swing Lows :", len(lows))
print("BOS :", bos)
print("CHoCH :", choch)
print("FVG :", len(fvg))
print("Order Blocks :", len(order_blocks))
print("Liquidity Sweeps :", len(sweeps))
chart.plot_chart(candles, highs, lows, bos)

mt5_data.disconnect()

if order_blocks:
    print("Latest Order Block :", order_blocks[-1])

if sweeps:
    print("Latest Sweep :", sweeps[-1])

print()
print("========== AI DECISION ==========")
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