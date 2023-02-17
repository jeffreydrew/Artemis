import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backtesting.time_machine import Time_Machine
from Manager.manager import Manager
import matplotlib.pyplot as plt
import sqlite3

assets_of_interest = [
    # "aapl",
    # "amzn",
    # "f",
    "spy",
    #"tsla",
]

period = "1y"
interval = "1d"

"""
period: data period to download (either use period parameter or use start and end) Valid periods are:
“1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
“1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

start: If not using period - in the format (yyyy-mm-dd) or datetime.

end: If not using period - in the format (yyyy-mm-dd) or datetime."""

summaries = []
if __name__ == "__main__":
    # ------------------------------------------------------------------------------------------------------------
    #                   Create a multiverse with universes seeded with every symbol of interest
    # ------------------------------------------------------------------------------------------------------------
    for asset in assets_of_interest:
        # ---------------------------------------------------------
        #                   Prepare the universe
        # ---------------------------------------------------------

        t = Time_Machine(period, interval, asset)
        m = Manager("Backtesting/testing.db", asset)

        # create database
        conn = sqlite3.connect("Backtesting/testing.db")
        c = conn.cursor()
        # clear database
        c.execute(
            "DROP TABLE IF EXISTS {}".format(f"{t.symbol}_{t.period}_{t.interval}")
        )
        # # clear table
        # c.execute("DELETE FROM {}".format(f"{t.symbol}"))
        c.execute(
            "CREATE TABLE IF NOT EXISTS {} (Id integer, Open real, High real, Low real, Close real, Volume real, Action text)".format(
                f"{t.symbol}_{t.period}_{t.interval}"
            )
        )

        # ---------------------------------------------------------
        #                   Run the universe
        # ---------------------------------------------------------
        now = 0
        while now < len(t.data):
            # visible is the first now rows of the data
            visible = t.data.iloc[:now, :]

            # integrate the database loader here in the universe
            # database is based on now, even though csv is filled with all data. This simulates data streaming

            # update database
            # row is 'now'th row of self.data
            row = t.data.iloc[now, :]
            # print everything in row except for Name
            print(row)
            # insert the row into the database
            c.execute(
                "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?)".format(
                    f"{t.symbol}_{t.period}_{t.interval}"
                ),
                (
                    now,
                    row["Open"],
                    row["High"],
                    row["Low"],
                    row["Close"],
                    row["Volume"],
                    "None",
                ),
            )
            conn.commit()

            # ---------------------------------------------------------
            #                   Implement strategy
            # ---------------------------------------------------------
            action = m.Macd_crossover(
                t.symbol, t.period, t.interval, now, len(t.data) - 1
            )
            print(f"===================={action}====================")

            # ---------------------------------------------------------
            #                       Visualize
            # ---------------------------------------------------------
            def visualize():
                # name of plot is name of table
                plt.title(f"{t.symbol}_{t.period}_{t.interval}")

                x = visible["Close"]
                y = visible.index

                plt.plot(y, x, "b-")
                plt.pause(0.0001)

            plt.clf()  # if now == len(t.data) - 1 else plt.show()
            # find way to implement buy signal, will need some sort of persistance

            print(now)
            now += 1

            # visualize()

        # simulation stats
        summaries.append(
            [
                f"Symbol: {m.symbol}",
                f'Buys: {m.orders["buys"]}',
                f'Sells: {m.orders["sells"]}',
                f"Balance: ${round(m.account.balance, 2)}",
                f"Profits: ${round(m.account.balance - m.account.get_principle(), 2)}",
                m.macds

            ]
        )

    for summary in summaries:
        for line in summary:
            print(line)
        print("")
