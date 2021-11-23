from kivy.uix.layout import Layout
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
import Utils
from Piece import Piece
import numpy as np
import os.path
from Board import Board
from Logic import Logic
import chess
import Constants


class ChessGame(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
        # self.source = os.path.join(Constants.ROOT_DIR, "images/marble-chessboard.jpg")
        self.board_image = Image(source=os.path.join(Constants.ROOT_DIR, "images/marble-chessboard.jpg"))
        self.board_image.pos = (100, 0)
        self.board_image.size = (600, 600)
        self.add_widget(self.board_image)
        self.fullscreen = False
        Window.bind(on_resize=self.window_resize)
        self.coord = Utils.get_coord(Constants.DELTA_SQUARE, Constants.XY_FIRST_SQUARE)

        self.pieces = []
        self.white_pieces = []
        self.black_pieces = []
        squares = list(Constants.START_POSITION.keys())
        # initialize white pieces
        for wsq in squares[0:16]:
            name = Constants.START_POSITION[wsq]
            piece = (name, 'w', wsq)
            self.white_pieces.append(piece)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(wsq)

        for bsq in squares[48:64]:
            name = Constants.START_POSITION[bsq]
            piece = Piece(name, 'b', bsq)
            self.black_pieces.append(piece)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(bsq)

        self.disable_pieces('b')

    def window_resize(self, *event):
        if self.fullscreen:
            scale = 1 + 50 / 600
            self.board_image.pos = (300, 0)
            self.board_image.size = (655, 655)
            self.coord = Utils.get_coord(Constants.DELTA_SQUARE_FULL, Constants.XY_FIRST_SQUARE_FULL)
        else:
            scale = 1
            self.board_image.pos = (100, 0)
            self.board_image.size = (600, 600)
            self.coord = Utils.get_coord(Constants.DELTA_SQUARE, Constants.XY_FIRST_SQUARE)
        for p in self.pieces:
            p.scale = scale  # scales the pieces
            p.move_to_square("-")  # moves the pieces to their original places

        self.fullscreen = not self.fullscreen
        print("size changed")

    def disable_pieces(self, color: str):
        pieces = self.get_all_pieces_color(color)
        for p in pieces:
            p.do_translation = False

    def enable_pieces(self, color: str):
        pieces = self.get_all_pieces_color(color)
        for p in pieces:
            p.do_translation = True

    def get_all_pieces_color(self, color: str) -> list:
        return self.white_pieces if color == 'w' else self.black_pieces

    def graphics(self):
        pass

    @staticmethod
    def get_all_moves(board: Board, pieces: list) -> list:
        moves = []
        for piece in pieces:
            name = piece.piece_name
            upper_name = name.upper()
            color = piece.piece_color
            possible_moves = []
            if upper_name == 'P':
                possible_moves = Logic.pawn(board, piece.square, color)
            if upper_name == 'N':
                possible_moves = Logic.knight(board, piece.square, color)
            if upper_name == 'B':
                possible_moves = Logic.bishop(board, piece.square, color)
            if upper_name == 'R':
                possible_moves = Logic.rook(board, piece.square, color)
            if upper_name == 'Q':
                possible_moves = Logic.queen(board, piece.square, color)
            if upper_name == 'K':
                possible_moves = Logic.king(board, piece.square, color)
            moves += possible_moves
        print(moves)
        return moves

    @staticmethod
    def check(board: Board, sq: str, pieces: list) -> bool:
        print(sq)
        return sq in Logic.get_all_moves(board, pieces)

    @staticmethod
    def checkmate():
        pass

    def legal_move(self, piece: Piece, sq: str) -> bool:
        name = piece.piece_name
        upper_name = name.upper()
        color = piece.piece_color
        possible_moves = []
        if upper_name == 'P':
            possible_moves = Logic.pawn(self.board, piece.square, color)
        if upper_name == 'N':
            possible_moves = Logic.knight(self.board, piece.square, color)
        if upper_name == 'B':
            possible_moves = Logic.bishop(self.board, piece.square, color)
        if upper_name == 'R':
            possible_moves = Logic.rook(self.board, piece.square, color)
        if upper_name == 'Q':
            possible_moves = Logic.queen(self.board, piece.square, color)
        if upper_name == 'K':
            possible_moves = Logic.king(self.board, piece.square, color)

        if not possible_moves:  # if possible moves is empty
            return False

        return sq in possible_moves

    def update_game(self, piece: Piece, sq: str):
        self.board.update_game(piece, sq)
