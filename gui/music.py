import os
import sys

try:
    from PyQt5 import QtCore, QtMultimedia
except Exception as e:
    print('PyQt5 not found: "{}".'.format(e), file=sys.stderr)
    sys.exit(5)


class Music:
    def __init__(self):
        back = QtCore.QUrl.fromLocalFile(self.get_path('background.mp3'))
        self.back_playlist = QtMultimedia.QMediaPlaylist()
        self.back_playlist.addMedia(QtMultimedia.QMediaContent(back))
        self.back_playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.back_player = QtMultimedia.QMediaPlayer()
        self.back_player.setPlaylist(self.back_playlist)

        hit = QtCore.QUrl.fromLocalFile(self.get_path('hit.mp3'))
        self.hit_player = QtMultimedia.QMediaPlayer()
        self.hit_player.setMedia(QtMultimedia.QMediaContent(hit))

        win = QtCore.QUrl.fromLocalFile(self.get_path('win.mp3'))
        self.win_player = QtMultimedia.QMediaPlayer()
        self.win_player.setMedia(QtMultimedia.QMediaContent(win))

        game_over = QtCore.QUrl.fromLocalFile(self.get_path('game_over.mp3'))
        self.game_over_player = QtMultimedia.QMediaPlayer()
        self.game_over_player.setMedia(QtMultimedia.QMediaContent(game_over))

        dying = QtCore.QUrl.fromLocalFile(self.get_path('dying.mp3'))
        self.dying_player = QtMultimedia.QMediaPlayer()
        self.dying_player.setMedia(QtMultimedia.QMediaContent(dying))

        hit_mystery_ship = QtCore.QUrl.fromLocalFile(
            self.get_path('hit_mystery.mp3'))
        self.hit_mystery_ship_player = QtMultimedia.QMediaPlayer()
        self.hit_mystery_ship_player.setMedia(
            QtMultimedia.QMediaContent(hit_mystery_ship))

    @staticmethod
    def get_path(file_name):
        return os.path.abspath(os.path.join('music', file_name))

    def play_background(self):
        self.back_player.play()

    def play_hit_sound(self):
        self.hit_player.stop()
        self.hit_player.play()

    def play_hit_mystery_ship_sound(self):
        self.hit_mystery_ship_player.stop()
        self.hit_mystery_ship_player.play()

    def play_win(self):
        self.win_player.play()

    def play_game_over(self):
        self.game_over_player.play()

    def play_dying(self):
        self.dying_player.play()
