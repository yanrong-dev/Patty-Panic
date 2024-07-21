import pygame.sprite

import assets
import configs
from objects.layer import Layer


class Floor(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.FLOOR
        self.image = assets.get_sprite("cashier_stock")
        self.rect = self.image.get_rect(bottomleft=(0, configs.SCREEN_HEIGHT))
        super().__init__(*groups)

    def get_floor_y(self):
        return self.rect.y