import pygame

from src.utils import *

SQUARE_COLORS = ((255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255)
)
GRAVITY = 0.981

class Square:

    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, color: int, direct: bool) -> None:
        self.screen = screen
        self.rect = pygame.Rect(x, y, size, size)
        self.surf = pygame.Surface((size, size))
        self.surf.fill(SQUARE_COLORS[color])
        self.color = color
        self.state = False
        self.velocity = 0
        self.DIR = direct
        self.LIMIT = x
    
    def draw(self) -> bool:
        flag = False
        if self.state:
            if self.DIR:
                if self.rect.x + self.velocity < self.LIMIT:
                    self.state = False
                    self.rect.x = self.LIMIT
                    flag = True
                else:
                    self.rect.x += self.velocity
                    self.velocity -= GRAVITY
            else:
                if self.rect.x + self.velocity > self.LIMIT:
                    self.state = False
                    self.rect.x = self.LIMIT
                    flag = True
                else:
                    self.rect.x += self.velocity
                    self.velocity += GRAVITY
        self.screen.blit(self.surf, self.rect)
        return flag

    def punch(self) -> None:
        self.color = (self.color + 1 ) % 6
        self.surf.fill(SQUARE_COLORS[self.color])
        self.state = True
        self.velocity = 15 if self.DIR else -15

class loadingScreen:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.rect1 = Square(screen, WIDTH // 2 - 60, HEIGHT // 2 - 30,
                            60, 0, False)
        self.rect2 = Square(screen, WIDTH // 2, HEIGHT // 2 - 30,
                            60, 3, True)
        self.rect1.punch()
    
    def draw(self, pos) -> None:
        self.screen.fill(BG_COLOR)
        if self.rect1.draw():
            self.rect2.punch()
        if self.rect2.draw():
            self.rect1.punch()
