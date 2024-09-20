import random

from pygame.sprite import Sprite
from pygame.image import load

from config import (
    PIPE_SPAWN,
    PIPE_SPAWN_GAP,
    PIPE_VELOCITY,
    PIPE_GAP,
    PIPE_ASSET_1,
    PIPE_ASSET_2
)
from init import Vector2D


class Pipes(Sprite):
    @staticmethod
    def generate_pipes():
        # Create coordinates
        y_1 = random.randint(300, 600)
        y_2 = random.randint(300, 600)
        # Create a pipe
        return [Pipes(PIPE_SPAWN, y_1), Pipes(PIPE_SPAWN + PIPE_SPAWN_GAP, y_2)]

    def __init__(self, x, y):
        # Initialize image
        super().__init__()

        # Create first pipe
        self.first_pipe = load(PIPE_ASSET_1)
        self.first_rect = self.first_pipe.get_rect(
            topleft=(x, y)
        )

        # Create second pipe
        self.second_pipe = load(PIPE_ASSET_2)
        self.second_rect = self.second_pipe.get_rect(
            bottomleft=(x, y - PIPE_GAP)
        )

        # Initialize the position of the pipes
        self.first_pos = Vector2D(x, y)
        self.second_pos = Vector2D(x, y - PIPE_GAP)
        self.velocity = Vector2D(-PIPE_VELOCITY, 0)

    def move(self):
        """
        Move the pipe
        :return: None
        """
        self.first_pos += self.velocity
        self.second_pos += self.velocity
        self.first_rect.topleft = self.first_pos
        self.second_rect.bottomleft = self.second_pos
