import pygame
import sys
from threading import Thread
import random
import sqlite3

from src.level import Level
from src.utils import *
from src.level_choose import levelChoose
from src.main_menu import mainMenu
from src.loading_screen import loadingScreen
from src.board_generator import boardGenerator

class Game:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Puzzle")
        self.clock = pygame.time.Clock()
        self.menu = mainMenu(self.screen)
        self.game_mode = 0
        self.generate_status = False
        self.generate_size = ()
        self.generate_bricks = ()
        self.pos = (0, 0)
        self.beaten_levels: list[int] = []
        self.levels = []

        conn = sqlite3.connect(res_path("assets/levels.db"))
        c = conn.cursor()
        c.execute("""SELECT * FROM lvl""")
        for i in c.fetchall():
            self.levels.append(((i[1], i[2]), ) + (tuple(tuple(tuple(map(int, x.split(':'))) for x in y.split(';')) for y in i[3].split('_')), ))
        self.lvl = Level(self.screen, 1, self.levels[1][1], self.levels[1][0])

        with open(res_path("assets/save.txt"), "r") as f:
            lines = f.readlines()
            if lines:
                for lvl in lines[0].rstrip(";").split(";"):
                    self.beaten_levels.append(int(lvl, 8))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                match self.game_mode:
                    case 0:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pressed_button = self.menu.click()
                            if pressed_button == 1: # levels list button
                                self.game_mode = 1
                                self.menu = levelChoose(self.screen, self.beaten_levels, len(self.levels))
                            elif pressed_button == 2: # generate levels button
                                self.game_mode = 3
                                self.generate_status = False
                                Thread(target=self.generate_level, daemon=True).start()
                                self.menu = loadingScreen(self.screen)
                        elif event.type == pygame.MOUSEMOTION:
                            self.pos = event.pos
                    case 1:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            res = self.menu.click()
                            if res >= 0:
                                self.game_mode = 2
                                self.lvl = Level(self.screen, res, self.levels[res][1], self.levels[res][0])
                            elif res == -1: # back button
                                self.game_mode = 0
                                self.menu = mainMenu(self.screen)
                        elif event.type == pygame.MOUSEMOTION:
                            self.pos = event.pos
                    case 2:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.lvl.click(event.pos[0], event.pos[1])
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            match self.lvl.release(event.pos[0], event.pos[1]):
                                case 1: # back button
                                    if self.lvl.index is None: # if level was generated
                                        self.game_mode = 0
                                        self.menu = mainMenu(self.screen)
                                        self.generate_status = False
                                    else: # if level is from list
                                        self.game_mode = 1
                                        if self.lvl.is_done and self.lvl.index not in self.beaten_levels:
                                            self.beaten_levels.append(self.lvl.index)
                                            with open(res_path("assets/save.txt"), "a") as f:
                                                f.write(str(oct(self.lvl.index))[2:] + ";")
                                        self.menu.update_beaten_levels(self.beaten_levels)
                                case 2: # next button
                                    if self.lvl.index is not None: # if level wasn't generated
                                        if self.lvl.index not in self.beaten_levels:
                                            self.beaten_levels.append(self.lvl.index)
                                            with open(res_path("assets/save.txt"), "a") as f:
                                                f.write(str(oct(self.lvl.index))[2:] + ";")
                                        if self.lvl.index < self.menu.LEVEL_QUANTITY - 1: # if button isn't the last one
                                            self.lvl = Level(self.screen, 
                                                             self.lvl.index + 1, 
                                                             self.levels[self.lvl.index + 1][1], 
                                                             self.levels[self.lvl.index + 1][0])
                                        else: # otherwise switch to menu
                                            self.game_mode = 1
                                        self.menu.update_beaten_levels(self.beaten_levels)
                                    else: # if level was generated
                                        self.game_mode = 3
                                        self.generate_status = False
                                        Thread(target=self.generate_level, daemon=True).start()
                                        self.menu = loadingScreen(self.screen)

                        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                            self.lvl.move(event.pos[0], event.pos[1])
                        elif event.type == pygame.MOUSEMOTION:
                            self.pos = event.pos        
            if self.game_mode in (0, 1, 3):
                self.menu.draw(self.pos)
                if self.generate_status:
                    self.game_mode = 2
                    self.lvl = Level(self.screen, 
                                    None, 
                                    self.generate_bricks, 
                                    self.generate_size)
            else:
                self.lvl.draw(self.pos)
            pygame.display.flip()
            self.clock.tick(90)
    
    def generate_level(self) -> None:
        n = random.randint(5, 9)
        m = random.randint(-n + 13, -n + 15)
        self.generate_size = (n, m)
        generator = boardGenerator(n, m)
        self.generate_bricks = generator.generate()[0]
        self.generate_status = True
