import random
from time import time
import numpy as np
import math

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.model import State, Piece
import multiprocessing

from typing import Tuple, List

class Minimax:
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

    def is_valid(self, board, kolom):
        return board[0, kolom] == 0

    def get_kolom_valid(self, board):
        sel_valid = []
        for kol in range(self.KOLOM_BOARD):
            if self.is_valid(board, kol):
                sel_valid.append(kol)
        return sel_valid
        
    def taruh_piece(self, boardnya, row, col, piece):
        boardnya[row,col] = piece
    
    def get_baris_valid(self, board, kol):
        for bar in range(self.BARIS_BOARD - 1, -1, -1):
            if board[bar,kol] == 0:
                return bar

    # Mengecek apabila ada langkah kemenangan dengan pion yang sama persis
    def winning_move(self, board, piece):
        # Check valid horizontal locations for win
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD):
                if board[r,c] == piece and board [r,c+1] == piece and board[r,c+2] == piece and board[r,c+3] == piece:
                    #print("horizontal win")
                    return True

        # Check valid vertical locations for win
        for c in range(self.KOLOM_BOARD):
            for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                if board[r,c] == piece and board[r-1,c] == piece and board[r-2,c] == piece and board[r-3,c] == piece:
                    #print(piece, "vertical win")
                    return True

        # Check valid positive diagonal locations for win
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                if board[r,c] == piece and board [r-1,c+1] == piece and board[r-2,c+2] == piece and board[r-3,c+3] == piece:
                    #print("diagonal positif win")
                    return True

        # check valid negative diagonal locations for win
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD-6, self.BARIS_BOARD-4):
                if board[r,c] == piece and board [r+1,c+1] == piece and board[r+2,c+2] == piece and board[r+3,c+3] == piece:
                    #print(("diagonal negatif win"))
                    return True

    #Mengecek apabila ada kemenangan yang dikarenakan warna yang sama atau shape yang sama
    def winning_by_element(self, board, piece):
        #print("piece dalam wbe",piece)
        if (type(piece) is list):
            #print("piecenya list:",type(piece) is list)
            for c in range(self.KOLOM_BOARD-3):
                for r in range(self.BARIS_BOARD):
                    if (board[r,c] in piece) and (board [r,c+1] in piece) and (board[r,c+2] in piece) and (board[r,c+3] in piece):
                        print("horizontal win",piece)
                        return True

            # Check valid vertical locations for win
            for c in range(self.KOLOM_BOARD):
                for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                    if (board[r,c] in piece) and (board[r-1,c] in piece) and (board[r-2,c] in piece) and (board[r-3,c] in piece):
                        # print(board[r,c])
                        # print(board[r-1,c])
                        # print(board[r-2,c])
                        # print(board[r-3,c])
                        print("vertical win",piece)
                        return True

            # Check valid positive diagonal locations for win
            for c in range(self.KOLOM_BOARD-3):
                for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                    if (board[r,c] in piece) and (board [r-1,c+1] in piece) and (board[r-2,c+2] in piece) and (board[r-3,c+3] in piece):
                        print("diagonal positif win", piece)
                        return True

            # check valid negative diagonal locations for win
            for c in range(self.KOLOM_BOARD-3):
                for r in range(self.BARIS_BOARD-6, self.BARIS_BOARD-4):
                    if (board[r,c] in piece) and (board [r+1,c+1] in piece) and (board[r+2,c+2] in piece) and (board[r+3,c+3] in piece):
                        print(("diagonal negatif win"),piece)
                        return True
        else:
            return False

    def evaluate_window(self, window, piece):
        score = 0
        if piece is list:
            # Prioritaskan 3 piece terurut
            if self.hitung_element_beda(window,piece[0], piece[1]) == 3 \
                and window.count(0) == 1:
                score += 5
            # Prioritaskan 2 piece terurut
            elif self.hitung_element_beda(window,piece[0], piece[1]) == 2 \
                and window.count(0) == 2:
                score += 2
        elif piece is int:
            # Prioritaskan 3 piece terurut
            if window.count(piece) == 3 and window.count(0) == 1:
                score += 5
            # Prioritaskan 2 piece terurut
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2
        return score

    def hitung_element_beda(self, senarai, element1, element2):
        return (senarai.count(element1) + senarai.count(element2))

    def score_position(self, board, piece):
        score = 0

        # Score centre column
        if (type(piece) is int):
            #print("piecenya integer")
            centre_array = [int(i) for i in list(board[:, self.KOLOM_BOARD // 2])]
            centre_count = centre_array.count(piece)
            score += centre_count * 3

        # Score horizontal positions
        for r in range(self.BARIS_BOARD-1, -1, -1):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.KOLOM_BOARD - 3):
                # Create a horizontal window of 4
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score vertical positions
        for c in range(self.KOLOM_BOARD):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-4, -1):
                # Create a vertical window of 4
                window = col_array[r:r - 4]
                score += self.evaluate_window(window, piece)

        # Score positive diagonals
        for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
            for c in range(self.KOLOM_BOARD-3):
                #Diagonal positif sebesar 4
                window = [board[r-i, c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        

        # Score negative diagonals
        for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-4, -1):
            for c in range(self.KOLOM_BOARD-3):
                # Create a negative diagonal window of 4
                window = [board[r - 3 + i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        return score

    # Pick the best move by looking at all possible future moves and comparing their scores
    def minimax(self, board, depth, alpha, beta, maximisingPlayer, piece):
        valid_locations = self.get_kolom_valid(board)
        #print("valid_location",valid_locations)
        is_terminal = self.winning_move(board, 1) \
                        or self.winning_move(board, 2) \
                        or self.winning_move(board, 3) \
                        or self.winning_move(board, 4) \
                        or self.winning_by_element(board, [1,4]) \
                        or self.winning_by_element(board, [2,3]) \
                        or self.winning_by_element(board, [1,2]) \
                        or self.winning_by_element(board, [3,4]) \
                        or len(valid_locations) == 0
        #is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if ((self.winning_move(board, 1)) \
                    or (self.winning_move(board, 4))) \
                    or (self.winning_by_element(board, [1,4])) \
                    or (self.winning_by_element(board, [1,2])) :
                # Weight the bot winning really high
                    #print("self.winning_move(board, 3) or self.winning_move(board, 2)")
                    # print("Menang karena winning move 3:",self.winning_move(board, 3))
                    # print("Menang karena winning move 2:",self.winning_move(board, 2))
                    # print("Menang karena winning by element [2,3]:", self.winning_by_element(board, [2,3]))
                    # print("Menang karena winning by element [3,4]:", self.winning_by_element(board, [3,4]))
                    return (None, 10000000)
                
                # Weight the human winning really low
                elif ((self.winning_move(board, 3)) \
                    or (self.winning_move(board, 2))) \
                    or (self.winning_by_element(board, [2,3])) \
                    or (self.winning_by_element(board, [3,4])):
                    #print("self.winning_move(board, 1) or self.winning_move(board, 4)")
                    # if(self.winning_by_element(board, [1,4])):
                    #     print("self.winning_by_element(board, [1,4])", self.winning_by_element(board, [1, 4]))
                    # if(self.winning_by_element(board, [1,2])):
                    #     print("self.winning_by_element(board, [1,2])",self.winning_by_element(board, [1,2]))
                    return (None, -10000000)
                else: # No more valid moves
                    #print("No valid moves")
                    return (None, 0)
            # Return the bot's score
            else:
                if(piece == self.player.shape):
                    return (None, \
                        self.score_position(board, 1) \
                        + self.score_position(board, 4)\
                        + self.score_position(board, [1,4]) \
                        + self.score_position(board, [1,2]))
                else:
                    return (None, \
                        self.score_position(board, 3) \
                        + self.score_position(board, 2)\
                        + self.score_position(board, [2,3]) \
                        + self.score_position(board, [3,4]))

        if maximisingPlayer:
            value = -math.inf
            # Randomise column to start
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_baris_valid(board, col)
                # Create a copy of the board
                b_copy = board.copy()
                # Drop a piece in the temporary board and record score
                if (piece == self.player.shape):
                    self.taruh_piece(b_copy, row, col, 1)
                else:
                    self.taruh_piece(b_copy, row, col, 2)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False, piece)[1]
                #print("score di max, kol:", new_score, col)
                #print(b_copy)
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
                if (piece == self.player.shape):
                    self.taruh_piece(b_copy, row, col, 3)
                else:
                    self.taruh_piece(b_copy, row, col, 4)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True, piece)[1]
                #print("score di min, kol:", new_score, col)
                #print(b_copy)
                if new_score < value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
    
    def salin_board_dari_state(self, board_asli, n_player):
        player_color = GameConstant.PLAYER_COLOR[n_player]
        if n_player == 0:
            player_shape = GameConstant.PLAYER1_SHAPE
            enemy_color = GameConstant.PLAYER2_COLOR
            enemy_shape = GameConstant.PLAYER2_SHAPE
        else:
            player_shape = GameConstant.PLAYER2_SHAPE
            enemy_color = GameConstant.PLAYER1_COLOR
            enemy_shape = GameConstant.PLAYER1_SHAPE
        for i in range (self.BARIS_BOARD):
            for j in range (self.KOLOM_BOARD):
                if(board_asli[i, j] == self.PIECE_KOSONG):
                    self.board[i, j] = 0
                elif(board_asli[i, j] == Piece(player_shape, player_color)):
                    self.board[i, j] = 1
                elif(board_asli[i, j] == Piece(player_shape, enemy_color)):
                    self.board[i, j] = 2
                elif(board_asli[i, j] == Piece(enemy_shape, enemy_color)):
                    self.board[i, j] = 3
                elif(board_asli[i, j] == Piece(enemy_shape, player_color)):
                    self.board[i, j] = 4
                else:
                    self.board[i, j] = 0
        self.piece_player = [1, 4]
        self.piece_enemy = [3, 2]
        return self.board

    def Solusi(self, state, n_player, thinking_time, queue):
        self.board = self.salin_board_dari_state(state.board, n_player)
        self.player = state.players[n_player]
        if(n_player == 1):
            self.enemy = state.players[0]
        else:
            self.enemy = state.players[1]
        #print(self.board)
        if(self.player.quota[self.player.shape] > 0):
            kolomnya, scorenya = self.minimax(self.board, 4, -math.inf, math.inf, True, self.player.shape)
            #print("kolomnya, shape = ",kolomnya,self.player.shape)
            queue.put(kolomnya)
            queue.put(self.player.shape)
            #return queue
        else:
            kolomnya, scorenya = self.minimax(self.board, 4, -math.inf, math.inf, True, self.enemy.shape)
            #print("kolomnya, shape = ",kolomnya,self.player.shape)
            queue.put(kolomnya)
            queue.put(self.enemy.shape)
            #return kolomnya, self.enemy.shape
        #return (random.randint(0, state.self.BARIS_BOARD), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        queue = multiprocessing.Queue()
        action_process = multiprocessing.Process(target=self.Solusi, args=(state, n_player, thinking_time, queue,))
        action_process.start()
        #Timeout 3 detik
        action_process.join(timeout=3)

        # We send a signal that the other thread should stop.
        action_process.terminate()
        
        #waktu habis, random saja
        if queue.qsize() == 0:
            return (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        #best_movement = self.Solusi(state, n_player, thinking_time) #minimax algorithm
        else:
            a = queue.get(0)
            b = queue.get(0)
            print(a,b)
            if (a == None):
                return (random.randint(0, state.board.col), b)
            return a,b
