import sqlite3

# ---------------------------------------------------------------------------------------
#                                       Candlesticks
# ---------------------------------------------------------------------------------------

class CandleStick:
    def __init__(self):
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.time = 0


# ---------------------------------------------------------------------------------------
#                                          Table
# ---------------------------------------------------------------------------------------
# create a new table named "in_use" if it doesn't exist
def create_table():
    conn = sqlite3.connect("in_use.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS in_use (id INTEGER PRIMARY KEY, name TEXT, in_use INTEGER)"""
    )
    conn.commit()
    conn.close()

def insert_candlestick():
    pass
