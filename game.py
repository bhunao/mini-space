import inspect

import pygame

from events.custom_events import STATE_POP
from events.event_handler import EventHandler
from states import GameState
from states.state import State

from states.start import StartState


class Game:
    def __init__(self):
        # pygame methods
        pygame.init()
        pygame.display.set_caption("project")

        # pygame variables
        self.screen_size = pygame.math.Vector2(800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.running = True
        self.clock = pygame.time.Clock()

        # my variables
        self.event_handler = EventHandler(self)
        self.state_manager = []
        self.load_state(StartState)
        self.load_state(GameState)

    def load_state(self, state):
        if inspect.isclass(state):
            if issubclass(state, State):
                self.state_manager.append(state())
        else:
            raise TypeError(f"state must be a subclass of State and not {state}")

    def unload_state(self) -> State:
        return self.state_manager.pop()

    def get_state(self):
        return self.state_manager[-1]

    def state_handler(self):
        state = self.state_manager[-1]
        state.update()
        state.render(self.screen)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.event_handler.handle_events()
            self.state_handler()
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)


Game().run()
