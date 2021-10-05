import pandas as pd


def get_data() -> pd.Series:
    games = pd.read_csv('games.csv')
    return games['moves']


d = get_data()
print(d)
