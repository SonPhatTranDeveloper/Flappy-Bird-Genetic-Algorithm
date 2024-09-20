from pygame.sprite import Sprite
from pygame.font import SysFont


BIG_FONT = SysFont('timenewsroman', 60)
SMALL_FONT = SysFont('timenewsroman', 40)


class BigText(Sprite):
    def __init__(self, text):
        # Initialize image
        super().__init__()
        self.surf = BIG_FONT.render(text, True, (255, 255, 255))
        self.rect = self.surf.get_rect()


class SmallText(Sprite):
    def __init__(self, text):
        # Initialize image
        super().__init__()
        self.surf = SMALL_FONT.render(text, True, (255, 255, 255))
        self.rect = self.surf.get_rect()
