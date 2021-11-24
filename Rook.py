from Piece import Piece
from Board import Board
import numpy as np
import Utils


class Rook(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)

    def moves(self, board: Board, sq: str) -> list:
        """
        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        idx: tuple = Utils.get_index(sq)
        row: np.array = board.sq_board[idx[0]]
        col: np.array = board.sq_board[:, idx[1]]
        possible_moves = []
        self.add_possible_moves(board, sq, possible_moves, Utils.split(row, sq))
        self.add_possible_moves(board, sq, possible_moves, Utils.split(col, sq))
        return possible_moves
