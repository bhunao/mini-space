import pygame
from pygame.math import Vector2

from events.custom_events import STATE_POP
from events.event_handler import EventHandler
from states.game_state import GameState
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
        self.state_manager.append(StartState())
        self.state_manager.append(GameState())

    def load_state(self, state):
        self.state_manager.append(state)

    def unload_state(self) -> State:
        return self.state_manager.pop()

    def get_state(self):
        return self.state_manager[-1]

    def state_handler(self):
        state = self.state_manager[-1]
        state.update()
        state.render(self.screen)

    def handle_events(self):
        self.handle_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = not self.running
                quit()
            if event.type == STATE_POP:
                self.unload_state()

    def handle_input(self):
        player = self.state_manager[-1].get_player()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            player.acceleration.y = 1
            asd = self.state_manager[-1].close()
        elif pressed[pygame.K_UP]:
            player.acceleration.y = -1
        else:
            player.acceleration.y = 0

        if pressed[pygame.K_LEFT]:
            player.acceleration.x = -1
        elif pressed[pygame.K_RIGHT]:
            player.acceleration.x = 1
        else:
            player.acceleration.x = 0
        if pressed[pygame.K_SPACE]:
            pass

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.event_handler.handle_events()
            self.state_handler()
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)


Game().run()
