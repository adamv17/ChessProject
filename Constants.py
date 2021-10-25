"""
The Constants file contains all game constants that may be used in all game files.
"""
import os.path

XY_FIRST_SQUARE = (145, 50)
DELTA_SQUARE = 75.5
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

UNICODE_PIECE_SYMBOLS = {
    "r": "♖", "R": "♜",
    "n": "♘", "N": "♞",
    "b": "♗", "B": "♝",
    "q": "♕", "Q": "♛",
    "k": "♔", "K": "♚",
    "p": "♙", "P": "♟",
}

START_POSITION = {
    "a1": "R", "b1": "N", "c1": "B", "d1": "Q", "e1": "K", "f1": "B", "g1": "N", "h1": "R",
    "a2": "P", "b2": "P", "c2": "P", "d2": "P", "e2": "P", "f2": "P", "g2": "P", "h2": "P",
    "a3": "-", "b3": "-", "c3": "-", "d3": "-", "e3": "-", "f3": "-", "g3": "-", "h3": "-",
    "a4": "-", "b4": "-", "c4": "-", "d4": "-", "e4": "-", "f4": "-", "g4": "-", "h4": "-",
    "a5": "-", "b5": "-", "c5": "-", "d5": "-", "e5": "-", "f5": "-", "g5": "-", "h5": "-",
    "a6": "-", "b6": "-", "c6": "-", "d6": "-", "e6": "-", "f6": "-", "g6": "-", "h6": "-",
    "a7": "p", "b7": "p", "c7": "p", "d7": "p", "e7": "p", "f7": "p", "g7": "p", "h7": "p",
    "a8": "r", "b8": "n", "c8": "b", "d8": "q", "e8": "k", "f8": "b", "g8": "n", "h8": "r",
}

PIECES = {
    "p": os.path.join(ROOT_DIR, "images/black-pawn.png"),
    "n": os.path.join(ROOT_DIR, "images/black-knight.png"),
    "b": os.path.join(ROOT_DIR, "images/black-bishop.png"),
    "r": os.path.join(ROOT_DIR, "images/black-rook.png"),
    "q": os.path.join(ROOT_DIR, "images/black-queen.png"),
    "k": os.path.join(ROOT_DIR, "images/black-king.png"),
    "P": os.path.join(ROOT_DIR, "images/white-pawn.png"),
    "N": os.path.join(ROOT_DIR, "images/white-knight.png"),
    "B": os.path.join(ROOT_DIR, "images/white-bishop.png"),
    "R": os.path.join(ROOT_DIR, "images/white-rook.png"),
    "Q": os.path.join(ROOT_DIR, "images/white-queen.png"),
    "K": os.path.join(ROOT_DIR, "images/white-king.png")
}
