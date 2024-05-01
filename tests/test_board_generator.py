import sys
import os

# Dodaj katalog nadrzędny do ścieżki modułów Pythona
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board_generator import boardGenerator

board = boardGenerator(6, 8)
max_attempts = -1
avg = []
for i in range(100):
    n = board.generate()[1]
    avg.append(n)
    if n > max_attempts:
        max_attempts = n
print(f"Max attempts: {max_attempts}, attempts average: {sum(avg) / len(avg)}")