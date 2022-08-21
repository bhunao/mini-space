from typing import List

from pygame.math import Vector2

from game_objects.bullets import Bullet
from game_objects.components.ship_components import ShipBase, ABCBullet, ABCRayGun


class Enemy(ShipBase):
    def __init__(self, bullets_group=None, pos=None):
        super().__init__(angle=180)
        self.bullets_group = bullets_group
        self.speed = Vector2(0, 1)
        self._angle = 90
        self._cooldown["primary_fire"]["delay"] = 1200

        if pos is not None:
            print(f"{pos=}, {bullets_group=}")
            self.rect.center = pos

    def primary_fire(self) -> List[ABCBullet]:
        if self.bullets_group:
            bullets = [Bullet(self.rect.center, self._angle)]
            self.bullets_group.add(bullets)
            return bullets
        return []

    def secondary_fire(self) -> List[ABCRayGun]:
        raise NotImplementedError

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.ship_update()
