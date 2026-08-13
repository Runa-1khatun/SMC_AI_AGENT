import analysis
import decision
import entry_confirmation
import indicators
import trend


def get_historical_killzone(candle):
    timestamp = candle["time"]

    from datetime import datetime

    dt = datetime.utcfromtimestamp(timestamp)

    current = dt.hour + (dt.minute / 60)

    # London Kill Zone
    if 7 <= current < 10:
        return "LONDON"

    # New York Kill Zone
    elif 13 <= current < 16:
        return "NEWYORK"

    return "NONE"


def check_trade_result(candles, start_index, trade):

    if trade is None:
        return "NO RESULT"

    entry = trade["entry"]
    sl = trade["sl"]
    tp = trade["tp"]

    # Signal candle-এর পরের candle থেকে check করবে
    for candle in candles[start_index + 1:]:

        high = candle["high"]
        low = candle["low"]

        # BUY
        if trade["decision"] == "BUY":

            # একই candle-এ দুটোই hit হলে conservative ভাবে LOSS
            if low <= sl and high >= tp:
                return "LOSS"

            if low <= sl:
                return "LOSS"

            if high >= tp:
                return "WIN"

        # SELL
        elif trade["decision"] == "SELL":

            # একই candle-এ দুটোই hit হলে conservative ভাবে LOSS
            if high >= sl and low <= tp:
                return "LOSS"

            if high >= sl:
                return "LOSS"

            if low <= tp:
                return "WIN"

    return "OPEN"


def run_backtest(candles, candles_h4, candles_h1):

    # =========================
    # Pre-calculate EMA
    # =========================

    df_h4_all = indicators.add_ema(candles_h4)
    df_h1_all = indicators.add_ema(candles_h1)

    total_trades = 0
    wins = 0
    losses = 0
    open_trades = 0
    trade_log = []

    for i in range(100, len(candles) - 1):

        history = candles[:i]

        current_time = history[-1]["time"]

        # =========================
        # Historical H4 candles
        # =========================

        h4_history = candles_h4[candles_h4["time"] <= current_time]
        h1_history = candles_h1[candles_h1["time"] <= current_time]

        # পর্যাপ্ত candle না থাকলে skip
        if len(h4_history) < 200 or len(h1_history) < 200:
            continue

        # =========================
        # Historical H4 Trend
        # =========================

        h4_rows = df_h4_all[df_h4_all["time"] <= current_time]

        if len(h4_rows) < 200:
            continue

        trend_h4 = trend.get_trend(
            h4_rows["EMA50"].iloc[-1],
            h4_rows["EMA200"].iloc[-1],
)

        # =========================
        # Historical H1 Trend
        # =========================

        h1_rows = df_h1_all[df_h1_all["time"] <= current_time]

        if len(h1_rows) < 200:
            continue

        trend_h1 = trend.get_trend(
            h1_rows["EMA50"].iloc[-1],
            h1_rows["EMA200"].iloc[-1],
)
        # =========================
        # SMC Analysis
        # =========================

        (
            highs,
            lows,
            equal_highs,
            equal_lows,
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
            ote_zone,
        ) = analysis.analyze_market(
            history,
            trend_h4,
            trend_h1,
            "NO ENTRY",
        )

        # =========================
        # Historical Kill Zone
        # =========================

        killzone = get_historical_killzone(history[-1])

        # =========================
        # Entry Confirmation
        # =========================

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

        # =========================
        # Decision
        # =========================

        result = decision.make_decision(
            history,
            highs,
            lows,
            equal_highs,
            equal_lows,
            history[-1]["close"],
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
            "NO ENTRY",
            ob_retest,
            fvg_retest,
        )

        trade_decision = result["decision"]

        if trade_decision == "NO TRADE":
            continue

        # =========================
        # Entry / SL / TP
        # =========================

        import risk

        trade = risk.calculate_trade(
            trade_decision,
            history,
            highs,
            lows,
        )

        if trade is None:
            continue

        trade["decision"] = trade_decision

        total_trades += 1

        # =========================
        # Check Result
        # =========================

        trade_result = check_trade_result(
            candles,
            i,
            trade,
        )

        if trade_result == "WIN":
            wins += 1

        elif trade_result == "LOSS":
            losses += 1

        elif trade_result == "OPEN":
            open_trades += 1

        trade_log.append({
            "time": history[-1]["time"],
            "decision": trade_decision,
            "entry": trade["entry"],
            "sl": trade["sl"],
            "tp": trade["tp"],
            "result": trade_result,
            "trend_h4": trend_h4,
            "trend_h1": trend_h1,
            "bos": bos,
            "choch": choch,
            "mss": mss_signal,
            "ob_retest": ob_retest,
            "fvg_retest": fvg_retest,
            "killzone": killzone,
        })
        # =========================
    # Backtest Statistics
    # =========================

    closed_trades = wins + losses

    if closed_trades > 0:
        win_rate = (wins / closed_trades) * 100
    else:
        win_rate = 0

    buy_trades = 0
    sell_trades = 0

    for trade in trade_log:

        if trade["decision"] == "BUY":
            buy_trades += 1

        elif trade["decision"] == "SELL":
            sell_trades += 1

    # =========================
    # Losing Streak
    # =========================

    current_loss_streak = 0
    max_loss_streak = 0

    for trade in trade_log:

        if trade["result"] == "LOSS":

            current_loss_streak += 1

            if current_loss_streak > max_loss_streak:
                max_loss_streak = current_loss_streak

        else:
            current_loss_streak = 0

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "open_trades": open_trades,
        "win_rate": round(win_rate, 2),
        "buy_trades": buy_trades,
        "sell_trades": sell_trades,
        "max_loss_streak": max_loss_streak,
        "trade_log": trade_log,
    }