import uuid
from .errors import InvalidCommandError


class Game():
    def __init__(self, name, player_id):
        self.id = uuid.uuid4()
        self.name = name
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.player_1_id = player_id
        self.player_2_id = None
        self.turn = self.player_1_id

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

    def place(self, player, position):
        try:
            if self.player_2_id is None:
                raise InvalidCommandError("No player 2 yet")
            if self.turn != player:
                raise InvalidCommandError("Not your turn")
            if self.board[position] != ' ':
                raise InvalidCommandError("Position already taken")
            self.board[position] = self._get_symbol(player)
            self.turn = self._next_turn()
        except IndexError:
            raise InvalidCommandError("Position out of bounds")
