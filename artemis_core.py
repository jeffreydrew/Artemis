import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import alpaca_trade_api as tradeapi
from Trader.trader import *
from Manager.manager import *
from Researcher.researcher import *
from Discord.artemis_discord import *
from config import *

PATH = 'Researcher/candles.db'
SYMBOL = 'SPY'
PERIOD = '1d'
INTERVAL = '1m'

if __name__ == "__main__":
    trader = Trader()
    researcher = Researcher(PATH, SYMBOL, PERIOD, INTERVAL)
    manager = Manager(PATH, SYMBOL)

