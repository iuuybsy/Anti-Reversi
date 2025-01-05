import pygame
import sys
import time

UNIT: int = 61
MID_UNIT: int = 31

BOARD_WIDTH_UNIT_NUM: int = 8
BOARD_HEIGHT_UNIT_NUM: int = 8

BOARD_WIDTH: int = BOARD_WIDTH_UNIT_NUM * UNIT
BOARD_HEIGHT: int = BOARD_HEIGHT_UNIT_NUM * UNIT

GAP: int = 3

LOGIC_WIDTH: int = 8
LOGIC_HEIGHT: int = 8
LOGIC_TOTAL = LOGIC_WIDTH * LOGIC_HEIGHT

STONE_OUTER_RADIUS: int = 25
STONE_INNER_RADIUS: int = 20
DOT_RADIUS: int = 8

DIRECTIONS: list[list[int]] = [[1, 0], [1, 1], [0, 1], [-1, 1],
                               [-1, 0], [-1, -1], [0, -1], [1, -1]]

WINNER_X: int = UNIT
WINNER_Y: int = 2 * UNIT
WINNER_WIDTH: int = 6 * UNIT
WINNER_HEIGHT: int = 2 * UNIT
WINNER_TEXT_SIZE = 50

REPLAY_X: int = 2 * UNIT
REPLAY_Y: int = 5 * UNIT
REPLAY_WIDTH: int = 4 * UNIT
REPLAY_HEIGHT: int = UNIT
REPLAY_TEXT_SIZE: int = 30

DEEP_GREY: tuple[int, int, int] = (100, 100, 100)
LIGHT_GREY: tuple[int, int, int] = (125, 125, 125)

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)

BLACK_FINAL: tuple[int, int, int] = (50, 50, 50)
WHITE_FINAL: tuple[int, int, int] = (205, 205, 205)


def get_mouse_cord() -> tuple[int, int]:
    """
    Get the mouse block ord
    :return: (x_num: int, y_num: int)
    """
    x, y = pygame.mouse.get_pos()
    x_num = x // UNIT
    y_num = y // UNIT
    return x_num, y_num


def is_valid_cord(x: int, y: int) -> bool:
    """
    Check if the cord is valid
    :param x: cord of x-axis
    :param y: cord of y-axis
    :return: flag to see if the cord is valid
    """
    return 0 <= x < LOGIC_WIDTH and 0 <= y < LOGIC_HEIGHT


class ReversiGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Anti Reversi Game")
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

        self.status: list[list[int]] = [[0 for _ in range(LOGIC_HEIGHT)] for __ in range(LOGIC_WIDTH)]
        self.status[3][3] = 1
        self.status[3][4] = -1
        self.status[4][3] = -1
        self.status[4][4] = 1

        self.is_black_turn: bool = True
        self.is_end: bool = False

        self.last_move: list[int] = [-1, -1]

        self.possible_moves: list[list[tuple[int, int]]] = [[] for _ in range(LOGIC_TOTAL)]
        self.check_possible_move()

    def self_play(self):
        """
        Self play mode
        :return: None
        """
        while True:
            self.screen.fill(DEEP_GREY)
            self.draw_board()
            self.plot_stones()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.is_end:
                self.winner_judgement_plot()
                self.change_restart_color()
                left, _, _ = pygame.mouse.get_pressed()
                if left:
                    self.restart_click_respond()
            else:
                self.self_play_move_respond()
                left, _, _ = pygame.mouse.get_pressed()
                if left:
                    self.self_play_click_respond()

            pygame.display.flip()

    def refresh(self):
        """
        After a game ends, refresh the board
        :return: None
        """
        self.status.clear()
        self.status = [[0 for _ in range(LOGIC_HEIGHT)] for __ in range(LOGIC_WIDTH)]
        self.status[3][3] = 1
        self.status[3][4] = -1
        self.status[4][3] = -1
        self.status[4][4] = 1

        self.is_black_turn: bool = True
        self.is_end: bool = False

        self.last_move = [-1, -1]

        self.possible_moves = [[] for _ in range(LOGIC_TOTAL)]
        self.check_possible_move()

    def change_restart_color(self):
        """
        Change the restart button's color when the mouse is on it
        :return: None
        """
        x_num, y_num = get_mouse_cord()
        if y_num == 5 and 2 <= x_num <= 5:
            text_string = "restart"
            rect_color = WHITE if self.is_black_turn else BLACK
            font_color = BLACK if self.is_black_turn else WHITE
            self.rect_with_text(rect_color, font_color, REPLAY_X, REPLAY_Y,
                                REPLAY_WIDTH, REPLAY_HEIGHT, REPLAY_TEXT_SIZE,
                                text_string=text_string)

    def restart_click_respond(self):
        """
        Click the restart button to restart the game
        :return: None
        """
        x_num, y_num = get_mouse_cord()
        if y_num == 5 and 2 <= x_num <= 5:
            self.refresh()
            time.sleep(0.5)

    def self_play_click_respond(self):
        """
        Mouse click respond for self play mode
        :return: None
        """
        x_num, y_num = get_mouse_cord()
        ind = y_num * LOGIC_WIDTH + x_num
        if len(self.possible_moves[ind]) > 0:
            is_black_turn_at_start: bool = self.is_black_turn
            self.set_stone(x_num, y_num)
            self.is_black_turn = not self.is_black_turn
            self.check_possible_move()
            is_black_turn_at_end: bool = self.is_black_turn

            self.last_move[0] = x_num
            self.last_move[1] = y_num

            if is_black_turn_at_start == is_black_turn_at_end:
                self.check_possible_move()
                black_count: int = 0
                white_count: int = 0
                for i in range(LOGIC_WIDTH):
                    for j in range(LOGIC_HEIGHT):
                        if self.status[i][j] > 0:
                            black_count += 1
                        elif self.status[i][j] < 0:
                            white_count += 1
                have_black_move, _ = self.have_possible_move(is_black_turn=True)
                have_white_move, _ = self.have_possible_move(is_black_turn=False)
                if not (have_black_move or have_white_move):
                    self.is_end = True
                    self.is_black_turn = black_count > white_count

    def set_stone(self, x_num: int, y_num: int):
        """
        Set the stone and the stones that can be flipped
        :param x_num: cord of x-axis
        :param y_num: cord of y-axis
        :return: None
        """
        ind = y_num * LOGIC_WIDTH + x_num
        stone_sign = 1 if self.is_black_turn else -1
        self.status[x_num][y_num] = stone_sign
        for i in range(len(self.possible_moves[ind])):
            x_temp, y_temp = self.possible_moves[ind][i]
            self.status[x_temp][y_temp] = stone_sign

    def get_possible_moves(self, is_black_turn: bool) -> list[list[tuple[int, int]]]:
        """
        Get the possible moves for current situation
        :param is_black_turn:
        :return: list of possible moves for every block
        """
        target: int = 1 if is_black_turn else -1
        enemy: int = -target
        possible_moves: list[list[tuple[int, int]]] = [[] for _ in range(LOGIC_TOTAL)]
        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] == target:
                    for direction in DIRECTIONS:
                        temp_rec = set()
                        x_next = i + direction[0]
                        y_next = j + direction[1]
                        if not is_valid_cord(x_next, y_next):
                            continue
                        if self.status[x_next][y_next] != enemy:
                            continue
                        while (is_valid_cord(x_next, y_next) and
                               self.status[x_next][y_next] == enemy):
                            temp_rec.add((x_next, y_next))
                            x_next = x_next + direction[0]
                            y_next = y_next + direction[1]
                        if not is_valid_cord(x_next, y_next):
                            continue
                        if self.status[x_next][y_next] == 0:
                            ind = y_next * LOGIC_WIDTH + x_next
                            for cord_tuple in temp_rec:
                                possible_moves[ind].append(cord_tuple)
        return possible_moves

    def check_possible_move(self):
        """
        Check the possible moves for current situation
        :return: None
        """
        have_possible_move, self.possible_moves = self.have_possible_move(self.is_black_turn)
        if not have_possible_move:
            self.is_black_turn = not self.is_black_turn

    def have_possible_move(self, is_black_turn: bool) -> (
            tuple)[bool, list[list[tuple[int, int]]]]:
        """
        Check if there's a possible move
        :param is_black_turn: Flag to see if it's black's turn
        :return: Flag to see if there's a possible move
        """
        possible_moves: list[list[tuple[int, int]]] = self.get_possible_moves(is_black_turn)
        count: int = sum(len(possible_move_list) for possible_move_list in possible_moves)
        return count > 0, possible_moves

    def self_play_move_respond(self):
        """
        Plot the possible moves for self play mode
        :return: None
        """
        x_num, y_num = get_mouse_cord()
        if len(self.possible_moves) == 0:
            return
        ind = y_num * LOGIC_WIDTH + x_num
        stone_plot_func = self.plot_black_stone if self.is_black_turn \
            else self.plot_white_stone
        dot_plot_func = self.plot_black_dot if self.is_black_turn \
            else self.plot_white_dot
        if self.status[x_num][y_num] == 0:
            stone_plot_func(x_num, y_num)
            for x_temp, y_temp in self.possible_moves[ind]:
                dot_plot_func(x_temp, y_temp)

    def draw_board(self):
        """
        Draw the board
        :return: None
        """
        for i in range(BOARD_WIDTH_UNIT_NUM):
            for j in range(BOARD_HEIGHT_UNIT_NUM):
                left = i * UNIT + GAP
                top = j * UNIT + GAP
                width = UNIT - 2 * GAP
                height = UNIT - 2 * GAP
                rect = (left, top, width, height)
                pygame.draw.rect(self.screen, LIGHT_GREY, rect, 0)

    def plot_stones(self):
        """
        Plot the stones
        :return: None
        """
        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] > 0:
                    self.plot_black_stone(i, j)
                elif self.status[i][j] < 0:
                    self.plot_white_stone(i, j)
        if is_valid_cord(self.last_move[0], self.last_move[1]):
            self.plot_red_dot(self.last_move[0], self.last_move[1])

    def plot_black_stone(self, x: int, y: int):
        """
        Plot a black stone
        :param x: cord of x-axis
        :param y: cord of y-axis
        :return: None
        """
        pygame.draw.circle(self.screen, BLACK,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           STONE_OUTER_RADIUS)

    def plot_white_stone(self, x: int, y: int):
        """
        Plot a white stone
        :param x: cord of x-axis
        :param y: cord of y-axis
        :return: None
        """
        self.plot_black_stone(x, y)
        pygame.draw.circle(self.screen, WHITE,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS)

    def plot_black_dot(self, x: int, y: int):
        """
        Plot a black dot over a white stone
        :param x: cord of x-axis
        :param y: cord of y-axis
        :return: None
        """
        pygame.draw.circle(self.screen, BLACK,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           DOT_RADIUS)

    def plot_white_dot(self, x: int, y: int):
        """
        Plot a white dot over a black stone
        :param x: cord of x-axis
        :param y: cord of y-axis
        :return: None
        """
        pygame.draw.circle(self.screen, WHITE,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           DOT_RADIUS)

    def plot_red_dot(self, x: int, y: int):
        """
        Plot a red dot over a stone
        :param x: cord of x-axis
        :param y: cord of y-axis
        :return: None
        """
        pygame.draw.circle(self.screen, RED,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           DOT_RADIUS)

    def rect_with_text(self, rect_color: tuple[int, int, int],
                       font_color: tuple[int, int, int],
                       x_start: int, y_start: int, width: int, height: int,
                       text_size: int, border_radius: int = 10, text_string: str = ""):
        """
        Plot a rectangle with text
        :param rect_color: color of the rectangle
        :param font_color: color of the text
        :param x_start: rectangle's up left cord of x-axis
        :param y_start: rectangle's up left cord of y-axis
        :param width: rectangle's width of blocks
        :param height: rectangle's height of blocks
        :param text_size: size of text font
        :param border_radius: size of border radius
        :param text_string: text to be plotted on rectangle
        :return: None
        """
        pygame.draw.rect(self.screen, rect_color,
                         (x_start, y_start,
                          width, height),
                         border_radius=border_radius)
        font = pygame.font.SysFont("Century", text_size)
        text = font.render(text_string, True, font_color)
        text_width = text.get_width()
        text_height = text.get_height()
        x_pix = width // 2 - text_width // 2 + x_start
        y_pix = height // 2 - text_height // 2 + y_start
        self.screen.blit(text, (x_pix, y_pix))

    def winner_judgement_plot(self):
        """
        Plot the winner on screen
        :return: None
        """
        rect_color = BLACK if self.is_black_turn else WHITE
        font_color = WHITE if self.is_black_turn else BLACK
        text_string = "Black Win!" if self.is_black_turn else "White Win!"

        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] > 0:
                    pygame.draw.circle(self.screen, BLACK_FINAL,
                                       (i * UNIT + MID_UNIT + 1,
                                        j * UNIT + MID_UNIT + 1),
                                       STONE_OUTER_RADIUS)
                elif self.status[i][j] < 0:
                    pygame.draw.circle(self.screen, BLACK_FINAL,
                                       (i * UNIT + MID_UNIT + 1,
                                        j * UNIT + MID_UNIT + 1),
                                       STONE_OUTER_RADIUS)
                    pygame.draw.circle(self.screen, WHITE_FINAL,
                                       (i * UNIT + MID_UNIT + 1,
                                        j * UNIT + MID_UNIT + 1),
                                       STONE_INNER_RADIUS)

        self.rect_with_text(rect_color, font_color, WINNER_X, WINNER_Y,
                            WINNER_WIDTH, WINNER_HEIGHT, WINNER_TEXT_SIZE,
                            text_string=text_string)

        self.rect_with_text(rect_color, font_color, REPLAY_X, REPLAY_Y,
                            REPLAY_WIDTH, REPLAY_HEIGHT, REPLAY_TEXT_SIZE,
                            text_string="restart")
