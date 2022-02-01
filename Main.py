from ChessApp import ChessApp
from kivy.config import Config

if __name__ == '__main__':
    print("Chess is awesome")
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    ChessApp().run()
