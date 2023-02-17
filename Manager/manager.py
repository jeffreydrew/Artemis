import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3


class Account:
    def __init__(self, balance: float):
        self.__principle = balance
        self.balance = balance
        self.cost_basis = 0

    def get_principle(self):
        return self.__principle


class Manager:
    def __init__(self, database_path: str, symbol):
        self.database_path = database_path
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()
        self.portfolio = {}
        self.rsi = []
        self.orders = {"buys": 0, "sells": 0}
        self.account = Account(10000)
        self.symbol = symbol

    def commit(self):
        try:
            self.conn.commit()
        except:
            print("Error committing to database")

    def unit_test_strategy(self, symbol: str, period: str, interval: str, now, end):
        # get last close price
        self.cursor.execute(
            "SELECT * FROM {} ORDER BY Id DESC LIMIT 1".format(
                f"{symbol}_{period}_{interval}"
            )
        )
        row = self.cursor.fetchone()
        close_price = row[4]
        # execute one buy order at the first price
        if now == 1:
            return self.buy_signal(self.account.balance / close_price, close_price)
        # execute one sell order at the last price
        if now == end:
            return self.sell_signal(1, close_price, "all")

    def test_strategy(self, symbol: str, period: str, interval: str, now, end):
        # if price of last period is greater than the price of the period before that and portfolio is 0, buy
        # if price of last period is less than the price of the period before that and portfolio is 1, sell
        # if price of last period is less than the price of the period before that and portfolio is 0, do nothing
        # if price of last period is greater than the price of the period before that and portfolio is 1, do nothing

        # select the last 2 rows from the table named symbol and put the close prices into a list
        self.cursor.execute(
            "SELECT * FROM {} ORDER BY Id DESC LIMIT 2".format(
                f"{symbol}_{period}_{interval}"
            )
        )
        rows = self.cursor.fetchall()
        close_prices = []
        for i in range(2):
            close_prices.append(rows[-i][4])
        if len(close_prices) < 2:
            close_prices.prepend(0)

        # if the price of the last period is greater than the price of the period before that and portfolio is 0, buy
        if close_prices[0] > close_prices[1]:
            self.portfolio = 1
            return self.buy_signal(
                self.account.balance / close_prices[0], close_prices[0]
            )
        # if the price of the last period is less than the price of the period before that and portfolio is 1, sell
        elif close_prices[0] < close_prices[1] and self.portfolio != 0:
            self.portfolio = 0
            return self.sell_signal(1, close_prices[0], "all")

        if now == end:
            return self.sell_signal(1, close_prices[0], "all")

        return

    def RisingRSI(self):
        # calculate RSI when it has three rising lows
        # math stuff
        # rsi = 100 - (100 / (1 + RS))
        # RS = average gain of last 14 days / average loss of last 14 periods

        return

    def FallingRSI(self):
        # calculate RSI when it has three falling highs
        # math stuff
        # rsi = 100 - (100 / (1 + RS))
        # RS = average gain of last 14 days / average loss of last 14 periods

        return

    def Macd_crossover(self, symbol: str, period: str, interval: str, now, end):
        # calculate MACD when it crosses over
        # MACD = 12 period EMA - 26 period EMA
        # Signal Line = 9 period EMA of MACD

        macds, last_close_price = self.__calculate_macd(
            symbol, period, interval, now, end
        )
        if len(macds) < 2:
            return
        if macds[0] < 0 and macds[1] > 0:
            return self.buy_signal(1, last_close_price), macds
        elif macds[0] > 0 and macds[1] < 0:
            return self.sell_signal(1, last_close_price, "all"), macds

        if now == end:
            return self.sell_signal(1, last_close_price, "all"), macds

        return None, macds
    # -----------------------------------------------------------------------------------
    #                                Helper Functions
    # -----------------------------------------------------------------------------------
    def __calculate_rsi(self):
        # connect to the candlestick database and pull the price of the last 14 periods

        # select the last 14 rows
        self.cursor.execute("SELECT * FROM candles ORDER BY id DESC LIMIT 14")
        rows = self.cursor.fetchall()

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

    def __calculate_macd(self, symbol: str, period: str, interval: str, now, end):
        macds = []
        last_close_price = 0
        # select the last 27 rows
        self.cursor.execute(
            "SELECT * FROM {} ORDER BY Id DESC LIMIT 27".format(
                f"{symbol}_{period}_{interval}"
            )
        )
        rows = self.cursor.fetchall()

        # put all closes prices into list
        if len(rows) >= 27:
            close_prices = []
            for i in range(len(rows)):
                close_prices.append(rows[-i][4])
            last_close_price = close_prices[0]

            # calculate macd for first 26 periods
            short_period = 12
            long_period = 26
            for j in range(2):
                short_moving_average = 0
                long_moving_average = 0
                for i in range(short_period):
                    short_moving_average += close_prices[i + j]
                for i in range(long_period):
                    long_moving_average += close_prices[i + j]

                short_moving_average = short_moving_average / short_period
                long_moving_average = long_moving_average / long_period

                macd = short_moving_average - long_moving_average
                macds.append(macd)

            # calculate the MACD
        return macds, last_close_price

    def __find_RSI_min(self):
        pass

    def __find_RSI_max(self):
        pass

    def __find_price_local_min(self):
        pass

    def __find_price_local_max(self):
        pass

    def calculate_cost_basis(self):
        for price in self.portfolio:
            self.account.cost_basis += price * self.portfolio[price]
        self.account.cost_basis /= sum(self.portfolio.values())
        return self.account.cost_basis

    # -----------------------------------------------------------------------------------
    #                                    Order Functions
    # -----------------------------------------------------------------------------------
    def buy_signal(self, qty, price) -> str:
        self.account.balance -= price * qty
        if price not in self.portfolio:
            self.portfolio[price] = qty
        else:
            self.portfolio[price] += qty
        self.orders["buys"] += 1
        return "buy"

    def sell_signal(self, qty, price, order_type="all") -> str:
        if not self.portfolio:
            return "no shares to sell"

        if order_type == "all":
            qty = sum(self.portfolio.values())
        self.account.balance += price * qty
        # update portfolio
        if order_type == "lifo":
            for price in sorted(self.portfolio.keys(), reverse=True):
                if qty > self.portfolio[price]:
                    qty -= self.portfolio[price]
                    self.portfolio.pop(price)
                else:
                    self.portfolio[price] -= qty
                    break
        elif order_type == "fifo":
            for price in sorted(self.portfolio.keys()):
                if qty > self.portfolio[price]:
                    qty -= self.portfolio[price]
                    self.portfolio.pop(price)
                else:
                    self.portfolio[price] -= qty
                    break
        elif order_type == "all":
            self.__liquidate()
            pass

        self.orders["sells"] += 1
        return "sell"

    def __liquidate(self):
        self.portfolio = {}
        return

    # -----------------------------------------------------------------------------------
    #                                    Results
    # -----------------------------------------------------------------------------------

    def show_order_summary(self):
        return [
            f"{self.symbol}",
            f'{self.orders["buys"]}',
            f'{self.orders["sells"]}',
            f"{round(self.account.balance, 2)}",
            f"{round(self.account.balance - self.account.get_principle(), 2)}",
        ]
