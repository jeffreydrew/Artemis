import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
from Researcher.researcher import *


# ---------------------------------------------------------------------------------------
#                                          Table
# ---------------------------------------------------------------------------------------
# create a new table named "in_use" if it doesn't exist with columns time, open, high, low, close
def create_table():
    conn = sqlite3.connect("in_use.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS in_use (time TEXT, open REAL, high REAL, low REAL, close REAL)"
    )
    conn.commit()
    conn.close()


def clear_table():
    conn = sqlite3.connect("in_use.db")
    c = conn.cursor()
    c.execute("DELETE FROM in_use")
    conn.commit()
    conn.close()


def add_last_candle():
    conn = sqlite3.connect("in_use.db")
    c = conn.cursor()

    # c.execute("INSERT INTO in_use VALUES (1, 'last_candle', 0)")
    conn.commit()
    conn.close()


create_table()
