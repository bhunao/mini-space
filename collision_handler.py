from typing import Dict

from pygame.sprite import Group, spritecollide, collide_mask, spritecollideany, groupcollide


class CollisionHandler:
    def __init__(self, groups: Dict[str, Group]):
        self._groups = groups

    def handle_player_enemies(self):
        player = self._groups["player"].sprites()[0]
        enemies = self._groups["enemies"]
        collisions = spritecollide(player, enemies, False)
        for enemy in collisions:
            if collide_mask(player, enemy):
                player.health -= 1

    def handle_collisions(self):
        self.handle_player_bullets()
        self.handle_player_enemies()
        self.handle_enemies_bullets()

    def handle_player_bullets(self):
        bullet_group = self._groups["bullets"]
        player = self._groups["player"].sprites()[0]
        collided = spritecollideany(player, bullet_group)
        if collided:
            mask_collision = collide_mask(player, collided)
            if mask_collision:
                collided.kill()
                player.health -= collided.damage

    def handle_enemies_bullets(self):
        enemies_group = self._groups["enemies"]
        bullets_group = self._groups["player_bullets"]
        collisions = groupcollide(enemies_group, bullets_group, False, False)
        for enemy, bullets in collisions.items():
            for bullet in bullets:
                if collide_mask(enemy, bullet) and hasattr(bullet, "damage"):
                    enemy.health -= bullet.damage
