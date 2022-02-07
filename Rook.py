from Piece import Piece
from Board import Board
import numpy as np
import Utils


class Rook(Piece):
    def __init__(self, piece_name, color, square):
        super().__init__(piece_name, color, square)
        self.castling_sq = ''
        if self.color == 'w':
            if self.square == 'h1':
                self.castling_sq = 'f1'
            else:
                self.castling_sq = 'd1'
        else:
            if self.square == 'h8':
                self.castling_sq = 'f8'
            else:
                self.castling_sq = 'd8'

    def moves(self, board: Board, sq: str) -> (list, False):
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
        return possible_moves, False

    def castle_rook(self):
        self.parent.board.update_position(self, self.castling_sq)
        self.update_square(self.castling_sq)
        self.move_to_square(self.castling_sq)
