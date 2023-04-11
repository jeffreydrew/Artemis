import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Manager.new_manager import NewManager
import time, datetime


if __name__ == "__main__":
    # new manager
    manager = NewManager("SPY", "1d", "1m")
    while True:
        # catch market timeframe
        if ((
            time.localtime().tm_hour == 9 and time.localtime().tm_min >= 30
        ) or time.localtime().tm_hour > 9) and time.localtime().tm_hour < 16:
            #if end of day, sell
            if time.localtime().tm_hour == 15 and time.localtime().tm_min == 59:
                manager.market_sell()
            
            if time.localtime().tm_sec == 1:
                print(datetime.datetime.now(), '|' , manager.macdhists.iloc[-2:])
                manager.update_manager()
                manager.strategy_macd()
                # wait 60 seconds
                time.sleep(57)          
                   

            elif time.localtime().tm_hour == 16 and time.localtime().tm_min == 0:
                manager.post_analytics()
                

   