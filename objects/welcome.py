import pygame.sprite

import assets
import configs
from objects.layer import Layer


class Welcome(pygame.sprite.Sprite):
    def __init__(self,  *groups):
        self._layer = Layer.BACKGROUND
        self.image = assets.get_sprite("welcome")
        self.rect = self.image.get_rect(topleft=(0, 0))
        super().__init__(*groups)