import uuid
from .errors import InvalidCommandError


"""
This implements the game state and the
operations that can be applied on them.

Currently joining a game and placing a symbol on the board.

Note that every command first validates (can be invalid).
And if valid sets something on the game state.
"""


class Game():
    def __init__(self, name, player_id):
        self.id = uuid.uuid4()
        self.name = name
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.player_1_id = player_id
        self.player_2_id = None
        self.turn = self.player_1_id
        self.events = [
            'Game created by {player_1}'
        ]

    def _next_turn(self):
        if self.turn == self.player_2_id:
            return self.player_1_id
        return self.player_2_id

    def _get_symbol(self, player):
        if player == self.player_2_id:
            return 'X'
        return 'O'

    def join(self, player_id):
        if player_id not in [self.player_1_id, self.player_2_id]:
            if self.player_2_id is not None:
                raise InvalidCommandError("The game is full")
            self.player_2_id = player_id
            self.events.append('Player {player_2_id} joined')
        else:
            raise InvalidCommandError("This player is already in the game")

    def player_can_get_status(self, player_id):
        if player_id not in [self.player_1_id, self.player_2_id]:
            raise InvalidCommandError("Player has no access to the game")

    def place(self, player, position):
        position = int(position)
        try:
            if self.player_2_id is None:
                raise InvalidCommandError("No player 2 yet")
            if self.turn != player:
                raise InvalidCommandError("Not your turn")
            if self.board[position] != ' ':
                raise InvalidCommandError("Position already taken")
            self.board[position] = self._get_symbol(player)
            self.events.append('Player {player} places a symbol on position {position}')
            self.turn = self._next_turn()
        except IndexError:
            raise InvalidCommandError("Position out of bounds")
