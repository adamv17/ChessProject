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
    games = open('data.pgn')
    y_np = np.empty((18000, 2))
    for i in range(18000):
        game = chess.pgn.read_game(games)
        exporter = chess.pgn.StringExporter(headers=False, variations=True, comments=False)
        pgn_string = game.accept(exporter)
        print(pgn_string)
        white_elo = game.headers.get('WhiteElo')
        black_elo = game.headers.get('BlackElo')
        y_np[i] = np.array([white_elo, black_elo])
        if i % 1000 == 0:
            print(f'{i}')
    print(y_np)
    y = torch.from_numpy(y_np)
    print(y)
    torch.save(y, 'Y.pt')


def get_lichess():
    with bz2.open('lichess_db_standard_rated_2021-08.pgn.bz2', 'rb') as lichess_data:
        for line in lichess_data:
            first_game = chess.pgn.read_game(''.join(line))
            break
    print(first_game)
    # lines = (line.decode().rstrip('\r\n') for line in lichess_data)



get_elo()
