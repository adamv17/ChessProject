from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
import Utils

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

    def update_square(self, square: str):
        self.square = square

    def get_close_square(self) -> str:
        for sq in Constants.START_POSITION.keys():
            if self.is_on_square(Utils.COORD[sq][0], Utils.COORD[sq][1]):
                return sq

        return "-"

    def is_on_square(self, x: int, y: int) -> bool:
        return self.collide_point(x, y)

    def set_square(self, square: str):
        coordinate = Utils.COORD[square]
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
        if self.parent.legal_move() and sq != self.square:
            captured = self.parent.update_position(self, sq)
            if captured != "-":
                self.capture(sq)
            played = self.move_to_square(sq)
            return played
        self.set_square(self.square)
        return False

    def on_touch_down(self, touch):
        if self.do_translation:
            return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            played = self.move()
            if played:
                self.parent.disable_pieces(self.piece_color)
                self.parent.enable_pieces(Utils.opposite_color(self.piece_color))
        return super().on_touch_up(touch)


