import alpaca_trade_api as tradeapi
import time

PAPER_KEY = "PKKZSVR4ICWFB6YOHU04"
PAPER_SECRET = "zaOMUgrElVp1ZFlchRIqM0oaOXlmcwePlifWKBdK"
PAPER_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(PAPER_KEY, PAPER_SECRET, PAPER_URL)


def buy():
    api.cancel_all_orders()

    api.submit_order(
        symbol="BTC/USD", qty=1, side="buy", type="market", time_in_force="gtc"
    )

def sell():
    api.cancel_all_orders()

    api.submit_order(
        symbol="BTC/USD", qty=1, side="sell", type="market", time_in_force="gtc"
    )


trades = 0
while trades < 100:
    buy()
    time.sleep(5)
    sell()
    trades += 1


