from Piece import Piece


class Rook(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)

    def moves(self, board: Board, sq: str) -> list:
        """
        :param board:
        :param sq:
        :return:
        """
        idx: tuple = Utils.get_index(sq)
        row: np.array = board.sq_board[idx[0]]
        col: np.array = board.sq_board[:, idx[1]]
        possible_moves = []
        self.add_possible_moves(board, sq, possible_moves, Utils.split(row, sq))
        self.add_possible_moves(board, sq, possible_moves, Utils.split(col, sq))
        return possible_moves
