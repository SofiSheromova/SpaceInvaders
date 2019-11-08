from . import Rectangle


class Ship:
    def __init__(self, x, y, width, height, step):
        self.x_left = x
        self.width = width
        self.y_top = y
        self.height = height
        self.angle = 90
        self.step = step
        self.live = 3

    def y_bottom(self):
        return self.y_top + self.height

    def x_right(self):
        return self.x_left + self.width

    def get_rectangle(self):
        return Rectangle(self.x_left, self.y_top, self.width, self.height)

    def rotate(self, direction, angle):
        if direction == -1 and self.angle + angle <= 170:
            self.angle += angle
        elif direction == 1 and self.angle - angle >= 10:
            self.angle -= angle
        elif direction != 1 and direction != -1:
            raise KeyError

    def move(self, direction, width):
        if direction == -1 and self.x_left >= self.step:
            self.x_left -= self.step
        if direction == 1 and self.x_right() <= width - self.step:
            self.x_left += self.step
        if direction != -1 and direction != 1:
            raise KeyError
