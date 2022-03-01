import time

import pandas as pd
import chess.pgn
import torch
import numpy as np
import bz2
import Utils


def get_eval():
    data = pd.read_csv('stockfish.csv')
    arr = data['MoveScores'].values
    l = np.empty((18000, 50))
    for i in range(18000):
        lst: list = arr[i].split(" ")
        game = np.empty((1, 50))
        for j in range(50):
            if len(lst) <= j:
                game[0, j] = 0
            else:
                inp = 0
                if lst[j] != 'NA' and lst[j] != '':
                    inp = int(lst[j])
                game[0, j] = inp
        l[i] = game
    print(l)
    x = torch.from_numpy(l)
    torch.save(x, 'X.pt')


def get_elo():
    games = open('data.pgn')
    y_np = np.empty((18000, 2))
    for i in range(18000):
        game = chess.pgn.read_game(games)
        white_elo = game.headers.get('WhiteElo')
        black_elo = game.headers.get('BlackElo')
        y_np[i] = np.array([white_elo, black_elo])
        if i % 1000 == 0:
            print(f'{i}')
    print(y_np)
    y = torch.from_numpy(y_np)
    print(y)

    torch.save(y, 'Y.pt')


def get_board_positions():
    x2_np = np.empty((18000, 50, 64))
    games = open('data.pgn')
    for i in range(18000):
        game = chess.pgn.read_game(games)
        board = game.board()
        start_pos = board
        for k in range(50):
            b = Utils.fen_to_board(board.fen())
            x2_np[i, k, :] = b
            try:
                game = game.next()
                board = game.board()
            except AttributeError:
                board = start_pos
        if i % 1000 == 0:
            print(f'{i}')
    print(x2_np)
    x2 = torch.from_numpy(x2_np)
    torch.save(x2, 'X2.pt')


def get_lichess(num_to_run: int):
    positions = torch.empty((1_000_000, 50, 64))
    games = open('lichess.pgn')
    for i in range(num_to_run):
        game = chess.pgn.read_game(games)
        board = game.board()
        eval = game.eval()

get_eval()