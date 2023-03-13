import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Manager.new_manager import NewManager
import time

while True:
    # new manager
    manager = NewManager("SPY", "1d", "1m")
    # catch market timeframe
    if (
        time.localtime().tm_hour == 9 and time.localtime().tm_min >= 30
    ) or time.localtime().tm_hour > 9:
        if time.localtime().tm_hour < 16:
            manager.update_manager()
            manager.strategy_macd()
            if time.localtime().tm_hour == 15 and time.localtime().tm_min == 59:
                manager.market_sell()

        elif time.localtime().tm_hour == 16 and time.localtime().tm_min == 0:
            manager.post_analytics()

    # wait 60 seconds
    print(time.strftime("%H:%M:%S", time.localtime()))
    time.sleep(60)
