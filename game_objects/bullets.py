from pygame import draw, Surface
from pygame.display import flip
from pygame.image import load
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.transform import scale


class Bullet(Sprite):
    def __init__(self, pos=(200, 200)):
        super().__init__()
        size = (8, 18)
        self.image = Surface(size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        draw.rect(self.image, (214, 244, 255), self.rect, border_radius=10)
        draw.rect(self.image, (75, 206, 255), self.rect, 2, border_radius=5)
        self.rect.center = pos
        self.damage = 1

        # stats
        self.velocity = Vector2(0, -5)
        self.life = 10

    def update(self):
        self.rect.center += self.velocity


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
        self.life = 10
        self.timer = 2

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()
        # self.rect.center += self.velocity
