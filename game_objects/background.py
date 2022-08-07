from random import randint

from pygame import Surface, Vector2, draw
from pygame.sprite import Group, Sprite


class Background(Group):
    def __init__(self, rect):
        super().__init__()
        self.image = Surface(rect.size)
        self.rect = self.image.get_rect()

    def update(self):
        super().update()
        n = randint(0, 5)
        stars = [BgStar(self.rect) for _ in range(n)]
        self.add(stars)

    def draw(self, screen):
        self.image.fill((0, 0, 0))
        super().draw(self.image)
        screen.blit(self.image, self.rect)


class BgStar(Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.image = Surface((30, 70))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        star_size = randint(1, 3)
        x = randint(0, size.width)
        speed = randint(10, 35)
        draw.line(self.image, (255, 255, 255, 25), (0, 0), (0, 70), star_size)
        self.pos = Vector2(x, 0)
        self.rect.center = self.pos
        self.speed = Vector2(0, speed)

    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.top > self.size.height:
            self.kill()
