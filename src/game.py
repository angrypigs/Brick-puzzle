import pygame
import sys

from src.level import Level
from src.utils import *
from src.level_choose import levelChoose

class Game:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.lvl = Level(self.screen, 1)
        self.menu = levelChoose(self.screen)
        self._is_in_menu = True
        self.pos = (0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self._is_in_menu:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        is_lvl_clicked = self.menu.click_input()
                        if is_lvl_clicked:
                            self._is_in_menu = False
                            self.lvl = Level(self.screen, is_lvl_clicked)
                    elif event.type == pygame.MOUSEMOTION:
                        self.pos = event.pos
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.lvl.click(event.pos[0], event.pos[1])
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        match self.lvl.release(event.pos[0], event.pos[1]):
                            case 1:
                                self._is_in_menu = True
                                print("lol")
                            case 2:
                                if self.lvl.index < self.menu.LEVEL_QUANTITY:
                                    self.lvl = Level(self.screen, self.lvl.index + 1)
                                else:
                                    self._is_in_menu = True
                    elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                        self.lvl.move(event.pos[0], event.pos[1])
                    elif event.type == pygame.MOUSEMOTION:
                        self.pos = event.pos
            if self._is_in_menu:
                self.menu.draw(self.pos)
            else:
                self.lvl.draw(self.pos)
            pygame.display.flip()
            self.clock.tick(90)
