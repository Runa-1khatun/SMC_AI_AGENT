def detect_liquidity_grab(candles, sweeps):

    if not sweeps:
        return "No Liquidity Grab"

    latest_sweep = sweeps[-1]

    sweep_type = latest_sweep["type"]
    sweep_index = latest_sweep["index"]

    # খুব পুরোনো Sweep হলে Ignore
    if len(candles) - sweep_index > 5:
        return "No Liquidity Grab"

    if sweep_type == "Bullish Sweep":
        return "Bullish Liquidity Grab"

    elif sweep_type == "Bearish Sweep":
        return "Bearish Liquidity Grab"

    return "No Liquidity Grab"