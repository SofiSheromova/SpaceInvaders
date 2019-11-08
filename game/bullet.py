import math

from . import Superellipse, Rectangle, Point


class Bullet:
    def __init__(self, x, y, speed, angle, radius, is_invader_bullet=False):
        self.radius = radius
        self.x_left = x
        self.x_vector = x
        self.y_top = y
        self.y_vector = y
        self.speed = speed
        self.angle = angle * math.pi / 180
        self.module_vector = 0
        self.is_invader_bullet = is_invader_bullet

    def y_bottom(self):
        return self.y_top + self.radius

    def x_right(self):
        return self.x_left + self.radius

    def centre(self):
        return Point(self.x_left + self.radius / 2,
                     self.y_top + self.radius / 2)

    def fire(self, playing_field):
        self.module_vector += self.speed
        self.y_top = self.y_vector - self.module_vector * math.sin(self.angle)
        self.x_left = self.x_vector + self.module_vector * math.cos(self.angle)
        if (self.x_left <= playing_field.x_left or
                self.x_right() >= playing_field.x_right()):
            self.angle = math.pi - self.angle
            self.x_vector = self.x_left
            self.y_vector = self.y_top
            self.module_vector = 0
        if self.is_invader_bullet and self.y_top <= playing_field.y_top:
            self.angle = - self.angle
            self.x_vector = self.x_left
            self.y_vector = self.y_top
            self.module_vector = 0

    def in_field(self, field):
        if self.is_invader_bullet:
            return self.y_top < field.y_bottom()
        return field.y_top <= self.y_top < field.y_bottom()

    def kill_invader(self, invader):
        if self.is_invader_bullet:
            return False
        rect = Superellipse(invader.get_rectangle(), self.radius)
        return rect.is_collapse(self.centre())

    def kill_ship(self, ship):
        if not self.is_invader_bullet:
            return False
        rect = Superellipse(ship.get_rectangle(), self.radius)
        return rect.is_collapse(self.centre())

    def kill_mystery_ship(self, mystery_ship):
        if self.is_invader_bullet:
            return False
        rect = Superellipse(mystery_ship.get_rectangle(), self.radius)
        return rect.is_collapse(self.centre())


class Bullets:
    def __init__(self):
        self.arr = []

    def add(self, bullet):
        self.arr.append(bullet)

    def remove(self, bullet):
        self.arr.pop(self.arr.index(bullet))

    def clear(self):
        self.arr = []

    def delete_out_of_field(self, field):
        for bullet in self.arr:
            if not bullet.in_field(field):
                self.arr.remove(bullet)

    def fire(self, field):
        for bullet in self.arr:
            bullet.fire(field)
            if not bullet.in_field(field):
                self.arr.remove(bullet)

    def kill(self, inv, ship, mystery_ship):
        invaders = inv.arr_invaders
        for bullet in self.arr:
            if bullet.kill_ship(ship):
                self.remove(bullet)
                return ship  # корабль умер
            if bullet.kill_mystery_ship(mystery_ship):
                self.remove(bullet)
                return mystery_ship  # mystery ship убит
            for y in range(len(invaders) - 1, -1, -1):
                for x in range(len(invaders[y])):
                    if bullet.kill_invader(invaders[y][x]):
                        self.remove(bullet)
                        invaders[y][x].health -= 1
                        if invaders[y][x].health == 0:
                            inv.remove(x, y)
                        return inv  # инвайдер умер
        return False

    def break_bunker(self, bunker, cell_width):
        for bullet in self.arr:
            bullet_centre = bullet.centre()
            for y, line in enumerate(bunker.arr):
                for x, cell in enumerate(line):
                    if not cell:
                        continue
                    rect = Rectangle(bunker.x_left + cell_width * x,
                                     bunker.y_top + cell_width * y,
                                     cell_width, cell_width)
                    bunker_ellipse = Superellipse(rect, bullet.radius)
                    if bunker_ellipse.is_collapse(bullet_centre):
                        bunker.collapse(x, y)
                        self.remove(bullet)
                        return
