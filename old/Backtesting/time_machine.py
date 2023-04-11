import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Historical_data.get_data import get_data_function


class Time_Machine:
    # each time machine instance is unique to a specific symbol to test in isolated environment
    def __init__(self, period, interval, symbol):
        self.period = period
        self.interval = interval
        self.symbol = symbol
        self.data = self.get_data_file()

    def get_data_file(self):
        return get_data_function(self.symbol, self.period, self.interval)
