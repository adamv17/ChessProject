from kivy.uix.layout import Layout

import Constants
import copy

import Utils
import numpy as np


class Board:
    position: dict  # a dictionary of the current chess position
    sq_board: np.array  # the position as a char numpy array
    notation: list  # the move notation

    def __init__(self):
        self.position = copy.deepcopy(Constants.START_POSITION)
        self.sq_board = Utils.dict_to_numpy(self.position)
        self.notation = []

    def update_game(self, piece, square: str, castle: int, unambiguous: str) -> str:
        """
        :param castle:
        :param unambiguous:
        :param piece: the piece played
        :param square: the square to move to
        :return: updates the board and notation
        """
        captured_piece, captured, tmp = self.update_position(piece, square)
        piece.update_square(square)
        notation_move: str = Utils.board_to_notation(
            piece.piece_name.upper(),
            [square, tmp[0] if piece.piece_name.upper() == 'P' and captured else unambiguous],
            [False, captured, False, False],
            castle, ''
        )
        self.update_notation(notation_move)
        return captured_piece

    def update_position(self, piece, square: str):
        """
        :param piece: the piece played
        :param square: the square to move to
        :return: updates the board position
        """
        captured_piece: str = self.position[square]
        captured: bool = captured_piece != "-"
        tmp = piece.square
        self.position[piece.square] = "-"
        self.position[square] = piece.piece_name
        return captured_piece, captured, tmp

    def update_notation(self, move: str):
        """
        :param move: the move played
        :return: updates the notation
        """
        self.notation.append(move)
        print(self.notation)

    def is_square_empty(self, square: str) -> bool:
        """
        :param square: the square to check
        :return: true if the square is empty otherwise false
        """
        return self.position[square] == "-"

