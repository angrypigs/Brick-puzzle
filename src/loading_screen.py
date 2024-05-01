import pygame

from src.utils import *

class loadingScreen:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
    
    def draw(self, pos) -> None:
        self.screen.fill(BG_COLOR)