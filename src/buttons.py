from random import shuffle
from typing import Any

from pygame import transform, draw, mouse
from pygame.math import Vector2
from pygame.sprite import Sprite

from src.configs import *
from src.functions import load_and_resize, draw_text


class Button(Sprite):
    def __init__(self, pos=(0 ,0), text="$NO_TEXT", size=(200,75), action=None):
        super().__init__()
        sx = size[0]
        sy = size[1] / 75
        # size = ()
        self.image = load_and_resize("assets/imgs/ui/grey.png", size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        t_x = self.rect.width / 2, self.rect.height / 2
        draw_text(self.image, text, t_x, size=30)
        self.text = text
        self.action = action
