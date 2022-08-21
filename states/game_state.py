from random import randint

import pygame
from pygame.sprite import Group, GroupSingle

from collision_handler import CollisionHandler
from game_objects.background import Background
from game_objects.bullets import Bullet
from game_objects.enemy import Enemy
from game_objects.player import Player
from states.state import State


class GameState(State):
    def __init__(self):
        super().__init__()
        self.collision_handler = CollisionHandler(self.groups)
        self._screen_size = pygame.display.get_surface().get_size()

    def update(self, *args, **kwargs):
        self.collision_handler.handle_collisions()
        super().update(*args, **kwargs)
        if len(self.groups["enemies"].sprites()) <= 0:
            pos = randint(0, self._screen_size[0]), 0
            enemy = Enemy(bullets_group=self.groups["bullets"], pos=pos)
            self.groups["enemies"].add(enemy)

        x = randint(0, self._screen_size[0])


    def load_assets(self) -> None:
        self.groups["background"] = Background(self.screen_rect)
        self.groups["player"] = Group()
        self.groups["player_bullets"] = Group()
        self.groups["bullets"] = Group()
        self.groups["enemies"] = Group()

        player = Player()
        enemy = Enemy(self.groups["bullets"])
        bullet = Bullet()

        self.groups["player"].add(player)
        self.groups["enemies"].add(enemy)
        self.groups["bullets"].add(bullet)

    def get_player(self):
        return self.groups["player"].sprites()[0]
