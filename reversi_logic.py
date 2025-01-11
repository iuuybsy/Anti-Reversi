from stone_enum import Stone

LOGIC_WIDTH: int = 8
LOGIC_HEIGHT: int = 8
LOGIC_TOTAL = LOGIC_WIDTH * LOGIC_HEIGHT

DIRECTIONS: list[list[int]] = [[1, 0], [1, 1], [0, 1], [-1, 1],
                               [-1, 0], [-1, -1], [0, -1], [1, -1]]


def is_valid_cord(x: int, y: int) -> bool:
    """
    Check if the cord is valid
    :param x: cord of x-axis
    :param y: cord of y-axis
    :return: flag to see if the cord is valid
    """
    return 0 <= x < LOGIC_WIDTH and 0 <= y < LOGIC_HEIGHT


class ReversiLogic:
    def __init__(self):
        self.status: list[list[Stone]] = \
            [[Stone.EMPTY for _ in range(LOGIC_HEIGHT)] for __ in range(LOGIC_WIDTH)]
        self.status[3][3] = Stone.BLACK
        self.status[3][4] = Stone.WHITE
        self.status[4][3] = Stone.WHITE
        self.status[4][4] = Stone.BLACK

        self.is_black_turn: bool = True
        self.is_end: bool = False

        self.last_move: list[int] = [-1, -1]

        self.possible_moves: list[list[tuple[int, int]]] = [[] for _ in range(LOGIC_TOTAL)]
        self.check_possible_move()

    def game_over(self):
        return self.is_end

    def set_stone(self, x_num: int, y_num: int):
        """
        Set the stone and the stones that can be flipped
        :param x_num: cord of x-axis
        :param y_num: cord of y-axis
        :return: None
        """
        ind = y_num * LOGIC_WIDTH + x_num
        stone_sign = Stone.BLACK if self.is_black_turn else Stone.WHITE
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
        target: Stone = Stone.BLACK if is_black_turn else Stone.WHITE
        enemy: Stone = Stone.WHITE if is_black_turn else Stone.BLACK
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
                        if self.status[x_next][y_next] == Stone.EMPTY:
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

    def refresh(self):
        self.status = [[Stone.EMPTY for _ in range(LOGIC_HEIGHT)] for __ in range(LOGIC_WIDTH)]
        self.status[3][3] = Stone.BLACK
        self.status[3][4] = Stone.WHITE
        self.status[4][3] = Stone.WHITE
        self.status[4][4] = Stone.BLACK

        self.is_black_turn: bool = True
        self.is_end: bool = False

        self.last_move = [-1, -1]

        self.possible_moves = [[] for _ in range(LOGIC_TOTAL)]
        self.check_possible_move()
