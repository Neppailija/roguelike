import pygame
import tcod

pygame.init()

# Game sizes
GAME_WIDTH = 1024
GAME_HEIGHT = 768
CELL_WIDTH = 32
CELL_HEIGHT = 32

# FPS LIMIT
GAME_FPS = 60

# MAP variables
MAP_WIDTH = 30
MAP_HEIGHT = 30

# Color definition
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

# Sprites
# S_PLAYER = pygame.image.load("data\\virusmies.png")
S_ENEMY = pygame.image.load("data\\matobakteerimies.png")

S_WALL = pygame.image.load("data\\wall.png")
S_WALL_EXPLORED = pygame.image.load("data\\wallunseen.png")

S_FLOOR = pygame.image.load("data\\floor.jpg")
S_FLOOR_EXPLORED = pygame.image.load("data\\floorunseen.png")

# FOV settings
FOV_ALGO = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

# FONTS
FONT_DEBUG_MESSAGE = pygame.font.Font("data\\joystix monospace.ttf", 20)
FONT_MESSAGE_TEXT = pygame.font.Font("data\\joystix monospace.ttf", 20)

# Message defaults
NUM_MESSAGES = 4