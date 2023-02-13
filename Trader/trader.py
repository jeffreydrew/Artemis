import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import config
#from Manager


class Trader:
    def __init__(self):
        self.PAPER_KEY = config.PAPER_KEY
        self.PAPER_SECRET = config.PAPER_SECRET
        self.PAPER_URL = config.PAPER_URL
        self.api = tradeapi.REST(
            self.PAPER_KEY, self.PAPER_SECRET, self.PAPER_URL, api_version="v2"
        )
        self.last_trade = None

    def get_account(self):
        account = self.api.get_account()
        return account

    def get_cash(self):
        cash = self.get_account().cash
        return cash

    def get_portfolio(self):
        portfolio = self.api.list_positions()
        return portfolio

    def read_directive(self):
        pass

    def set_trade_data(self):
        #takes in a list from Manager
        trade_data = None

        return trade_data

    def buy(self):
        data = self.set_trade_data()
        
        pass

    def sell(self):
        pass

    def sell_all(self):
        confirmation = input("Are you sure you want to sell all? (y/n)")
        #lowercase the input
        confirmation = confirmation.lower()
        if confirmation == "y":
            portfolio = self.get_portfolio()
            for position in portfolio:
                self.api.submit_order(
                    symbol=position.symbol,
                    qty=position.qty,
                    side="sell",
                    type="market",
                    time_in_force="gtc",
                )

    def create_trade_receipt(self):
        #return a receipt of the trade
        pass