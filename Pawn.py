import Utils
from Board import Board
from Piece import Piece


class Pawn(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)

    def moves(self, board: Board, sq: str) -> (list, bool):
        en_passant = False
        idx: tuple = Utils.get_index(sq)
        row: int = idx[0] - 1
        sign = -1
        if self.is_white:
            sign = 1
            row: int = idx[0] + 1
        possible_sq: list = [[row, idx[1]], [row, idx[1] - 1], [row, idx[1] + 1]]
        if not self.has_been_played:
            if idx[0] == 1 and self.is_white:
                possible_sq.append([idx[0] + 2, idx[1]])
            elif idx[0] == 6 and not self.is_white:
                possible_sq.append([idx[0] - 2, idx[1]])

        possible_moves = []
        for index, square in enumerate(possible_sq):
            if Utils.borders(square[0]) and Utils.borders(square[1]):
                move = board.sq_board[square[0]][square[1]]
                if index == 1 or index == 2:
                    if self.en_passant(board, move):
                        possible_moves.append(move)
                        en_passant = True
                    if Utils.get_color_piece(board.position[move]) != self.color and \
                            not board.is_square_empty(move):
                        possible_moves.append(move)
                if index == 0:
                    if board.is_square_empty(move):
                        possible_moves.append(move)
                if index == 3:
                    if board.is_square_empty(move) and board.is_square_empty(move[0] + str(int(move[1])-sign)):
                        possible_moves.append(move)

        return possible_moves, en_passant

    def en_passant(self, board: Board, sq: str) -> bool:
        if not board.notation:
            return False
        last_move = board.notation[-1]
        if len(last_move) != 2:
            return False
        if self.is_white:
            return last_move[0] + str(int(last_move[1]) + 1) == sq and board.is_square_empty(sq)
        return last_move[0] + str(int(last_move[1]) - 1) == sq and board.is_square_empty(sq)


