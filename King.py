from Piece import Piece
from Board import Board
import Utils


class King(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)

    def moves(self, board: Board, sq: str):
        """
        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        idx = Utils.get_index(sq)
        possible_moves = []
        for d in [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]:
            sq_row = idx[0] + d[0]
            sq_col = idx[1] + d[1]
            if Utils.borders(sq_row) and Utils.borders(sq_col):
                possible_moves.append(board.sq_board[sq_row][sq_col])
        return self.filter_possible_moves(board, possible_moves, False)
