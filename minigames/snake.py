import pygame
from pygame.locals import *
from pygame.sprite import Group

from configs import *
from functions import draw_score, draw_text
from buttons import Cables


def snake(screen_, mouse_):
    btns = Group()
    btn = Cables((WIDTH / 2, HEIGHT / 2))
    btns.add(btn)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen_.fill((131, 135, 150))
        draw_text(screen_, "asdasd", (50, 50))
        btns.update()
        btns.draw(screen_)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(NAME)
    snake(screen)
    pygame.quit()
    exit()
