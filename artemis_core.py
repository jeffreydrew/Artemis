import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import alpaca_trade_api as tradeapi
from Trader.trader import *
from Manager.manager import *
from Discord.artemis_discord import *

if __name__ == "__main__":
    pass