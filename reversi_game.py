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
LOGIC_TOTAL = LOGIC_WIDTH * LOGIC_HEIGHT

STONE_OUTER_RADIUS: int = 25
STONE_INNER_RADIUS: int = 20
DOT_RADIUS: int = 8

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
        self.is_end: bool = False

        self.possible_moves: list[list[tuple[int, int]]] = [[] for _ in range(LOGIC_TOTAL)]
        self.check_possible_move()

    def self_play(self):
        while True:
            self.screen.fill(colors.DEEP_GREY)
            self.draw_board()
            self.plot_stones()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.is_end:
                self.plot_rect()
            else:
                self.mouse_move_respond()
                left, _, _ = pygame.mouse.get_pressed()
                if left:
                    self.click_respond()

            pygame.display.flip()

    def click_respond(self):
        x, y = pygame.mouse.get_pos()
        x_num = x // UNIT
        y_num = y // UNIT
        ind = y_num * LOGIC_WIDTH + x_num
        if len(self.possible_moves[ind]) > 0:
            is_black_turn_at_start: bool = self.is_black_turn
            self.set_stone(x_num, y_num)
            self.is_black_turn = not self.is_black_turn
            self.check_possible_move()
            is_black_turn_at_end: bool = self.is_black_turn
            if is_black_turn_at_start == is_black_turn_at_end:
                self.check_possible_move()
                black_count: int = 0
                white_count: int = 0
                for i in range(LOGIC_WIDTH):
                    for j in range(LOGIC_HEIGHT):
                        if self.status[i][j] == 0:
                            break
                        elif self.status[i][j] > 0:
                            black_count += 1
                        else:
                            white_count += 1
                if black_count + white_count == LOGIC_WIDTH * LOGIC_HEIGHT:
                    self.is_end = True
                    if black_count > white_count:
                        self.is_black_turn = True
                    else:
                        self.is_black_turn = False

    def set_stone(self, x_num: int, y_num: int):
        ind = y_num * LOGIC_WIDTH + x_num
        if self.is_black_turn:
            self.status[x_num][y_num] = 1
            for i in range(len(self.possible_moves[ind])):
                x_temp, y_temp = self.possible_moves[ind][i]
                self.status[x_temp][y_temp] = 1
        else:
            self.status[x_num][y_num] = -1
            for i in range(len(self.possible_moves[ind])):
                x_temp, y_temp = self.possible_moves[ind][i]
                self.status[x_temp][y_temp] = -1

    def check_possible_move(self):
        target: int = 1
        enemy: int = -1
        if not self.is_black_turn:
            target = -1
            enemy = 1
        self.possible_moves.clear()
        self.possible_moves = [[] for _ in range(LOGIC_TOTAL)]
        count: int = 0
        for i in range(LOGIC_WIDTH):
            for j in range(LOGIC_HEIGHT):
                if self.status[i][j] == target:
                    for direction in DIRECTIONS:
                        temp_rec = []
                        x_next = i + direction[0]
                        y_next = j + direction[1]
                        if not self.is_valid_cord(x_next, y_next):
                            continue
                        if self.status[x_next][y_next] != enemy:
                            continue
                        while (self.is_valid_cord(x_next, y_next) and
                               self.status[x_next][y_next] == enemy):
                            temp_rec.append((x_next, y_next))
                            x_next = x_next + direction[0]
                            y_next = y_next + direction[1]
                        if not self.is_valid_cord(x_next, y_next):
                            continue
                        if self.status[x_next][y_next] == 0:
                            ind = y_next * LOGIC_WIDTH + x_next
                            for cord_tuple in temp_rec:
                                self.possible_moves[ind].append(cord_tuple)
                            count += 1
        if count == 0:
            self.is_black_turn = not self.is_black_turn

    def mouse_move_respond(self):
        x, y = pygame.mouse.get_pos()
        x_num = x // UNIT
        y_num = y // UNIT
        ind = y_num * LOGIC_WIDTH + x_num
        if len(self.possible_moves[ind]) > 0:
            if self.is_black_turn:
                self.plot_black_stone(x_num, y_num)
                for i in range(len(self.possible_moves[ind])):
                    x_temp, y_temp = self.possible_moves[ind][i]
                    self.plot_black_dot(x_temp, y_temp)
            else:
                self.plot_white_stone(x_num, y_num)
                for i in range(len(self.possible_moves[ind])):
                    x_temp, y_temp = self.possible_moves[ind][i]
                    self.plot_white_dot(x_temp, y_temp)

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

    def plot_black_dot(self, x: int, y: int):
        pygame.draw.circle(self.screen, colors.BLACK,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           DOT_RADIUS)

    def plot_white_dot(self, x: int, y: int):
        pygame.draw.circle(self.screen, colors.WHITE,
                           (x * UNIT + MID_UNIT + 1,
                            y * UNIT + MID_UNIT + 1),
                           DOT_RADIUS)

    def plot_rect(self):
        rect_color = colors.BLACK if self.is_black_turn else colors.WHITE
        font_color = colors.WHITE if self.is_black_turn else colors.BLACK
        text_string = "Black Win!" if self.is_black_turn else "White Win!"

        pygame.draw.rect(self.screen, rect_color,
                         (UNIT, 3 * UNIT,
                          6 * UNIT, 2 * UNIT),
                         border_radius=10)
        font = pygame.font.SysFont("Century", 50)
        text = font.render(text_string, False, font_color)
        text_width = text.get_width()
        text_height = text.get_height()
        x_pix = BOARD_WIDTH // 2 - text_width // 2
        y_pix = BOARD_HEIGHT // 2 - text_height // 2
        self.screen.blit(text, (x_pix, y_pix))
