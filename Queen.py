from Piece import Piece


class Queen(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)

    def moves(self, board: Board, sq: str):
        diag_moves: list = Bishop.moves(self, board, sq)
        perp_moves: list = Rook.moves(self, board, sq)
        possible_moves: list = diag_moves + perp_moves
        return possible_moves