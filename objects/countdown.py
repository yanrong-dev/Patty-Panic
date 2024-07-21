import pygame

import assets
import configs
from objects.layer import Layer


class Countdown(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.time_left = 0
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        self.__create()
        super().__init__(*groups)

    def __create(self):
        minutes = int(self.time_left / 60)
        seconds = int(self.time_left % 60)
        display_text = "0" + str(minutes) + "=" + "00"[:2 - len(str(seconds))] + str(seconds)
        images = []
        total_width = 0
        total_height = 0
        clock_bg = assets.get_sprite("clock")
        for str_value in display_text:
            img = assets.get_sprite(str_value)
            images.append(img)
            total_width += img.get_width()
            total_height = max(total_height, img.get_height())
        self.image = pygame.surface.Surface((clock_bg.get_width(), clock_bg.get_height()), pygame.SRCALPHA)
        self.image.blit(clock_bg, clock_bg.get_rect(topleft=(0, 0)))
        image_x = (clock_bg.get_width() - total_width) / 2
        for letter in images:
            self.image.blit(letter, letter.get_rect(
                topleft=(image_x, (clock_bg.get_height() - 10 - letter.get_height()) / 2)))
            image_x += letter.get_width()
        self.rect = self.image.get_rect(topleft = (configs.SCREEN_WIDTH - 185, 10))

    def set_time(self, time_left):
        self.time_left = max(0, time_left)
        self.__create()