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

    def update_game(self, piece, square: str) -> str:
        """
        :param piece: the piece played
        :param square: the square to move to
        :return: updates the board and notation
        """
        captured_piece, captured, tmp = self.update_position(piece, square)
        piece.update_square(square)
        notation_move: str = Utils.board_to_notation(
            piece.piece_name.upper(),
            [square, tmp[0] if captured else None],
            [False, captured, False, False],
            2, ''
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

    def reverse_move(self):
        move = self.notation.pop(-1)
        self.play_to_position(self.notation)

    def play_to_position(self, notation: list):
        self.position: dict = copy.deepcopy(Constants.START_POSITION)
        for i, move in enumerate(notation):
            name, squares, special, castle = Utils.notation_to_board(move, Utils.get_color(i + 1))
            # TODO: continue writing this method
    #
    # def play_move(self, name: str, squares: list[str], special: list[bool], castle: int):
    #     if castle == 2:
    #         pass

    def is_square_empty(self, square: str) -> bool:
        """
        :param square: the square to check
        :return: true if the square is empty otherwise false
        """
        return self.position[square] == "-"

