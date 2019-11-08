import sys
import os

try:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtGui import QImage, QIcon, QColor
except Exception as e:
    print('PyQt5 not found: "{}".'.format(e), file=sys.stderr)
    sys.exit(5)

try:
    from game import Constants
except Exception as e:
    print('Module not found: {}'.format(e), file=sys.stderr)
    sys.exit(6)


class GUI:
    def __init__(self):
        self.icon = self.QIcon('invader1_1(0).png')
        self.background_img = self.QImage('background.jpg')
        self.ship_img = self.QImage('ship.png')
        self.bullet_img = self.QImage('bullet.png')
        self.invader_bullet_img = self.QImage('invader_bullet.png')
        self.pause_img = self.QImage('pause.png')
        self.game_over_img = self.QImage('game_over.png')
        self.you_win_img = self.QImage('win.png')
        self.level = self.QImage('level.png')
        self.level_selection = self.QImage('level_selection.png')
        self.record = self.QImage('table_of_records.png')
        self.mystery_ship_img = self.QImage('mystery_ship.png')
        self.arrows_up_down = self.QImage('choice_level.png')
        self.arrows_left_right = self.QImage('choice_scoreboard.png')

        self.digits = []
        for i in range(10):
            self.digits.append(self.QImage(f"{i}.png"))

        self.invader_img = {}
        for health in range(1, 4):
            for sector in range(4):
                for style in range(2):
                    self.invader_img[f"{health}{sector}{style}"] \
                        = self.QImage(f"invader{health}_{sector}({style}).png")

    @staticmethod
    def QImage(file_name):
        return QImage(os.path.join('images', file_name))

    @staticmethod
    def QIcon(file_name):
        return QIcon(os.path.join('images', file_name))

    def get_img_invader(self, health, sector, style):
        return self.invader_img[f"{health}{sector}{style}"]

    def paint_invaders(self, painter, arr_invaders):
        for dy, i in enumerate(arr_invaders):
            for dx, j in enumerate(i):
                x = j.x_left
                y = j.y_top
                rect = QtCore.QRect(x, y, Constants.INVADER_WIDTH,
                                    Constants.INVADER_HEIGHT)
                image = self.get_img_invader(j.health, j.sector, j.style)
                painter.drawImage(rect, image)

    def paint_bullets(self, painter, arr_bullets, invader=False):
        for bullet in arr_bullets:
            if invader:
                image = self.invader_bullet_img
                radius = Constants.INVADER_BULLET_RADIUS
            else:
                image = self.bullet_img
                radius = Constants.BULLET_RADIUS
            rect = QtCore.QRect(bullet.x_left, bullet.y_top,
                                2 * radius, 2 * radius)
            painter.drawImage(rect, image)

    def paint_ship(self, painter, ship):
        rect = QtCore.QRect(ship.x_left, ship.y_top, ship.width, ship.height)
        self.rotate_obj(painter, 90 - ship.angle, ship)
        painter.drawImage(rect, self.ship_img)
        self.rotate_obj(painter, -90 + ship.angle, ship)

    def rotate_obj(self, painter, angle, obj):
        painter.translate(obj.x_left + obj.width // 2,
                          obj.y_top + obj.height // 2)
        painter.rotate(angle)
        painter.translate(-obj.x_left - obj.width // 2,
                          -obj.y_top - obj.height // 2)

    def paint_bunkers(self, painter, bunkers):
        for bunker in bunkers:
            for y, line in enumerate(bunker.arr):
                for x, cell in enumerate(line):
                    if not cell:
                        continue
                    painter.setBrush(QColor(200, 0, 0))
                    painter.drawRect(
                        bunker.x_left + Constants.BUNKER_CELL_WIDTH * x,
                        bunker.y_top + Constants.BUNKER_CELL_WIDTH * y,
                        Constants.BUNKER_CELL_WIDTH,
                        Constants.BUNKER_CELL_WIDTH)

    def paint_mystery_ship(self, painter, ship):
        rect = QtCore.QRect(ship.x_left, ship.y_top, ship.width, ship.height)
        painter.drawImage(rect, self.mystery_ship_img)

    def paint_game_over(self, painter, rect):
        painter.drawImage(rect, self.game_over_img)

    def paint_you_win(self, painter, rect):
        painter.drawImage(rect, self.you_win_img)

    def paint_pause(self, painter, rect):
        painter.drawImage(rect, self.pause_img)

    def paint_level(self, painter, number):
        level_width = 470
        level_height = 75

        painter.drawImage(QtCore.QRect(
            (Constants.WINDOW_WIDTH - level_width) / 2,
            Constants.WINDOW_HEIGHT / 2 - level_height, level_width,
            level_height), self.level)
        for i, digit in enumerate(str(number)):
            self.paint_digit(painter, int(digit), i, len(str(number)))

    def paint_digit(self, painter, digit, index, length):
        digit_height = 75
        digit_width = digit_height / 10 * 8
        painter.drawImage(QtCore.QRect(
            (Constants.WINDOW_WIDTH - length * digit_width) / 2 + int(
                index) * digit_width,
            Constants.WINDOW_HEIGHT / 2 + 20,
            digit_width,
            digit_height),
            self.digits[digit])

    @staticmethod
    def paint_button(painter, button, img):
        painter.drawImage(QtCore.QRect(button.x_left, button.y_top,
                                       button.width, button.height), img)

    def paint_arrows_left_right(self, painter, rect):
        painter.drawImage(rect, self.arrows_left_right)

    def paint_arrows_up_down(self, painter, rect):
        painter.drawImage(rect, self.arrows_up_down)
