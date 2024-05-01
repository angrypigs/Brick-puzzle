from src.utils import *
from src.board_generator import boardGenerator

import random
import pygame

class Square(pygame.sprite.Sprite):

    def __init__(self, 
                 x_start: int, 
                 y_start: int,
                 x_offset: int,
                 y_offset: int,
                 color: tuple[int, int, int]):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x_start + x_offset, 
                                                y_start + y_offset))
        self.x = x_offset
        self.y = y_offset

class Figure(pygame.sprite.Group):
    
    def __init__(self,
                 index: int,
                 offsets: tuple[tuple[int, int]],
                 color: tuple[int, int, int]) -> None:
        super().__init__()
        self.INDEX = index
        self.offsets = offsets
        for offset in offsets:
            square = Square(150 * index, 150 * index,
                            offset[1] * BLOCK_SIZE, offset[0] * BLOCK_SIZE,
                            color)
            self.add(square)

class Level:

    def __init__(self, 
                 screen: pygame.Surface,
                 index: int | None,
                 blocks: tuple[tuple[tuple[int, int]]] | None = None,
                 size: tuple[int, int] | None = None) -> None:
        self.screen = screen
        self.figures : list[Figure] = []
        self.current_figure = None
        self.current_shadow = None
        self.current_coords = [0, 0]
        self._is_done = False
        self._last_button = None
        self.index = index
        self.home_btn = Button(self.screen, 40, 40, 80, 80, "", IMG_HOME)
        self.next_btn = Button(self.screen, WIDTH - 120, 40, 80, 80, "", IMG_ARROW_RIGHT)
        if index is None:
            self.RECT_WIDTH = size[0]
            self.RECT_HEIGHT = size[1]
            for i, block in enumerate(blocks):
                self.figures.append(Figure(i + 1, block, COLORS[i]))
        else:
            with open(res_path(f"assets/levels/level{index}.txt"), "r") as f:
                counter = 1
                for line in f.readlines():
                    if line[0] == "S":
                        size1 = line.rstrip().split()
                        self.RECT_WIDTH = int(size1[1])
                        self.RECT_HEIGHT = int(size1[2])
                    else:
                        block = tuple([tuple([int(y) for y in x.split(":")]) for x in line.rstrip().split(";")])
                        print(block)
                        self.figures.append(Figure(counter, block, COLORS[counter - 1]))
                        counter += 1
        self.GRID_HEIGHT = HEIGHT // BLOCK_SIZE
        self.GRID_WIDTH = WIDTH // BLOCK_SIZE
        self.matrix = [[0 for x in range(self.GRID_HEIGHT)] for y in range(self.GRID_WIDTH)]
        for figure in self.figures:
            places = [(i, j) for i in range(3, self.GRID_HEIGHT) 
                      for j in range(self.GRID_WIDTH) 
                      if self.__is_valid(figure.offsets, i, j)]
            place = random.choice(places)
            self.__place(figure.offsets, place[0], place[1], figure.INDEX)
            for square in figure:
                square.rect = square.image.get_rect(center=(place[1] * BLOCK_SIZE + square.x + BLOCK_SIZE // 2,
                                                            place[0] * BLOCK_SIZE + square.y + BLOCK_SIZE // 2))
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill(BG_COLOR)
        self.X_OFFSET = (self.GRID_WIDTH - self.RECT_WIDTH) // 2 * BLOCK_SIZE
        self.Y_OFFSET = (self.GRID_HEIGHT - self.RECT_HEIGHT) // 2 * BLOCK_SIZE
        pygame.draw.rect(self.bg, BTN_COLOR,
                         (self.X_OFFSET, self.Y_OFFSET,
                          self.RECT_WIDTH * BLOCK_SIZE,
                          self.RECT_HEIGHT * BLOCK_SIZE))

    def __is_valid(self, brick: tuple[tuple[int, int]],
                   row: int, col: int) -> None:
        for block in brick:
            a = row + block[0]
            b = col + block[1]
            if (a < 2 or a >= self.GRID_WIDTH or
                b < 0 or b >= self.GRID_HEIGHT or
                self.matrix[a][b] != 0):
                return False
        return True

    def __place(self, brick: tuple[tuple[int, int]],
                   row: int, col: int, fill: int) -> None:
        for block in brick:
            self.matrix[row + block[0]][col + block[1]] = fill

    def __remove(self, brick: tuple[tuple[int, int]],
                   row: int, col: int) -> None:
        counter = 0
        for block in brick:
            if self.matrix[row + block[0]][col + block[1]] != 0:
                counter += 1
            self.matrix[row + block[0]][col + block[1]] = 0
        print(counter)

    def draw(self, pos) -> None:
        self.screen.blit(self.bg, (0, 0))
        if self.current_shadow is not None:
            self.current_shadow.draw(self.screen)
        self._last_button = None
        if self.home_btn.draw(pos):
            self._last_button = -1
        if self._is_done and self.next_btn.draw(pos):
            self._last_button = -2
        for figure in self.figures:
            figure.draw(self.screen)
        
    def click(self, x: int, y: int) -> None:
        print(x, y)
        flag = False
        for figure in self.figures:
            if flag:
                break
            for square in figure:
                if square.rect.collidepoint((x, y)):
                    self.current_figure = figure
                    self.current_shadow = Figure(self.current_figure.INDEX, 
                                                 self.current_figure.offsets,
                                                 tuple([max(0, x - 100) for x in COLORS[self.current_figure.INDEX - 1]]))
                    self.current_coords = [(x - square.x) // BLOCK_SIZE,
                                            (y - square.y) // BLOCK_SIZE]
                    for square in self.current_shadow:
                        square.rect = square.image.get_rect(center=(self.current_coords[0] * BLOCK_SIZE + square.x + BLOCK_SIZE // 2,
                                                                    self.current_coords[1] * BLOCK_SIZE + square.y + BLOCK_SIZE // 2))
                    self.__remove(figure.offsets, 
                                  self.current_coords[1], 
                                  self.current_coords[0])
                    flag = True
                    break
        if flag:
            self.figures.remove(self.current_figure)
            self.figures.append(self.current_figure)

    def move(self, x: int, y: int) -> None:
        if self.current_figure is not None:
            for square in self.current_figure:
                square.rect = square.image.get_rect(center=(x + square.x,
                                                            y + square.y))
            new_x = x // BLOCK_SIZE
            new_y = y // BLOCK_SIZE
            if self.current_coords[0] != new_x or self.current_coords[1] != new_y:
                if self.__is_valid(self.current_figure.offsets, new_y, new_x):
                    self.current_coords = [new_x, new_y]
                for square in self.current_shadow:
                    square.rect = square.image.get_rect(center=(self.current_coords[0] * BLOCK_SIZE + square.x + BLOCK_SIZE // 2,
                                                                self.current_coords[1] * BLOCK_SIZE + square.y + BLOCK_SIZE // 2))

    def release(self, x: int, y: int) -> int:
        if self._last_button == -2:
            return 2
        elif self._last_button == -1:
            return 1
        if self.current_figure is not None:
            for square in self.current_figure:
                square.rect = square.image.get_rect(center=(self.current_coords[0] * BLOCK_SIZE + square.x + BLOCK_SIZE // 2,
                                                            self.current_coords[1] * BLOCK_SIZE + square.y + BLOCK_SIZE // 2))
            self.__place(self.current_figure.offsets,
                         self.current_coords[1],
                         self.current_coords[0],
                         self.current_figure.INDEX)
            self.current_figure = None
            self.current_shadow = None
            for i in range(self.Y_OFFSET // BLOCK_SIZE, self.Y_OFFSET // BLOCK_SIZE + self.RECT_HEIGHT):
                if 0 in self.matrix[i][self.X_OFFSET // BLOCK_SIZE : self.X_OFFSET // BLOCK_SIZE + self.RECT_WIDTH]:
                    break
            else:
                self._is_done = True
                print("lol")
        return 0
            
    