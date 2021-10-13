import random
from time import time
import numpy as np

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.model import State, Piece

from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        self.board = self.create_board_kosong()
        self.BARIS_BOARD = 6
        self.KOLOM_BOARD = 7
        self.PIECE_ROUND_BIRU = Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE)
        self.PIECE_ROUND_MERAH = Piece(ShapeConstant.CIRCLE, ColorConstant.RED)
        self.PIECE_CROSS_BIRU = Piece(ShapeConstant.CROSS, ColorConstant.BLUE)
        self.PIECE_CROSS_MERAH = Piece(ShapeConstant.CROSS, ColorConstant.RED)
        self.PIECE_KOSONG = Piece(ShapeConstant.BLANK, ColorConstant.BLACK)
        pass

    def create_board_kosong(self):
        board = np.zeros((6, 7))
        return board

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return None