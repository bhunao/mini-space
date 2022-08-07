import pygame
from pygame import time
from pygame.event import post, Event

from events.custom_events import STATE_POP, LOAD_STATE


class EventHandler:
    def __init__(self, game):
        self.game = game
        tick = time.get_ticks()
        self.ticks = {
            "esc": tick,
        }

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game.running = False
                quit()
            if event.type == STATE_POP:
                self.game.unload_state()
            if event.type == LOAD_STATE:
                self.game.load_state(event.state)

    def handle_events(self):
        self.handle_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game.running = False
                quit()
            if event.type == STATE_POP:
                self.game.unload_state()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass

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
        if pressed[pygame.K_e]:
            bullets = player.secondary_fire()
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
