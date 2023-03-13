import os, sys
import talib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
import yfinance as yf
import alpaca_trade_api as tradeapi


class NewManager:
    def __init__(self, symbol, period, interval):
        self.api = tradeapi.REST(PAPER_KEY, PAPER_SECRET, PAPER_URL, "v2")
        self.account = self.get_account()
        # stock specific
        self.symbol = symbol
        self.period = period
        self.interval = interval

        # strategy specific
        self.stoploss = 0.0015
        self.risk_coefficient = 0.45

        # data (that gets updated every check, per period)
        self.bars = self.set_bars()
        self.macdhists = self.set_macds()
        self.write_out_data()

    #--------------------------------------------------------
    #                      Account Management
    #--------------------------------------------------------
    def get_account(self):
        account = self.api.get_account()
        return account

    def set_bars(self):
        # get data from yf
        bars = yf.Ticker(self.symbol).history(self.period, self.interval)
        return bars

    def set_macds(self):
        # macd signal
        # consider using macd on open price instead of close, backtest on this
        _, _, macdhist = talib.MACD(self.bars["Close"])
        return macdhist

    def update_manager(self):
        self.account = self.get_account()
        self.bars = self.get_bars()
        self.macdhists = self.get_macds()
        self.write_out_data()


    #--------------------------------------------------------
    #                        Strategies
    #--------------------------------------------------------
    def strategy_macd(self):
        # if price is less than stoploss, sell everything
        price = self.bars.iloc[-1]["close"]
        if price < self.last_buy_price * (1 - self.stop_loss):
            self.market_sell()

        # look at the last two macdhist values
        first, second = self.macdhists[-2:]

        # buy signal
        if first > 0 and second < 0:
            self.market_buy()

        # sell signal but does nothing if price is less than last buy price
        if first < 0 and second > 0:
            if price < self.last_buy_price:
                return
            else:
                self.market_sell()

    #--------------------------------------------------------
    #                      Market functions
    #--------------------------------------------------------
    def market_buy(self):
        qty = int(self.risk_coefficient * float(self.account.equity))

        self.api.submit_order(
            symbol=self.symbol, qty=qty, side="buy", type="market", time_in_force="gtc",
        )

    def market_sell(self):
        # qty is the number of shares in the portfolio
        pos = self.api.get_position(self.symbol)
        qty = pos.qty

        self.api.submit_order(
            symbol=self.symbol,
            qty=qty,
            side="sell",
            type="market",
            time_in_force="gtc",
        )

    #--------------------------------------------------------
    #                      Visualization
    #--------------------------------------------------------
    def see_bars(self):
        # write to csv
        self.bars.to_csv(f"deploy_1/data/{self.symbol}_bars.csv")

    def see_macds(self):
        # write to csv
        self.macdhists.to_csv(f"deploy_1/data/{self.symbol}_macd.csv")

    def write_out_data(self):
        # write to csv
        self.see_bars()
        self.see_macds()

    #--------------------------------------------------------
    #                         Analysis
    #--------------------------------------------------------
    def post_analytics(self):
        #get list of all trades from self.api
        trades = self.api.list_orders(status="all", limit=1000)
        return trades


# driver temp
if __name__ == "__main__":
    m = NewManager("INTC", "1d", "1m")
