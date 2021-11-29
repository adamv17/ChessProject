from Piece import Piece
import Utils
from Board import Board
import numpy as np


class Bishop(Piece):
    def __init__(self, piece_name, color, square):
        super().__init__(piece_name, color, square)

    def moves(self, board: Board, sq: str) -> list:
        """
        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        idx: tuple = Utils.get_index(sq)
        # main diagonal calculation
        k_main: int = idx[1] - idx[0]
        main_d: np.array = Bishop.get_k_diag(board.sq_board, k_main)
        possible_moves = []
        self.add_possible_moves(board, sq, possible_moves, Utils.split(main_d, sq))

        # secondary diagonal calculation
        k_sec: int = idx[0] + idx[1] - 7  # k for secondary diagonal
        sec_d: np.array = Bishop.get_k_diag(np.flipud(board.sq_board), k_sec)  # vertical flip
        self.add_possible_moves(board, sq, possible_moves, Utils.split(sec_d, sq))

        return possible_moves

    @staticmethod
    def get_k_diag(board: np.array, k: int) -> np.array:
        """
        :param board: the current board
        :param k: the k-th diagonal from the main
        :return: the squares in the k-th diagonal
        """
        diagonal = []
        if abs(k) != 7:
            diagonal = np.diag(board, k=k)
        return diagonal
