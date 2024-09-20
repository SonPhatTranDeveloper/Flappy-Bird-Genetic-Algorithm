# Import from PyGame
import pygame
from pygame.locals import *

# Initialize vector
Vector2D = pygame.math.Vector2

# Initialize
pygame.init()

# Import config variables
from config import GAME_HEIGHT, GAME_WIDTH, GAME_TITLE

# Create clock
FRAME_PER_SEC = pygame.time.Clock()

# Create display surface
DISPLAY_SURFACE = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

# Set caption for the display surface
pygame.display.set_caption(GAME_TITLE)
