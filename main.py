from random import choices
from typing import Callable
from string import hexdigits

from pygame import mouse, mixer, time
from pygame._sprite import Group
from pygame.locals import *
import pygame
from pygame.surface import Surface

from src.buttons import Button
from src.configs import *
from src.effects import TakeDamage
from src.functions import draw_text, quit_game, player_hud
from src.game_objects import Camera, Player, Enemy, Boss, Board, Cables

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.SRCALPHA)
size = screen.get_rect()
WIDTH, HEIGHT = size.width, size.height
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

t_delay = 0

# game objects
camera = Camera()
player = Player((WIDTH / 2, HEIGHT / 8 * 7))
camera.add(player)
enemy = Enemy((WIDTH / 2, 0))
camera.enemies.add(enemy)
boss = Boss()
camera.enemies.add(boss)
boss.add_gun()
boss.add_gun(True)


def instructions():
    # buttons
    buttons = Group()
    bg = Camera()
    exit_btn = Button((WIDTH / 8 * 1, HEIGHT / 8 * 7), "EXIT", (150, 50))
    buttons.add(exit_btn)
    bg_text = Rect(0, 0, WIDTH / 8 * 7, HEIGHT / 8 * 5)
    bg_text.center = (WIDTH / 2, HEIGHT / 2)
    instructions_panel = Surface(bg_text.size, pygame.SRCALPHA)
    instructions_panel.fill((131, 135, 150))


    running_ = True
    while running_:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running_ = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons.sprites():
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        print(f"clicked on {button.text}")
                        button.color = (255, 0, 0)
                        running_ = False

        # draw and udpate
        screen.fill(BG_COLOR)
        bg.update()
        bg.draw(screen)
        buttons.update()
        buttons.draw(screen)
        draw_text(screen, "Instructions", (WIDTH/2, HEIGHT / 8 * 1), size=80)
        screen.blit(instructions_panel, bg_text)
        draw_text(screen, INSTRUCTIONS[0], (WIDTH/2, HEIGHT / 8 * 2), size=35)
        draw_text(screen, INSTRUCTIONS[1], (WIDTH/2, HEIGHT / 8 * 3), size=35)
        draw_text(screen, INSTRUCTIONS[2], (WIDTH/2, HEIGHT / 8 * 4), size=35)
        draw_text(screen, INSTRUCTIONS[3], (WIDTH/2, HEIGHT / 8 * 5), size=35)
        # space()
        pygame.display.update()
        clock.tick(60)
        pygame.time.delay(t_delay)


def main():
    # buttons
    buttons = Group()
    bg = Camera()

    start_btn = Button((WIDTH / 2, HEIGHT / 8 * 3), "Start", action=space)
    instructions_btn = Button((WIDTH / 2, HEIGHT / 8 * 5), "Instructions", size=(250,70), action=instructions)
    exit_butn = Button((WIDTH / 2, HEIGHT / 8 * 7), "Exit", action=quit_game)
    buttons.add(start_btn, instructions_btn, exit_butn)

    running_ = True
    while running_:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running_ = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons.sprites():
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        print(f"clicked on {button.text}")
                        button.color = (255, 0, 0)
                        if isinstance(button.action, Callable):
                            button.action()

        # draw and udpate
        screen.fill(BG_COLOR)
        bg.update()
        bg.draw(screen)
        buttons.update()
        buttons.draw(screen)
        draw_text(screen, "MINI-SPACE", (WIDTH/2, HEIGHT / 8 * 1), size=80)
        pygame.display.update()
        clock.tick(60)
        pygame.time.delay(t_delay)


def space():
    running_ = True
    while running_:
        # events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # player input
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running_ = False
                if event.key == K_w:
                    player.speed.y = -3
                if event.key == K_s:
                    player.speed.y = 3
                if event.key == K_a:
                    player.speed.x = -3
                if event.key == K_d:
                    player.speed.x = 3
                if event.key == K_SPACE:
                    bullet = player.shoot()
                    camera.bullets.add(bullet)


        if pygame.mouse.get_pressed()[0]:
            bullet = player.shoot()
            camera.bullets.add(bullet)
        # draw and udpate
        screen.fill(BG_COLOR)

        camera.update()
        camera.draw(screen)

        player_hud(screen, camera.points, player.life)

        pygame.display.update()
        clock.tick(60)
        pygame.time.delay(t_delay)

        if player.life <= 0:
            running_ = False
            break


if __name__ == '__main__':
    main()
