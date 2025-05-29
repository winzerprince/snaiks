# food.py: Defines the Food class
import pygame
import random
from settings import *
from pygame.math import Vector2

class Food:
    def __init__(self):
        self.position = Vector2(random.randint(FOOD_RADIUS, SCREEN_WIDTH - FOOD_RADIUS),
                                random.randint(FOOD_RADIUS, SCREEN_HEIGHT - FOOD_RADIUS))
        self.color = FOOD_COLOR
        self.radius = FOOD_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)


