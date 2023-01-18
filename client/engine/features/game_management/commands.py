from client.engine.primitives.command import Command
from .events import (
    ErrorCreatingGameEvent,
    ErrorJoiningGameEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    NewGameRequestEvent,
)


class CreateAGame(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(profile, queue, f"Create a new game called {new_game_name}")
        self.events = [CreateAGameNetworkRequestEvent(new_game_name)]


class JoinAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f"Join game {game_id}")
        self.events = [JoinAGameNetworkRequestEvent(game_id)]


class ErrorCreatingGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Creating game")
        self.events = [ErrorCreatingGameEvent()]


class ErrorJoiningGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Joining game")
        self.events = [ErrorJoiningGameEvent()]


class RequestGameCreation(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(
            profile, queue, f"Request creating a game called {new_game_name}"
        )
        self.events = [NewGameRequestEvent(new_game_name)]


class RequestJoiningAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f"Request joining game {game_id}")
        self.events = [JoinExistingGameEvent(game_id)]
