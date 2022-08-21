import math
from random import randint

from pygame import Surface, draw, Color
from pygame.math import Vector2
from pygame.sprite import Sprite


class Spark(Sprite):
    def __init__(self, pos=(200, 200)):
        super(Spark, self).__init__()
        self.size = (30, 30)
        self.image = Surface(self.size)
        self.image.set_colorkey((0, 0, 0))
        self.color1 = Color("cornsilk")
        self.color2 = Color("cyan")
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        r = randint(-5, 5)
        self.velocity = Vector2(r, -5)
        self.timer = 200
        points1 = [(randint(0, self.size[0]), randint(0, self.size[1])) for p in range(3)]
        points2 = [(randint(0, self.size[0]), randint(0, self.size[1])) for p in range(3)]
        # draw.lines(self.image, self.color1, False, points1, 2)
        p1 = points1[0]
        p2 = points1[0][0] + math.cos(math.radians(self.rect.y)), points1[0][1] + math.sin(math.radians(self.rect.x))  # + math.pi / 2bb
        print(p1, p2)
        draw.line(self.image, self.color1, p1, p2, 2)
        # draw.polygon(self.image, self.color1, points1, 0)
        # draw.polygon(self.image, self.color2, points1, 2)
        circle_size = randint(5, 8)
        # if circle_size > 4:
        #     # self.color1, self.color2 = self.color2, self.color1
        #     circle_size = randint(7, 30)
        draw.rect(self.image, self.color1, (0, 0, circle_size, circle_size), 0)
        draw.rect(self.image, self.color2, (0, 0, circle_size, circle_size), 2)
        draw.circle(self.image, self.color1, (self.size[0]//2, self.size[1]//2), circle_size)
        draw.circle(self.image, self.color2, (self.size[0]//2, self.size[1]//2), circle_size, 2)

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()
        self.rect.center += self.velocity
        # self.velocity.x += math.sin(self.rect.y) * 10
        return
        self.image.fill((0, 0, 0))
        points1 = [(randint(10, self.size[0]-10), randint(0, self.size[1])) for p in range(3)]
        points2 = [(randint(0, self.size[0]), randint(0, self.size[1])) for p in range(3)]
        draw.lines(self.image, self.color1, False, points1, 2)
        # draw.polygon(self.image, self.color1, points1, 0)
        draw.polygon(self.image, self.color2, points2, 2)
        draw.circle(self.image, self.color1, points1[0], 10)
        draw.circle(self.image, self.color2, points1[0], 10, 2)
