from kivy.uix.layout import Layout
from kivy.uix.image import Image
from kivy.core.window import Window
import Utils
from Piece import Piece
import numpy as np
import os.path
from Board import Board
import Constants
from kivy.uix.popup import Popup
from kivy.uix.label import Label
# from ChessApp import ChessApp


class ChessGame(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
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
            piece = Utils.cls_from_symbol(name, 'w', wsq)
            if name == 'K':
                self.white_king = piece
            self.white_pieces.append(piece)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(wsq)

        # initialize black pieces
        for bsq in squares[48:64]:
            name = Constants.START_POSITION[bsq]
            piece = Utils.cls_from_symbol(name, 'b', bsq)
            if name == 'k':
                self.black_king = piece
            self.black_pieces.append(piece)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(bsq)

        self.piece_translation('b', False)
        self.game_ended = False

    def window_resize(self, *event):
        """
        :param event: the resize event data
        :return: resize the pieces and board to fit the screen
        """
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

    def piece_translation(self, color: str, translate: bool):
        """
        :param color:
        :param translate:
        :return:
        """
        pieces = self.get_all_pieces_color(color)
        for p in pieces:
            p.do_translation = (translate, translate)

    def get_all_pieces_color(self, color: str) -> list:
        """
        :param color: the color of the pieces wanted
        :return: all the pieces of a certain color
        """
        return self.white_pieces if color == 'w' else self.black_pieces

    def get_all_moves(self, board: Board, pieces: list) -> list:
        """
        :param board: the current board position
        :param pieces: a list of the pieces for which to get the moves
        :return: all the possible moves of these pieces
        """
        moves = []
        for piece in pieces:
            moves += piece.moves(board, piece.square)
        return moves

    def check(self, board: Board, sq: str, pieces: list) -> bool:
        """
        :param board: the current board position
        :param sq:
        :param pieces: a list of the pieces for which to get the moves
        :return: whether the square is under attack (the king is in check)
        """
        return sq in self.get_all_moves(board, pieces)

    def legal_move(self, piece: Piece, sq: str) -> bool:
        """
        :param piece: the piece trying to move
        :param sq: the square the piece wants to move to
        :return: true if the move is legal otherwise false
        """
        possible_moves = piece.moves(self.board, piece.square)
        print(possible_moves)
        return sq in possible_moves

    def update_game(self, piece: Piece, sq: str):
        """
        :param piece: the piece played
        :param sq: the square to move to
        :return: updates the board and notation
        """
        self.board.update_game(piece, sq)

    def end(self, color: str):
        """
        :param color: the color of the last player
        :return: ends the game if the king is checkmated
        """
        king = self.black_king if color == 'w' else self.white_king
        if king.checkmate(self.board):
            self.game_ended = True
            winner = 'white' if color == 'w' else 'black'
            popupWindow = Popup(title="checkmate!", content=Label(text=winner + ' won!'),
                                size_hint=[None, None],
                                size=(400, 400), auto_dismiss=True)
            popupWindow.open()

    def remove_piece(self, pieces: list, sq: str) -> Piece:
        for i, p in enumerate(pieces):
            if p.square == sq:
                cp = pieces.pop(i)
                return cp
