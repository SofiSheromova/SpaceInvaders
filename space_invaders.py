import sys
import json
from collections import Counter

try:
    from PyQt5 import QtGui, QtCore, QtWidgets
except Exception as e:
    print('PyQt5 not found: "{}".'.format(e), file=sys.stderr)
    sys.exit(5)

try:
    from game import AllLevels, Constants, Rectangle, Point, GameMode, \
        WindowMode, EmptyLevelsFile, IncorrectFormatLevelsFile, GameState
    from gui import GUI, Music
except Exception as e:
    print('Module not found: {}'.format(e), file=sys.stderr)
    sys.exit(6)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Space Invaders')
        self.ui = GUI()
        self.setFixedSize(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.setWindowIcon(self.ui.icon)
        self.current_mode = WindowMode.CHOICE_LEVEL

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(10)

        self.button_record = Rectangle(90, 430, 430, 53)
        self.button_select = Rectangle(90, 500, 430, 53)

        self.current_level = 0

        try:
            levels = AllLevels(AllLevels.LEVELS_FILE)
        except EmptyLevelsFile as e:
            QtWidgets.QMessageBox.critical(
                self, "Failed to launch the game",
                f"{AllLevels.LEVELS_FILE} is empty. Write levels for the game",
                QtWidgets.QMessageBox.Ok)
            sys.exit(8)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Failed to launch the game",
                f"{AllLevels.LEVELS_FILE} not found: \n{e}",
                QtWidgets.QMessageBox.Ok)
            sys.exit(7)

        self.count_levels = levels.get_count_level()

        self.game = GameState(levels, QtCore.QTimer.stop, QtCore.QTimer.start)
        self.game.init_game(**self.get_game_timer())

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_timeout)
        self.update_timer.start(10)

        self.previous_score = self.game.score
        self.previous_ship_live = self.game.ship.live
        self.previous_game_mode = self.game.current_mode

        self.music = Music()
        self.music.play_background()

        self.scoreboard = Scoreboard(self.count_levels)
        self.current_player = None
        self.names_players = self.scoreboard.get_players()

        self.show()
        self.show_name_choice()

    def update_timeout(self):
        self.update()
        if (self.game.score - self.previous_score ==
                Constants.MYSTERY_SHIP_BILL):
            self.music.play_hit_mystery_ship_sound()
        elif self.game.score - self.previous_score == Constants.INVADER_BILL:
            self.music.play_hit_sound()
        if self.previous_ship_live > self.game.ship.live:
            self.music.play_dying()
        if (self.previous_game_mode == GameMode.GAME_PLAY and
                self.game.current_mode == GameMode.GAME_OVER):
            if self.game.invaders.count > 0:
                self.music.play_game_over()
            else:
                self.music.play_win()
        self.previous_score = self.game.score
        self.previous_ship_live = self.game.ship.live
        self.previous_game_mode = self.game.current_mode

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), QtGui.QPixmap(self.ui.background_img))

        if self.current_mode == WindowMode.SCOREBOARD:
            painter.setPen(QtGui.QColor(255, 255, 255))
            painter.setFont(QtGui.QFont('Decorative', 20))
            level = self.scoreboard.get_top_scoreboard(self.current_level)
            painter.drawText(100, 70, f"Level {self.current_level}")
            for site, player in enumerate(level):
                painter.drawText(100, 40 * site + 120,
                                 f"{site + 1}. {player[0]}: {player[1]}")
            self.ui.paint_button(painter, self.button_select,
                                 self.ui.level_selection)
            self.ui.paint_arrows_left_right(painter, self.rect())

        elif self.current_mode == WindowMode.GAME_PLAY:
            if self.game.current_mode == GameMode.GAME_OVER:
                if self.game.invaders.count == 0:
                    self.ui.paint_you_win(painter, self.rect())
                else:
                    self.ui.paint_game_over(painter, self.rect())
                self.ui.paint_button(painter, self.button_select,
                                     self.ui.level_selection)
                self.ui.paint_button(painter, self.button_record,
                                     self.ui.record)

            elif self.game.current_mode == GameMode.GAME_PLAY:
                game = self.game
                painter.setPen(QtGui.QColor(255, 255, 255))
                painter.setFont(QtGui.QFont('Decorative', 20))
                painter.drawText(50, 25, "Score: {}".format(game.score))
                painter.drawText(250, 25,
                                 "Time: {}".format(int(game.time / 1000)))
                painter.drawText(450, 25, "Live: {}".format(game.ship.live))

                self.ui.paint_invaders(painter, game.invaders.arr_invaders)
                self.ui.paint_bullets(painter, game.ship_bullets.arr)
                self.ui.paint_bullets(painter, game.invader_bullets.arr,
                                      invader=True)
                self.ui.paint_ship(painter, game.ship)
                self.ui.paint_bunkers(painter, game.bunkers.arr)
                self.ui.paint_mystery_ship(painter, game.mystery_ship)

            elif self.game.current_mode == GameMode.GAME_PAUSE:
                self.ui.paint_pause(painter, self.rect())

        elif self.current_mode == WindowMode.CHOICE_LEVEL:
            self.ui.paint_level(painter, self.current_level)
            self.ui.paint_arrows_up_down(painter, self.rect())

    def get_game_timer(self):
        keys = {
            'KEY_UP': QtCore.Qt.Key_Up,
            'KEY_DOWN': QtCore.Qt.Key_Down,
            'KEY_RIGHT': QtCore.Qt.Key_Right,
            'KEY_LEFT': QtCore.Qt.Key_Left,
            'KEY_SPACE': QtCore.Qt.Key_Space
        }
        invader_timer = QtCore.QTimer()
        invader_timer.timeout.connect(self.game.invader_timeout)
        press_timer = QtCore.QTimer()
        press_timer.timeout.connect(lambda: self.game.press_timeout(**keys))
        run_timer = QtCore.QTimer()
        run_timer.timeout.connect(self.game.game_timeout)
        return {
            'invader_timer': invader_timer,
            'press_timer': press_timer,
            'run_timer': run_timer
        }

    def mousePressEvent(self, event):
        click = Point(event.x(), event.y())

        if self.current_mode == WindowMode.SCOREBOARD:
            if self.button_select.contains_point(click):
                self.game.init_game(**self.get_game_timer())
                self.current_mode = WindowMode.CHOICE_LEVEL

        elif (self.current_mode == WindowMode.GAME_PLAY and
              self.game.current_mode == GameMode.GAME_OVER):
            level = self.current_level
            player = self.current_player
            if player:
                scoreboard = self.scoreboard.board
                if player not in scoreboard[level]:
                    scoreboard[level][player] = 0
                scoreboard[level][player] = max(
                    self.game.score, scoreboard[level][player])

            if self.button_select.contains_point(click):
                self.game.init_game(**self.get_game_timer())
                self.current_mode = WindowMode.CHOICE_LEVEL
            if self.button_record.contains_point(click):
                self.current_mode = WindowMode.SCOREBOARD

    def keyPressEvent(self, event):
        key = event.key()
        if self.current_mode == WindowMode.GAME_PLAY:
            self.game.key_press_event(event)

        elif self.current_mode == WindowMode.CHOICE_LEVEL:
            if key == QtCore.Qt.Key_Down:
                self.current_level = ((self.current_level + 1) %
                                      self.count_levels)
            elif key == QtCore.Qt.Key_Up:
                self.current_level = ((self.current_level - 1 +
                                       self.count_levels) % self.count_levels)
            elif key == QtCore.Qt.Key_Enter - 1 or key == QtCore.Qt.Key_Enter:
                try:
                    self.game.start_level(self.current_level)
                    self.previous_score = self.game.score
                    self.previous_ship_live = self.game.ship.live
                except IncorrectFormatLevelsFile as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Failed to launch the game",
                        f'Incorrect format {AllLevels.LEVELS_FILE}: \n{e}',
                        QtWidgets.QMessageBox.Ok)
                    sys.exit(9)
                self.current_mode = WindowMode.GAME_PLAY
        elif self.current_mode == WindowMode.SCOREBOARD:
            if key == QtCore.Qt.Key_Right:
                self.current_level = ((self.current_level + 1) %
                                      self.count_levels)
            elif key == QtCore.Qt.Key_Left:
                self.current_level = ((self.current_level - 1 +
                                       self.count_levels) % self.count_levels)

    def keyReleaseEvent(self, event):
        self.game.key_release_event(event, QtCore.Qt.Key_P)

    def closeEvent(self, event):
        self.scoreboard.dump_board()

    def show_name_choice(self):
        add_item = "Add new player..."
        items = list(self.names_players)
        if add_item not in items:
            items.insert(0, add_item)
        item, ok_pressed = QtWidgets.QInputDialog.getItem(
            self, "Choice player", "Player:", items, 0, False)
        if ok_pressed and item:
            if item == add_item:
                self.show_dialog()
            else:
                self.current_player = item

    def show_dialog(self):
        answer = 'Enter your name:'
        widget = QtWidgets.QInputDialog
        text, ok = widget.getText(self, "Enter player", answer)
        while True:
            if not ok:
                return
            if text in self.names_players:
                answer = "This name already used!"
            elif not text:
                answer = "You didn't enter name!"
            else:
                break
            text, ok = widget.getText(self, "Enter player", answer)
        self.current_player = text


class Scoreboard:
    def __init__(self, count_levels):
        self.count_levels = count_levels
        self.SCOREBOARD_FILE = "scoreboard.json"
        self.board = self.get_scoreboard()

    def get_scoreboard(self):
        try:
            with open(self.SCOREBOARD_FILE, 'r') as f:
                inp = json.loads(f.read())[:self.count_levels]
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Failed to launch the game",
                f'Failed to read the scoreboard file. {self.SCOREBOARD_FILE}',
                QtWidgets.QMessageBox.Ok)
            inp = []
        while len(inp) < self.count_levels:
            inp.append({})
        return inp

    def get_top_scoreboard(self, level):
        return Counter(self.board[level]).most_common(10)

    def get_players(self):
        names_players = set()
        for users in self.board:
            names_players.update(set(users))
        return names_players

    def dump_board(self):
        with open(self.SCOREBOARD_FILE, "w") as f:
            json.dump(self.board, f)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
