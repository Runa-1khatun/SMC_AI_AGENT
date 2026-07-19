import MetaTrader5 as mt5
import mt5_data
import indicators
import trend
import entry


def load_market():

    if not mt5_data.connect():
        return None

    candles_h4 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_H4)
    candles_h1 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_H1)
    candles_m15 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_M15)
    candles_m5 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_M5)

    print("H4 Candles :", len(candles_h4))
    print("H1 Candles :", len(candles_h1))
    print("M15 Candles:", len(candles_m15))
    print("M5 Candles :", len(candles_m5))

    df_h4 = indicators.add_ema(candles_h4)

    trend_h4 = trend.get_trend(
        df_h4["EMA50"].iloc[-1],
        df_h4["EMA200"].iloc[-1],
    )

    print("H4 Trend :", trend_h4)

    df_h1 = indicators.add_ema(candles_h1)

    trend_h1 = trend.get_trend(
        df_h1["EMA50"].iloc[-1],
        df_h1["EMA200"].iloc[-1],
    )

    print("H1 Trend :", trend_h1)

    entry_signal = entry.confirm_entry(candles_m5)

    print("Entry Signal :", entry_signal)

    return {
        "candles": candles_m15,
        "trend_h4": trend_h4,
        "trend_h1": trend_h1,
        "entry_signal": entry_signal,
    }