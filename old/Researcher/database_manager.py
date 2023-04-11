import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
from Researcher.researcher import *
from datetime import date
import time

CANDLES = "Researcher/candles.db"


# ---------------------------------------------------------------------------------------
#                                          Table
# ---------------------------------------------------------------------------------------
# create a new table named "in_use" if it doesn't exist with columns time, open, high, low, close
def create_table(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS in_use (time BLOB, open REAL, high REAL, low REAL, close REAL)"
    )
    conn.commit()
    conn.close()


def clear_table(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DELETE FROM in_use")
    conn.commit()
    conn.close()


def delete_table(path):
    table_name = path[:-3]
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DROP TABLE in_use")
    conn.commit()
    conn.close()


def add_last_candle(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    r = Researcher()
    last = r.get_last_ticker("aapl")
    c.execute(
        "INSERT INTO in_use VALUES (?, ?, ?, ?, ?)",
        (last.name, last.Open, last.High, last.Low, last.Close),
    )

    conn.commit()
    conn.close()


# manage the table
if __name__ == "__main__":
    r = Researcher(CANDLES, "SPY", "1d", "1m")
    r.clear_table()
    r.create_table('test')

    # while True:
    #     # if seconds is 01
    #     if time.localtime().tm_sec == 1:
    #         index = f'{date.today()} {time.strftime("%H:%M", time.localtime(time.time() - 60))}'

    #         last = r.get_last_ticker()
            
    #         r.add_candle(last, index)

    #         print(
    #             f"Added candle successfully: {index} {last.Open} {last.High} {last.Low} {last.Close} {last.Volume}"
    #         )
    #         # wait 60 seconds
    #         time.sleep(60)

    r.update_table()