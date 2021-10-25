from kivy.uix.scatter import Scatter


class Piece(Scatter):
    piece_name: str
    piece_color: str
    square: str

    def __init__(self, piece_name, piece_color, square):
        super().__init__(do_rotation=False, do_scale=False)
        self.piece_name = piece_name
        self.piece_color = piece_color
        self.square = square

    def update_square(self, square: str):
        self.square = square

    def get_close_square(self) -> str:
        for sq in self.parent.coord.keys():
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

    def move(self):
        sq: str = self.get_close_square()
        if self.parent.legal_move():
            self.parent.update_position(self, sq)
            played = self.move_to_square(sq)