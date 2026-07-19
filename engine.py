import MetaTrader5 as mt5
import indicators
import trend
import entry

mt5_data = mt5

def run():
    if not mt5_data.connect():
        return None, None, None, None

    candles_h4 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_H4)
    candles_h1 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_H1)
    candles_m15 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_M15)
    candles_m5 = mt5_data.get_candles(timeframe=mt5.TIMEFRAME_M5)

    print("H4 Candles :", len(candles_h4))
    print("H1 Candles :", len(candles_h1))
    print("M15 Candles:", len(candles_m15))
    print("M5 Candles :", len(candles_m5))

    df_h4 = indicators.add_ema(candles_h4)

    ema50_h4 = df_h4["EMA50"].iloc[-1]
    ema200_h4 = df_h4["EMA200"].iloc[-1]

    trend_h4 = trend.get_trend(
        ema50_h4,
        ema200_h4,
    )
    print("H4 Trend :", trend_h4)

    df_h1 = indicators.add_ema(candles_h1)

    ema50_h1 = df_h1["EMA50"].iloc[-1]
    ema200_h1 = df_h1["EMA200"].iloc[-1]

    trend_h1 = trend.get_trend(ema50_h1, ema200_h1)
    
    print("H1 Trend :", trend_h1)
    entry_signal = entry.confirm_entry(candles_m5)
    print("Entry Signal :", entry_signal)

    candles = candles_m15
    return candles, trend_h4, trend_h1, entry_signal