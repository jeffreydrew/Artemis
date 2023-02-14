import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3


class Manager:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()

    def commit(self):
        try:
            self.conn.commit()
        except:
            print("Error committing to database")
        
    def test_strategy(self):
        
        pass

    def RisingRSI(self):
        # calculate RSI when it has three rising lows
        # math stuff
        # rsi = 100 - (100 / (1 + RS))
        # RS = average gain of last 14 days / average loss of last 14 periods

        return

    # calculate the RSI of the last 14 periods, starts on the 15th period
    def __calculate_rsi(self):
        # connect to the candlestick database and pull the price of the last 14 periods
        
        # select the last 14 rows
        self.c.execute("SELECT * FROM candles ORDER BY id DESC LIMIT 14")
        rows = self.c.fetchall()


        # put the last 14 close prices into a list
        close_prices = []
        for i in range(14):
            close_prices.append(rows[-i][4])

        # calculate the average gain and loss of the last 14 periods
        average_gain = 0
        average_loss = 0
        for i in range(14):
            if close_prices[i] > close_prices[i + 1]:
                average_gain += close_prices[i] - close_prices[i + 1]
            else:
                average_loss += close_prices[i + 1] - close_prices[i]
        average_gain = average_gain / 14
        average_loss = average_loss / 14

        rs = average_gain / average_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi

    def __calculate_macd(self, data: str):
        
        # select the last 14 rows
        self.c.execute("SELECT * FROM candles ORDER BY id DESC LIMIT 14")
        rows = self.c.fetchall()

        # put the last 14 close prices into a list
        close_prices = []
        for i in range(14):
            close_prices.append(rows[-i][4])

        # calculate the 12 and 26 period moving averages
        short_period = 12
        long_period = 26
        short_moving_average = 0
        long_moving_average = 0
        for i in range(short_period):
            short_moving_average += close_prices[i]
        for i in range(long_period):
            long_moving_average += close_prices[i]

        short_moving_average = short_moving_average / short_period
        long_moving_average = long_moving_average / long_period

        # calculate the MACD
        macd = short_moving_average - long_moving_average

        return macd
