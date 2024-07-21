import pygame

import assets
import configs
from objects.layer import Layer

def visualize_hamburger(ingredients, marginal_height):
    if len(ingredients) == 0:
        return pygame.surface.Surface((20, 20), pygame.SRCALPHA)
    else:
        images = []
        for ing in ingredients:
            images.append(assets.get_sprite(ing))
        total_height = images[-1].get_height()
        total_width = images[-1].get_width()
        for i in range(len(images) - 1):
            total_width = max(total_width, images[i].get_width())
            total_height += marginal_height

        image = pygame.surface.Surface((total_width, total_height), pygame.SRCALPHA)
        target_y = total_height
        for i in range(len(images)):
            sprite = images[i]
            image.blit(sprite, sprite.get_rect(
                topleft=((total_width - sprite.get_width()) / 2, target_y - sprite.get_height())))
            target_y -= marginal_height
        return image

DEFAULT_HEIGHT = 25
class Hamburger(pygame.sprite.Sprite):
    def __init__(self, *groups, ingredients=[]):
        #print(ingredients)
        self._layer = Layer.HAMBURGER
        self.ingredients = ingredients
        self.marginal_height = DEFAULT_HEIGHT
        self.__create()
        super().__init__(*groups)

    def __create(self):
        if len(self.ingredients) == 0:
            self.image = pygame.surface.Surface((20, 20), pygame.SRCALPHA)
        else:
            self.image = visualize_hamburger(self.ingredients, self.marginal_height)

        self.rect = self.image.get_rect(topleft = (configs.SCREEN_WIDTH - self.image.get_width() - 43, configs.SCREEN_HEIGHT - self.image.get_height() - 5))

    def set_marginal_height(self, height):
        self.marginal_height = height
    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
        more_than_5 = max(0, len(ingredients) - 5)
        self.set_marginal_height(DEFAULT_HEIGHT - more_than_5 * 4)
        self.__create()