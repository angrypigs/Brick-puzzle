import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board_generator import boardGenerator
from src.utils import *

for i in range(100):
    n = random.randint(5, 9)
    m = random.randint(-n + 13, -n + 15)
    board = boardGenerator(n, m)
    res = board.generate()
    with open(res_path(f"../assets/levels/level{i + 1}.txt"), "w") as f:
        for square in res[0]:
            f.write(";".join([":".join([str(y) for y in x]) for x in square]) + "\n")
        f.write(f"S {n} {m}")
    os.chmod(res_path(f"../assets/levels/level{i + 1}.txt"), 0o444)