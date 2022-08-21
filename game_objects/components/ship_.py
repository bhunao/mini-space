from abc import ABC, abstractmethod
from typing import List

from pygame import time
from pygame.rect import Rect

from functions import cooldown
from game_objects.bullets import Bullet
from game_objects.components.BaseBullet import BaseBullet


class ShipStats(ABC):
    health = 10
    ship_name = "Ship"

    def __init__(self):
        super(ShipStats, self).__init__()


class PrimaryFire(ABC):
    rect: Rect

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, bullet_type: BaseBullet = Bullet, delay: int = 200):
        self._cooldown_ = time.get_ticks()
        self._delay_ = 200
        self.bullet = bullet_type

    @abstractmethod
    def primary_fire(self) -> List[BaseBullet]: pass
