import random
from time import time
import numpy as np
import math

from src.constant import ShapeConstant, ColorConstant
from src.model import State, Piece

from typing import Tuple, List

class Minimax:
    def __init__(self):
        self.BARIS_BOARD = 6
        self.KOLOM_BOARD = 7
        self.PIECE_ROUND_BIRU = Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE)
        self.PIECE_ROUND_MERAH = Piece(ShapeConstant.CIRCLE, ColorConstant.RED)
        self.PIECE_CROSS_BIRU = Piece(ShapeConstant.CROSS, ColorConstant.BLUE)
        self.PIECE_CROSS_MERAH = Piece(ShapeConstant.CROSS, ColorConstant.RED)
        self.PIECE_KOSONG = Piece(ShapeConstant.BLANK, ColorConstant.BLACK)
        pass

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

    def is_valid(self, board, kolom):
        return board[self.BARIS_BOARD - 1, kolom] == self.PIECE_KOSONG

    def get_kolom_valid(self, board):
        sel_valid = []
        for kol in range(self.BARIS_BOARD):
            if self.is_valid(board, kol):
                sel_valid.append(kol)
        return sel_valid
        
    def taruh_piece(self, boardnya, row, col, piece):
        boardnya[row,col] = piece
    
    def get_baris_valid(self, board, kol):
        for bar in range(self.BARIS_BOARD):
            if board[bar,kol] == Piece(ShapeConstant.BLANK, ColorConstant.BLACK):
                return bar

    # Check to see if the game has been won
    def winning_move(self, board, piece):
        # Check valid horizontal locations for win
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD):
                if board[r,c] == piece and board [r,c+1] == piece and board[r,c+2] == piece and board[r,c+3] == piece:
                    return True

        # Check valid vertical locations for win
        for c in range(self.KOLOM_BOARD):
            for r in range(self.BARIS_BOARD-3):
                if board[r,c] == piece and board [r+1,c] == piece and board[r+2,c] == piece and board[r+3,c] == piece:
                    return True

        # Check valid positive diagonal locations for win
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD-3):
                if board[r,c] == piece and board [r+1,c+1] == piece and board[r+2,c+2] == piece and board[r+3,c+3] == piece:
                    return True

        # check valid negative diagonal locations for win
        for c in range(self.KOLOM_BOARD-3):
            for r in range(3, self.BARIS_BOARD):
                if board[r,c] == piece and board [r-1,c+1] == piece and board[r-2,c+2] == piece and board[r-3,c+3] == piece:
                    return True

    def evaluate_window(self, window, piece, jenis):
        score = 0
        # Switch scoring based on turn
        #opp_piece = PLAYER_PIECE
        if jenis == "bentuk":
            opp_piece = self.PIECE_KOSONG

        # Prioritise a winning move
        # Minimax makes this less important
        #if window.count(piece) == 4:
         #   score += 100
        # Make connecting 3 second priority
        elif window.count(piece) == 3 and window.count(self.PIECE_KOSONG) == 1:
            score += 5
        # Make connecting 2 third priority
        elif window.count(piece) == 2 and window.count(self.PIECE_KOSONG) == 2:
            score += 2
        # Prioritise blocking an opponent's winning move (but not over bot winning)
        # Minimax makes this less important
        #if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
         #   score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        # Score centre column
        centre_array = [int(i) for i in list(board[:, self.BARIS_BOARD // 2])]
        centre_count = centre_array.count(piece)
        score += centre_count * 3

        # Score horizontal positions
        for r in range(self.BARIS_BOARD):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.BARIS_BOARD - 3):
                # Create a horizontal window of 4
                window = row_array[c:c + 4]
                score += self.evaluate_window(self, window, piece)

        # Score vertical positions
        for c in range(self.BARIS_BOARD):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.BARIS_BOARD - 3):
                # Create a vertical window of 4
                window = col_array[r:r + 4]
                score += self.evaluate_window(self, window, piece)

        # Score positive diagonals
        for r in range(self.BARIS_BOARD - 3):
            for c in range(self.BARIS_BOARD - 3):
                # Create a positive diagonal window of 4
                window = [board[r + i, c + i] for i in range(4)]
                score += self.evaluate_window(self, window, piece)

        # Score negative diagonals
        for r in range(self.BARIS_BOARD - 3):
            for c in range(self.BARIS_BOARD - 3):
                # Create a negative diagonal window of 4
                window = [board[r + 3 - i, c + i] for i in range(4)]
                score += self.evaluate_window(self, window, piece)
        return score

    # Pick the best move by looking at all possible future moves and comparing their scores
    def minimax(self, board, depth, alpha, beta, maximisingPlayer):
        valid_locations = self.get_kolom_valid(board)

        is_terminal = self.winning_move(board, self.PIECE_CROSS_BIRU)\
                        or self.winning_move(board, self.PIECE_ROUND_BIRU)\
                        or self.winning_move(board, self.PIECE_CROSS_MERAH)\
                        or self.winning_move(board, self.PIECE_ROUND_MERAH)\
                        or len(valid_locations) == 0
        #is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                # Weight the bot winning really high
                if self.winning_move(board, BOT_PIECE):
                    return (None, 10000000)
                # Weight the human winning really low
                elif self.winning_move(board, PLAYER_PIECE):
                    return (None, -10000000)
                else: # No more valid moves
                    return (None, 0)
            # Return the bot's score
            else:
                return (None, score_position(board, BOT_PIECE))

        if maximisingPlayer:
            value = -math.inf
            # Randomise column to start
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_baris_valid(board, col)
                # Create a copy of the board
                b_copy = board.copy()
                # Drop a piece in the temporary board and record score
                self.taruh_piece(b_copy, row, col, BOT_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimising player
            value = math.inf
            # Randomise column to start
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_baris_valid(board, col)
                # Create a copy of the board
                b_copy = board.copy()
                # Drop a piece in the temporary board and record score
                self.taruh_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


    def Solusi(self, state, n_player, thinking_time):
        return self.minimax(state.board, 4, -math.inf, math.inf, True)
        #return (random.randint(0, state.self.BARIS_BOARD), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        print("n_player", n_player)

        best_movement = self.Solusi(state, n_player, thinking_time) #minimax algorithm
        return best_movement
