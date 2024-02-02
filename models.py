import random

from pygame.math import Vector2
from pygame.transform import rotozoom
import pygame

from utils import get_random_velocity, load_sound, load_sprite, wrap_position, get_random_position

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface, fps=30):
        self.position = wrap_position(self.position + self.velocity * 30 / fps, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3
    MAX_SPEED = 25
    hypotic_speed = 1
    DOUBLE_BOOM = False
    SUPER_LASER = False
    TRIPLE_BOOM = False

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        self.direction.rotate_ip(self.MANEUVERABILITY * (int(clockwise) * 2 - 1))

    def accelerate(self):
        if self.hypotic_speed < self.MAX_SPEED:
            self.hypotic_speed *= 1.25
            self.velocity += self.direction * self.ACCELERATION

    def stop_acceleration(self):
        if self.hypotic_speed >= 1.2:
            self.velocity /= 1.2
            self.hypotic_speed /= 1.2
        else: self.velocity /= 2

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self, Super=SUPER_LASER):
        for _ in range(1 + int(self.DOUBLE_BOOM) + int(self.TRIPLE_BOOM)):
            bullet_velocity = self.direction * self.BULLET_SPEED*2 + self.velocity if Super else self.direction * self.BULLET_SPEED + self.velocity
            bullet = Bullet(self.position, bullet_velocity, Super)
            self.create_bullet_callback(bullet)
            self.laser_sound.play()


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.2, 2: 0.8, 1: 0.5}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(random.randint(2, 3)):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)

    def OnClick(self, mouse):
        xmouse, ymouse = mouse.get_pos()
        self.is_hover = pygame.Rect(self.startx, self.starty, self.width, self.height).collidepoint([xmouse, ymouse])
        if self.is_hover:
            if mouse.get_pressed()[0]:
                exec(open(f"assets\some_other_files\{self.onclick}.txt", 'r').readline())
            else:
                pass
        else:
            print(mouse.get_pos(), self.x)
        self.x = self.on_hover()

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))