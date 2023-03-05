import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import alpaca_trade_api as tradeapi
from Trader.trader import *
from Manager.manager import *
from Researcher.researcher import *
from Discord.artemis_discord import *
from config import *
from datetime import datetime, timedelta

PATH = "Researcher/candles.db"
SYMBOL = "SPY"
PERIOD = "2d"
INTERVAL = "1m"

if __name__ == "__main__":
    trader = Trader()
    researcher = Researcher(PATH, SYMBOL, PERIOD, INTERVAL)
    manager = Manager(PATH, SYMBOL)

    # while it is not 4:00pm
    while datetime.now().time() < datetime.strptime("16:00", "%H:%M").time():
        action = None
        # get latest candle
        candle = researcher.get_latest_candle()
        # add candle to database
        researcher.add_candle(candle)



        time.sleep(60)