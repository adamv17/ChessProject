from Piece import Piece
import Utils
from Board import Board


class Bishop(Piece):
    def __init__(self, piece_name, piece_color, square):
        super().__init__(piece_name, piece_color, square)

    def moves(self, board: Board, sq: str) -> list:
        """
        available moves
        :param color:
        :param board:
        :param sq:
        :return:
        """
        idx: tuple = Utils.get_index(sq)
        # main diagonal calculation
        k_main: int = idx[1] - idx[0]
        main_d: np.array = get_k_diag(board.sq_board, k_main)
        possible_moves = []
        self.add_possible_moves(board, sq, possible_moves, Utils.split(main_d, sq))

        # secondary diagonal calculation
        k_sec: int = idx[0] + idx[1] - 7  # k for secondary diagonal
        sec_d: np.array = get_k_diag(np.flipud(board.sq_board), k_sec)  # vertical flip
        self.add_possible_moves(board, sq, possible_moves, Utils.split(sec_d, sq))

        return possible_moves

    @staticmethod
    def get_k_diag(board: np.array, k: int) -> np.array:
        """
        :param board:
        :param k:
        :return:
        """
        diagonal = []
        if abs(k) != 7:
            diagonal = np.diag(board, k=k)
        return diagonal
