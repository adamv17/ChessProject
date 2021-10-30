import numpy as np

import Constants
import Utils
from Piece import Piece


class Logic:

    @staticmethod
    def pawn():
        pass

    @staticmethod
    def knight(board: np.array, sq: str, color: str):
        idx = Utils.get_index(sq)
        moves = []
        print(idx)
        addition = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for a in addition:
            move_sq = Logic.try_move(board, (idx[0] + a[0], idx[1] + a[1]))
            if move_sq != 'E: Out of Range':
                moves.append(move_sq)
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
    def bishop(board: np.array, sq: str, color: str) -> list:
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
        main_d = Logic.get_k_diag(board, k_main)

        # secondary diagonal calculation
        k_sec = idx[0] + idx[1] - 7  # k for secondary diagonal
        sec_d = Logic.get_k_diag(np.flipud(board), k_sec)  # vertical flip

        possible_moves = []
        Logic.filter_possible_moves()

        return possible_moves

    @staticmethod
    def get_k_diag(board: np.array, k: int):
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
    def rook(board: np.array, sq: str, color: str):
        idx = Utils.get_index(sq)
        row = board[idx[0]]
        col = board[:, idx[1]]
        possible_moves = []
        Logic.filter_possible_moves()
        return possible_moves

    @staticmethod
    def queen(board: np.array, sq: str, color: str):
        diag_moves = Logic.bishop(board, sq, color)
        perp_moves = Logic.rook(board, sq, color)
        possible_moves = diag_moves + perp_moves
        return possible_moves

    @staticmethod
    def king():
        pass

    @staticmethod
    def filter_possible_moves():
        # TODO: write method to be modular
        pass

    @staticmethod
    def check():
        pass

    @staticmethod
    def checkmate():
        pass
