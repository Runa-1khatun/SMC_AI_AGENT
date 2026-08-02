import market
import report
import analysis
import decision
import session_filter
import killzone
import entry_confirmation

# initialize defaults to avoid NameError when not connected
candles = []
highs, lows = [], []
bos = None
choch = None
fvg = []
order_blocks = []
sweeps = []
# keep module name `decision` imported; do not shadow it with a variable
confidence = None
reasons = []
trade = None

data = market.load_market()

candles = data["candles"]
candles_m15 = data.get("candles_m15", candles)
trend_h4 = data["trend_h4"]
trend_h1 = data["trend_h1"]
entry_signal = data["entry_signal"]

print()
print("========== TREND ==========")

trend_result = trend_h1

print("Trend :", trend_result)

session = session_filter.get_session()
kill_zone = killzone.get_killzone()

print("Session :", session)
print("Kill Zone :", kill_zone)

(
    highs,
    lows,
    bos,
    choch,
    mss_signal,
    displacement_signal,
    liquidity_grab_signal,
    bias,
    pd_zone_result,
    fvgs,
    order_blocks,
    valid_order_block,
    sweeps,
    ob_retest,
    valid_ob,
    valid_fvg,
    fvg_retest,
) = analysis.analyze_market(
    candles,
    trend_h4,
    trend_h1,
    entry_signal,
)
entry_confirmation_signal = entry_confirmation.confirm_entry(
    trend_h4,
    trend_h1,
    bos,
    choch,
    mss_signal,
    ob_retest,
    fvg_retest,
    killzone,
)

print("MSS :", mss_signal)
print("Displacement :", displacement_signal)
print("Liquidity Grab :", liquidity_grab_signal)
print("Entry Confirmation :", entry_confirmation_signal)
print("Structure Bias :", bias)
print("Premium/Discount :", pd_zone_result)
result = decision.make_decision(
    candles,
    highs,
    lows,
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
)
trade_decision = result["decision"]
confidence = result["confidence"]
reasons = result["reasons"]
buy_score = result["buy_score"]
sell_score = result["sell_score"]
checks = result["checks"]
trade = result["trade"]

report.show_smc_report(
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
)
report.show_trade_checklist(checks)
report.show_ai_decision(
    buy_score,
    sell_score,
    trade_decision,
    confidence,
    reasons,
)
report.show_trade(trade)