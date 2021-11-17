import numpy as np

import Constants
import Utils
from Piece import Piece
from Board import Board


class Logic:

    @staticmethod
    def pawn(board: Board, sq: str, color: str) -> list:
        idx: tuple = Utils.get_index(sq)
        row: int = idx[0] - 1
        if color == 'w':
            row: int = idx[0] + 1
        possible_sq: list = [[row, idx[1]], [row, idx[1] - 1], [row, idx[1] + 1]]
        if idx[0] == 1 and color == 'w':
            possible_sq.append([idx[0] + 2, idx[1]])
        elif idx[0] == 6 and color == 'b':
            possible_sq.append([idx[0] - 2, idx[1]])
        possible_moves = [board.sq_board[square[0]][square[1]] for square in possible_sq if
                          Utils.borders(square[0]) and Utils.borders(square[1])]
        sq_en = [None, None]
        en = [False, False]
        for i in range(1, 3):
            try:
                en[i - 1] = Logic.en_passant(board, possible_moves[i], color)
                sq_en[i - 1] = possible_moves[i]
            except IndexError:
                en[i - 1] = False
        for i, m in enumerate(possible_moves):
            if abs(Utils.get_index(m)[1] - idx[1]) == 1 and board.is_square_empty(m):
                del possible_moves[i]
        print(possible_moves)
        possible_moves = Logic.filter_possible_moves(board, possible_moves, color, False)

        if en[0]:
            possible_moves.append(sq_en[0])
        if en[1]:
            possible_moves.append(sq_en[1])

        return possible_moves

    @staticmethod
    def en_passant(board: Board, sq: str, color: str):
        if not board.notation:
            return False
        last_move = board.notation[-1]
        if len(last_move) != 2:
            return False
        if color == 'w':
            return last_move[0] + str(int(last_move[1]) + 1) == sq and board.is_square_empty(sq)
        return last_move[0] + str(int(last_move[1]) - 1) == sq and board.is_square_empty(sq)

    @staticmethod
    def knight(board: Board, sq: str, color: str):
        idx: tuple = Utils.get_index(sq)
        moves = []
        addition = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for a in addition:
            move: tuple = (idx[0] + a[0], idx[1] + a[1])
            if Utils.borders(move[0]) and Utils.borders(move[1]):
                moves.append(board.sq_board[move[0]][move[1]])

        moves: list = Logic.filter_possible_moves(board, moves, color, False)
        return moves

    @staticmethod
    def can_capture(sq: str, color: str):
        pass

    @staticmethod
    def bishop(board: Board, sq: str, color: str) -> list:
        """
        available moves
        :param color:
        :param board:
        :param sq:
        :return:
        """
        idx: tuple = Utils.get_index(sq)
        # main diagonal calculation
        k_main: int = idx[1] - idx[0]
        main_d: np.array = Logic.get_k_diag(board.sq_board, k_main)
        possible_moves = []
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(main_d, sq))

        # secondary diagonal calculation
        k_sec: int = idx[0] + idx[1] - 7  # k for secondary diagonal
        sec_d: np.array = Logic.get_k_diag(np.flipud(board.sq_board), k_sec)  # vertical flip
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(sec_d, sq))

        return possible_moves

    @staticmethod
    def get_k_diag(board: np.array, k: int) -> np.array:
        """
        :param board:
        :param k:
        :return:
        """
        diagonal = []
        if abs(k) != 7:
            diagonal = np.diag(board, k=k)
        return diagonal

    @staticmethod
    def add_possible_moves(board: Board, sq: str, color: str, possible_moves: list, rays: tuple):
        possible_moves += Logic.ray_filtering(board, rays[0], color, sq)
        if rays[1] is not None:
            possible_moves += Logic.ray_filtering(board, rays[1], color, sq)

    @staticmethod
    def ray_filtering(board: Board, ray: np.array, color: str, sq: str):
        ray: np.array = Utils.flip_ray(ray, sq)
        ray: list = Utils.delete_sq(list(ray), sq)
        return Logic.filter_possible_moves(board, ray, color, True)

    @staticmethod
    def filter_possible_moves(board: Board, moves: list, color: str, seq: bool) -> list:
        filtered = []
        if not moves:
            return filtered
        for move in moves:
            if board.is_square_empty(move):
                filtered.append(move)
            elif Utils.get_color_piece(board.position[move]) != color:
                filtered.append(move)
                if seq:
                    break
            elif seq:
                break
        return filtered

    @staticmethod
    def rook(board: Board, sq: str, color: str):
        idx: tuple = Utils.get_index(sq)
        row: np.array = board.sq_board[idx[0]]
        col: np.array = board.sq_board[:, idx[1]]
        possible_moves = []
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(row, sq))
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(col, sq))
        return possible_moves

    @staticmethod
    def queen(board: Board, sq: str, color: str):
        diag_moves: list = Logic.bishop(board, sq, color)
        perp_moves: list = Logic.rook(board, sq, color)
        possible_moves: list = diag_moves + perp_moves
        return possible_moves

    @staticmethod
    def king(board: Board, sq: str, color: str):
        idx = Utils.get_index(sq)
        possible_moves = []
        for d in [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]:
            sq_row = idx[0] + d[0]
            sq_col = idx[1] + d[1]
            if Utils.borders(sq_row) and Utils.borders(sq_col):
                possible_moves.append(board.sq_board[sq_row][sq_col])
        return Logic.filter_possible_moves(board, possible_moves, color, False)

    @staticmethod
    def get_all_moves(board: Board, sq: str, color: str):
        pass

    @staticmethod
    def check(board: Board, sq: str, color: str):
        pass

    @staticmethod
    def checkmate():
        pass
