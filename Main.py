from ChessApp import ChessApp
from kivy.config import Config
from kivy.core.window import Window

if __name__ == '__main__':
    print("Chess is awesome")
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    ChessApp().run()


