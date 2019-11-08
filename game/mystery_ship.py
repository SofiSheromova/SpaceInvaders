from . import Rectangle
from . import Constants


class MysteryShip:
    def __init__(self, width, height, step, frequency):
        self.x_left = -width
        self.y_top = Constants.PLAYING_FIELD.y_top + step
        self.width = width
        self.height = height
        self.step = step
        self.frequency = frequency

    def y_bottom(self):
        return self.y_top + self.height

    def x_right(self):
        return self.x_left + self.width

    def move(self):
        self.x_left += self.step

    def get_rectangle(self):
        return Rectangle(self.x_left, self.y_top, self.width, self.height)

    def in_field(self, field):
        return field.x_left < self.x_right() and self.x_left < field.x_right()

    def remove(self):
        self.x_left = -self.width
