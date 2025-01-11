import pygame
from stone_enum import Stone

UNIT: int = 61
MID_UNIT: int = 31

BOARD_WIDTH_UNIT_NUM: int = 8
BOARD_HEIGHT_UNIT_NUM: int = 8

BOARD_WIDTH: int = BOARD_WIDTH_UNIT_NUM * UNIT
BOARD_HEIGHT: int = BOARD_HEIGHT_UNIT_NUM * UNIT

GAP: int = 3

STONE_OUTER_RADIUS: int = 25
STONE_INNER_RADIUS: int = 20
DOT_RADIUS: int = 8

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


class ReversiPlot:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Anti Reversi Game")
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    def game_render(self, board_status: list[list[Stone]], last_move: list[int]):
        self.screen.fill(DEEP_GREY)
        self.draw_board()
        self.plot_stones(board_status, last_move)

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

    def plot_stones(self, board_status: list[list[Stone]], last_move: list[int]):
        """
        Plot the stones
        :return: None
        """
        for i in range(len(board_status)):
            for j in range(len(board_status[i])):
                if board_status[i][j] == Stone.BLACK:
                    self.plot_black_stone(i, j)
                elif board_status[i][j] == Stone.WHITE:
                    self.plot_white_stone(i, j)
        if (0 <= last_move[0] < BOARD_WIDTH_UNIT_NUM and
                0 <= last_move[1] < BOARD_HEIGHT_UNIT_NUM):
            self.plot_red_dot(last_move[0], last_move[1])

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

    def winner_judgement_plot(self, board_status: list[list[Stone]], is_black_turn: bool):
        """
        Plot the winner on screen
        :return: None
        """
        rect_color = BLACK if is_black_turn else WHITE
        font_color = WHITE if is_black_turn else BLACK
        text_string = "Black Win!" if is_black_turn else "White Win!"

        for i in range(BOARD_WIDTH_UNIT_NUM):
            for j in range(BOARD_HEIGHT_UNIT_NUM):
                if board_status[i][j] == Stone.BLACK:
                    pygame.draw.circle(self.screen, BLACK_FINAL,
                                       (i * UNIT + MID_UNIT + 1,
                                        j * UNIT + MID_UNIT + 1),
                                       STONE_OUTER_RADIUS)
                elif board_status[i][j] == Stone.WHITE:
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

    def change_restart_color(self, is_black_turn: bool):
        """
        Change the restart button's color when the mouse is on it
        :return: None
        """
        x_num, y_num = self.get_mouse_cord()
        if y_num == 5 and 2 <= x_num <= 5:
            text_string = "restart"
            rect_color = WHITE if is_black_turn else BLACK
            font_color = BLACK if is_black_turn else WHITE
            self.rect_with_text(rect_color, font_color, REPLAY_X, REPLAY_Y,
                                REPLAY_WIDTH, REPLAY_HEIGHT, REPLAY_TEXT_SIZE,
                                text_string=text_string)

    @staticmethod
    def get_mouse_cord() -> tuple[int, int]:
        """
        Get the mouse block ord
        :return: (x_num: int, y_num: int)
        """
        x, y = pygame.mouse.get_pos()
        x_num = x // UNIT
        y_num = y // UNIT
        return x_num, y_num
