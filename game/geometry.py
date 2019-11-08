class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


class Round:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def point_is_inside(self, point):
        return ((point.x - self.x) ** 2 + (point.y - self.y) ** 2 <=
                self.radius ** 2)


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height

    def x_right(self):
        return self.x_left + self.width

    def y_bottom(self):
        return self.y_top + self.height

    def contains_point(self, point):
        return (self.x_left <= point.x <= self.x_right() and
                self.y_top <= point.y <= self.y_bottom())


class Superellipse:
    def __init__(self, rect, radius):
        self.rect1 = Rectangle(rect.x_left - radius, rect.y_top,
                               rect.width + 2 * radius, rect.height)
        self.rect2 = Rectangle(rect.x_left, rect.y_top - radius, rect.width,
                               rect.height + 2 * radius)
        self.rounds = [Round(rect.x_left, rect.y_top, radius),
                       Round(rect.x_right(), rect.y_top, radius),
                       Round(rect.x_left, rect.y_bottom(), radius),
                       Round(rect.x_right(), rect.y_bottom(), radius)]

    def is_collapse(self, point):
        if (self.rect1.contains_point(point) or
                self.rect2.contains_point(point)):
            return True
        for r in self.rounds:
            if r.point_is_inside(point):
                return True
        return False
