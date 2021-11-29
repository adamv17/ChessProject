import copy

from Piece import Piece
from Board import Board
import Utils


class King(Piece):
    def __init__(self, piece_name, color, square):
        super().__init__(piece_name, color, square)

    def moves(self, board: Board, sq: str) -> list:
        """
        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        idx: tuple = Utils.get_index(sq)
        possible_moves = []
        for d in [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]:
            sq_row = idx[0] + d[0]
            sq_col = idx[1] + d[1]
            if Utils.borders(sq_row) and Utils.borders(sq_col):
                possible_moves.append(board.sq_board[sq_row][sq_col])
        return self.filter_king_moves(board, self.filter_possible_moves(board, possible_moves, False))

    def checkmate(self, board: Board) -> bool:
        """
        :param board:
        :return:
        """
        in_check: bool = self.parent.check(board, self.square,
                                           self.parent.get_all_pieces_color(Utils.opposite_color(self.color)))
        no_moves: bool = len(self.moves(board, self.square)) == 0
        return in_check and no_moves

    def can_move(self, board: Board, move):
        """
        :param board:
        :param move:
        :return:
        """
        board_copy = copy.deepcopy(board)
        board_copy.update_position(self, move)
        in_check: bool = self.parent.check(board_copy, move,
                                           self.parent.get_all_pieces_color(Utils.opposite_color(self.color)))
        return not in_check

    def filter_king_moves(self, board: Board, moves: list) -> list:
        """
        :param board:
        :param moves:
        :return:
        """
        legal = []
        for m in moves:
            if self.can_move(board, m):
                legal.append(m)
        return legal