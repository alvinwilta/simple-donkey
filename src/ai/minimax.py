import random
from time import time

from src.constant import ShapeConstant, ColorConstant
from src.model import State

from typing import Tuple, List

class Minimax:
    def __init__(self):
        self.board = State.board

    def is_valid(self, board, kolom):
        return board[self.board.row - 1][kolom] == self.board.Piece(ShapeConstant.BLANK, ColorConstant.BLACK)

    def get_kolom_valid(self, board):
        sel_valid = []
        for kol in range(self.board.col):
            if is_valid(board, kol):
                sel_valid.append(kol)
        return sel_valid
        
    def taruh_piece(self, boardnya, row, col, piece):
        boardnya[row][col] = piece
    
    

    def get_baris_valid(self, board, kol):
        for bar in range(self.board.row):
            if board[bar][kol] == self.board.Piece(ShapeConstant.BLANK, ColorConstant.BLACK):
                return bar

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement
