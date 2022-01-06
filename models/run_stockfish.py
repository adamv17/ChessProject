from stockfish import Stockfish

fish = Stockfish(path="stockfish_14.1_win_x64_avx2.exe")


def get_pos_eval(fen: str):
    fish.set_fen_position(fen)
    return fish.get_evaluation()['value'] / 100


print(get_pos_eval("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"))
