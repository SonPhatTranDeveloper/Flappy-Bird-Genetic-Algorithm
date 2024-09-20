from pygame.sprite import Sprite
from pygame.image import load


class Background(Sprite):
    def __init__(self):
        super().__init__()
        self.surf = load("assets/background/background.png")
        self.rect = self.surf.get_rect()