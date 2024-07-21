import pygame

import assets
import configs
from objects import layer
from objects.hamburger import Hamburger, visualize_hamburger
from objects.layer import Layer

# These parematers are derived from the geometry of the jenny picture
tray_width = 36
class Jenny(pygame.sprite.Sprite):
    def __init__(self, floor_y, *groups):
        self._layer = Layer.PLAYER
        self.collected_ingredients = []
        self.floor_y = floor_y
        self.move_speed = 0
        self.__create()

        super().__init__(*groups)

    def update_collected_ingredients(self, ingredients):
        self.restore_x = self.rect.x
        self.collected_ingredients = ingredients
        self.__create()

    def __create(self):
        jenny = assets.get_sprite("jenny")
        hamburger = visualize_hamburger(self.collected_ingredients, 10)
        hamburger_scaled = pygame.transform.scale(hamburger, (tray_width, tray_width * hamburger.get_height() / hamburger.get_width()))

        total_width = jenny.get_width()
        total_height = jenny.get_height()
        total_height += hamburger_scaled.get_height()

        self.image = pygame.surface.Surface((total_width, total_height), pygame.SRCALPHA)
        self.image.blit(jenny, (0, total_height - jenny.get_height()))
        self.image.blit(hamburger_scaled, ((total_width - hamburger_scaled.get_width()) / 2, 0))

        pos_x = self.restore_x if hasattr(self, 'restore_x') else (configs.SCREEN_WIDTH - self.image.get_rect().width) / 2
        self.rect = self.image.get_rect(
            topleft=(pos_x, self.floor_y - self.image.get_rect().height))
        self.mask = pygame.mask.from_surface(self.image)
        #print("Jenny mask:", self.mask)


    def handle_event(self, event):
        new_x = self.rect.x
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            new_x -= configs.JENNY_MOVE_SPEED
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            new_x += configs.JENNY_MOVE_SPEED
        elif event.type == pygame.MOUSEMOTION:
            new_x = pygame.mouse.get_pos()[0] - self.image.get_width() / 2
        new_x = max(new_x, self.image.get_width() / -2)
        new_x = min(new_x, configs.SCREEN_WIDTH - self.image.get_width() / 2)
        self.rect.x = new_x

    def teleport_to(self, x):
        self.rect.x = x
    def check_overlap(self, sprite):
        if sprite.layer not in [Layer.INGREDIENT_BUN_BOTTOM,
                                Layer.INGREDIENT_BUN_TOP,
                                Layer.INGREDIENT_MEAT,
                                Layer.INGREDIENT_CHEESE,
                                Layer.INGREDIENT_TOPPING,
                                Layer.INGREDIENT_VEGGI]:
            return
        if not hasattr(sprite, 'mask'):
            sprite.mask = pygame.mask.from_surface(sprite.image)
        if sprite.mask.overlap(self.mask,
                               (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)):
            sprite_x = sprite.rect.x + sprite.rect.width / 2
            trey_x = self.rect.x + self.image.get_width() / 2
            if abs(trey_x - sprite_x) < configs.INGREDIENT_COLLECTION_MARGIN\
                    and sprite.rect.y < self.rect.y + 20:
                return True
        return False

    def check_collision(self, sprites):
        for sprite in sprites:
            if sprite._layer in [Layer.INGREDIENT_BUN_BOTTOM, Layer.INGREDIENT_BUN_TOP, Layer.INGREDIENT_TOPPING, Layer.INGREDIENT_CHEESE, Layer.INGREDIENT_MEAT, Layer.INGREDIENT_VEGGI]:
                if self.check_overlap(sprite):
                    return sprite
        return None
