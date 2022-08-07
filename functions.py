from typing import Dict
from pygame.time import get_ticks


def cooldown(tick: Dict):
    if get_ticks() - tick["tick"] > tick["delay"]:
        tick["tick"] = get_ticks()
        return True
    return False
