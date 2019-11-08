class Bunker:
    def __init__(self, x, y, size, width):
        self.x_left = x
        self.y_top = y
        self.size = size
        self.arr = [[True for i in range(size[0])] for j in range(size[1])]
        self.count = size[0] * size[1]
        self.width = width

    def collapse(self, x, y):
        try:
            self.arr[y][x] = False
            self.count -= 1
        except IndexError:
            pass


class Bunkers:
    def __init__(self):
        self.arr = []

    def add(self, bunker):
        self.arr.append(bunker)

    def remove(self, bunker):
        self.arr.pop(self.arr.index(bunker))

    def clear(self):
        self.arr.clear()

    def top(self):
        return min(self.arr, key=lambda bunker: bunker.y_top).y_top
