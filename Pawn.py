from Piece import Piece
from Board import Board
import numpy as np
import Utils


class Pawn(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)
        self.promotion = False

    def moves(self, board: Board, sq: str) -> list:
        """

        :param board: the current board position
        :param sq: the current square of the piece
        :return: the possible moves of the piece
        """
        idx: tuple = Utils.get_index(sq)
        row: int = idx[0] - 1
        is_white = self.piece_color == 'w'
        if is_white:
            row: int = idx[0] + 1
        possible_sq: list = [[row, idx[1]], [row, idx[1] - 1], [row, idx[1] + 1]]
        if idx[0] == 1 and is_white:
            possible_sq.append([idx[0] + 2, idx[1]])
        elif idx[0] == 6 and not is_white:
            possible_sq.append([idx[0] - 2, idx[1]])
        possible_moves = [board.sq_board[square[0]][square[1]] for square in possible_sq if
                          Utils.borders(square[0]) and Utils.borders(square[1])]
        sq_en = [None, None]
        en = [False, False]
        for i in range(1, 3):
            try:
                en[i - 1] = self.en_passant(board, possible_moves[i])
                sq_en[i - 1] = possible_moves[i]
            except IndexError:
                en[i - 1] = False
        for i, m in enumerate(possible_moves):
            if abs(Utils.get_index(m)[1] - idx[1]) == 1 and board.is_square_empty(m):
                del possible_moves[i]
        possible_moves = self.filter_possible_moves(board, possible_moves, False)

        if en[0]:
            possible_moves.append(sq_en[0])
        if en[1]:
            possible_moves.append(sq_en[1])

        return possible_moves

    def en_passant(self, board: Board, sq: str):
        if not board.notation:
            return False
        last_move = board.notation[-1]
        if len(last_move) != 2:
            return False
        if self.piece_color == 'w':
            return last_move[0] + str(int(last_move[1]) + 1) == sq and board.is_square_empty(sq)
        return last_move[0] + str(int(last_move[1]) - 1) == sq and board.is_square_empty(sq)
