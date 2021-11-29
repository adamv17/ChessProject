from Piece import Piece
from Board import Board
from Bishop import Bishop
from Rook import Rook


class Queen(Piece):
    def __init__(self, piece_name, color, square):
        super().__init__(piece_name, color, square)

    def moves(self, board: Board, sq: str):
        """
        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        diag_moves: list = Bishop.moves(self, board, sq)
        perp_moves: list = Rook.moves(self, board, sq)
        return diag_moves + perp_moves

