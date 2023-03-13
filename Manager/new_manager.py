import os, sys
import talib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import *
import yfinance as yf
import alpaca_trade_api as tradeapi
        

class NewManager:
    def __init__(self, symbol, period, interval):
        self.api = tradeapi.REST(PAPER_KEY, PAPER_SECRET)
        self.account = self.api.get_account()

        #stock specific
        self.symbol = symbol
        self.period = period
        self.interval = interval

        #strategy specific
        self.stoploss = 0.0015
        self.risk_coefficient = 0.45

        #data (that gets updated every check, per period)
        self.bars = self.get_bars()
        self.macdhists = self.get_macds()

    def get_bars(self):
        # get data from yf
        bars = yf.Ticker(self.symbol).history(self.period, self.interval)
        return bars

    def get_macds(self):
        # macd signal
	    # consider using macd on open price instead of close, backtest on this
        _, _, macdhist = talib.MACD(self.bars["Close"])
        return macdhist
    
    def strategy_macd(self):
        #if price is less than stoploss, sell everything
        #reconsider stoploss implementation !!!!

        price = self.bars.iloc[-1]["close"]
        if price < self.last_buy_price * (1 - self.stop_loss):
            self.sell(self.portfolio, price)

        #look at the last two macdhist values
        first, second = self.macdhists[-2:]
       

        #buy signal
        if first > 0 and second < 0:
            return "buy"
        
        #sell signal with stop loss
        if first < 0 and second > 0:
            return "sell"

    def market_buy(self, qty):
        pass

    def market_sell(self, qty):
        pass


    def see_macds(self):
        #write to csv
        self.macdhists.to_csv("macdhist.csv")


# driver temp
if __name__ == "__main__":
    m = NewManager("SPY", "1d", "1m")
