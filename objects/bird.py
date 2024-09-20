from typing import List

from pygame.sprite import Sprite
from pygame.image import load

import numpy as np

from config import (
    GAME_HEIGHT,
    GAME_WIDTH,
    BIRD_ASSET,
    BIRD_ACCEL,
    BIRD_FLAP_STRENGTH
)
from init import Vector2D
from ai import Brain


class Bird(Sprite):
    def __init__(self):
        # Initialize image
        super().__init__()
        self.surf = load(BIRD_ASSET)
        self.rect = self.surf.get_rect(
            center=(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        )

        # Initialize movements
        self.pos = Vector2D(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.velocity = Vector2D(0, 0)
        self.acceleration = Vector2D(0, BIRD_ACCEL)
        self.flap_strength = Vector2D(0, -BIRD_FLAP_STRENGTH)

        # Create a brain of the bird
        self.brain = Brain()

        # Check if dead
        self.dead = False

        # Initialize a score - how long the bird has survived
        self.score = 0

    def move(self):
        # Update the position, velocity
        self.velocity += self.acceleration
        self.pos += self.velocity

        # Update rectangle
        self.rect.midbottom = self.pos

    def make_decision(self, pipes):
        # Get the vision
        vision = self.get_vision(pipes)

        # Pass through the brain and make decision
        if self.brain.perform_action(vision):
            self.flap()

    def flap(self):
        # Make flap
        self.velocity = Vector2D(0, -BIRD_FLAP_STRENGTH)

    def increase_score(self):
        self.score += 1

    def _has_drop_below_screen(self):
        """
        Check if a bird has dropped below screen
        :return: True or False
        """
        return self.rect.bottomleft[1] >= GAME_HEIGHT

    def _has_collided_with_pipes(self, pipes: List):
        """
        Check if a bird has collided with pipes
        :param pipes: a list of pipes
        :return: True or False
        """
        for pipe in pipes:
            if self.rect.colliderect(pipe.first_rect):
                return True
            if self.rect.colliderect(pipe.second_rect):
                return True

        return False

    def is_dead(self, pipes: List):
        """
        Return if the bird has collided with the ground or with the pipe
        :return: True or False
        """
        if self._has_drop_below_screen() or self._has_collided_with_pipes(pipes):
            self.dead = True
            return True

    def get_vision(self, pipes):
        """
        Return the vision of the bird, which contain
        - bird_y_pos
        - bird_velocity
        - bird_dist_x to the next pipe
        - bird_dist_y_bottom to the bottom pipe
        - bird_dist_y_top to the top pipe
        in that order
        :param pipes: a list of pipe
        :return: a numpy vector
        """
        # Get the bird position and velocity
        bird_y_pos = self.rect.centery + 0.0
        bird_velocity = self.velocity.y + 0.0

        # Find the next pipe
        bird_dist_x = 0
        bird_dist_y_bottom = 0
        bird_dist_y_top = 0

        for pipe in pipes:
            if pipe.first_rect.midtop[0] >= self.rect.centerx:
                bird_dist_x = pipe.first_rect.midtop[0] - self.rect.centerx + 0.0
                bird_dist_y_bottom = self.rect.centery - pipe.first_rect.midtop[1] + 0.0
                bird_dist_y_top = pipe.second_rect.midbottom[1] - self.rect.centery + 0.0
                break

        return np.array(
            [
                bird_y_pos,
                bird_velocity,
                bird_dist_x,
                bird_dist_y_bottom,
                bird_dist_y_top
            ]
        )

    def clone(self):
        """
        Clone the current bird
        :return: new bird with the same brain
        """
        # Create a new bird
        new_bird = Bird()

        # Transfer the brain
        new_bird.brain.receive_genes(
            W1=self.brain.W1,
            b1=self.brain.b1,
            W2=self.brain.W2,
            b2=self.brain.b1
        )

        return new_bird