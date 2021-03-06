"""
Utils class, contains all utility functions that are modular and unrelated to the User or the Engine.
"""
from Constants import START_POSITION
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen
from King import King

import numpy as np


# TODO: add doc


def notation_to_board(move: str, color: str) -> (str, list[str], list[bool], int):
    """
    :param move:
    :param color:
    :return:
    """
    piece_name = None  # the name of the piece
    squares = [None, None]  # to square, row or column letter hint
    special = [False, False, False, False]  # check, capture, checkmate, promotion
    castle = 2  # whether the player has castled short (0) or long (1)

    if move == "O-O":
        return piece_name, squares, special, 0
    elif move == "O-O-O":
        return piece_name, squares, special, 1

    special_notation = ['+', 'x', '#', '=']
    for index, notation in enumerate(special_notation):
        if move.__contains__(notation):
            special[index] = True
            move = move.replace(notation, '')

    if move[0].islower():
        piece_name = get_piece_name('P', color)
        if len(move) == 3 and not move[-1].isupper():  # pawn capture, upper in case of promotion
            squares[1] = move[0]
    else:  # strong piece move
        piece_name = get_piece_name(move[0], color)
        if len(move) == 4:  # row or column letter hint
            squares[1] = move[1]

    squares[0] = move[-2:] if not special[3] else move[len(move) - 3:-1]  # in case of promotion

    return piece_name, squares, special, castle


def board_to_notation(piece_name: str, squares: list[str], special: list[bool], castle: int,
                      promotion_piece: str) -> str:
    """
    :param piece_name:
    :param squares:
    :param special:
    :param castle:
    :param promotion_piece:
    :return:
    """
    if castle == 0:
        return "O-O"
    elif castle == 1:
        return "O-O-O"
    notation_list = []
    if piece_name == 'P' or piece_name == 'p':
        if special[1]:
            notation_list.append(squares[1] + 'x')
    else:
        notation_list.append(piece_name)
        if squares[1]:
            notation_list.append(squares[1])
        if special[1]:
            notation_list.append('x')

    notation_list.append(squares[0])
    if special[-1]:
        notation_list.append('=' + promotion_piece)
    if special[0]:
        notation_list.append('+')
    if special[2]:
        notation_list.append('#')

    return ''.join(notation_list)


def get_piece_name(piece_type: str, color: str) -> str:
    """
    :param piece_type:
    :param color:
    :return:
    """
    return piece_type if color == 'w' else piece_type.lower()


def invert_dict(dictionary: dict) -> dict:
    """
    :param dictionary:
    :return:
    """
    return dict(map(reversed, dictionary.items()))


def dict_to_numpy(dictionary: dict) -> np.array:
    """
    :param dictionary:
    :return:
    """
    data = list(dictionary.keys())
    array = np.array(data)
    return array.reshape(8, 8)


def get_coord(delta, first) -> dict:
    """
    :return:
    """
    coord: dict = {}
    keys = START_POSITION.keys()
    for i, k in enumerate(keys):
        coord[k] = ((i % 8) * delta + first[0],
                    (i // 8) * delta + first[1])
    return coord


def get_color(turn: int) -> str:
    """
    :param turn:
    :return:
    """
    return 'w' if turn % 2 == 1 else 'b'


def get_color_piece(piece: str) -> str:
    return 'w' if piece.isupper() else 'b'


def opposite_color(color: str) -> str:
    return 'w' if color == 'b' else 'b'


def get_index(sq: str) -> tuple:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    j: int = letters.index(sq[0])
    i: int = int(sq[1]) - 1
    return i, j


def borders(index: int) -> bool:
    return 0 <= index <= 7


def delete_sq(lst: list, sq: str) -> list:
    return list(filter(sq.__ne__, lst))


def flip_ray(ray: np.array, sq: str) -> np.array:
    if ray[0] != sq:
        return ray[::-1]
    return ray


def split(moves: np.array, sq: str) -> (np.array, np.array):
    idx = int(np.where(moves == sq)[0])
    if idx == 0:
        return moves, None
    return moves[0: idx + 1], moves[idx:]


def cls_from_symbol(symbol: str, color: str, sq: str) -> object:
    upper_name = symbol.upper()
    if upper_name == 'P':
        return Pawn(symbol, color, sq)
    if upper_name == 'N':
        return Knight(symbol, color, sq)
    if upper_name == 'B':
        return Bishop(symbol, color, sq)
    if upper_name == 'R':
        return Rook(symbol, color, sq)
    if upper_name == 'Q':
        return Queen(symbol, color, sq)
    if upper_name == 'K':
        return King(symbol, color, sq)


def fen_to_board(fen: str) -> np.array:
    board = []
    for row in fen.split('/'):
        brow = []
        for c in row:
            if c == ' ':
                break
            elif c in '12345678':
                brow.extend([0] * int(c))
            elif c > 'Z' or 'A' < c < 'Z':
                brow.append(ord(c))
        board.append(brow)
    return np.asarray(board).reshape(64, )


def diff_squares(sq_main: str, sq_aux: str):
    if sq_main[0] != sq_aux[0]:
        return sq_main[0]
    if sq_main[1] != sq_aux[1]:
        return sq_main[1]
