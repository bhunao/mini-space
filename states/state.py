import inspect
from abc import ABC, abstractmethod
from typing import Dict

import pygame.font
from pygame import Surface, font
from pygame.event import post, Event
from pygame.sprite import Group, GroupSingle

from events.custom_events import STATE_POP


class State(ABC):
    groups: Dict[str, Group | GroupSingle]
    assets: Dict[str, Surface]

    def __init__(self, screen=None):
        self.screen_rect = screen.get_rect() if screen else pygame.display.get_surface().get_rect()
        self.groups = dict()
        self.assets = dict()
        self.load_assets()
        self.font = font.SysFont("Sans", 36, bold=True)

    @staticmethod
    def close() -> Event:
        event = Event(STATE_POP)
        post(event)
        return event

    def draw_text(self, screen, text, pos, color):
        text = self.font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = pos
        screen.blit(text, text_rect)
        return text_rect

    @abstractmethod
    def load_assets(self) -> None: pass

    def render(self, screen) -> None:
        for group_name, group in self.groups.items():
            group.draw(screen)

        name = self.__class__.__name__ + " screen"
        pos = screen.get_rect().center
        self.draw_text(screen, name, pos, (255, 255, 255))

    def update(self, dt=0, *args, **kwargs) -> None:
        for group_name, group in self.groups.items():
            group.update(*args, **kwargs)


def get_state_class(state: str) -> State:
    import states as _states
    for state_name, state_class in inspect.getmembers(_states, inspect.isclass):
        if state_name.lower() == state.lower():
            return state_class
    raise ValueError(f"State {state} not found")
