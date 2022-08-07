from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.transform import scale, flip


class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("enemy.gif")
        self.image = scale(self.image, (50, 50))
        self.image = flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.health = 10

        # stats
        self.velocity = Vector2(1, 0)
        self.life = 10

    def update(self):
        self.rect.center += self.velocity
        if self.health <= 0:
            self.kill()
