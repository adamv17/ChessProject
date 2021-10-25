from abc import ABC

from kivy.uix.gridlayout import Layout


class ChessGame(Layout, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


