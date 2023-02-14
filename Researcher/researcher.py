import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yfinance as yf


class Researcher:
    def __init__(self):
        pass

    def get_last_ticker(self, symbol: str):
        # get 1 minute ticker info for aapl from today
        ticker = yf.Ticker(symbol)
        ticker_data = ticker.history(period="1d", interval="1m")
        return ticker_data.iloc[-1]


r = Researcher()
print(r.get_last_ticker("aapl"))
