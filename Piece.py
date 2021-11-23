import copy

from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
import Utils
from Logic import Logic

import Constants


class Piece(Scatter):
    piece_name: str
    piece_color: str
    square: str

    def __init__(self, piece_name, piece_color, square):
        super().__init__(do_rotation=False, do_scale=False)
        self.piece_name = piece_name
        self.piece_color = piece_color
        self.square = square
        image = Image(source=Constants.PIECES[piece_name])
        image.size = (80, 80)
        self.add_widget(image)
        self.moved = False

    def update_square(self, square: str):
        self.square = square

    def get_close_square(self) -> str:
        for sq in Constants.START_POSITION.keys():
            if self.is_on_square(self.parent.coord[sq][0], self.parent.coord[sq][1]):
                return sq

        return "-"

    def is_on_square(self, x: int, y: int) -> bool:
        return self.collide_point(x, y)

    def set_square(self, square: str):
        coordinate = self.parent.coord[square]
        self.set_center_x(coordinate[0])
        self.set_center_y(coordinate[1])
        self.square = square

    def move_to_square(self, sq: str) -> bool:
        if sq != "-":
            self.set_square(sq)
            return True
        self.set_square(self.square)
        return False

    def capture(self, sq: str):
        for p in self.parent.pieces:
            if p.square == sq and self.piece_color != p.piece_color:
                self.parent.remove_widget(p)

    def move(self) -> bool:
        sq: str = self.get_close_square()
        if self.parent.legal_move(self, sq) and sq != self.square:
            board = copy.deepcopy(self.parent.board)
            board.update_position(self, sq)
            d = Utils.invert_dict(board.position)
            print(d)
            print(Utils.get_piece_name("K", self.piece_color))
            if not Logic.check(
                    board,
                    d[Utils.get_piece_name("K", self.piece_color)],
                    self.parent.get_all_pieces_color(Utils.opposite_color(self.piece_color))):
                print("no check")
                captured = self.parent.board.update_game(self, sq)
                if captured != "-":
                    self.capture(sq)
                played = self.move_to_square(sq)
                return played
        self.set_square(self.square)
        return False

    def on_touch_down(self, touch):
        if self.do_translation:
            return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        self.moved = True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.moved:
            played = self.move()
            if played:
                self.parent.disable_pieces(self.piece_color)
                self.parent.enable_pieces(Utils.opposite_color(self.piece_color))
        self.moved = False
        return super().on_touch_up(touch)

    def add_possible_moves(self, board: Board, sq: str, possible_moves: list, rays: tuple):
        possible_moves += self.ray_filtering(board, rays[0], sq)
        if rays[1] is not None:
            possible_moves += self.ray_filtering(board, rays[1], sq)

    def ray_filtering(self, board: Board, ray: np.array, sq: str):
        ray: np.array = Utils.flip_ray(ray, sq)
        ray: list = Utils.delete_sq(list(ray), sq)
        return self.filter_possible_moves(board, ray, True)

    def filter_possible_moves(self, board: Board, moves: list, seq: bool) -> list:
        filtered = []
        if not moves:
            return filtered
        for move in moves:
            if board.is_square_empty(move):
                filtered.append(move)
            elif Utils.get_color_piece(board.position[move]) != self.piece_color:
                filtered.append(move)
                if seq:
                    break
            elif seq:
                break
        return filtered



