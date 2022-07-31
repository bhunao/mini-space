from random import randint
from typing import Any

import pygame.draw
from pygame import time, Color
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface

from configs import WIDTH, HEIGHT
from functions import load_and_resize


class BgStar(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((30, 70))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        star_size = randint(1, 3)
        x = randint(0, WIDTH)
        speed = randint(10, 35)
        # pygame.draw.circle(self.image, (255, 255, 255), self.rect.center, star_size)
        pygame.draw.line(self.image, (255, 255, 255, 25), (0, 0), (0, 70), star_size)
        self.pos = Vector2(x, 0)
        self.rect.center = self.pos
        self.speed = Vector2(0, speed)

    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.top > HEIGHT:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image.set_colorkey((0, 0, 0)), self.rect)


class Explosion(Sprite):
    def __init__(self, pos, size=1):
        super().__init__()
        self.images = [
            load_and_resize(f"imgs/effects/explosion_{n:02d}.png", (30*size, 30*size))
            for n in range(1, 6)
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.tick = time.get_ticks()
        self.index = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        tick = time.get_ticks()
        if tick - self.tick > 50:
            self.image = self.images[self.index]
            self.index += 1
            self.tick = tick
            if self.index >= len(self.images):
                self.kill()
                return


class TakeDamage(Sprite):
    def __init__(self, sprite: Sprite):
        super().__init__()
        mask = pygame.mask.from_surface(sprite.image)
        self.image = mask.to_surface(unsetcolor=Color(0, 0, 0), setcolor=Color(255, 0, 9, 50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = sprite.rect
        self.index = 5
        self.tick = time.get_ticks()

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        tick = time.get_ticks()
        if tick - self.tick > 50:
            self.index -= 1
            self.tick = tick
            if self.index <= 0:
                self.kill()
                return
