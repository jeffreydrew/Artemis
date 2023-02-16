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
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()
        self.portfolio = {}
        self.rsi = []
        self.orders = {"buys": 0, "sells": 0}
        self.account = Account(10000)

    def commit(self):
        try:
            self.conn.commit()
        except:
            print("Error committing to database")

    def unit_test_strategy(self, symbol: str, period: str, interval: str, now, end):
        # get last close price
        self.c.execute(
            "SELECT * FROM {} ORDER BY Id DESC LIMIT 1".format(
                f"{symbol}_{period}_{interval}"
            )
        )
        row = self.c.fetchone()
        close_price = row[4]
        # execute one buy order at the first price
        if now == 0:
            return self.buy_signal(close_price)
        # execute one sell order at the last price
        if now == end:
            return self.sell_signal(close_price)

    def v2_test_strategy(self, symbol: str, period: str, interval: str, now, end):
        pass

    def test_strategy(self, symbol: str, period: str, interval: str, now, end):
        # if price of last period is greater than the price of the period before that and portfolio is 0, buy
        # if price of last period is less than the price of the period before that and portfolio is 1, sell
        # if price of last period is less than the price of the period before that and portfolio is 0, do nothing
        # if price of last period is greater than the price of the period before that and portfolio is 1, do nothing

        # select the last 2 rows from the table named symbol and put the close prices into a list
        self.c.execute(
            "SELECT * FROM {} ORDER BY Id DESC LIMIT 2".format(
                f"{symbol}_{period}_{interval}"
            )
        )
        rows = self.c.fetchall()
        close_prices = []
        for i in range(2):
            close_prices.append(rows[-i][4])
        if len(close_prices) < 2:
            close_prices.prepend(0)

        # if the price of the last period is greater than the price of the period before that and portfolio is 0, buy
        if close_prices[0] > close_prices[1]:
            self.portfolio = 1
            return self.buy_signal(close_prices[0], self.account.balance / close_prices[0])
        # if the price of the last period is less than the price of the period before that and portfolio is 1, sell
        elif close_prices[0] < close_prices[1] and self.portfolio != 0:
            self.portfolio = 0
            return self.sell_signal(close_prices[0])

        if now == end:
            return self.sell_signal(close_prices[0])

        return

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

    def __find_RSI_min(self):
        pass

    def find_price_local_min(self):
        pass

    def find_price_local_max(self):
        pass

    def calculate_cost_basis(self):
        for price in self.portfolio:
            self.account.cost_basis += price * self.portfolio[price]
        self.account.cost_basis /= sum(self.portfolio.values())
        return self.account.cost_basis
    # -------------------------------------------------------------------------------------------------------------------
    #                                                       Order Functions
    # -------------------------------------------------------------------------------------------------------------------

    def buy_signal(self, qty, price) -> str:
        self.account.balance -= price * qty
        if price not in self.portfolio:
            self.portfolio[price] = qty
        else:
            self.portfolio[price] += qty
        self.orders["buys"] += 1
        return "buy"

    def sell_signal(self, qty, price, order_type="lifo") -> str:
        if not self.portfolio:
            return "no shares to sell"
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

        return "sell"

    def __liquidate(self):
        # sell all shares in portfolio and clear portfolio
        for price in self.portfolio:
            self.account.balance += price * self.portfolio[price]
        self.portfolio = {}
        return

    # -------------------------------------------------------------------------------------------------------------------
    #                                                       Results
    # -------------------------------------------------------------------------------------------------------------------

    def show_order_summary(self):
        print("Buys: {}".format(self.orders["buys"]))
        print("Sells: {}".format(self.orders["sells"]))
        print("Profit: {}".format(self.account.balance - self.account.get_principle()))
