import pygame
import os

# window
WIDTH = 900
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)

# game settings
FPS = 60
TILE = 100
# player/ship
p_pos = (200, HEIGHT / 2 + 300)
p_vis = 0

# bullet
b_speed = 20

# asteroids
astr_images = ['assets/astro1.png', 'assets/astro2.png']