import numpy as np

import Constants
import Utils
from Piece import Piece
from Board import Board


class Logic:

    @staticmethod
    def pawn():
        pass

    @staticmethod
    def knight(board: Board, sq: str, color: str):
        idx = Utils.get_index(sq)
        moves = []
        print(idx)
        addition = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for a in addition:
            move_sq = Logic.try_move(board.sq_board, (idx[0] + a[0], idx[1] + a[1]))
            if move_sq != 'E: Out of Range':
                moves.append(move_sq)

        moves = Logic.filter_possible_moves(board, moves, color)
        return moves

    @staticmethod
    def try_move(board: np.array, move: tuple) -> str:
        if Utils.borders(move[0]) and Utils.borders(move[1]):
            return board[move[0]][move[1]]
        return 'E: Out of Range'

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
        idx = Utils.get_index(sq)
        # main diagonal calculation
        k_main = idx[1] - idx[0]
        main_d = Logic.get_k_diag(board.sq_board, k_main)
        possible_moves = []
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(main_d, sq))

        # secondary diagonal calculation
        k_sec = idx[0] + idx[1] - 7  # k for secondary diagonal
        sec_d = Logic.get_k_diag(np.flipud(board.sq_board), k_sec)  # vertical flip
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(sec_d, sq))

        return possible_moves

    @staticmethod
    def add_possible_moves(board: Board, sq: str, color: str, possible_moves: list, rays: tuple):
        possible_moves += Logic.ray_filtering(board, rays[0], color, sq)
        if rays[1] is not None:
            possible_moves += Logic.ray_filtering(board, rays[1], color, sq)

    @staticmethod
    def ray_filtering(board: Board, ray: np.array, color: str, sq: str):
        ray = Utils.flip_ray(ray, sq)
        ray = Utils.delete_sq(list(ray), sq)
        return Logic.filter_possible_moves(board, ray, color)

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
    def rook(board: Board, sq: str, color: str):
        idx = Utils.get_index(sq)
        row = board.sq_board[idx[0]]
        col = board.sq_board[:, idx[1]]
        possible_moves = []
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(row, sq))
        Logic.add_possible_moves(board, sq, color, possible_moves, Utils.split(col, sq))
        return possible_moves

    @staticmethod
    def queen(board: Board, sq: str, color: str):
        diag_moves = Logic.bishop(board, sq, color)
        perp_moves = Logic.rook(board, sq, color)
        possible_moves = diag_moves + perp_moves
        return possible_moves

    @staticmethod
    def king():
        pass

    @staticmethod
    def split_and_filter_rays():
        pass

    @staticmethod
    def filter_possible_moves(board: Board, moves: list, color: str) -> list:
        filtered = []
        if not moves:
            return filtered
        for move in moves:
            if board.is_square_empty(move):
                filtered.append(move)
            elif Utils.get_color_piece(board.position[move]) != color:
                filtered.append(move)
                return filtered
            else:
                return filtered
        return filtered

    @staticmethod
    def check():
        pass

    @staticmethod
    def checkmate():
        pass
