from pygame import font, Surface, draw
from pygame.event import Event
from pygame.mouse import get_pos
from pygame.sprite import Sprite, GroupSingle

from events.custom_events import LOAD_STATE


class Button(Sprite):
    def __init__(self, focus_group=None, pos=(200, 200), text="Button", state_link=None):
        super().__init__()
        self.focus_group = focus_group
        self.size = (175, 55)
        color = (234, 12, 144)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.text = text
        self.render_button(color)
        self.event = None if state_link is None else Event(LOAD_STATE, state_name=state_link)

    def render_button(self, color):
        # button bg
        _pos = 0, 0
        draw.rect(self.image, color, (_pos, self.size), border_radius=100)
        # outline
        draw.rect(self.image, color, (_pos, self.size), 3, border_radius=100)

        # button text
        text_color = (23, 231, 211)
        button_text = self.text
        _font = font.SysFont("Sans", 28, bold=True)
        _text = _font.render(button_text, True, text_color)
        text_rect = _text.get_rect()
        text_rect.center = self.rect.width // 2, self.rect.height // 2
        self.image.blit(_text, text_rect)

    def update(self):
        mouse_pos = get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.focus_group.add(self)
        if self.focus_group.has(self):
            draw.rect(self.image, (255, 255, 255), (0,0, *self.size), 8, border_radius=1)
        else:
            color = (234, 12, 144)
            draw.rect(self.image, color, ((0,0), self.size), 8, border_radius=1)
