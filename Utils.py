"""
Utils class, contains all utility functions that are modular and unrelated to the User or the Engine.
"""
from Constants import START_POSITION
from Constants import XY_FIRST_SQUARE
from Constants import DELTA_SQUARE

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
        if squares[1] is not None:
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
    data = list(dictionary.values())
    array = np.array(data)
    return array.reshape(8, 8)


def get_coord() -> dict:
    """
    :return:
    """
    coord = {}
    keys = START_POSITION.keys()
    for i, k in enumerate(keys):
        coord[k] = ((i % 8) * DELTA_SQUARE + XY_FIRST_SQUARE[0],
                    (i // 8) * DELTA_SQUARE + XY_FIRST_SQUARE[1])
    return coord


def get_color(turn: int) -> str:
    """
    :param turn:
    :return:
    """
    return 'w' if turn % 2 == 1 else 'b'


def opposite_color(color: str) -> str:
    return 'w' if color == 'b' else 'b'


print(get_coord())

name, sq, bol, cas = notation_to_board('Rcxc4#', 'b')

print("name =", name)
print("sq =", sq)
print("bol =", bol)
print("cas =", cas)

n = board_to_notation('P', ['e8', 'd'], [False, True, True, True], 2, 'Q')
print(n)
