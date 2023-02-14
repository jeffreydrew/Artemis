import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Historical_data import get_data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Time_Machine:
    # each time machine instance is unique to a specific symbol to test in isolated environment
    def __init__(self, period, interval, symbol):
        self.period = period
        self.interval = interval
        self.symbol = symbol
        self.data = self.get_data()

    def get_data_file(self):
        get_data.get_data(self.symbol, self.period, self.interval)


t = Time_Machine("1d", "5m", "aapl")
data = t.get_data_file()
print(t.symbol, t.period, t.interval)
