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

    def octople_shot(self, Super=False):
        for _ in range(1 + int(self.DOUBLE_BOOM) + int(self.TRIPLE_BOOM)):
            for i in range(8):
                self.direction.rotate_ip(40)
                bullet_velocity = self.direction * 2 + self.velocity if Super else self.direction * self.BULLET_SPEED + self.velocity
                bullet = Bullet(self.position, bullet_velocity, Super=False)
                self.create_bullet_callback(bullet)
            self.laser_sound.play()

    def rotate(self, clockwise=True):
        self.direction.rotate_ip(self.MANEUVERABILITY * (int(clockwise) * 2 - 1))

    def CHEATS_ON(self):
        self.MANEUVERABILITY = 7
        self.MAX_SPEED = 10000000000000
        self.BULLET_SPEED = 7
        self.ACCELERATION = 0.4

    def level_up(self, level):
        if level == 2:
            self.MANEUVERABILITY = 4
            self.MAX_SPEED = 100
        if level == 3:
            self.ACCELERATION = 0.4
            self.MANEUVERABILITY = 5
            self.BULLET_SPEED = 4
        if level == 4:
            self.BULLET_SPEED = 5
            self.MANEUVERABILITY = 6
        if level == 5:
            self.MAX_SPEED = 500
            self.BULLET_SPEED = 6
        if level == 6:
            self.MAX_SPEED = 750
            self.MANEUVERABILITY = 7
        if level == 7:
            self.DOUBLE_BOOM = True
        if level == 8:
            self.SUPER_LASER = True
            self.BULLET_SPEED = 7
        if level > 8:
            self.MAX_SPEED += 100
            self.BULLET_SPEED += round(2 / level, 2)
        if level == 13:
            self.TRIPLE_BOOM = True

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


class Bullet(GameObject):
    def __init__(self, position, velocity, Super=False):
        super().__init__(position, [load_sprite("bullet"), load_sprite("super_bullet")][Super], velocity)

    def move(self, surface, fps=30):
        self.position = self.position + self.velocity * 30 / fps

class Star(GameObject):
    def __init__(self, surface, position=(-999, -999), velocity=get_random_velocity(1, 3)):
        if position == (-999, -999): position = get_random_position(surface)
        super().__init__(position, load_sprite('star', True), velocity)

    def move(self, surface, fps=30):
        self.position = self.position + self.velocity * 30 / fps


class Harvester(GameObject):
    def __init__(self, surface, position, velocity=Vector2(0)):
        sprite = rotozoom(load_sprite("harvester2", True), 0, 0.3)
        self.direction = Vector2(UP)
        super().__init__(position, sprite, velocity)

    def move(self, surface, fps=30):
        self.direction.rotate_ip(30/fps)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

class ElectroStation(GameObject):
    def __init__(self, surface, position, velocity=Vector2(0)):
        sprite = rotozoom(load_sprite("electrostation", True), 0, 0.15)
        self.direction = Vector2(UP)
        super().__init__(position, sprite, velocity)

    def move(self, surface, fps=30):
        self.direction.rotate_ip(72/fps)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class Button(GameObject):
    def __init__(self, button_name, surface, onclick='', position=(0, 0), sizes=(1, 1)):
        self.x, self.y = position
        self.startx, self.starty = position
        self.width = sizes[0]
        self.height = sizes[1]
        self.onclick = onclick
        self.is_hover = False
        self.on_hover = lambda: self.x + 1 * [[0, 0], [-1, 1]][self.startx <= self.x if not self.is_hover else self.x <= self.startx + 20][self.is_hover]
        sprite = rotozoom(load_sprite("buttons/" + button_name, True), 0, 1)
        self.direction = Vector2(UP)
        super().__init__(position, sprite, Vector2(0))

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


class Talants(GameObject):
    def __init__(self, position, velocity=Vector2(0)):
        sprite = rotozoom(load_sprite("talants_icon", True), 0, 0.25)
        self.direction = Vector2(UP)
        super().__init__(position, sprite, velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)


class TalantsMenu(GameObject):
    def __init__(self, position=(400, 385), velocity=Vector2(0)):
        sprite = rotozoom(load_sprite("talants_tree", True), 0, 1)
        self.direction = Vector2(UP)
        super().__init__(position, sprite, velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

class TalantsIcon(GameObject):
    def __init__(self, position, velocity=Vector2(0), name='not_invented_talent'):
        sprite = rotozoom(load_sprite(name, True), 0, 0.75)
        self.direction = Vector2(UP)
        self.name = name
        super().__init__(position, sprite, velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

class Preview(GameObject):
    def __init__(self, position=(0,0), velocity=Vector2(0), name='Кадр1'):
        sprite = rotozoom(load_sprite(name, True), 0, 1)
        self.direction = Vector2(UP)
        self.name = name
        super().__init__(position, sprite, velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)


class EnergyShield(GameObject):
    def __init__(self, position=(0,0), velocity=Vector2(0), name='EnergyShield'):
        sprite = rotozoom(load_sprite(name, True), 0, 0.1)
        self.direction = Vector2(UP)
        self.name = name
        super().__init__(position, sprite, velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)


class NeuroNet():
    def __init__(self, Spaceship, parameters='R'):
        self.preference = parameters[0]
        self.ticker = 0
        self.Spaceship = Spaceship
        self.previous_choices = ['', '', '']

    def predict(self, data=('angle')):
        lst = []
        from_choice = ["R", "D", "L", "U"]
        if self.previous_choices != []:
            if self.previous_choices[-1] == 'U': from_choice.pop(1)
            if self.previous_choices[-1] == "D": from_choice.pop(-1)
        if not self.preference == "D": from_choice.append(self.preference)
        else:
            from_choice.append(self.preference)
            from_choice.append("R")
        randoom = random.choice(from_choice)
        lst.append(randoom)
        self.previous_choices.append(randoom)
        lst.append('Heal')
        if self.ticker % 20 == 0: lst.append("shoot")
        if self.previous_choices[-1] == "U" == self.previous_choices[-2] and self.ticker % 2 == 0: lst.append("shoot")
        self.ticker += 1
        return lst


class NeyroNet():
    def __init__(self, Spaceship, parameters='R'):
        self.preference = parameters[0]
        self.ticker = 0
        self.previous_choices = []

    def should_turn(self, params={"xcoord": {0: 0.89}, "ycoord": {0: 0.966}, "current_angle": {0: 2.18}, "asteroidX": {0: 0.39}, "asteroidY": {0: 0.255}}):
        return sum([params[i].keys() * params[i].values() for i in params]) >= 1000

    def should_move(self, params={"xcoord": {0: 0.88}, "ycoord": {0: 1}, "current_angle": {0: 2.56}, "asteroidX": {0: 0.32}, "asteroidY": {0: 0.234}}):
        return sum([params[i].keys() * params[i].values() for i in params]) >= 1000
