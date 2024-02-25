import pygame
import sys

from src.board_generator import boardGenerator
from src.level import Level
from src.utils import *



class Game:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.lvl = Level(self.screen, 52)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.lvl.click(event.pos[0], event.pos[1])
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.lvl.release(event.pos[0], event.pos[1])
                elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    self.lvl.move(event.pos[0], event.pos[1])
            self.lvl.draw()
            pygame.display.flip()
            self.clock.tick(90)
