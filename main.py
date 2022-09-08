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
# boss = Boss()
# camera.enemies.add(boss)
# boss.add_gun()
# boss.add_gun(True)


def test():
    print("test")


def type_the_code() -> bool:
    buttons = Group()
    effects = Group()
    confimation = (
        mixer.Sound("sounds/confirmation_001.ogg"),
        mixer.Sound("sounds/confirmation_002.ogg"),
        mixer.Sound("sounds/confirmation_003.ogg"),
        mixer.Sound("sounds/confirmation_004.ogg"),
    )

    # board
    camera = Camera()
    bx = WIDTH / 14 * 8
    by = HEIGHT / 14 * 8
    board_pos = (bx, by)
    bord_size = (WIDTH / 10 * 8, HEIGHT / 10 * 7)
    board = Board(board_pos, bord_size)
    buttons.add(board)

    x_btn = Button((WIDTH / 9 * 1, HEIGHT / 9 * 8), " X ", (50, 50))
    buttons.add(x_btn)

    code = choices(hexdigits, k=9)
    for i, digit in enumerate(code):
        x = WIDTH / 11 * (3 + i % 3)
        y = HEIGHT / 9 * (3 + i // 3)
        btn = Button((x, y), digit, (50, 50), action=test)
        buttons.add(btn)
    right_anwser = choices(code, k=3)
    print(right_anwser)
    awnser = ""
    wrong_trys = 0



    running_ = True
    tick = time.get_ticks()
    while running_:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running_ = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tick + 500 > time.get_ticks():
                    continue
                btns = [button for button in buttons.sprites() if isinstance(button, Button)]
                for button in btns:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if button.text == " X ":
                            running_ = False
                            break
                        rights = len(awnser)
                        if button.text == right_anwser[rights]:
                            confimation[rights].play()
                            awnser += button.text
                        else:
                            wrong_trys += 1
                            red = TakeDamage(button)
                            effects.add(red)

        # draw and udpate
        camera.update()
        camera.draw(screen)
        buttons.update()
        buttons.draw(screen)
        draw_text(screen, "Type the code...", (WIDTH / 2, HEIGHT / 8 * 1), size=50)
        player_hud(screen, camera.points, player.life)
        # code
        draw_text(screen, "".join(right_anwser), (WIDTH / 9 * 3, HEIGHT / 8 * 6), size=50)
        # screen
        awnser_text_pos = (WIDTH / 10 * 7, HEIGHT / 9 * 4)
        rect = Rect(awnser_text_pos, (310, 80))
        rect.center = awnser_text_pos
        pygame.draw.rect(screen, (0, 255, 0), rect)
        pygame.draw.rect(screen, (0, 204, 0), rect, 3)
        draw_text(screen, "-".join(awnser), awnser_text_pos, size=50)
        effects.update()
        effects.draw(screen)
        pygame.display.update()
        clock.tick(60)

        if set(awnser) == set(right_anwser):
            print(f"You win! The code is {awnser}")
            return True
        elif wrong_trys >= 3:
            print(f"You lose! The code is {awnser}")
            return False


def cables() -> bool:
    x_btn = Button((WIDTH / 9 * 1, HEIGHT / 9 * 8), " X ", (50, 50))
    buttons = Group()
    buttons.add(x_btn)


    # board
    camera = Camera()
    bx = WIDTH / 14 * 8
    by = HEIGHT / 14 * 8
    board_pos = (bx, by)
    bord_size = (WIDTH / 10 * 8, HEIGHT / 10 * 7)
    board = Board(board_pos, bord_size)
    camera.add(board)
    cables = Cables(board_pos, bord_size)
    camera.add(cables)

    running_ = True
    while running_:
        mouse_ = mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cables.draw_cables(True)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running_ = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons.sprites():
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        running_ = False
                        break

        # draw and udpate
        camera.draw(screen)
        camera.update()
        buttons.update()
        buttons.draw(screen)
        player_hud(screen, camera.points, player.life)
        if cables.draw_cables():
            return True
        draw_text(screen, "Connect the cables...", (WIDTH/2, HEIGHT / 8 * 1), size=50)

        pygame.display.flip()
        clock.tick(60)


def minigame():
    x_btn = Button((WIDTH / 9 * 1, HEIGHT / 9 * 8), "X", (50, 50))
    buttons = Group()
    buttons.add(x_btn)

    # board
    camera = Camera()
    bx = WIDTH / 14 * 8
    by = HEIGHT / 14 * 8
    board_pos = (bx, by)
    bord_size = (WIDTH / 10 * 8, HEIGHT / 10 * 7)
    board = Board(board_pos, bord_size)
    camera.add(board)

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
                        running_ = False
                        break

        # draw and udpate
        draw_text(screen, "MINI-SPACE", (WIDTH/2, HEIGHT / 8 * 1), size=80)
        camera.draw(screen)
        camera.update()
        buttons.update()
        buttons.draw(screen)
        player_hud(screen, camera.points, player.life)
        pygame.display.update()
        clock.tick(60)


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
                if event.key == K_UP:
                    player.speed.y = -3
                if event.key == K_DOWN:
                    player.speed.y = 3
                if event.key == K_LEFT:
                    player.speed.x = -3
                if event.key == K_RIGHT:
                    player.speed.x = 3
                if event.key == K_SPACE:
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
