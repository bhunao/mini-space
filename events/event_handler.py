import pygame
from pygame import time
from pygame.event import post, Event

from events.custom_events import STATE_POP, LOAD_STATE
from states.state import get_state_class


class EventHandler:
    def __init__(self, game):
        self.game = game
        tick = time.get_ticks()
        self.ticks = {
            "esc": tick,
        }

    def handle_event(self, event, state, mouse_pos):
        self.handle_pygame_events(event)
        self.handle_custom_events(event)
        self.handle_buttons(event, state, mouse_pos)

    def handle_pygame_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            self.game.running = False
            quit()

    def handle_custom_events(self, event):
        if event.type == STATE_POP:
            self.game.unload_state()
        if event.type == LOAD_STATE:
            state_to_load = get_state_class(event.state_name)
            self.game.load_state(state_to_load)

    def handle_buttons(self, event, state, mouse_pos):
        if state.groups.get("focus"):
            focus_button = [button for button in state.groups["buttons"] if button.rect.collidepoint(mouse_pos)]
            state.groups["focus"].add(focus_button)

        if event.type == pygame.MOUSEBUTTONDOWN and state.groups.get("buttons"):
            for button in state.groups["buttons"]:
                if button.rect.collidepoint(mouse_pos):
                    if state.groups.get("focus"):
                        state.groups["focus"].add(button)
                    if event.button == 1:
                        button.on_click()

    def handle_events(self):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        state = self.game.get_state()

        for event in events:
            self.handle_event(event, state, mouse_pos)

        self.handle_input()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE] and self.ticks["esc"] + 800 < time.get_ticks():
            post(Event(STATE_POP))
            self.ticks["esc"] = time.get_ticks()

        state = self.game.get_state()
        if state.__class__.__name__ == "StartState":
            return

        player = self.game.state_manager[-1].get_player()

        if pressed[pygame.K_SPACE]:
            bullets = player.primary_fire()
            state.groups["player_bullets"].add(bullets)
        if pressed[pygame.K_DOWN]:
            player.acceleration.y = 1
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

    @staticmethod
    def close_state(game, event):
        game.state_manager.pop()
        event.pop()
