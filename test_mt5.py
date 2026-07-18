import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 Connection Failed")
    quit()

symbol = "XAUUSDm"

rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 10)

for candle in rates:
    print(candle)

mt5.shutdown()