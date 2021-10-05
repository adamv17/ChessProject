import pandas as pd


def get_data():
    games = pd.read_csv('games.csv')
    moves = games['moves']
    return moves


get_data()
