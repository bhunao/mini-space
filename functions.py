from typing import Dict

from pygame import display
from pygame.time import get_ticks


def cooldown_(tick: Dict):
    if get_ticks() - tick["tick"] > tick["delay"]:
        tick["tick"] = get_ticks()
        return True
    return False


def cooldown(time, delay):
    if get_ticks() - time > delay:
        time += -time + get_ticks()
        return True
    return False


class GridPlacement:
    def __init__(self, x: int, y: int):
        self.size = display.get_surface().get_rect()
        self.width = self.size.width
        self.height =  self.size.height
        self.x = x
        self.y = y

    def pos(self, x: int, y: int) -> (int, int):
        x = self.width // self.x * x
        y = self.height // self.y * y
        return x, y


