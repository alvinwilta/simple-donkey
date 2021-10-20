import random
from time import time
import numpy as np

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.utility import is_out
from src.model import State, Piece, Board
import multiprocessing

from typing import Tuple, List

class LocalSearchGroup15:
    def __init__(self):
        self.BOARD_ROW = 6
        self.BOARD_COL = 7
        pass
    
    def generate_neighbour(self, state: State, player_turn, thinking_time: float):
        # Menghasilkan list tetangga dari state awal
        player = state.players[player_turn]
        neighbour_list = []
        
        for column in range(state.board.col):
            for shape,value in player.quota.items():
                if value> 0:
                    board = self.copy_board(state.board, player_turn)
                    piece = Piece(shape, player.color)
                    score = self.score_position(board, piece)
                    neighbour_list.append([(column, piece.shape), score])

        return neighbour_list

    def hill_climbing(self, state: State, player_turn, thinking_time: float, result):
        neighbour_list = self.generate_neighbour(state, player_turn, thinking_time)

        current = neighbour_list[random.randint(0, len(neighbour_list)-1)]
        neighbour_list.sort(reverse=True, key=lambda x: x[1])

        for neighbour in neighbour_list:
            if neighbour[1] <= current[1]:
                # Jika score neighbour kurang atau sama dengan current, masukkan ke hasil
                result.put(current)

            # Jika score neighbour lebih baik dari current, current menjadi neighbour
            current = neighbour
    
    def copy_board(self, board_asli, n_player):
        board = np.zeros((6,7))
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
        
        for i in range(self.BOARD_ROW):
            for j in range(self.BOARD_COL):
                if(board_asli[i, j] == Piece(ShapeConstant.BLANK, ColorConstant.BLACK)):
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
            centre_array = [int(i) for i in list(board[:, self.BOARD_COL // 2])]
            centre_count = centre_array.count(piece)
            #Apabila ada piece yang akan ditaruh disini, score dikali 8
            score += centre_count * 3

        # Menilai posisi horizontal
        for r in range(self.BOARD_ROW-1, -1, -1):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.BOARD_COL - 3):
                # Membuat window horizontal berukuran 4
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Menilai posisi vertikal
        for c in range(self.BOARD_COL):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.BOARD_ROW-1, self.BOARD_ROW-4, -1):
                # Membuat window vertikal berukuran 4
                window = col_array[r:r - 4]
                score += self.evaluate_window(window, piece)

        # Menilai posisi diagonal positif
        for r in range(self.BOARD_ROW-1, self.BOARD_ROW-5, -1):
            for c in range(self.BOARD_COL-3):
                # Membuat window diagonal positif berukuran 4
                window = [board[r-i, c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        
        # Menilai posisi diagonal negatif
        for r in range(self.BOARD_ROW-1, self.BOARD_ROW-4, -1):
            for c in range(self.BOARD_COL-3):
                # Membuat window diagonal negatif berukuran 4
                window = [board[r - 3 + i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        return score
        
    def find(self, state: State, player_turn, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        result = multiprocessing.Queue()
        p = multiprocessing.Process(target=self.hill_climbing, args=(state, player_turn, thinking_time, result))
        p.start()
        #Timeout 3 detik
        p.join(timeout=3)

        # Kirim signal supaya stop event setelah 3 detik
        p.terminate()

        if result.qsize() != 0:
            ret_val = result.get(0)
            return ret_val[0]
        else:
            # Jika tidak terdapat hasil, random
            return (random.randint(0, state.board.col-1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
