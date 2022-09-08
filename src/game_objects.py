import math
from random import randint, shuffle

from pygame import time, mixer, mouse
from pygame.math import Vector2
from pygame.sprite import Sprite, Group, groupcollide, spritecollide
from pygame.image import load
from pygame.surface import Surface
from pygame.transform import scale, flip

from pygame import mask, draw

from src.configs import *
from src.configs import WIDTH, HEIGHT
from src.effects import BgStar, Explosion, TakeDamage
from src.functions import get_screen_size, load_and_resize


class Player(Sprite):
    def __init__(self, pos):
        super().__init__()
        self._screen_size = get_screen_size()
        self.shoot_sound = mixer.Sound("sounds/shoot.ogg")
        self.shoot_sound.set_volume(0.3)
        self.image = load("Ships/ship_0003.png")
        self.image = scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = Vector2(0, 0)
        self.n_bullets = 3
        tick = time.get_ticks()
        self.ticks = {
            "move": tick,
            "damage_taken": tick
        }
        self.life = 3

    def update(self):
        tick = time.get_ticks()
        if self.ticks["move"] + 10 < tick:
            self.rect.move_ip(self.speed)
            self.ticks["move"] = tick
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self._screen_size.x:
            self.rect.right = self._screen_size.x
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self._screen_size.y:
            self.rect.bottom = self._screen_size.y

    def shoot(self):
        self.shoot_sound.play()
        bullets = [
            Bullet(self.rect.center),
            Bullet(self.rect.center, 45),
            Bullet(self.rect.center, -45)
        ]
        n = self.n_bullets if self.n_bullets < len(bullets) else len(bullets)
        return bullets[:n]


