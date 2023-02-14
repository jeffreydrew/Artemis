import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backtesting.time_machine import Time_Machine
from Manager.manager import Manager
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

if __name__ == "__main__":
    # ---------------------------------------------------------
    #                   Prepare the universe
    # ---------------------------------------------------------
    t = Time_Machine("5d", "5m", "aapl")

    # create database
    conn = sqlite3.connect("Backtesting/testing.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS {} (Date text, Open real, High real, Low real, Close real, Volume real)".format(
            t.symbol
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
            "INSERT INTO {} VALUES (0, ?, ?, ?, ?, ?)".format(t.symbol),
            (
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"],
            ),
        )
        conn.commit()

        # ---------------------------------------------------------
        #                   Implement strategy
        # ---------------------------------------------------------
        m = Manager("Backtesting/testing.db")



        # ---------------------------------------------------------
        #                       Visualize
        # ---------------------------------------------------------
        plt.plot(visible["Close"])
        plt.pause(0.01)
        plt.clf() if now != len(t.data) - 1 else plt.show()

        # find way to implement buy signal, will need some sort of persistance

        now += 1

