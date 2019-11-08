import random

from . import Bullet, Bullets, Bunkers, Constants, Invader, Invaders, Level, \
    GameMode, MysteryShip, Ship


class GameState:
    def __init__(self, levels, stop_timer_function, start_timer_function):
        self.dict_keys = set()
        self.bunkers = Bunkers()
        self.ship_bullets = Bullets()
        self.invader_bullets = Bullets()
        self.invader = Invader(0, 0, Constants.INVADER_WIDTH,
                               Constants.INVADER_HEIGHT,
                               Constants.INVADER_STEP, 1, 0, 0)
        self.all_levels = levels
        self.current_mode = GameMode.DEFAULT
        self.stop_timer_function = stop_timer_function
        self.start_timer_function = start_timer_function

    def init_game(self, invader_timer, press_timer, run_timer):
        self.time = 0
        self.score = 0
        self.last_ship_shot_time = - Constants.FREQUENCY_SHOT
        self.last_invader_shot_time = 0
        self.last_mystery_ship_time = 0

        x_ship = ((Constants.PLAYING_FIELD.width - Constants.SHIP_WIDTH) //
                  2 + Constants.PLAYING_FIELD.x_left)
        y_ship = Constants.PLAYING_FIELD.y_bottom() - Constants.SHIP_HEIGHT
        self.ship = Ship(x_ship, y_ship, Constants.SHIP_WIDTH,
                         Constants.SHIP_HEIGHT, Constants.SHIP_STEP)
        self.mystery_ship = MysteryShip(Constants.MYSTERY_SHIP_WIDTH,
                                        Constants.MYSTERY_SHIP_HEIGHT,
                                        Constants.MYSTERY_SHIP_STEP,
                                        Constants.MYSTERY_SHIP_FREQUENCY)

        self.ship_bullets.clear()
        self.invader_bullets.clear()
        self.bunkers.clear()

        self.invader_timer = invader_timer
        self.press_timer = press_timer
        self.run_timer = run_timer

    def start_level(self, level):
        self.current_mode = GameMode.GAME_PLAY

        self.current_level = Level(self.all_levels.levels_string[level])
        self.invaders = self.current_level.invaders
        self.bunkers = self.current_level.bunkers

        self.start_timer_function(self.invader_timer,
                                  Constants.INVADER_FREQUENCY)
        self.start_timer_function(self.press_timer,
                                  Constants.PRESS_FREQUENCY)
        self.start_timer_function(self.run_timer,
                                  Constants.GAME_FREQUENCY)

    def game_timeout(self):
        """ Передвижение пули, обработка выхода за экран и обновление
        изображения """
        self.time += Constants.GAME_FREQUENCY

        self.ship_bullets.fire(Constants.PLAYING_FIELD)
        self.invader_bullets.fire(Constants.PLAYING_FIELD)

        for bunker in self.bunkers.arr:
            self.ship_bullets.break_bunker(bunker, Constants.BUNKER_CELL_WIDTH)
            self.invader_bullets.break_bunker(bunker,
                                              Constants.BUNKER_CELL_WIDTH)
            if bunker.count == 0:
                self.bunkers.remove(bunker)

        dead_enemy = self.ship_bullets.kill(self.invaders, self.ship,
                                            self.mystery_ship)
        if isinstance(dead_enemy, Invaders):
            self.score += Constants.INVADER_BILL
        elif isinstance(dead_enemy, MysteryShip):
            self.score += Constants.MYSTERY_SHIP_BILL
            self.mystery_ship.remove()
            self.last_mystery_ship_time = self.time

        dead_enemy = self.invader_bullets.kill(self.invaders, self.ship, None)
        if isinstance(dead_enemy, Ship):
            self.ship.live -= Constants.DAMAGE_FROM_INVADER
            if not self.ship.live:
                self.current_mode = GameMode.GAME_OVER
                self.stop_all_timers()

        if (self.last_invader_shot_time + Constants.FREQUENCY_INVADER_SHOT <=
                self.time):
            self.last_invader_shot_time = self.time
            if self.invaders.count <= 0:  # победа
                return
            rnd_invader = random.choice(random.choice(
                list(filter(None, self.invaders.arr_invaders))))

            bullet = Bullet(rnd_invader.x_left + rnd_invader.width // 2,
                            rnd_invader.y_top + rnd_invader.height // 2,
                            Constants.INVADER_BULLET_SPEED,
                            random.randint(90 * rnd_invader.sector + 5,
                                           90 * (rnd_invader.sector + 1) - 5),
                            Constants.INVADER_BULLET_RADIUS, True)
            self.invader_bullets.add(bullet)

    def press_timeout(self, KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SPACE):
        """ Обработка нажатий на клавиши """
        for key in self.dict_keys:
            if key == KEY_UP or key == KEY_DOWN:
                self.ship.rotate(1 if key == KEY_UP else -1,
                                 Constants.SHIP_ROTATION_ANGLE)
            if key == KEY_RIGHT or key == KEY_LEFT:
                self.ship.move(1 if key == KEY_RIGHT else -1,
                               Constants.PLAYING_FIELD.width)
            if (key == KEY_SPACE and self.last_ship_shot_time +
                    Constants.FREQUENCY_SHOT <= self.time):
                self.last_ship_shot_time = self.time
                bullet = Bullet(
                    self.ship.x_left + Constants.SHIP_WIDTH // 2,
                    self.ship.y_top + Constants.SHIP_HEIGHT // 2,
                    Constants.BULLET_SPEED,
                    self.ship.angle, Constants.BULLET_RADIUS)
                self.ship_bullets.add(bullet)

    def invader_timeout(self):
        if self.invaders.count > 0 and self.invaders.can_move_down(
                self.ship, self.bunkers):
            self.invaders.move(Constants.PLAYING_FIELD)
        elif self.current_mode == GameMode.GAME_PLAY:
            self.current_mode = GameMode.GAME_OVER

        if self.mystery_ship.in_field(Constants.PLAYING_FIELD):
            self.mystery_ship.move()
        elif (self.last_mystery_ship_time + self.mystery_ship.frequency <
              self.time):
            self.mystery_ship.move()
            self.last_mystery_ship_time = self.time
        else:
            self.mystery_ship.remove()

    def stop_all_timers(self):
        for timer in {self.invader_timer, self.press_timer, self.run_timer}:
            self.stop_timer_function(timer)

    def start_all_timers(self):
        for timer in {self.invader_timer, self.press_timer, self.run_timer}:
            self.start_timer_function(timer)

    def key_press_event(self, event):
        key = event.key()
        self.dict_keys.add(key)

    def key_release_event(self, event, KEY_P):
        key = event.key()
        if key == KEY_P:
            if self.current_mode == GameMode.GAME_PAUSE:
                self.current_mode = GameMode.GAME_PLAY
                self.start_all_timers()
            else:
                self.current_mode = GameMode.GAME_PAUSE
                self.stop_all_timers()

        if key in self.dict_keys:
            self.dict_keys.remove(key)
