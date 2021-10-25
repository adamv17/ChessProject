from kivy.uix.layout import Layout
from kivy.uix.image import Image
import Utils
from Piece import Piece
import numpy as np
import os.path
from Board import Board

import Constants


class ChessGame(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
        self.board_image = Image(source=os.path.join(Constants.ROOT_DIR, "images/marble-chessboard.jpg"))
        self.board_image.pos = (100, 0)
        self.board_image.size = (600, 600)
        self.add_widget(self.board_image)
        self.coord = Utils.get_coord()

        self.pieces = []
        squares = list(Constants.START_POSITION.keys())
        # initialize white pieces
        for wsq in squares[0:16]:
            name = Constants.START_POSITION[wsq]
            piece = Piece(name, 'w', wsq)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(wsq)

        for bsq in squares[48:64]:
            name = Constants.START_POSITION[bsq]
            piece = Piece(name, 'b', bsq)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(bsq)

    def graphics(self):
        pass

    def legal_move(self) -> bool:
        return True

    def update_position(self, piece, sq):
        self.board.update_position(piece, sq)

