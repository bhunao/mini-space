from typing import List

from pygame import time
from pygame.image import load
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.transform import scale

from functions import cooldown
from game_objects.bullets import Bullet, RayGun


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("white-yellow.png")
        self.image = scale(self.image, (50, 50))
        # self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 250

        # stats
        self.max_velocity = Vector2(3, 3)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.ray = 50
        self._health = 10

        tick = time.get_ticks()
        self.ticks = {
            "primary_fire": {"tick": tick, "delay": 200},
            "secondary_fire": {"tick": tick, "delay": 10},
            "damage_taken": {"tick": tick, "delay": 200},
        }

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value) -> None:
        if self._cooldown("damage_taken"):
            self._health = value

    def _cooldown(self, tick_name: str) -> bool:
        return cooldown(self.ticks[tick_name])

    @property
    def velocity(self) -> Vector2:
        return self.__velocity

    @velocity.setter
    def velocity(self, value) -> None:
        x = abs(value.x)
        y = abs(value.y)
        if x > self.max_velocity.x:
            value.x = self.max_velocity.x if value.x > 0 else -self.max_velocity.x
        if y > self.max_velocity.y:
            value.y = self.max_velocity.y if value.y > 0 else -self.max_velocity.y
        self.__velocity = value

    def update(self):
        self.ray -= 1 if self.ray > 0 else 0
        self.velocity += self.acceleration
        if self.acceleration.x == 0:
            self.velocity.x *= 0.4
        if self.acceleration.y == 0:
            self.velocity.y *= 0.4
        self.rect.center += self.velocity

    def primary_fire(self) -> List[Bullet]:
        if self._cooldown("primary_fire"):
            self.ray += 5
            return [Bullet(self.rect.center)]
        return []

    def secondary_fire(self) -> List[RayGun]:
        if self._cooldown("secondary_fire"):
            self.ray += 25 if self.ray < 500 else 0
            return [RayGun(self.rect.center, self.ray)]
        return []
