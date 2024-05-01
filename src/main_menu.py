import pygame

from src.utils import *

class mainMenu:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.levels_btn = Button(self.screen, 
                               WIDTH // 2 - 90,
                               HEIGHT // 2, 180, 80, 
                               "Level list")
        self.generate_btn = Button(self.screen, 
                               WIDTH // 2 - 150,
                               HEIGHT // 2 + 100, 300, 80, 
                               "Generate levels")
        self.font = pygame.font.Font(None, 100)
        self.title_text = self.font.render("Brick Puzzle", True, (204, 204, 204))
        self.title_text_rect = self.title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        self.current_btn = 0
        
    def draw(self, pos) -> None:
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.title_text, self.title_text_rect)
        self.current_btn = 0
        if self.levels_btn.draw(pos):
            self.current_btn = 1
        if self.generate_btn.draw(pos):
            self.current_btn = 2

    def click(self) -> int:
        return self.current_btn
    
    