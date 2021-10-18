import random
from time import time
import numpy as np
import math

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.model import State, Piece
import multiprocessing

from typing import Tuple, List

class MinimaxGroup15:
    def __init__(self):
        pass

    def create_board_kosong(self):
        #Membuat board kosong
        board = np.zeros((6, 7))
        return board

    def is_valid(self, board, kolom):
        #Mengecek apakah suatu kolom sudah penuh atau belum
        return board[0, kolom] == 0

    def get_kolom_valid(self, board):
        #Mengembalikan array of kolom yang masih bisa diisi piece
        sel_valid = []
        for kol in range(self.KOLOM_BOARD):
            if self.is_valid(board, kol):
                sel_valid.append(kol)
        return sel_valid
        
    def taruh_piece(self, boardnya, row, col, piece):
        #Menaruh piece pada sebuah board (bisa board real atau board jadi-jadian)
        boardnya[row,col] = piece
    
    def get_baris_valid(self, board, kol):
        #Mendapatkan Baris paling bawah dari suatu kolom yang kosong untuk diisi 
        for bar in range(self.BARIS_BOARD - 1, -1, -1):
            if board[bar,kol] == 0:
                return bar

    def winning_move(self, board, piece):
        # Mengecek apabila ada langkah kemenangan dengan piece yang sama persis
    
        # Mengecek secara horizontal apakah ada kemenangan atau tidak
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD):
                if board[r,c] == piece and board [r,c+1] == piece and board[r,c+2] == piece and board[r,c+3] == piece:
                    return True

        # Mengecek secara vertikal apakah ada kemenangan atau tidak
        for c in range(self.KOLOM_BOARD):
            for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                if board[r,c] == piece and board[r-1,c] == piece and board[r-2,c] == piece and board[r-3,c] == piece:
                    return True

        # Mengecek secara diagonal positif apakah ada kemenangan atau tidak
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                if board[r,c] == piece and board [r-1,c+1] == piece and board[r-2,c+2] == piece and board[r-3,c+3] == piece:
                    return True

        # Mengecek secara diagonal negatif apakah ada kemenangan atau tidak
        for c in range(self.KOLOM_BOARD-3):
            for r in range(self.BARIS_BOARD-6, self.BARIS_BOARD-4):
                if board[r,c] == piece and board [r+1,c+1] == piece and board[r+2,c+2] == piece and board[r+3,c+3] == piece:
                    return True

    def winning_by_element(self, board, piece):
        #Mengecek apabila ada kemenangan yang dikarenakan warna piece yang sama atau shape piece yang sama

        if (type(piece) is list): #cek apakah piece berbentuk list?
            # Mengecek secara horizontal apakah ada kemenangan atau tidak
            for c in range(self.KOLOM_BOARD-3):
                for r in range(self.BARIS_BOARD):
                    if (board[r,c] in piece) and (board [r,c+1] in piece) and (board[r,c+2] in piece) and (board[r,c+3] in piece):
                        return True

            # Mengecek secara vertikal apakah ada kemenangan atau tidak
            for c in range(self.KOLOM_BOARD):
                for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                    if (board[r,c] in piece) and (board[r-1,c] in piece) and (board[r-2,c] in piece) and (board[r-3,c] in piece):
                        return True

            # Mengecek secara diagonal positif apakah ada kemenangan atau tidak
            for c in range(self.KOLOM_BOARD-3):
                for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
                    if (board[r,c] in piece) and (board [r-1,c+1] in piece) and (board[r-2,c+2] in piece) and (board[r-3,c+3] in piece):
                        return True

            # Mengecek secara diagonal negatif apakah ada kemenangan atau tidak
            for c in range(self.KOLOM_BOARD-3):
                for r in range(self.BARIS_BOARD-6, self.BARIS_BOARD-4):
                    if (board[r,c] in piece) and (board [r+1,c+1] in piece) and (board[r+2,c+2] in piece) and (board[r+3,c+3] in piece):
                        return True
        else:
            return False

    def evaluate_window(self, window, piece):
        # Mengevaluasi setiap window yang dicek, untuk menghitung scorenya
        score = 0
        if (type(piece) is list): #piece berbentuk list
            # Prioritaskan 3 piece terurut
            if self.hitung_element_beda(window,piece[0], piece[1]) == 3 \
                and window.count(0) == 1:
                score += 5
            # Prioritaskan 2 piece terurut
            elif self.hitung_element_beda(window,piece[0], piece[1]) == 2 \
                and window.count(0) == 2:
                score += 2
        elif (type(piece) is int): #piece berbentuk int
            # Prioritaskan 3 piece terurut
            if window.count(piece) == 3 and window.count(0) == 1:
                score += 5
            # Prioritaskan 2 piece terurut
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2
        return score

    def hitung_element_beda(self, senarai, element1, element2):
        #Menghitung jumlah piece yang berbeda, tetapi secara lojik sama
        return (senarai.count(element1) + senarai.count(element2))

    def score_position(self, board, piece):
        #Menghitung posisi pada board
        score = 0

        # Utamakan piece dimasukkan pada kolom tengah
        if (type(piece) is int):
            centre_array = [int(i) for i in list(board[:, self.KOLOM_BOARD // 2])]
            centre_count = centre_array.count(piece)
            #Apabila ada piece yang akan ditaruh disini, score dikali 8
            score += centre_count * 3

        # Menilai posisi horizontal
        for r in range(self.BARIS_BOARD-1, -1, -1):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.KOLOM_BOARD - 3):
                # Membuat window horizontal berukuran 4
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Menilai posisi vertikal
        for c in range(self.KOLOM_BOARD):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-4, -1):
                # Membuat window vertikal berukuran 4
                window = col_array[r:r - 4]
                score += self.evaluate_window(window, piece)

        # Menilai posisi diagonal positif
        for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-5, -1):
            for c in range(self.KOLOM_BOARD-3):
                # Membuat window diagonal positif berukuran 4
                window = [board[r-i, c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        
        # Menilai posisi diagonal negatif
        for r in range(self.BARIS_BOARD-1, self.BARIS_BOARD-4, -1):
            for c in range(self.KOLOM_BOARD-3):
                # Membuat window diagonal negatif berukuran 4
                window = [board[r - 3 + i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        return score
    #Fungsi Utama
    def minimax(self, board, depth, alpha, beta, maximisingPlayer, piece):
        valid_locations = self.get_kolom_valid(board)
        #Fungsi Terminal terjadi apabila ada kondisi yang membuat pertandingan selesai
        is_terminal = self.winning_move(board, 1) \
                        or self.winning_move(board, 2) \
                        or self.winning_move(board, 3) \
                        or self.winning_move(board, 4) \
                        or self.winning_by_element(board, [1,4]) \
                        or self.winning_by_element(board, [2,3]) \
                        or self.winning_by_element(board, [1,2]) \
                        or self.winning_by_element(board, [3,4]) \
                        or len(valid_locations) == 0
        if depth == 0 or is_terminal:
            if is_terminal:
                #Yang menang kita
                if ((self.winning_move(board, 1)) \
                    or (self.winning_move(board, 4)) \
                    or (self.winning_by_element(board, [1,4])) \
                    or (self.winning_by_element(board, [1,2]))) :
                    return (None, 10000000) #nilai jadi sangat besar
                #Yang menang lawan
                elif ((self.winning_move(board, 3)) \
                    or (self.winning_move(board, 2)) \
                    or (self.winning_by_element(board, [2,3])) \
                    or (self.winning_by_element(board, [3,4]))):
                    return (None, -10000000) #nilai jadi sangat kecil
                else:
                    return (None, 0)
            
            else:
                #Mengembalikan penilaian kondisi board saat ini
                #Untuk depth teratas, score semakin besar
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
            #Inisiasi kolomnya dulu supaya tidak null
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_baris_valid(board, col)
                # Membuat copy board
                b_copy = board.copy()
                # Taruh piece di board jadi-jadian dan nilai kondisi sekarang
                if (piece == self.player.shape):
                    self.taruh_piece(b_copy, row, col, 1)
                else:
                    self.taruh_piece(b_copy, row, col, 2)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False, piece)[1]
                if new_score > value:
                    value = new_score
                    # Kolom diganti dengan nilai terbaik
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimising player
            value = math.inf
            #Inisiasi kolomnya dulu supaya tidak null
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_baris_valid(board, col)
                # Create a copy of the board
                b_copy = board.copy()
                # Taruh piece di board jadi-jadian dan nilai kondisi sekarang
                if (piece == self.player.shape):
                    self.taruh_piece(b_copy, row, col, 3)
                else:
                    self.taruh_piece(b_copy, row, col, 4)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True, piece)[1]
                if new_score < value:
                    value = new_score
                    # Kolom diganti dengan nilai terbaik
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
    
    def salin_board_dari_state(self, board_asli, n_player):
        board = self.create_board_kosong()
        player_color = GameConstant.PLAYER_COLOR[n_player]
        if n_player == 0:
            #Apabila giliran pertama, jadikan piece kita property player 1
            player_shape = GameConstant.PLAYER1_SHAPE
            enemy_color = GameConstant.PLAYER2_COLOR
            enemy_shape = GameConstant.PLAYER2_SHAPE
        else: #n_player = 1
            #Apabila giliran kedua, jadikan piece kita property player 2
            player_shape = GameConstant.PLAYER2_SHAPE
            enemy_color = GameConstant.PLAYER1_COLOR
            enemy_shape = GameConstant.PLAYER1_SHAPE
        for i in range (self.BARIS_BOARD):
            for j in range (self.KOLOM_BOARD):
                if(board_asli[i, j] == self.PIECE_KOSONG):
                    board[i, j] = 0
                elif(board_asli[i, j] == Piece(player_shape, player_color)):
                    board[i, j] = 1
                elif(board_asli[i, j] == Piece(player_shape, enemy_color)):
                    board[i, j] = 2
                elif(board_asli[i, j] == Piece(enemy_shape, enemy_color)):
                    board[i, j] = 3
                elif(board_asli[i, j] == Piece(enemy_shape, player_color)):
                    board[i, j] = 4
                else:
                    board[i, j] = 0
        return board

    def Solusi(self, state, n_player, thinking_time, queue):
        self.BARIS_BOARD = 6
        self.KOLOM_BOARD = 7
        self.PIECE_ROUND_BIRU = Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE)
        self.PIECE_ROUND_MERAH = Piece(ShapeConstant.CIRCLE, ColorConstant.RED)
        self.PIECE_CROSS_BIRU = Piece(ShapeConstant.CROSS, ColorConstant.BLUE)
        self.PIECE_CROSS_MERAH = Piece(ShapeConstant.CROSS, ColorConstant.RED)
        self.PIECE_KOSONG = Piece(ShapeConstant.BLANK, ColorConstant.BLACK)
        #Solusi dari permasalahan minimax
        self.board = self.salin_board_dari_state(state.board, n_player)
        self.player = state.players[n_player]
        if(n_player == 1):
            self.enemy = state.players[0]
        else:
            self.enemy = state.players[1]
        #Apabila kuota shape player masih cukup
        if(self.player.quota[self.player.shape] > 0):
            seed = random.randint(0,100)
            if (seed<50):
                kolomnya, scorenya = self.minimax(self.board, 4, -math.inf, math.inf, False, self.enemy.shape)
                queue.put(kolomnya)
                queue.put(self.enemy.shape)
            else:
                kolomnya, scorenya = self.minimax(self.board, 4, -math.inf, math.inf, True, self.player.shape)
                queue.put(kolomnya)
                queue.put(self.player.shape)
        else: #kuota shape player sudah habis
            kolomnya, scorenya = self.minimax(self.board, 4, -math.inf, math.inf, False, self.enemy.shape)
            queue.put(kolomnya)
            queue.put(self.enemy.shape)

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        queue = multiprocessing.Queue()
        action_process = multiprocessing.Process(target=self.Solusi, args=(state, n_player, thinking_time, queue,))
        action_process.start()
        #Timeout 3 detik
        action_process.join(timeout=3)

        # Kirim signal supaya stop event setelah 3 detik
        action_process.terminate()
        
        #waktu habis, random saja
        if queue.qsize() == 0:
            return (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        else:
            #Queue memiliki isi solusi
            a = queue.get(0)
            b = queue.get(0)
            print("Bot Simple-donkey:",a,b)
            if (a == None):
                return (random.randint(0, state.board.col), b)
            else:
                return a,b

import random
from copy import deepcopy
from time import time

from src.utility import *
from src.model import State

from typing import Tuple, List

class Minimax2:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement