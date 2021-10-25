from kivy.uix.layout import Layout

import Constants
import copy

import Utils
from Piece import Piece


class Board(Layout):
    position: dict

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
        self.play_to_position()

    def play_to_position(self):
        pass

    def is_square_empty(self, square: str) -> bool:
        return self.position[square] == "-"

    def position_to_graphics(self):
        pass
