import random

import pygame

import assets
import configs
from objects.layer import Layer


class Customer(pygame.sprite.Sprite):
    def __init__(self, floor_y, *groups):
        self._layer = Layer.UI
        self.images = list(assets.search_sprite("customers-").values())
        self.frame_index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(10, floor_y + 50))

        self.mask = pygame.mask.from_surface(self.image)
        #print(self.mask)

        super().__init__(*groups)

    def collect(self):
        self.kill()

    def update(self):
        self.frame_index += 1
        self.image_index = (int(self.frame_index / (configs.FPS / configs.ANIMATION_FPS)) + 1) % len(self.images)
        self.image = self.images[self.image_index]