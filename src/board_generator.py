from src.utils import *
import random



class boardGenerator:

    def __init__(self,
                 width: int,
                 height: int) -> None:
        self.matrix = [[0 for x in range(width)] for y in range(height)]
        self.WIDTH = width
        self.HEIGHT = height

    def is_board_full(self) -> bool:
        return all([self.matrix[i][j] != 0 
                    for i in range(self.HEIGHT) 
                    for j in range(self.WIDTH)])
    
    def are_empty_spaces_after(self, 
                         brick: tuple[tuple[int, int]],
                         row: int,
                         col: int) -> bool:
        matrix = [x[:] for x in self.matrix]
        self.place_brick(matrix, brick, row, col)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if (matrix[i][j] == 0 and
                    (i == 0 or matrix[i - 1][j] != 0) and
                    (i == self.HEIGHT - 1 or matrix[i + 1][j] != 0) and
                    (j == 0 or matrix[i][j - 1] != 0) and
                    (j == self.WIDTH - 1 or matrix[i][j + 1] != 0)):
                    return True
        return False

    def place_brick(self, 
                    matrix: list[list[int]],
                    brick: tuple[tuple[int, int]], 
                    row: int, 
                    col: int,
                    fill: int = 1) -> None:
        for coord in brick:
            matrix[row + coord[0]][col + coord[1]] = fill
    
    def get_weight(self, 
                   brick: tuple[tuple[int, int]],
                   row: int, 
                   col: int) -> int:
        weight = 0
        for place in brick:
            a = row + place[0]
            b = col + place[1]
            if (a < 0 or a >= self.HEIGHT or
                b < 0 or b >= self.WIDTH or
                self.matrix[a][b] != 0):
                return -1
            if (a == 0 or self.matrix[a - 1][b] != 0):
                weight += 1
            if (b == 0 or self.matrix[a][b - 1] != 0):
                weight += 1
            if (a == (self.HEIGHT - 1) or self.matrix[a + 1][b] != 0):
                weight += 1
            if (b == (self.WIDTH - 1) or self.matrix[a][b + 1] != 0):
                weight += 1
        if self.are_empty_spaces_after(brick, row, col):
            return -1
        return weight

    def generate(self) -> tuple[tuple[tuple[tuple[int, int]]], int]:
        self.matrix = [[0 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
        placed_blocks = []
        all_blocks = random.sample(BRICKS, len(BRICKS) // 2)
        fill_counter = 0
        tries = 0
        while True:
            fill_counter += 1
            max_weight = -1
            best_placements = []
            for i in range(self.HEIGHT):
                for j in range(self.WIDTH):
                    if self.matrix[i][j] == 0:
                        for block in all_blocks:
                            weight = self.get_weight(block[1], i, j)
                            if fill_counter < 3:
                                if weight >= 0:
                                    best_placements.append((block, i, j))
                                    max_weight = weight
                            else:
                                if weight == max_weight:
                                    best_placements.append((block, i, j))
                                elif weight > max_weight:
                                    max_weight = weight
                                    best_placements.clear()
                                    best_placements.append((block, i, j))
            if max_weight == -1:
                if self.is_board_full():
                    print(f"Attempts: {tries}")
                    for i in self.matrix:
                        print(i)
                    return (placed_blocks, tries, )
                else:
                    tries += 1
                    self.matrix = [[0 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
                    fill_counter = 0
                    all_blocks = random.sample(BRICKS, len(BRICKS) // 2)
                    placed_blocks.clear()
            else:
                place = random.choice(best_placements)
                self.place_brick(self.matrix, place[0][1], place[1], place[2], fill_counter)
                all_blocks = [b for b in all_blocks if b[0] != place[0][0]]
                placed_blocks.append(place[0][1])


