from kivy.app import App
from ChessGame import ChessGame


class ChessApp(App):
    def build(self):
        return ChessGame()
