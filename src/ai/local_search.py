import random
from time import time
import numpy as np

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.model import State, Piece, Board
from src.utility import place

from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        self.papan = Board(6,7)
        self.NUM_ROW = 6
        self.NUM_COL = 7
        # self.PIECE_ROUND_BIRU = Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE)
        # self.PIECE_ROUND_MERAH = Piece(ShapeConstant.CIRCLE, ColorConstant.RED)
        # self.PIECE_CROSS_BIRU = Piece(ShapeConstant.CROSS, ColorConstant.BLUE)
        # self.PIECE_CROSS_MERAH = Piece(ShapeConstant.CROSS, ColorConstant.RED)
        # self.PIECE_KOSONG = Piece(ShapeConstant.BLANK, ColorConstant.BLACK)
        pass

    # def create_board_kosong(self):
    #     board = np.zeros((6, 7))
    #     return board

    # def copy_board(self, state: State):
    #     for i in range (self.BARIS_BOARD):
    #         for j in range (self.KOLOM_BOARD):
    #             piece = state.board.__getItem__([i,j])
    #             place(state, n_player: int, piece.shape, piece.color)
    
    def get_row(self, board, col):
        for brs in range(self.board.row - 1, -1, -1):
            if self.board.__getitem__([brs, col]) == Piece(ShapeConstant.BLANK, ColorConstant.BLACK):
                return brs
        return -1

    def copy_board(self, board) -> Board:
        for i in range (self.papan.row):
            for j in range (self.papan.col):
                self.papan.set_piece(i, j, board.__getitem__([i, j]))

        return self.papan

    def generate_neighbour(self, state: State, thinking_time: float):
        n_player = state.round - 1 % 2
        player = state.players[n_player]
        neighbour_list = []
        
        for column in range(state.board.col):
            for shape,value in player.quota:
                if value> 0:
                    board = copy_board(state.board)
                    row = get_row(board,column)
                    piece = Piece(shape, player.color)
                    board.set_piece(row, column, piece)
                    score = evaluate(board, piece)
                    neighbour_list.append(board, score)
            
        return neighbour_list

    def hill_climbing(self, state: State, thinking_time: float) -> Tuple[str, str]:
        neighbour_list = generate_neighbour(state, thinking_time)        
        sorted(neighbour_list,key=lambda x: x[1])

        # return solusi
        return neighbour_list[0]
    
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

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return None