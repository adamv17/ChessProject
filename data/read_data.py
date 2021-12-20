import pandas as pd
import chess.pgn
import torch
import numpy as np
import bz2


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

    x = torch.from_numpy(l)
    torch.save(x, 'X.pt')


def get_elo():
    start_pos = [114, 110, 98, 113, 107, 98, 110, 114,
                 112, 112, 112, 112, 112, 112, 112, 112,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 80, 80, 80, 80, 80, 80, 80, 80,
                 82, 78, 66, 81, 75, 66, 78, 82]
    games = open('data.pgn')
    y_np = np.empty((18000, 2))
    x2_np = np.empty((18000, 50, 64))
    for i in range(18000):
        game = chess.pgn.read_game(games)
        board = game.board()
        for k in range(50):
            b = fen_to_board(board.fen())
            x2_np[i, k, :] = b
            try:
                game.next()
                board = game.board()
            except TypeError:
                board = start_pos

        white_elo = game.headers.get('WhiteElo')
        black_elo = game.headers.get('BlackElo')
        y_np[i] = np.array([white_elo, black_elo])
        if i % 1000 == 0:
            print(f'{i}')
    print(y_np)
    y = torch.from_numpy(y_np)
    print(y)
    print(x2_np)
    x2 = torch.from_numpy(x2_np)
    torch.save(y, 'Y.pt')
    torch.save(x2, 'X2.pt')


def fen_to_board(fen):
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
    return np.asarray(board).reshape(64,)


def get_lichess():
    with bz2.open('lichess_db_standard_rated_2021-08.pgn.bz2', 'rb') as lichess_data:
        for line in lichess_data:
            first_game = chess.pgn.read_game(''.join(line))
            break
    print(first_game)
    # lines = (line.decode().rstrip('\r\n') for line in lichess_data)


get_elo()
