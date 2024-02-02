import random

import pygame
from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

def load_sprite(name, with_alpha=True):
    return [load(f"assets/sprites/{name}.png").convert(), load(f"assets/sprites/{name}.png").convert_alpha()][with_alpha]

def load_sound(name): return Sound(f"assets/sounds/{name}.wav")


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, color="tomato", coords=None):
    try:
        _color = Color(color)
    except: _color = Color(255, 255, 255)
    text_surface = font.render(text, False, _color)
    rect = text_surface.get_rect()
    if coords: rect.center = Vector2(coords)
    else: rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)

def draw_rectangle(surface, color=(0, 0, 0), params=(0, 0, 0, 0), param2=0):
    pygame.draw.rect(surface, color, params, param2)

def check_zone(obj_location: list, mouse_location: list, obj_radius: int):
    obj_radius += 3
    if mouse_location[0] > obj_location[0] - obj_radius and mouse_location[0] < obj_location[0] + obj_radius and mouse_location[1] > obj_location[1] - obj_radius and mouse_location[1] < obj_location[1] + obj_radius:
        return True
    return False

def some_vector_angle_func():
    pass

