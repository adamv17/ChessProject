from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
import Utils
from Board import Board

import numpy as np
import Constants
import copy


class Piece(Scatter):
    piece_name: str  # the name of the piece
    color: str  # the color of the piece
    square: str  # the current square of the piece

    def __init__(self, piece_name, color, square):
        super().__init__(do_rotation=False, do_scale=False)
        self.piece_name = piece_name
        self.color = color
        self.square = square
        try:
            image = Image(source=Constants.PIECES[piece_name])
            image.size = (80, 80)
            self.add_widget(image)
        except KeyError:
            print(f"{piece_name} initialized: {self}")
        self.moved = False
        self.has_been_played = False

    def update_square(self, square: str):
        """
        :param square: the square of the piece
        :return: updates the square
        """
        self.square = square

    def get_close_square(self) -> str:
        """
        :return: the closest square to the piece coordinate position
        """
        for sq in Constants.START_POSITION.keys():
            if self.is_on_square(self.parent.coord[sq][0], self.parent.coord[sq][1]):
                return sq

        return "-"

    def is_on_square(self, x: int, y: int) -> bool:
        """
        :param x: the x coordinate
        :param y: the y coordinate
        :return: whether the piece is on the coordinates
        """
        return self.collide_point(x, y)

    def set_square(self, square: str):
        """
        :param square: the square to move to
        :return: updates the graphics and properties of the piece
        """
        coordinate = self.parent.coord[square]
        self.set_center_x(coordinate[0])
        self.set_center_y(coordinate[1])
        self.square = square

    def move_to_square(self, sq: str) -> bool:
        """
        :param sq: the square to move to
        :return: updates the piece in the game otherwise keeps it in the same place
        """
        if sq != "-":
            self.set_square(sq)
            return True
        self.set_square(self.square)
        return False

    def capture(self, sq: str):
        """
        :param sq: the square of the piece to capture
        :return: removes the piece
        """
        for p in self.parent.pieces:
            if p.square == sq and self.color != p.color:
                self.parent.remove_widget(p)

    def move(self) -> bool:
        """
        :return: moves the piece if it is legal then returns true otherwise false
        """
        sq: str = self.get_close_square()
        if self.parent.legal_move(self, sq):
            board = copy.deepcopy(self.parent.board)
            board.update_position(self, sq)
            d = Utils.invert_dict(board.position)
            if not self.parent.is_square_attacked(board, d[Utils.get_piece_name("K", self.color)],
                                                  Utils.opposite_color(self.color)):
                captured = self.parent.board.update_game(self, sq)
                if captured != "-":
                    self.capture(sq)

                played = False
                if self.piece_name.upper() == 'P' and (
                        Utils.get_index(self.square)[0] == 0 or Utils.get_index(self.square)[0] == 7):
                    self.parent.promotion(self)
                else:
                    played = self.move_to_square(sq)
                    self.parent.end(self.color)
                return played
        self.set_square(self.square)
        return False

    def on_touch_down(self, touch):
        """
        :param touch: the piece touched
        :return: if the piece can move now allows the grab
        """
        if self.do_translation[0] and not self.parent.game_ended:
            return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        """
        :param touch: the piece moved
        :return: continues to move the piece and says that it has moved
        """
        self.moved = True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """
        :param touch: the piece touched
        :return: moves the piece to the closest square otherwise returns it
        """
        if self is None or self.parent is None:
            return None
        if self.collide_point(*touch.pos) and self.moved:
            played = self.move()
            if self.parent is None:
                return None
            if played:
                self.has_been_played = True
                self.parent.piece_translation(self.color, False)
                self.parent.piece_translation(Utils.opposite_color(self.color), True)
        self.moved = False
        return super().on_touch_up(touch)

    def add_possible_moves(self, board: Board, sq: str, possible_moves: list, rays: tuple):
        """
        :param board: the current board
        :param sq: the current square
        :param possible_moves: the current possible moves
        :param rays: rays of moves
        :return: adds to the possible moves the rays
        """
        possible_moves += self.ray_filtering(board, rays[0], sq)
        if rays[1] is not None:
            possible_moves += self.ray_filtering(board, rays[1], sq)

    def ray_filtering(self, board: Board, ray: np.array, sq: str):
        """
        :param board: the current board
        :param ray: a ray of possible moves
        :param sq: the current square
        :return: the filtered ray
        """
        ray: np.array = Utils.flip_ray(ray, sq)
        ray: list = Utils.delete_sq(list(ray), sq)
        return self.filter_possible_moves(board, ray, True)

    def filter_possible_moves(self, board: Board, moves: list, seq: bool) -> list:
        """
        :param board: the current board
        :param moves: the possible moves
        :param seq: whether there is a sequence in the moves
        :return: the filtered possible moves
        """
        filtered = []
        for move in moves:
            if board.is_square_empty(move):
                filtered.append(move)
            elif Utils.get_color_piece(board.position[move]) != self.color:
                filtered.append(move)
                if seq:
                    break
            elif seq:
                break
        return filtered
