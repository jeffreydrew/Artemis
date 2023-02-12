import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import config

class Trader:
    def __init__(self):
        self.PAPER_KEY = config.PAPER_KEY
        self.PAPER_SECRET = config.PAPER_SECRET
        self.PAPER_URL = config.PAPER_URL
        self.api = tradeapi.REST(self.PAPER_KEY, self.PAPER_SECRET, self.PAPER_URL, api_version='v2')

    def get_account(self):
        account = self.api.get_account()
        return account

    def read_directive(self):
        pass

    def set_trade_data(self):
        trade_data = None
        
        return trade_data

    def send_buy_order(self):
        pass

    def send_sell_order(self):
        pass


