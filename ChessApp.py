from kivy.app import App
from ChessGame import ChessGame
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.label import Label

Builder.load_string("""
<MenuScreen>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'images/king_queen_wall.jpg'
    Label:
        text: 'Welcome to Elo Guesser!'
        size_hint: (None, None)
        pos: (200, 475)
        font_size: '40sp'
    Button:
        text: 'Play! The computer will guess your elo rating!'
        size_hint: (None, None)
        size: (400, 100)
        pos: (0, 300)
        background_color: 0, 0, 0, 0
        on_press:
            root.manager.transition.direction = 'left'
            root.manager.current = 'game'
    Button:
        text: 'Read the game rules'
        size_hint: (None, None)
        size: (400, 100)
        pos: (0, 200)  
        background_color: 0, 0, 0, 0
        on_press: 
            root.manager.transition.direction = 'left'
            root.manager.current = 'rules'
<RulesScreen>:
    BoxLayout:
        Button: 
            size_hint: (None, None)
            size: (100, 100)
            pos: (0, 0)
            background_normal: 'images/back_arrow.png'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
""")

sm = ScreenManager()


def restore_screens():
    sm.clear_widgets()
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(RulesScreen(name='rules'))
    sm.add_widget(GameScreen(name='game'))
    sm.add_widget(ResultsScreen(name='results'))


class MenuScreen(Screen):
    pass


class RulesScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.rules_of_chess = Label(
            text="The king moves exactly one square horizontally, vertically, or diagonally. A special move with the \n"
                 "king known as castling is allowed only once per player, per game (see below). A rook moves any \n"
                 "number of vacant squares horizontally or vertically. It also is moved when castling. \n "
                 "A bishop moves any number of vacant squares diagonally. \n"
                 "The queen moves any number of vacant squares horizontally, vertically, or diagonally. \n"
                 "A knight moves to one of the nearest squares not on the same rank, file, or diagonal. (This can be \n"
                 "thought of as moving two squares horizontally then one square vertically, or moving one square \n"
                 "horizontally then two squares vertically—i.e. in an L pattern.) The knight is not blocked by other \n"
                 "pieces; it jumps to the new location. \n"
                 "Pawns have the most complex rules of movement: \n"
                 "A pawn moves straight forward one square, if that square is vacant. If it has not yet moved, \n"
                 "a pawn also has the option of moving two squares straight forward, provided both squares are \n"
                 "vacant. Pawns cannot move backwards. \n"
                 "A pawn, unlike other pieces, captures differently from how it moves. A pawn can capture an enemy \n"
                 "piece on either of the two squares diagonally in front of the pawn. It cannot move to those squares "
                 "\n "
                 "when vacant except when capturing en passant. \n"
                 "The pawn is also involved in the two special moves en passant and promotion \n")
        self.add_widget(self.rules_of_chess)


class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.game = ChessGame()
        self.add_widget(self.game)
        self.quit = Button(text='quit', font_size='30sp', size=(200, 300), pos=(600, 0),
                           background_color=(150 / 255, 40 / 255, 27 / 255, 1), background_normal='')
        self.quit.bind(on_press=self.quit_game)
        self.results = Button(text='results', size=(200, 300), pos=(600, 300), font_size='30sp',
                              background_color=(52 / 255, 45 / 255, 113 / 255, 1), background_normal='')
        self.results.bind(on_press=self.goto_results)
        self.game.add_widget(self.quit)
        self.game.add_widget(self.results)

    def quit_game(self, *touch):
        restore_screens()
        sm.switch_to(sm.screens[0], direction='right')

    def goto_results(self, *touch):
        restore_screens()
        sm.switch_to(sm.screens[3], direction='left')
        sm.screens[3].show_elos(self.game.elos)


class ResultsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.label_to_menu = Label(size=(200, 200), pos=(-300, -250), text='To menu', font_size='20sp')
        self.back_button = Button(size=(200, 200), pos=(0, 0), size_hint=(None, None))
        self.back_button.background_normal = 'images/back_arrow.png'
        self.back_button.bind(on_press=self.to_menu)

    def to_menu(self, *touch):
        restore_screens()
        sm.switch_to(sm.screens[0], direction='right')

    def show_elos(self, elos):
        if len(elos) > 0:
            elo_label_white = Label(text="white elo = " + str(round(elos[-1][0])), pos=(-300, 150))
            elo_label_black = Label(text="black elo = " + str(round(elos[-1][1])), pos=(-300, 200))
            self.add_widget(elo_label_white)
            self.add_widget(elo_label_black)
            graph = Graph(xlabel='Moves', ylabel='Elo',
                          x_ticks_major=5, y_ticks_major=100,
                          y_grid_label=True, x_grid_label=True,
                          x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=0, ymax=3000)

            graph.size_hint = (None, None)
            graph.size = (400, 400)
            graph.pos = (300, 300)
            plot = MeshLinePlot(color=[1, 0, 0, 1])
            plot.points = [(i, e[0].item()) for i, e in enumerate(elos)]
            graph.add_plot(plot)
            plot_b = MeshLinePlot(color=[0, 1, 0, 1])
            plot_b.points = [(i, e[1].item()) for i, e in enumerate(elos)]
            graph.add_plot(plot_b)
            graph.size = (400, 400)
            graph.pos = (200, 200)
            self.add_widget(graph)
        else:
            self.add_widget(Label(text='sorry no results'))
        self.add_widget(self.back_button)
        self.add_widget(self.label_to_menu)


class ChessApp(App):
    def build(self):
        restore_screens()
        return sm