class Bullet(Sprite):
    def __init__(self, pos, angle=0):
        super().__init__()
        self._screen_size = get_screen_size()
        self.images = [
            load_and_resize("assets/imgs/effects/bullet_0000.png", (30, 30), angle),
            load_and_resize("assets/imgs/effects/bullet_0002.png", (30, 30), angle)
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = Vector2(0, -10)
        self.last_update = time.get_ticks()
        self.image_index = 0
        self.angle = angle

    def update(self):
        self.rect.move_ip(self.speed)
        # velocity based on angle
        if self.angle > 0:
            self.speed.x = math.cos(math.radians(self.angle)) * -10
        elif self.angle < 0:
            self.speed.x = math.cos(math.radians(self.angle)) * +10

        # animation
        if self.last_update + 20 < time.get_ticks():
            self.image = self.images[self.image_index]
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0
            self.last_update = time.get_ticks()
        # remove if out of screen
        if self.rect.top < 0 or self.rect.bottom > self._screen_size.y:
            self.kill()


class Boss(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("Ships/ship_0014.png")
        self.image = scale(self.image, (475, 275))
        self.image = flip(self.image, False, True)
        self.image.set_colorkey(Color(0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 70)
        self.speed = Vector2(0, 0)
        self.gun = None
        self.life = 10
        self.guns = Group()

    def add_gun(self, left=False):
        group = self.groups()[0]
        print(f"group: {group}")

        # gun left_gun
        gun = Gun()
        gun.rect.center = self.rect.center
        gun.rect.bottom += 30
        left_wing_x = self.rect.size[1] / 2
        if left:
            gun.rect.left -= left_wing_x
        else:
            gun.rect.left += left_wing_x
        group.add(gun)
        #
        # # gun right_gun
        # gun2 = Gun()
        # gun2.rect.center = self.rect.center
        # gun2.rect.bottom += 10
        # gun2.rect.left += left_wing_x
        # group.add(gun2)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)
        # self.gun.draw(screen)
        self.guns.draw(screen)


class Gun(Sprite):
    image = load_and_resize("assets/imgs/enemies/gun_01.png", (100, 100))
    rect = image.get_rect()
    mask = mask.from_surface(image).outline()
    draw.lines(image, (255, 255, 255), True, mask, 3)
    life = 5


class Enemy(Sprite):
    def __init__(self, pos=Vector2(0, 0), life=1):
        super().__init__()
        self.image = load("Ships/ship_0014.png")
        self.image = scale(self.image, (75, 75))
        self.image = flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = Vector2(0, 1)
        self.life = life

    def update(self):
        frame = time.get_ticks()
        mult = math.sin(frame / 500)
        self.speed.x = mult * 4
        self.rect.move_ip(self.speed)
        if self.rect.bottom > HEIGHT + self.rect.height:
            self.kill()


class Item(Sprite):
    def __init__(self, pos=Vector2(0, 0), callback=None):
        super().__init__()
        self.image = load_and_resize("assets/imgs/ui/life.png", (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = Vector2(0, 1)
        self.callback = lambda: print("callback")

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.rect.move_ip(self.speed)
        if self.rect.bottom > HEIGHT + self.rect.height:
            self.kill()


class Camera(Group):
    def __init__(self):
        super().__init__()
        self.bullets = Group()
        self.enemies = Group()
        self.ticks = {"enemy_spawn": time.get_ticks()}
        self.points = 0
        self.bg = Background()
        self.effects = Group()
        self.items = Group()
        self.sound_explosion = mixer.Sound("sounds/explosion_01.ogg")
        self.sound_explosion.set_volume(0.1)
        self.sound_impact = mixer.Sound("sounds/impact.ogg")
        self.sound_impact.set_volume(0.1)

    def respawn_enemie(self):
        tick = self.ticks.get("enemy_spawn", time.get_ticks())
        if not [enemy for enemy in self.enemies.sprites() if isinstance(enemy, Enemy)]:
            if tick + 1000 < time.get_ticks():
                x = WIDTH // 2 + (math.sin(time.get_ticks() / 100) * WIDTH // 2)
                enemy = Enemy((x, 0))
                self.enemies.add(enemy)
                self.ticks["enemy_spawn"] = tick

    def player_get_item(self):
        player = [player for player in self.sprites() if isinstance(player, Player)]
        if player:
            player = player[0]
        else:
            return
        collid = spritecollide(player, self.items, True)
        for collided in collid:
            collided.callback()
            player.life += 1

    def damage_player(self):
        player = [player for player in self.sprites() if isinstance(player, Player)]
        if player:
            player = player[0]
        else:
            return
        enemies = [enemy for enemy in self.enemies.sprites() if isinstance(enemy, Enemy) or isinstance(enemy, Boss)]
        collid = spritecollide(player, enemies, False)
        if collid:
            tick = time.get_ticks()
            if tick - player.ticks.get("damage_taken", tick) > 1000:
                player.ticks["damage_taken"] = tick
                player.life -= 1
                red = TakeDamage(player)
                self.effects.add(red)
                self.effects.add(Explosion(player.rect.center))
                self.sound_impact.play()
                if player.life <= 0:
                    self.sound_explosion.play()
                    player.kill()
                    self.effects.add(Explosion(player.rect.center))

    def kill_enemies(self):
        player = [player for player in self.sprites() if isinstance(player, Player)]
        if player:
            player = player[0]

        sprt_dict = groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullets in zip(sprt_dict.keys(), sprt_dict.values()):
            enemy_mask = mask.from_surface(enemy.image)
            print(f"bullets: {bullets}")
            bullets_mask = [mask.from_surface(bullet.image) for bullet in bullets]
            print(f"masks: {bullets_mask}")
            self.effects.add(Explosion(enemy.rect.center, size=2))
            self.sound_impact.play()
            for bullet in bullets_mask:
                overlap = enemy_mask.overlap(bullet, (1, 1))
                print(f"overlap: {overlap}")
                print(f"bullet: {bullet}")
                print(f"enemy: {enemy_mask}")
                if overlap:
                    print(f"{enemy_mask.overlap(bullet, (1, 1))}. enemy: {enemy}")
                    enemy.life -= 1
                    if enemy.life <= 0:
                        self.points += 1
                        enemy.kill()
                        self.sound_explosion.play()

                        # spawn item
                        chance = randint(0, 100)
                        if chance > 80:
                            item = Item(enemy.rect.center)
                            self.items.add(item)
                    break
            else:
                red = TakeDamage(enemy)
                self.effects.add(red)
                self.effects.add(Explosion(enemy.rect.center))

    def update(self):
        super().update()
        self.bg.update()
        self.kill_enemies()
        self.player_get_item()
        self.damage_player()
        self.bullets.update()
        self.enemies.update()
        self.effects.update()
        self.items.update()

        # respawn
        self.respawn_enemie()

        # go to menu if player is dead
        player = [player for player in self.sprites() if isinstance(player, Player)]
        if not player: ...

    def draw(self, screen):
        self.bg.draw(screen)

        super().draw(screen)
        self.bullets.draw(screen)
        self.enemies.draw(screen)
        self.effects.draw(screen)
        self.items.draw(screen)


class Background(Group):
    def __init__(self):
        super().__init__()
        self.image = Surface(get_screen_size())
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        starts = [BgStar() for _ in range(100)]
        self.add(starts)

    def update(self):
        super().update()
        n = randint(0, 5)
        stars = [BgStar() for _ in range(n)]
        self.add(stars)

    def draw(self, screen):
        self.image.fill((0, 0, 0))
        super().draw(self.image)
        screen.blit(self.image, self.rect)


class Board(Sprite):
    def __init__(self, pos=None, size=(300, 300)):
        super().__init__()
        self.image = load_and_resize("assets/imgs/ui/grey.png", size)
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pressed = False
        self.rect.center = pos if pos else self.rect.center
        # self.draw_cable()


class Cables(Sprite):
    def __init__(self, pos=None, size=(300, 300)):
        super().__init__()
        self.image = Surface(size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pressed = False
        self.rect.center = pos if pos else self.rect.center
        # self.draw_cable()
        self.cables = self.create_cables(6)
        self.connect_sound = mixer.Sound("sounds/cable_connect.ogg")
        self.connect_sound.set_volume(0.3)

    def draw(self, screen):
        super().draw(screen)
        self.draw_cables()
        screen.blit(self.image, self.rect)

    def create_cables(self, n):
        top = self.rect.top
        left = self.rect.left
        right = self.rect.width
        cable_points = [y for y in range(0, self.rect.height, int(self.rect.height / n * .6))][:n]

        cables = []
        shuffled_points = cable_points.copy()
        shuffle(shuffled_points)
        for start, end in zip(cable_points, shuffled_points):
            # start
            l1 = Vector2(0, top + start)
            l2 = Vector2(150, top + start)
            l3 = Vector2(150, top + start)     # if l3 != l4 == mouse
            # end
            l4 = Vector2(right - 150, top + end)
            l5 = Vector2(right, top + end)
            cable = [[l1, l2, l3], (l4, l5)]
            cables.append(cable)
        return cables

    def draw_cables(self, click=False):
        self.image.fill((0, 0, 0))
        colors = (
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
        )
        c = (color for color in colors)
        use_mouse = True
        mouse_ = mouse.get_pos()
        for start, end in self.cables:
            first = end[0]
            last = start[-1]
            mouse_cable_dist = math.hypot(first[0] - mouse_[0], first[1] - mouse_[1])
            if last != first and use_mouse:
                use_mouse = False
                start[-1] = mouse_
                if click and abs(mouse_cable_dist) < 10:
                    self.connect_sound.play()
                    start[-1] = first

            color = next(c)
            draw.lines(self.image, color, False, start, 12)
            draw.lines(self.image, color, False, end, 12)

        if use_mouse:
            return True
        return False
