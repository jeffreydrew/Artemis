import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backtesting.time_machine import Time_Machine
from Manager.manager import Manager
import matplotlib.pyplot as plt
import sqlite3

if __name__ == "__main__":
    # ---------------------------------------------------------
    #                   Prepare the universe
    # ---------------------------------------------------------

    t = Time_Machine("1d", "5m", "tsla")
    m = Manager("Backtesting/testing.db")

    # create database
    conn = sqlite3.connect("Backtesting/testing.db")
    c = conn.cursor()
    # clear database
    c.execute("DROP TABLE IF EXISTS {}".format(f"{t.symbol}_{t.period}_{t.interval}"))
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
        action = m.unit_test_strategy(
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

        plt.clf() #if now == len(t.data) - 1 else plt.show()
        # find way to implement buy signal, will need some sort of persistance

        print(now)
        now += 1

        visualize()

    # simulation stats
    m.show_order_summary()
