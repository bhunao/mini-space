from pygame import font, Surface, draw
from pygame.color import Color
from pygame.event import post
from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(self, focus_group=None, pos=(200, 200), text="Button", event=None):
        super().__init__()
        self.focus_group = focus_group
        self.size = (175, 55)
        self.color = Color("azure4")
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.text = text
        self.render_button()
        self.event = event

    def on_click(self):
        if self.event:
            post(self.event)

    def render_button(self):
        # button bg
        _pos = 0, 0
        draw.rect(self.image, self.color, (_pos, self.size), border_radius=100)
        # outline
        draw.rect(self.image, self.color, (_pos, self.size), 3, border_radius=100)

        # button text
        button_text = self.text
        _font = font.SysFont("Sans", 28, bold=True)
        _text = _font.render(button_text, True, Color("azure2"))
        text_rect = _text.get_rect()
        text_rect.center = self.rect.width // 2, self.rect.height // 2
        self.image.blit(_text, text_rect)

    def update(self):
        if self.focus_group.has(self):
            draw.rect(self.image, Color("azure"), (0,0, *self.size), 8, border_radius=1)
        else:
            color = (234, 12, 144)
            draw.rect(self.image, Color("Azure3"), ((0,0), self.size), 8, border_radius=1)
