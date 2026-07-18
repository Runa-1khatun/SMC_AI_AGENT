import matplotlib.pyplot as plt

def plot_chart(candles, highs, lows, bos):

    closes = [c["close"] for c in candles]

    plt.figure(figsize=(14, 6))
    plt.plot(closes, label="Close Price")

    # Swing High
    for i, price in highs:
        plt.scatter(i, price, marker="^", s=80, color="red")
        plt.text(i, price, "SH", fontsize=8)

    # Swing Low
    for i, price in lows:
        plt.scatter(i, price, marker="v", s=80, color="green")
        plt.text(i, price, "SL", fontsize=8)
    # Break of Structure label (outside the loops)
    # Break of Structure label (outside the loops)
    if bos == "Bullish BOS":
        plt.text(
            2,
            max(closes) + 2,
            "BULLISH BOS",
            fontsize=14,
            color="green",
            weight="bold"
        )
    elif bos == "Bearish BOS":
        plt.text(
            2,
            max(closes) + 2,
            "BEARISH BOS",
            fontsize=14,
            color="red",
            weight="bold"
        )

    plt.title("SMC AI Chart")
    plt.xlabel("Candles")
    plt.ylabel("Price")
    plt.legend()

    plt.show()