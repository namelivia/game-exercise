import uuid
from .errors import InvalidCommandError
from common.events import (
    GameCreated,
    PlayerJoined,
    PlayerPlacedSymbol
)


"""
This implements the game state and the
operations that can be applied on them.

Currently joining a game and placing a symbol on the board.

Note that every command first validates (can be invalid).
And if valid sets something on the game state.
"""

PLAYERS_PER_GAME = 2


class Game():

    def __init__(self, name, player_id):
        self.id = uuid.uuid4()
        self.name = name
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.players = [player_id]
        self.events = [
            GameCreated(player_id)
        ]

    def _next_turn(self):
        if self.turn == self.players[1]:
            return self.players[0]
        return self.players[1]

    def _get_symbol(self, player):
        if player == self.players[1]:
            return 'X'
        return 'O'

    def join(self, player_id):
        if player_id not in self.players:
            if len(self.players) >= PLAYERS_PER_GAME:
                raise InvalidCommandError("The game is full")
            self.players.append(player_id)
            self.events.append(PlayerJoined(player_id))
        else:
            raise InvalidCommandError("This player is already in the game")

    def player_can_get_status(self, player_id):
        if player_id not in self.players:
            raise InvalidCommandError("Player has no access to the game")

    def place(self, player, position):
        position = int(position)
        try:
            if len(self.players) < PLAYERS_PER_GAME:
                raise InvalidCommandError("No player 2 yet")
            if self.turn != player:
                raise InvalidCommandError("Not your turn")
            if self.board[position] != ' ':
                raise InvalidCommandError("Position already taken")
            self.board[position] = self._get_symbol(player)
            self.events.append(PlayerPlacedSymbol(player, position))
            self.turn = self._next_turn()
        except IndexError:
            raise InvalidCommandError("Position out of bounds")
