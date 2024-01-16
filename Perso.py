from pygame.sprite import *
import pygame as py

from GameObject import GameObject


class Perso(GameObject):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height, (0, 0))
        self.lives = 3
        self.points = 0

    def update(self):
        # *args, **kwargs
        pass
