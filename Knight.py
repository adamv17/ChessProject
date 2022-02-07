from Piece import Piece
from Board import Board
import numpy as np
import Utils


class Knight(Piece):
    def __init__(self, piece_name, color, square):
        super().__init__(piece_name, color, square)

    def moves(self, board: Board, sq: str) -> (list, False):
        """
        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        idx: tuple = Utils.get_index(sq)
        moves = []
        addition = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for a in addition:
            move: tuple = (idx[0] + a[0], idx[1] + a[1])
            if Utils.borders(move[0]) and Utils.borders(move[1]):
                moves.append(board.sq_board[move[0]][move[1]])

        return self.filter_possible_moves(board, moves, False), False
