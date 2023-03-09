import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yfinance as yf
import sqlite3


class Researcher:
    def __init__(self, path, symbol, period, interval):
        self.path = path
        self.symbol = symbol
        self.period = period
        self.interval = interval
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    # --------------------------------------------------
    #                   Database stuff
    # --------------------------------------------------

    def clear_table(self):
        self.cursor.execute("DELETE FROM {}".format(f"{self.symbol}_{self.period}_{self.interval}"))
        self.conn.commit()

    def create_table(self):
        self.cursor.execute(
            "DROP TABLE IF EXISTS {}".format(
                f"{self.symbol}_{self.period}_{self.interval}"
            )
        )
        # # clear table
        # c.execute("DELETE FROM {}".format(f"{t.symbol}"))
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (Time text, Open real, High real, Low real, Close real, Volume real)".format(
                f"{self.symbol}_{self.period}_{self.interval}"
            )
        )

    def add_candle(self, candle, time):
        self.cursor.execute(
            "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)".format(
                f"{self.symbol}_{self.period}_{self.interval}"
            ),
            (
                time, #date, minutes
                candle["Open"],
                candle["High"],
                candle["Low"],
                candle["Close"],
                candle["Volume"],
            ),
        )
        self.conn.commit()

    def get_last_ticker(self):
        # get 1 minute ticker info for aapl from today
        ticker = yf.Ticker(self.symbol)
        ticker_data = ticker.history(period="1d", interval="1m")
        return ticker_data.iloc[-1]


