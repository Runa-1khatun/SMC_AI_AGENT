import MetaTrader5 as mt5

def connect():

    if not mt5.initialize():
        print("MT5 Connection Failed")
        print("Error:", mt5.last_error())
        return False

    print("MT5 Connected Successfully")
    return True


def disconnect():
    mt5.shutdown()


def get_candles(symbol="XAUUSDm", timeframe=None, bars=100):

    if timeframe is None:
        timeframe = mt5.TIMEFRAME_M15

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        bars
    )

    return rates