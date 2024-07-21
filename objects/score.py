import pygame

import assets
import configs
from objects.layer import Layer


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.level = 1
        self.value = 0
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        self.__create()
        super().__init__(*groups)

    def __create(self):
        self.str_value = "L" + str(self.level) + "-" + str(self.value) + "%" + str(configs.GOALS_PER_ROUND)
        self.images = []
        self.width = 0
        for str_value in self.str_value:
            img = assets.get_sprite(str_value)
            self.images.append(img)
            self.width += img.get_width()
        self.height = self.images[0].get_height()
        self.image = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (30, 30))

        score_x = 0
        for img in self.images:
            self.image.blit(img, (score_x, 0))
            score_x += img.get_width()

    def set_level(self, level):
        self.level = level

    def update(self):
        self.__create()