import pygame
import sys
from threading import Thread
import random

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
        self.clock = pygame.time.Clock()
        self.lvl = Level(self.screen, 1)
        self.menu = mainMenu(self.screen)
        self.game_mode = 0
        self.generate_status = False
        self.generate_size = ()
        self.generate_bricks = ()
        self.pos = (0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                match self.game_mode:
                    case 0:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pressed_button = self.menu.click()
                            if pressed_button == 1:
                                self.game_mode = 1
                                self.menu = levelChoose(self.screen)
                            elif pressed_button == 2:
                                self.game_mode = 3
                                self.generate_status = False
                                Thread(target=self.generate_level).start()
                                self.menu = loadingScreen(self.screen)
                        elif event.type == pygame.MOUSEMOTION:
                            self.pos = event.pos
                    case 1:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            is_lvl_clicked = self.menu.click()
                            if is_lvl_clicked > 0:
                                self.game_mode = 2
                                self.lvl = Level(self.screen, is_lvl_clicked)
                            elif is_lvl_clicked == -1:
                                self.game_mode = 0
                                self.menu = mainMenu(self.screen)
                        elif event.type == pygame.MOUSEMOTION:
                            self.pos = event.pos
                    case 2:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.lvl.click(event.pos[0], event.pos[1])
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            match self.lvl.release(event.pos[0], event.pos[1]):
                                case 1:
                                    if self.lvl.index is None:
                                        self.game_mode = 0
                                        self.menu = mainMenu(self.screen)
                                    else:
                                        self.game_mode = 1
                                        self.menu = levelChoose(self.screen)
                                case 2:
                                    if self.lvl.index is not None:
                                        if self.lvl.index < self.menu.LEVEL_QUANTITY:
                                            self.lvl = Level(self.screen, self.lvl.index + 1)
                                        else:
                                            self.game_mode = 1
                                    else:
                                        self.game_mode = 3
                                        self.generate_status = False
                                        Thread(target=self.generate_level).start()
                                        self.menu = loadingScreen(self.screen)
                        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                            self.lvl.move(event.pos[0], event.pos[1])
                        elif event.type == pygame.MOUSEMOTION:
                            self.pos = event.pos
                    case 3:
                        if self.generate_status:
                            self.game_mode = 2
                            self.lvl = Level(self.screen, None, 
                                             self.generate_bricks, 
                                             self.generate_size)
            if self.game_mode in (0, 1, 3):
                self.menu.draw(self.pos)
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
