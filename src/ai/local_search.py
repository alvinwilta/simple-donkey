import random
from time import time
import numpy as np

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.utility import is_out
from src.model import State, Piece, Board
import multiprocessing

from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        self.papan = Board(6,7)
        self.NUM_ROW = 6
        self.NUM_COL = 7
        pass
    
    def get_row(self, board, col):
        for brs in range(self.papan.row - 1, -1, -1):
            if self.papan.__getitem__([brs, col]) == Piece(ShapeConstant.BLANK, ColorConstant.BLACK):
                return brs
        return -1

    def copy_board(self, board) -> Board:
        for i in range (self.papan.row):
            for j in range (self.papan.col):
                self.papan.set_piece(i, j, board.__getitem__([i, j]))

        return self.papan

    def generate_neighbour(self, state: State, thinking_time: float):
        n_player = (state.round - 1) % 2
        player = state.players[n_player]
        neighbour_list = []
        
        for column in range(state.board.col):
            for shape,value in player.quota.items():
                if value> 0:
                    board = self.copy_board(state.board)
                    row = self.get_row(board,column)
                    piece = Piece(shape, player.color)
                    board.set_piece(row, column, piece)
                    score = self.evaluate_board(board)
                    neighbour_list.append([(column, piece.shape), score])

        return neighbour_list

    def hill_climbing(self, state: State, thinking_time: float, result):
        neighbour_list = self.generate_neighbour(state, thinking_time)
        # value = evaluate_board(state.board)

        current = neighbour_list[random.randint(0, len(neighbour_list)-1)]
        neighbour_list.sort(reverse=True, key=lambda x: x[1])

        for neighbour in neighbour_list:
            if neighbour[1] <= current[1]:
                # Jika score lebih baik dari current
                result.put(current)
            current = neighbour

    # ngetest: aas
    def evaluate_board(self, board: Board):
        streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        scores = {0}
        for row in range(self.NUM_ROW):
            for col in range(self.NUM_COL):
                piece = board[row, col]
                if piece.shape != ShapeConstant.BLANK:
                    for prior in GameConstant.WIN_PRIOR:
                        for row_ax, col_ax in streak_way:
                            mark = 1
                            row_ = row + row_ax
                            col_ = col + col_ax
                            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                                if is_out(board, row_, col_):
                                    break

                                shape_condition = (
                                    prior == GameConstant.SHAPE
                                    and piece.shape != board[row_, col_].shape)
                                color_condition = (
                                    prior == GameConstant.COLOR
                                    and piece.color != board[row_, col_].color)
                                if shape_condition or color_condition:
                                    break

                                row_ += row_ax
                                col_ += col_ax
                                mark += 1
                                if mark == 4: return mark
                            scores.add(mark)

        scores_list = list(scores)
        scores_list.sort(reverse = True)
        return scores_list[0]

    def count_different_piece(self, arr, p1, p2):
        return (arr.count(p1) + arr.count(p2))

    def eval_help(self, board, piece):
        score = 0

        if piece is int:
            if board.count(piece) == 3 and board.count(0) == 1:
                score += 5
            elif board.count(piece) == 2 and board.count(0) == 2:
                score += 2
        elif piece is list:
            if self.count_different_piece(board, piece[0], piece[1]) == 3 and board.count(0) == 1:
                score += 5
            elif self.count_different_piece(board, piece[0], piece[1]) == 2 and board.count(0) == 2:
                score += 2
                
        return score

    def evaluate(self, board, piece):
        score = 0

        # horizontal
        for r in range(self.NUM_ROW-1, -1, -1):
            row_arr = [int(i) for i in list(board[r, :])]
            for c in range(self.NUM_COL-3):
                area = row_arr[c:c+4]
                score += self.eval_help(area, piece)

        # vertikal
        for r in range(self.NUM_COL):
            col_arr = [int(i) for i in list(board[:, c])]
            for r in range(self.NUM_ROW-1, self.NUM_ROW-4, -1):
                area = row_arr[r:r-4]
                score += self.eval_help(area, piece)

        # serong kiri
        for r in range(self.NUM_ROW-1, self.NUM_ROW-4, -1):
            for c in range(self.NUM_COL-3):
                area = [board[r-3+i, c+i] for i in range(4)]
                score += self.eval_help(area, piece)

        # serong kanan
        for r in range(self.NUM_ROW-1, self.NUM_ROW-5, -1):
            for c in range(self.NUM_COL-3):
                area = [board[r-i, c+i] for i in range(4)]
                score += self.eval_help(area, piece)
        
        return score
        
    def find(self, state: State, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        result = multiprocessing.Queue()
        p = multiprocessing.Process(target=self.hill_climbing, args=(state, thinking_time, result))
        p.start()
        #Timeout 3 detik
        p.join(timeout=3)

        # Kirim signal supaya stop event setelah 3 detik
        p.terminate()

        if result.qsize() != 0:
            return result.get(0)
        else:
            return (random.randint(0, state.board.col-1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))