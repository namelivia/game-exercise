from client.graphics.shapes import SmallText
from client.primitives.ui import UIElement


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
