import mt5_data
import smc
import strategy
import risk
import chart
import indicators
import trend

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
    candles = mt5_data.get_candles()
    df = indicators.add_ema(candles)

    ema50 = df["EMA50"].iloc[-1]
    ema200 = df["EMA200"].iloc[-1]

    print()
    print("========== TREND ==========")

    trend_result = trend.get_trend(ema50, ema200)
    print("Trend :", trend_result)

    highs, lows = smc.find_swings(candles, lookback=3)

    bos = smc.detect_bos(candles, highs, lows)
    choch = smc.detect_choch(candles, highs, lows)
    fvg = smc.detect_fvg(candles)
    order_blocks = smc.detect_order_blocks(candles)
    sweeps = smc.detect_liquidity_sweep(candles, highs, lows)
    decision, confidence, reasons = strategy.trade_decision(
    trend_result,
    bos,
    choch,
    fvg,
    order_blocks,
    sweeps,
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