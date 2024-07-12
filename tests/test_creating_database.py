import sqlite3
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board_generator import boardGenerator
from src.utils import *

matrix = []

conn = sqlite3.connect(res_path("../assets/levels.db"))
c = conn.cursor()

c.execute('''
DROP TABLE IF EXISTS lvl
''')

c.execute('''
CREATE TABLE IF NOT EXISTS lvl (
    id INTEGER,
    width INTEGER,
    height INTEGER,
    bricks TEXT
)
''')

for i in range(2000):
    n = random.randint(5, 9)
    m = random.randint(-n + 13, -n + 15)
    board = boardGenerator(n, m)
    res = board.generate()
    text = "_".join([";".join([":".join([str(y) for y in x]) for x in z]) for z in res[0]])
    c.execute('''INSERT INTO lvl (id, width, height, bricks) VALUES (?, ?, ?, ?)''', (i, n, m, text))

conn.commit()
conn.close()