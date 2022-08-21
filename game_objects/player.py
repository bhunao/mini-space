from typing import List

import pygame.display
from pygame.image import load
from pygame.math import Vector2
from pygame.transform import scale

from effects.spark import Spark
from game_objects.bullets import Bullet, RayGun, Ray
from game_objects.components.ship_components import ShipBase


class Player(ShipBase):
    def __init__(self):
        super().__init__(path="white-yellow.png")
        self.rect.x = 250
        self.rect.y = 250

        # stats
        self.max_velocity = Vector2(3, 3)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self._health = 10
        self._angle = -90
        self._screen_size = pygame.display.get_surface().get_size()

    def _player_out_of_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self._screen_size[0]:
            self.rect.right = self._screen_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self._screen_size[1]:
            self.rect.bottom = self._screen_size[1]

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value) -> None:
        if self.is_ready("damage_taken"):
            self._health = value

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, value) -> None:
        x = abs(value.x)
        y = abs(value.y)
        if x > self.max_velocity.x:
            value.x = self.max_velocity.x if value.x > 0 else -self.max_velocity.x
        if y > self.max_velocity.y:
            value.y = self.max_velocity.y if value.y > 0 else -self.max_velocity.y
        self._velocity = value

    def update(self):
        self._player_out_of_bounds()

        self.velocity += self.acceleration
        if self.acceleration.x == 0:
            self.velocity.x *= 0.4
        if self.acceleration.y == 0:
            self.velocity.y *= 0.4
        self.rect.center += self.velocity

    def primary_fire(self) -> List[Bullet]:
        if self.is_ready("primary_fire"):
            return [Bullet(self.rect.center, self._angle)]
        return []
