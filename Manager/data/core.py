import os, sys
import yfinance as yf
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

restriction = 20


class DataAnalyst:
    def __init__(self):
        self.tickers = self.set_tickers()
        self.movers = self.get_top_movers()

    def set_tickers(self):
        symbols = pd.read_csv("Manager/data/sp500.csv")
        tickers = symbols["Symbol"].tolist()
        return tickers

    def get_top_movers(self):
        movers = []
        for t in self.tickers[:restriction]:
            curr = yf.Ticker(t)
            # print the closing price of curr
            c = curr.history(period="2d", interval="1d")["Close"][0]
            o = curr.history(period="2d", interval="1d")["Open"][0]
            diff = c - o
            percent_diff = diff / o * 100
            if percent_diff < 0:
                movers.append((t, abs(percent_diff), "down"))
            elif percent_diff > 0:
                movers.append((t, percent_diff, "up"))

        movers.sort(key=lambda x: x[1], reverse=True)
        # return the top 20 movers
        return movers[:20]


if __name__ == "__main__":
    da = DataAnalyst()
    for m in da.movers:
        print(m)

