import MetaTrader5 as mt5


def connect():
    if not mt5.initialize():
        print("MT5 Connection Failed")
        return False
    return True


def disconnect():
    mt5.shutdown()


def get_candles(symbol="XAUUSDm", timeframe=mt5.TIMEFRAME_M15, bars=100):
    return mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)