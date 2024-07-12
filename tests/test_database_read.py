import sqlite3
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board_generator import boardGenerator
from src.utils import *

conn = sqlite3.connect(res_path("../assets/levels.db"))
c = conn.cursor()

c.execute("""SELECT * FROM lvl""")
for i in c.fetchall():
    print(tuple(i[:3]) + (tuple(tuple(tuple(map(int, x.split(':'))) for x in y.split(';')) for y in i[3].split('_')), ))

conn.commit()
conn.close()