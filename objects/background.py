import pygame

import assets
import configs
from objects.layer import Layer


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.BACKGROUND
        self.sprite = assets.get_sprite("background")
        x_ratio = configs.SCREEN_WIDTH / self.sprite.get_rect().width
        y_ratio = configs.SCREEN_HEIGHT / self.sprite.get_rect().height
        scale_ratio = max(x_ratio, y_ratio)
        #print(x_ratio, y_ratio, scale_ratio)
        self.image = pygame.transform.scale(self.sprite, (self.sprite.get_rect().width * scale_ratio, self.sprite.get_rect().height * scale_ratio))
        #print(self.image.get_rect())

        self.rect = self.image.get_rect(topleft=((self.image.get_rect().width - configs.SCREEN_WIDTH)/-2, (self.image.get_rect().height - configs.SCREEN_HEIGHT)/-2))
        #print(self.rect)


        super().__init__(*groups)