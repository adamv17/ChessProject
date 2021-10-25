from kivy.uix.layout import Layout

import Constants
import copy

import Utils
from Piece import Piece


class Board(Layout):
    position: dict  # a dictionary of the current chess position
    coord: dict  # the coordinates (x, y) for each square
    notation: list  # the move notation

    def __init__(self):
        super().__init__()
        self.position = copy.deepcopy(Constants.START_POSITION)
        self.coord = Utils.get_coord()
        self.notation = []

    def update_position(self, piece: Piece, square: str):
        self.position[piece.square] = "-"
        self.position[square] = piece.piece_name
        piece.update_square(square)

    def legal_move(self) -> bool:
        pass

    def reverse_move(self):
        move = self.notation.pop(-1)
        self.play_to_position(self.notation)

    def play_to_position(self, notation: list):
        self.position = copy.deepcopy(Constants.START_POSITION)
        for i, move in enumerate(notation):
            name, squares, special, castle = Utils.notation_to_board(move, Utils.get_color(i + 1))
            # TODO: continue writing this method

    def play_move(self, name: str, squares: list[str], special: list[bool], castle: int):
        if castle == 2:
            pass

    def is_square_empty(self, square: str) -> bool:
        return self.position[square] == "-"

    def position_to_graphics(self):
        pass
