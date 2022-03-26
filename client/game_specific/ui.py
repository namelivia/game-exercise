from abc import ABC
from client.graphics.shapes import Text, SmallText

# Each of these are ANIMATIONS (thats why they have time)


class UIElement(ABC):

    # No animations yet
    # def render(self, time, window):
    # UI elements can hold a small state too that can be updated
    def render(self, window):
        [shape.render(window) for shape in self.shapes]

    def update(self, data):
        pass


class WelcomeMessage(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            Text(f'Welcome to game, {name}', 20, 0)
        ]


class OptionList(UIElement):
    def __init__(self, options):
        self.options = options
        self.shapes = []
        for index, option in self.options.items():
            self.shapes.append(
                Text(f'{index} - {option}', 20, 200 + (30 * int(index)))
            )


class ClockUI(UIElement):
    def __init__(self, value):
        self.shapes = [
            Text(f'Time is {value}', 20, 100)
        ]

    def update(self, data):
        # What if data does not contain time? Throw an exception
        time = data['time']
        self.shapes[0].set_message(f'Time is {time}')  # Not supersure about this


class Title(UIElement):
    def __init__(self, value):
        self.shapes = [
            Text('Welcome to the game', 20, 10)
        ]

    def update(self, data):
        time = data['time']
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.shapes[0].set_x((time/inverse_speed) % (640 + offset) - offset)  # Not supersure about this


class NewGameMessage(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            Text('Create a new game', 20, 0),
            Text('Please write the name for your new game:', 20, 40),
            Text(name, 20, 70)
        ]

    def update(self, data):
        # What if data does not contain new_game_name? Throw an exception
        name = data['new_game_name']
        self.shapes[2].set_message(name)  # Not supersure about this


class GameIdMessage(UIElement):
    def __init__(self, game_id):
        self.game_id = game_id
        self.shapes = [
            Text('Join an existing game', 20, 0),
            Text('Please write the id for the game:', 20, 40),
            Text(game_id, 20, 70)
        ]

    def update(self, data):
        # What if data does not contain game_id? Throw an exception
        game_id = data["game_id"]
        self.shapes[2].set_message(game_id)  # Not supersure about this


class TurnIndicator(UIElement):
    def __init__(self, turn):
        self.turn = turn
        self.shapes = [
            SmallText(f'Player turn: {turn}', 20, 20)
        ]


class GameIdIndicator(UIElement):
    def __init__(self, game_id):
        self.game_id = game_id
        self.shapes = [
            SmallText(f'Game Id: {game_id}', 20, 40)
        ]


class GameNameIndicator(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            SmallText(f'Game name: {name}', 20, 60)
        ]


class Player1NameIndicator(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            SmallText(f'Player 1 name: {name}', 20, 80)
        ]


class Player2NameIndicator(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            SmallText(f'Player 2 name: {name}', 20, 100)
        ]


class Board(UIElement):
    def __init__(self, board):
        self.board = board
        self.shapes = [
            SmallText(f"[{self.board[0]}] [{self.board[1]}] [{self.board[2]}]", 20, 120),
            SmallText(f"[{self.board[3]}] [{self.board[4]}] [{self.board[5]}]", 20, 130),
            SmallText(f"[{self.board[6]}] [{self.board[7]}] [{self.board[8]}]", 20, 140)
        ]


class Instructions(UIElement):
    def __init__(self):
        self.shapes = [
            SmallText('Press the square number to place a symbol', 20, 200)
        ]
