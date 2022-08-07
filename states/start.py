from game_objects.background import Background
from states.state import State
from pygame.sprite import Group, GroupSingle

from ui_elements.buttons import Button


class StartState(State):
    def load_assets(self) -> None:
        self.groups["background"] = Background(self.screen_rect)
        self.groups["buttons"] = Group()
        self.groups["focus"] = GroupSingle()
        focus = self.groups["focus"]

        button = Button(focus, (200, 100), "Start")
        button2 = Button(focus, (200, 200), "Instructions")
        button3 = Button(focus, (200, 300), "Settings")
        button4 = Button(focus, (200, 400), "Exit")

        self.groups["buttons"].add(button)
        self.groups["buttons"].add(button2)
        self.groups["buttons"].add(button3)
        self.groups["buttons"].add(button4)
        self.groups["focus"].add(button)

    def render(self, screen) -> None:
        super().render(screen)

