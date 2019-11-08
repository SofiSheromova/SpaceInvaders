from . import Rectangle


class Invader:
    def __init__(self, x, y, width, height, step, health, sector, style):
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.step = step
        self.health = health
        self.sector = sector
        self.style = style

    def y_bottom(self):
        return self.y_top + self.height

    def x_right(self):
        return self.x_left + self.width

    def can_move_right(self, direction, field_width):
        return self.x_right() + self.step < field_width and direction == 1

    def can_move_left(self, direction):
        return self.x_left - self.step > 0 and direction == -1

    def can_move_down(self, ship, bunkers):
        top = bunkers.top() if bunkers.arr else ship.y_top
        return self.y_bottom() + self.step <= top

    def change_style(self):
        self.style = 1 - self.style

    def move(self, x_direction, y_direction):
        self.x_left += self.step * x_direction
        self.y_top += self.step * y_direction
        self.change_style()

    def __eq__(self, other):
        if not isinstance(other, Invader):
            return False
        return ((self.x_left, self.y_top, self.width, self.height, self.step,
                 self.health, self.sector) ==
                (other.x_left, other.y_top, self.width, self.height,
                 self.step, self.health, self.sector))

    def get_rectangle(self):
        return Rectangle(self.x_left, self.y_top, self.width, self.height)


class InvaderState:
    def __init__(self, health, sector):
        self.health = health
        self.sector = sector

    def __eq__(self, other):
        return self.health == other.health and self.sector == other.sector


class Invaders:
    def __init__(self, x, y, invader, arr_state):
        self.x_left = x
        self.y_top = y
        self.width = 0
        self.height = 0
        self.arr_invaders = arr_state
        self.direction = 1
        self.count = 0
        for y, line in enumerate(arr_state):
            for x, element in enumerate(line):
                self.arr_invaders[y][x] = Invader(
                    self.x_left + (invader.step + invader.width) * x,
                    self.y_top + (invader.step + invader.height) * y,
                    invader.width, invader.height, invader.step,
                    element.health, element.sector, 0)
                self.count += 1
                if self.width < x + 1:
                    self.width = x + 1
            if self.height < y + 1:
                self.height = y + 1

        self.delete()

    def delete(self):
        for y in range(len(self.arr_invaders) - 1, -1, -1):
            line = self.arr_invaders[y]
            for x in range(len(line) - 1, -1, -1):
                if not (1 <= line[x].health <= 3 and 0 <= line[x].sector <= 3):
                    self.remove(x, y)

    @staticmethod
    def unite_lists(arr):
        combine_arr = []
        for el in arr:
            combine_arr.extend(el)
        return combine_arr

    def get_left_invader(self):
        return min(self.unite_lists(self.arr_invaders), key=lambda i: i.x_left)

    def get_right_invader(self):
        return max(self.unite_lists(self.arr_invaders), key=lambda i: i.x_left)

    def get_bottom_invader(self):
        return max(self.unite_lists(self.arr_invaders), key=lambda i: i.y_top)

    def can_move_down(self, ship, bunkers):
        bottom_invader = self.get_bottom_invader()
        return bottom_invader.can_move_down(ship, bunkers)

    def remove(self, x, y):
        del self.arr_invaders[y][x]
        self.count -= 1

    def move(self, field):
        if self.count == 0:
            return
        left_invader = self.get_left_invader()
        right_invader = self.get_right_invader()

        if (left_invader.can_move_left(self.direction) or
                right_invader.can_move_right(self.direction, field.width)):
            for group in self.arr_invaders:
                for inv in group:
                    inv.move(self.direction, 0)
        else:
            for group in self.arr_invaders:
                for inv in group:
                    inv.move(0, 2)
            self.direction *= -1
