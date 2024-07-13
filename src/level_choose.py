import pygame
import os
import re
import math

from src.utils import *

class levelChoose:

    def __init__(self,
                 screen: pygame.Surface,
                 levels_done: list[int],
                 levels_quantity: int) -> None:
        self.screen = screen
        self.LEVEL_QUANTITY = levels_quantity
        self.BTN_ROWS = 6
        self.BTN_COLS = 6
        self.BTN_SIZE = 80
        self.X_OFFSET = 40
        self.Y_OFFSET = 120
        self.X_DELAY = (WIDTH - 2 * self.X_OFFSET - self.BTN_ROWS * self.BTN_SIZE) / (self.BTN_ROWS + 1)
        self.Y_DELAY = (HEIGHT - self.Y_OFFSET - self.BTN_COLS * self.BTN_SIZE) / (self.BTN_COLS + 1)
        self.PAGES_LIMIT = math.ceil(self.LEVEL_QUANTITY / (self.BTN_COLS * self.BTN_ROWS))
        self.levels_done = divide_list(levels_done, self.BTN_COLS * self.BTN_ROWS, self.PAGES_LIMIT)
        self.current_page = 0
        self.current_btn : int | None = None
        self.back_btn = Button(self.screen, 40, 40, self.BTN_SIZE, self.BTN_SIZE, "", IMG_ARROW_LEFT)
        self.next_btn = Button(self.screen, WIDTH - 40 - self.BTN_SIZE, 40, self.BTN_SIZE, self.BTN_SIZE, "", IMG_ARROW_RIGHT)
        self.home_btn = Button(self.screen, WIDTH // 2 - 40, 40, self.BTN_SIZE, self.BTN_SIZE, "", IMG_HOME)
        self.level_btns : list[Button | None] = [None for x in range(self.BTN_COLS * self.BTN_ROWS)]
        self.__create_new_btns()
    
    def __create_new_btns(self) -> None:
        print(self.levels_done)
        for i in range(self.BTN_ROWS):
            for j in range(self.BTN_COLS):
                index = self.current_page * self.BTN_COLS * self.BTN_ROWS + i * self.BTN_COLS + j
                if index < self.LEVEL_QUANTITY:
                    self.level_btns[i * self.BTN_COLS + j] = Button(self.screen, 
                    self.X_OFFSET + self.X_DELAY * (j + 1) + self.BTN_SIZE * j,
                    self.Y_OFFSET + self.Y_DELAY * (i + 1) + self.BTN_SIZE * i,
                    self.BTN_SIZE, self.BTN_SIZE, str(index + 1),
                    color = (25, 79, 33) if (index) in self.levels_done[self.current_page] else None)
                else:
                    self.level_btns[i * self.BTN_COLS + j] = None
    
    def update_beaten_levels(self, levels: list[int]) -> None:
        self.levels_done = divide_list(levels.copy(), self.BTN_COLS * self.BTN_ROWS, self.PAGES_LIMIT)
        self.__create_new_btns()

    def draw(self, pos) -> None:
        self.screen.fill(BG_COLOR)
        self.current_btn = None
        for i in range(self.BTN_ROWS):
            for j in range(self.BTN_COLS):
                if (self.level_btns[i * self.BTN_COLS + j] is not None and
                    self.level_btns[i * self.BTN_COLS + j].draw(pos)):
                    self.current_btn = i * self.BTN_COLS + j
        if self.current_page > 0 and self.back_btn.draw(pos):
            self.current_btn = -1
        if self.current_page < (self.PAGES_LIMIT - 1) and self.next_btn.draw(pos):
            self.current_btn = -2
        if self.home_btn.draw(pos):
            self.current_btn = -3
    
    def click(self) -> bool:
        if self.current_btn is not None and self.current_btn > -1:
            return self.current_page * self.BTN_COLS * self.BTN_ROWS + self.current_btn
        elif self.current_btn == -1:
            self.current_page -= 1
            self.__create_new_btns()
        elif self.current_btn == -2:
            self.current_page += 1
            self.__create_new_btns()
        elif self.current_btn == -3:
            return -1
        return -2
