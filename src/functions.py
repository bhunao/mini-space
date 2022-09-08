from random import shuffle
import re

import pygame
from pygame import image, draw, display
from pygame.locals import *
from pygame.math import Vector2


def get_screen_size():
    _screen = display.get_surface()
    rect = _screen.get_rect()
    return Vector2(rect.width, rect.height)

def load_and_resize(path, size, rotate=None):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, size)
    if rotate:
        img = pygame.transform.rotate(img, rotate)
    return img


def draw_score(screen, score):
    global numbers

    points = f"{score:03d}"
    screen.blit(numbers[int(points[0])], (0, 0))
    screen.blit(numbers[int(points[1])], (30, 0))
    screen.blit(numbers[int(points[2])], (60, 0))


def load_numbers(path, size):
    numbers = {}
    for i in range(10):
        img = load_and_resize(path + str(i) + ".png", size)
        numbers[i] = img
    return numbers


def draw_text(screen, text, pos, size=30, color=(255, 255, 255), bold=False):
    font = pygame.font.Font("fonts/Kenney Pixel.ttf", size)
    font.set_bold(True)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    screen.blit(text, text_rect)
    return text_rect


def quit_game():
    pygame.quit()
    exit()


def draw_lifes(screen, lives):
    xoff = int(life.get_rect().width * 1.2)
    for x in range(800, 800 - xoff * (lives+1), -xoff):
        screen.blit(life, (x, 0))


def player_hud(screen, points, lives):
    draw_score(screen, points)
    draw_lifes(screen, lives)


life = load_and_resize("assets/imgs/ui/life.png", (35, 35))
numbers = load_numbers("assets/imgs/ui/", (50, 50))
