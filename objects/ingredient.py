import random

import pygame

import assets
import configs
from objects.layer import Layer

def get_layer_from_name(name):
    if name == 'bun-bottom':
        return Layer.INGREDIENT_BUN_BOTTOM
    elif name == 'bun-top':
        return Layer.INGREDIENT_BUN_TOP
    elif name.startswith('meat'):
        return Layer.INGREDIENT_MEAT
    elif name.startswith('cheese'):
        return Layer.INGREDIENT_CHEESE
    elif name.startswith('topping'):
        return Layer.INGREDIENT_TOPPING
    elif name.startswith('veggi'):
        return Layer.INGREDIENT_VEGGI
class Ingredient(pygame.sprite.Sprite):
    def __init__(self, floor_y, *groups, prevent="", name=""):
        self.floor_y = floor_y
        self.all_ingredients = assets.search_sprite_by_names(['bun-', 'meat-', 'cheese-', 'topping-', 'veggi-'])
        if name == "":
            all_keys = list(self.all_ingredients.keys())
            while name == "" or name == prevent:
                name = all_keys[random.randint(0, len(all_keys) - 1)]
                #print("Randomly get ingredient name ", name)
        #else:
            #print("Spawn given ingredient ", name)
        self.ingredient_name = name
        self._layer = get_layer_from_name(name)
        self.image = assets.get_sprite(name)
        x = random.uniform(10, configs.SCREEN_WIDTH - self.image.get_rect().width - 10)
        self.rect = self.image.get_rect(topleft=(x, -1 * self.image.get_rect().height))
        #print("Spawn ", name, " at ", self.rect)

        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    def get_ingredient_name(self):
        return self.ingredient_name

    def update(self):
        self.rect.y += 3
        if self.rect.y >= self.floor_y:
            self.kill()