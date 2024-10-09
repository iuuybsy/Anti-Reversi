import pygame
import colors
import sys


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


class ReversiGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.status: list[list[int]] = [[0 for _ in range(LOGIC_HEIGHT)] for __ in range(LOGIC_WIDTH)]
        self.status[3][3] = 1
        self.status[3][4] = -1
        self.status[4][3] = -1
        self.status[4][4] = 1

    def self_play(self):
        while True:
            self.screen.fill(colors.DEEP_GREY)
            self.draw_board()
            self.set_stones()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.flip()

    def draw_board(self):
        for i in range(BOARD_WIDTH_UNIT_NUM):
            for j in range(BOARD_HEIGHT_UNIT_NUM):
                left = i * UNIT + GAP
                top = j * UNIT + GAP
                width = UNIT - 2 * GAP
                height = UNIT - 2 * GAP
                rect = (left, top, width, height)
                pygame.draw.rect(self.screen, colors.LIGHT_GREY, rect, 0)

    def set_stones(self):
        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] > 0:
                    self.set_black_stone(i, j)
                elif self.status[i][j] < 0:
                    self.set_white_stone(i, j)

    def set_black_stone(self, x: int, y: int):
        pygame.draw.circle(self.screen, colors.BLACK,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           STONE_OUTER_RADIUS)

    def set_white_stone(self, x: int, y: int):
        self.set_black_stone(x, y)
        pygame.draw.circle(self.screen, colors.WHITE,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS)



