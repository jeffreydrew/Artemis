This is the library of trading strategies
It will ultimately make the decisions for when to execute a trade

Once the manager finds an entry or exit point based on :
    if strategy is on buy:
        look for entry point
    else:
        look for exit point

it will create a trade directive object and pipe it to the Trader
