def detect_equal_levels(highs, lows, tolerance=2.0):

    equal_highs = []
    equal_lows = []

    # Equal High
    for i in range(len(highs) - 1):
        h1 = highs[i][1]
        h2 = highs[i + 1][1]

        if abs(h1 - h2) <= tolerance:
            equal_highs.append(
                {
                    "level": round((h1 + h2) / 2, 3),
                    "index": highs[i + 1][0],
                }
            )

    # Equal Low
    for i in range(len(lows) - 1):
        l1 = lows[i][1]
        l2 = lows[i + 1][1]

        if abs(l1 - l2) <= tolerance:
            equal_lows.append(
                {
                    "level": round((l1 + l2) / 2, 3),
                    "index": lows[i + 1][0],
                }
            )

    return equal_highs, equal_lows