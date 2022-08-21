from pygame.event import Event

from events.custom_events import LOAD_STATE
from functions import GridPlacement
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

        grid = GridPlacement(14, 7)

        start_pos = grid.pos(2, 3)
        start_event = Event(LOAD_STATE, state_name="gamestate")
        start_btn = Button(focus, start_pos, "Start", start_event)

        instruc_pos = grid.pos(2, 4)
        instruc_btn = Button(focus, instruc_pos, "Instructions")

        sett_pos = grid.pos(2, 5)
        sett_btn = Button(focus, sett_pos, "Settings")

        exit_pos = grid.pos(2, 6)
        exit_btn = Button(focus, exit_pos, "Exit")

        self.groups["buttons"].add(start_btn)
        self.groups["buttons"].add(instruc_btn)
        self.groups["buttons"].add(sett_btn)
        self.groups["buttons"].add(exit_btn)
        self.groups["focus"].add(start_btn)

    def render(self, screen) -> None:
        super().render(screen)
