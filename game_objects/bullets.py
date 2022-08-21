from pygame import draw, Surface
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.transform import rotate

from game_objects.components.ship_components import ABCBullet, ABCRayGun


class Bullet(ABCBullet):
    def __init__(self, pos=(200, 200), angle=270):
        super(Bullet, self).__init__(angle)
        self.rect.center = pos

    def update(self):
        self.rect.center += self.speed


class Ray(ABCRayGun):
    def __init__(self, pos=(200, 200)):
        super().__init__()
        self.rect.midbottom = pos
        self.timer = 5

    def update(self):
        self.rect.center += self.speed
        self.timer -= 1
        if self.timer == 0:
            self.kill()


class RayGun(Sprite):
    def __init__(self, pos=(200, 200), length=1):
        super().__init__()
        max_height = 350
        width = 15
        height = length if length < max_height else max_height
        self.size = Vector2(width, height)
        self.image = Surface(self.size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        draw.rect(self.image, (214, 244, 255), self.rect, border_radius=10)
        draw.rect(self.image, (75, 206, 255), self.rect, 2, border_radius=5)
        self.rect.center = pos
        self.rect.bottom = pos[1]
        self.damage = 1

        # stats
        self.velocity = Vector2(0, -5)
        self.timer = 50

    def update(self):
        super().update()
        print(f"{self.timer=}")
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
        # self.rect.center += self.velocity
