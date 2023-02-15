# Conventions:
1. for importing local modules in other folders:

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from folder.subfolder.file import *

#Do not have driver code in the file, otherwise don't import *, only classes and functions you need

2. for sqlite3 database connections:

conn = sqlite3.connect('database.db')
c = conn.cursor()

3. Keep everything modular

4. Generally do not have any driver code inside def files; name driver files <foldername>_core.py

5. Use the following format for driver code:
if __name__ == "__main__":
    #driver code