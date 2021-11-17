from ChessApp import ChessApp
from kivy.config import Config

if __name__ == '__main__':
    print("Chess is awesome")
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    ChessApp().run()

