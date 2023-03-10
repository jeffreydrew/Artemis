import os, sys
import talib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import sqlite3
from config import *
import requests


class NewManager:
    def __init__(self):
        self.bars = []


# driver temp
if __name__ == "__main__":
    function = "TIME_SERIES_INTRADAY"
    symbol = "SPY"
    interval = "1min"
    apikey = ALPHA_VANTAGE_API_KEY
    reqString = f"https://www.alphavantage.com/query?function={function}&symbol={symbol}&interval={interval}&apikey={apikey}"
    print(reqString)
    r = requests.get(
        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={apikey}"
    )

    print(r.json()["Time Series (5min)"])
    df = pd.DataFrame(r.json()["Time Series (5min)"])
    #invert the rows and columns
    df = df.transpose()
    print(df)
