import math
from abc import abstractmethod
from typing import Dict, List, Any

import pygame
from pygame import Surface, draw, Color
from pygame.image import load
from pygame.math import Vector2
from pygame.sprite import Sprite, AbstractGroup
from pygame.time import get_ticks
from pygame.transform import rotate, scale


class ABCBullet(Sprite):
    def __init__(self, angle, *groups: AbstractGroup):
        super().__init__(*groups)
        size = (18, 8)
        base_speed = 6
        speed_x = math.cos(math.radians(angle)) * base_speed
        speed_y = math.sin(math.radians(angle)) * base_speed

        self.color1 = Color("cornsilk")
        self.color2 = Color("cyan")
        self._angle: int = angle
        self.damage: int = 1
        self.speed: Vector2 = Vector2(speed_x, speed_y)
        self.image = Surface(size)
        self.image = rotate(self.image, self._angle)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.draw_bullet()

    def draw_bullet(self):
        draw.rect(self.image, self.color1, self.rect, border_radius=10)
        draw.rect(self.image, self.color2, self.rect, 2, border_radius=5)


class ABCRayGun(Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        size = (18, 550)
        base_speed = 6

        self.color1 = Color("cornsilk")
        self.color2 = Color("cyan")
        self.damage: int = 1
        self.speed: Vector2 = Vector2(0, 0)
        self.image = Surface(size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.draw_bullet()
        self.timer = 50

    def draw_bullet(self):
        draw.rect(self.image, self.color1, self.rect, border_radius=10)
        draw.rect(self.image, self.color2, self.rect, 2, border_radius=10)

    def update(self, *args: Any, **kwargs: Any) -> None:
        print(123123123)
        super().update(*args, **kwargs)
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class ShipBase(Sprite):
    def __init__(self, *groups: AbstractGroup, path=None, angle=0):
        super().__init__(*groups)
        self._cooldown = self.generate_cooldowns()
        image_path = path if path else "enemy.gif"
        self.image = load(image_path)
        self.image = scale(self.image, (50, 50))
        self._angle = angle
        self.image = rotate(self.image, self._angle)
        self.rect = self.image.get_rect()
        self.health: int = 10
        self.direction: float = 0
        self.speed: Vector2 = Vector2(0, 0)
        self._angle: int = 0
        self._primary: ABCBullet = ABCBullet(0)
        self._secondary_energy: int = 0
        self._screen_size = pygame.display.get_surface().get_size()

    def _player_out_of_bounds(self):
        if self.rect.bottom < 0 or self.rect.top > self._screen_size[1]:
            self.kill()

    @staticmethod
    def generate_cooldowns() -> Dict[str, Dict]:
        return {
            "primary_fire": {"last_update": get_ticks(), "delay": 200},
            "damage_taken": {"last_update": get_ticks(), "delay": 200},
        }

    @property
    def primary(self) -> ABCBullet: return self._primary

    @primary.setter
    def primary(self, value) -> None: self._primary = value

    @abstractmethod
    def primary_fire(self) -> List[ABCBullet]: pass

    def ship_update(self) -> None:
        self._player_out_of_bounds()
        if self.health <= 0:
            self.kill()

        self.rect.center += self.speed

        if self.is_ready("primary_fire"):
            self.primary_fire()

    def is_ready(self, cd_name: str) -> bool:
        current_tick = get_ticks()
        cooldown = self._cooldown.get(cd_name)
        if cooldown:
            cd = cooldown.get("last_update", 1)
            delay = cooldown.get("delay", 300)
            if current_tick - cd > delay:
                self._cooldown[cd_name] = {"last_update": current_tick, "delay": delay}
                return True
        else:
            self._cooldown[cd_name] = {"last_update": current_tick, "delay": 300}
        return False
