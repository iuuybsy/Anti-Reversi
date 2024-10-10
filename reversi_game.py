import pygame
import colors
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

STONE_OUTER_RADIUS: int = 25
STONE_INNER_RADIUS: int = 20

DIRECTIONS = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]


class ReversiGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

        self.status: list[list[int]] = [[0 for _ in range(LOGIC_HEIGHT)] for __ in range(LOGIC_WIDTH)]
        self.status[3][3] = 1
        self.status[3][4] = -1
        self.status[4][3] = -1
        self.status[4][4] = 1

        self.is_black_turn: bool = True

        self.possible_move_set: set[int] = set()

    def self_play(self):
        while True:
            self.screen.fill(colors.DEEP_GREY)
            self.draw_board()
            self.plot_stones()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.check_black_possible_move()
            self.mouse_move_respond()

            pygame.display.flip()

    def check_black_possible_move(self):
        target: int = 1
        enemy: int = -1
        if not self.is_black_turn:
            target = -1
            enemy = 1
        self.possible_move_set.clear()
        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] == target:
                    for direction in DIRECTIONS:
                        x_next = i + direction[0]
                        y_next = j + direction[1]
                        if not self.is_valid_cord(x_next, y_next):
                            continue
                        if self.status[x_next][y_next] != enemy:
                            continue
                        while (self.is_valid_cord(x_next, y_next) and
                               self.status[x_next][y_next] == enemy):
                            x_next = x_next + direction[0]
                            y_next = y_next + direction[1]
                        if self.status[x_next][y_next] == 0:
                            ind = y_next * LOGIC_WIDTH + x_next
                            self.possible_move_set.add(ind)




    def mouse_move_respond(self):
        x, y = pygame.mouse.get_pos()
        x_num = x // UNIT
        y_num = y // UNIT
        ind = y_num * LOGIC_WIDTH + x_num
        if ind in self.possible_move_set:
            if self.is_black_turn:
                self.plot_black_stone(x_num, y_num)
            else:
                self.plot_white_stone(x_num, y_num)

    @classmethod
    def is_valid_cord(cls, x: int, y: int) -> bool:
        return 0 <= x < LOGIC_WIDTH and 0 <= y < LOGIC_HEIGHT

    def draw_board(self):
        for i in range(BOARD_WIDTH_UNIT_NUM):
            for j in range(BOARD_HEIGHT_UNIT_NUM):
                left = i * UNIT + GAP
                top = j * UNIT + GAP
                width = UNIT - 2 * GAP
                height = UNIT - 2 * GAP
                rect = (left, top, width, height)
                pygame.draw.rect(self.screen, colors.LIGHT_GREY, rect, 0)

    def plot_stones(self):
        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] > 0:
                    self.plot_black_stone(i, j)
                elif self.status[i][j] < 0:
                    self.plot_white_stone(i, j)

    def plot_black_stone(self, x: int, y: int):
        pygame.draw.circle(self.screen, colors.BLACK,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           STONE_OUTER_RADIUS)

    def plot_white_stone(self, x: int, y: int):
        self.plot_black_stone(x, y)
        pygame.draw.circle(self.screen, colors.WHITE,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS)



