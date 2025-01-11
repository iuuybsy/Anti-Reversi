import pygame
import sys
import time

from reversi_logic import ReversiLogic
from reversi_plot import ReversiPlot
from stone_enum import Stone


class ReversiGame:
    def __init__(self):
        pygame.init()
        self.logic = ReversiLogic()
        self.plot_logic = ReversiPlot()

    def play(self):
        while True:
            self.plot_logic.game_render(self.logic.status, self.logic.last_move)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.logic.game_over():
                self.plot_logic.winner_judgement_plot(self.logic.status,
                                                      self.logic.is_black_turn)
                self.plot_logic.change_restart_color(self.logic.is_black_turn)
                left, _, _ = pygame.mouse.get_pressed()
                if left:
                    self.restart_click_respond()
            else:
                self.self_play_move_respond()
                left, _, _ = pygame.mouse.get_pressed()
                if left:
                    self.self_play_click_respond()

            pygame.display.flip()

    def restart_click_respond(self):
        """
        Click the restart button to restart the game
        :return: None
        """
        x_num, y_num = self.plot_logic.get_mouse_cord()
        if y_num == 5 and 2 <= x_num <= 5:
            self.logic.refresh()
            time.sleep(0.5)

    def self_play_move_respond(self):
        """
        Plot the possible moves for self play mode
        :return: None
        """
        x_num, y_num = self.plot_logic.get_mouse_cord()
        if len(self.logic.possible_moves) == 0:
            return
        ind = y_num * 8 + x_num
        stone_plot_func = self.plot_logic.plot_black_stone if self.logic.is_black_turn \
            else self.plot_logic.plot_white_stone
        dot_plot_func = self.plot_logic.plot_black_dot if self.logic.is_black_turn \
            else self.plot_logic.plot_white_dot
        if self.logic.status[x_num][y_num] == Stone.EMPTY:
            stone_plot_func(x_num, y_num)
            for x_temp, y_temp in self.logic.possible_moves[ind]:
                dot_plot_func(x_temp, y_temp)

    def self_play_click_respond(self):
        """
        Mouse click respond for self play mode
        :return: None
        """
        x_num, y_num = self.plot_logic.get_mouse_cord()
        ind = y_num * 8 + x_num
        if len(self.logic.possible_moves[ind]) > 0:
            is_black_turn_at_start: bool = self.logic.is_black_turn
            self.logic.set_stone(x_num, y_num)
            self.logic.is_black_turn = not self.logic.is_black_turn
            self.logic.check_possible_move()
            is_black_turn_at_end: bool = self.logic.is_black_turn

            self.logic.last_move[0] = x_num
            self.logic.last_move[1] = y_num

            if is_black_turn_at_start == is_black_turn_at_end:
                self.logic.check_possible_move()
                black_count: int = 0
                white_count: int = 0
                for i in range(8):
                    for j in range(8):
                        if self.logic.status[i][j] == Stone.BLACK:
                            black_count += 1
                        elif self.logic.status[i][j] == Stone.WHITE:
                            white_count += 1
                have_black_move, _ = self.logic.have_possible_move(is_black_turn=True)
                have_white_move, _ = self.logic.have_possible_move(is_black_turn=False)
                if not (have_black_move or have_white_move):
                    self.logic.is_end = True
                    self.logic.is_black_turn = black_count > white_count
