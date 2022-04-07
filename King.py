import copy

from Piece import Piece
from Board import Board
import Utils


class King(Piece):
    def __init__(self, piece_name, color, square):
        super().__init__(piece_name, color, square)
        self.start_sq = self.square
        self.rook_short = None
        self.rook_long = None

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
        self.castle(board, possible_moves)
        return self.filter_king_moves(board, self.filter_possible_moves(board, possible_moves, False))

    def checkmate(self, board: Board) -> bool:
        """
        :param board:
        :return:
        """
        in_check: bool = self.parent.is_square_attacked(board, self.square, Utils.opposite_color(self.color))
        if not in_check:
            return False
        no_moves: bool = len(self.moves(board, self.square)) == 0
        if not no_moves:
            return False
        return in_check and no_moves and not self.parent.legal_move_present(self.color)

    def can_move(self, board: Board, move):
        """
        :param board:
        :param move:
        :return:
        """
        board_copy = copy.deepcopy(board)
        board_copy.update_position(self, move)
        in_check: bool = self.parent.is_square_attacked(board_copy, move, Utils.opposite_color(self.color))
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

    def short(self, board):
        squares = ['f8', 'g8']
        self.rook_short = self.parent.black_rooks[1]
        if self.is_white:
            squares = ['f1', 'g1']
            self.rook_short = self.parent.white_rooks[1]
        return board.is_square_empty(squares[0]) and board.is_square_empty(
            squares[1]) and not self.rook_short.has_been_played

    def long(self, board):
        squares = ['d8', 'c8', 'b8']
        self.rook_long = self.parent.black_rooks[0]
        if self.is_white:
            squares = ['d1', 'c1', 'b1']
            self.rook_long = self.parent.white_rooks[0]
        return board.is_square_empty(squares[0]) and board.is_square_empty(squares[1]) and board.is_square_empty(
            squares[2]) and not self.rook_long.has_been_played

    def castle(self, board, possible_moves):
        if not self.has_been_played:
            if self.short(board):
                possible_moves.append('g1' if self.is_white else 'g8')
            if self.long(board):
                possible_moves.append('c1' if self.is_white else 'c8')
