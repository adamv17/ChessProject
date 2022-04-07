from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.image import Image
from kivy.core.window import Window
import Utils
from Bishop import Bishop
from Knight import Knight
from Piece import Piece
import numpy as np
import os.path
from Board import Board
import Constants
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# from ChessApp import ChessApp
from Rook import Rook
import chess
from stockfish import Stockfish
from kivy.clock import Clock
from matplotlib import pyplot as plt
import torch
from models.Model import EloNN
import copy


class ChessGame(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n = Button(text='Knight', size=(100, 100), x=400, y=225)
        self.n.button_name = 'N'
        self.b = Button(text='Bishop', size=(100, 100), x=300, y=225)
        self.b.button_name = 'B'
        self.r = Button(text='Rook', size=(100, 100), x=200, y=225)
        self.r.button_name = 'R'
        self.q = Button(text='Queen', size=(100, 100), x=100, y=225)
        self.q.button_name = 'Q'
        self.board = Board()
        self.board_image = Image(source=os.path.join(Constants.ROOT_DIR, "images/marble-chessboard.jpg"))
        self.board_image.pos = (0, 0)
        self.board_image.size = (600, 600)
        self.add_widget(self.board_image)
        self.coord = Utils.get_coord(Constants.DELTA_SQUARE, Constants.XY_FIRST_SQUARE)

        self.pieces = []
        self.white_pieces = []
        self.black_pieces = []
        self.white_rooks = []
        self.white_knights = []
        squares = list(Constants.START_POSITION.keys())
        # initialize white pieces
        for wsq in squares[0:16]:
            name = Constants.START_POSITION[wsq]
            piece = Utils.cls_from_symbol(name, 'w', wsq)
            if name == 'K':
                self.white_king = piece
            if name == 'R':
                self.white_rooks.append(piece)
            if name == 'N':
                self.white_knights.append(piece)
            self.white_pieces.append(piece)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(wsq)

        # initialize black pieces
        self.black_rooks = []
        self.black_knights = []
        for bsq in squares[48:64]:
            name = Constants.START_POSITION[bsq]
            piece = Utils.cls_from_symbol(name, 'b', bsq)
            if name == 'k':
                self.black_king = piece
            if name == 'r':
                self.black_rooks.append(piece)
            if name == 'n':
                self.black_knights.append(piece)
            self.black_pieces.append(piece)
            self.pieces.append(piece)
            self.add_widget(piece)
            piece.set_square(bsq)

        self.piece_translation('b', False)
        self.game_ended = False
        self.promoted_pawn = None

        self.pgn_board = chess.Board()
        self.fish = Stockfish(path="models/stockfish_14.1_win_x64_avx2.exe")
        self.stockfish_evals = np.empty((1, 100))
        self.stockfish_evals.fill(0)
        self.model = EloNN()
        weights_file = 'models/eval_game_model_100_v2.pt'
        self.model.load_state_dict(torch.load(weights_file, map_location=torch.device('cpu')))
        self.model.eval()
        self.elos = []
        self.all_positions = np.empty((1, 100, 64))
        for p in range(100):
            self.all_positions[0, p, :] = (Utils.fen_to_board(self.pgn_board.fen()))
        self.pindex = 1

    def get_elo(self):
        x = torch.from_numpy(self.stockfish_evals)
        x2 = torch.from_numpy(self.all_positions)
        t = self.model(x[None, :].float(), x2[None, :, :].float())
        self.elos.append(t.detach().numpy()[0])
        print(self.elos)

    def get_pos_eval(self, fen: str):
        self.fish.set_fen_position(fen)
        return self.fish.get_evaluation()['value']

    def schedule_eval(self):
        Clock.schedule_once(self.eval_pos, 0)

    def eval_pos(self, *args):
        if self.pindex != 100:
            self.stockfish_evals[0, self.pindex] = self.get_pos_eval(self.pgn_board.fen())
            self.all_positions[0, self.pindex, :] = Utils.fen_to_board(self.pgn_board.fen())
            self.pindex = self.pindex + 1
            self.get_elo()
        else:
            print("sorry ran out of space")

    def add_position(self):
        move = self.pgn_board.push_san(self.board.notation[-1])
        print(self.pgn_board)
        if not self.pgn_board.is_checkmate():
            self.schedule_eval()

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

    def is_square_attacked(self, board: Board, sq: str, color: str) -> bool:
        """
        :param board: the given board position
        :param sq: the square to check
        :param color: the color attacking
        creates a "super piece" on the square to check whether another piece is attacking this square
        :return: true if the square is attacked otherwise false
        """
        super_piece = Piece('super piece', Utils.opposite_color(color), sq)
        attackers = Knight.moves(super_piece, board, sq)
        knight = Utils.get_piece_name('N', color)
        for attack_sq in attackers:
            if board.position[attack_sq] == knight:
                return True

        attackers = Bishop.moves(super_piece, board, sq)
        queen = Utils.get_piece_name('Q', color)
        bishop = Utils.get_piece_name('B', color)
        for attack_sq in attackers:
            p = board.position[attack_sq]
            if p == bishop or p == queen:
                return True

        rook = Utils.get_piece_name('R', color)
        attackers = Rook.moves(super_piece, board, sq)
        for attack_sq in attackers:
            p = board.position[attack_sq]
            if p == rook or p == queen:
                return True

        return False

    def legal_move(self, piece: Piece, sq: str) -> (bool, bool):
        """
        :param piece: the piece trying to move
        :param sq: the square the piece wants to move to
        :return: true if the move is legal otherwise false
        """
        possible_moves = piece.moves(self.board, piece.square)
        print(possible_moves)

        return sq in possible_moves and not self.is_in_check_after_move(piece, sq)

    def is_in_check_after_move(self, piece: Piece, sq: str):
        board = copy.deepcopy(self.board)
        board.update_position(piece, sq)
        d = Utils.invert_dict(board.position)
        is_attacked = self.is_square_attacked(board, d[Utils.get_piece_name("K", piece.color)],
                                              Utils.opposite_color(piece.color))
        return is_attacked

    def legal_move_present(self, color: str) -> bool:
        pieces = self.get_all_pieces_color(color)
        for p in pieces:
            mv = p.moves(self.board, p.square)
            for m in mv:
                if self.legal_move(p, m):
                    print(m)
                    return True

        return False

    def update_game(self, piece: Piece, sq: str, castle: int, unambiguous: str):
        """
        :param en_passant:
        :param castle:
        :param unambiguous:
        :param piece: the piece played
        :param sq: the square to move to
        :return: updates the board and notation
        """
        self.board.update_game(piece, sq, castle, unambiguous)

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

    def remove_piece(self, piece: Piece):
        pieces = self.get_all_pieces_color(piece.color)
        for i, p in enumerate(pieces):
            if p.square == piece.square:
                pieces.pop(i)
                break

    def promotion(self, piece):
        self.piece_translation('b', False)
        self.piece_translation('w', False)
        self.promotion_graphics()
        self.promoted_pawn = piece
        self.remove_widget(piece)
        self.remove_piece(piece)

    def promotion_graphics(self):
        self.q.bind(on_press=self.on_click)
        self.r.bind(on_press=self.on_click)
        self.b.bind(on_press=self.on_click)
        self.n.bind(on_press=self.on_click)

        self.add_widget(self.q)
        self.add_widget(self.r)
        self.add_widget(self.b)
        self.add_widget(self.n)

    def on_click(self, touch: Button):
        color = self.promoted_pawn.color
        name = Utils.get_piece_name(touch.button_name, color)
        piece = Utils.cls_from_symbol(name, color, self.promoted_pawn.square)
        self.add_widget(piece)
        self.get_all_pieces_color(color).append(piece)
        self.pieces.append(piece)
        piece.set_square(piece.square)
        self.board.notation[-1] += '=' + name
        self.add_position()

        self.remove_widget(self.q)
        self.remove_widget(self.r)
        self.remove_widget(self.b)
        self.remove_widget(self.n)
        self.piece_translation(Utils.opposite_color(piece.color), True)
        self.board.position[piece.square] = piece.piece_name
        print(self.board.position)
        self.end(piece.color)
